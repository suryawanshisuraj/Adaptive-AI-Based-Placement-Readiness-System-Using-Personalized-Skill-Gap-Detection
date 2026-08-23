import os
import sqlite3
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env in project root
load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", ".env"
    )
)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

_supabase_client: Optional[Client] = None
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "placement_readiness.db")


def get_sqlite_connection() -> sqlite3.Connection:
    """Returns a connection to the local SQLite database with dictionary rows."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_supabase() -> Optional[Client]:
    """Return a singleton Supabase client using the service key."""
    global _supabase_client
    if _supabase_client is None and SUPABASE_URL and SUPABASE_SERVICE_KEY:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        except Exception:
            _supabase_client = None
    return _supabase_client


def init_db():
    """Initializes local SQLite tables and verifies Supabase connection."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            target_role TEXT DEFAULT 'java_developer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS assessment_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            session_type TEXT DEFAULT 'adaptive_practice',
            target_role TEXT,
            status TEXT DEFAULT 'in_progress',
            total_questions INTEGER DEFAULT 8,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS response_logs (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            user_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            selected_index INTEGER,
            is_correct INTEGER NOT NULL,
            response_time_sec REAL DEFAULT 45.0,
            subtopic TEXT NOT NULL,
            topic TEXT,
            skill TEXT,
            difficulty INTEGER DEFAULT 2,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS skill_mastery (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            skill TEXT NOT NULL,
            mastery_score REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, skill)
        );

        CREATE TABLE IF NOT EXISTS learning_roadmaps (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            target_role TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS roadmap_steps (
            id TEXT PRIMARY KEY,
            roadmap_id TEXT NOT NULL,
            day_number INTEGER NOT NULL,
            skill TEXT NOT NULL,
            topic TEXT,
            subtopic TEXT NOT NULL,
            action_title TEXT NOT NULL,
            explanation_summary TEXT,
            target_questions_count INTEGER DEFAULT 5,
            is_completed INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

    # Verify Supabase if available
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").select("id").limit(1).execute()
            print("[OK] Supabase cloud connection active.")
        except Exception as e:
            print(f"[INFO] Running with high-performance local SQLite engine. Supabase cloud optional: {e}")
    else:
        print("[OK] Local SQLite placement readiness database initialized.")


# ── DATA ACCESS HELPERS ───────────────────────────────────────────────

def db_get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetches user record from SQLite or Supabase."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    
    sb = get_supabase()
    if sb:
        try:
            res = sb.table("users").select("*").eq("id", user_id).execute()
            if res.data:
                u = res.data[0]
                db_upsert_user(u)
                return u
        except Exception:
            pass
    return None


def db_upsert_user(user_data: Dict[str, Any]):
    """Saves user record to SQLite and Supabase."""
    user_id = user_data.get("id")
    name = user_data.get("name", "Student")
    email = user_data.get("email", f"{user_id}@campus.edu")
    target_role = user_data.get("target_role", "java_developer")

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (id, name, email, target_role)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            email = excluded.email,
            target_role = excluded.target_role
    """, (user_id, name, email, target_role))
    conn.commit()
    conn.close()

    sb = get_supabase()
    if sb:
        try:
            sb.table("users").upsert({
                "id": user_id,
                "name": name,
                "email": email,
                "target_role": target_role
            }).execute()
        except Exception:
            pass


def db_get_user_responses(user_id: str) -> List[Dict[str, Any]]:
    """Retrieves all real response logs for a user."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM response_logs
        WHERE user_id = ?
        ORDER BY rowid ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()


    local_logs = [dict(r) for r in rows]
    if local_logs:
        return local_logs

    sb = get_supabase()
    if sb:
        try:
            res = sb.table("response_logs").select("*").eq("user_id", user_id).execute()
            if res.data:
                for r in res.data:
                    db_insert_response_log(r)
                return res.data
        except Exception:
            pass

    return local_logs


def db_insert_response_log(log: Dict[str, Any]):
    """Records an assessment / aptitude response log to SQLite and Supabase."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO response_logs 
        (id, session_id, user_id, question_id, selected_index, is_correct, response_time_sec, subtopic, topic, skill, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log.get("id"),
        log.get("session_id", "sess_direct"),
        log.get("user_id"),
        log.get("question_id"),
        log.get("selected_index", 0),
        1 if log.get("is_correct") in (1, True) else 0,
        float(log.get("response_time_sec", 45.0)),
        log.get("subtopic", "General"),
        log.get("topic", "General"),
        log.get("skill", "Aptitude"),
        int(log.get("difficulty", 2))
    ))
    conn.commit()
    conn.close()

    sb = get_supabase()
    if sb:
        try:
            sb.table("response_logs").insert(log).execute()
        except Exception:
            pass


def db_get_user_skill_priors(user_id: str) -> Dict[str, float]:
    """Fetches custom skill mastery priors for user."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT skill, mastery_score FROM skill_mastery WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {r["skill"]: float(r["mastery_score"]) for r in rows}


def db_save_user_skill_priors(user_id: str, priors: Dict[str, float]):
    """Saves custom skill mastery sliders for user."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    for skill, score in priors.items():
        mastery_id = f"mst_{user_id}_{skill}"
        cursor.execute("""
            INSERT OR REPLACE INTO skill_mastery (id, user_id, skill, topic, subtopic, mastery_score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (mastery_id, user_id, skill, skill, skill, float(score)))
    conn.commit()
    conn.close()





def db_clear_user_logs(user_id: str):
    """Clears all response logs and reset data for a fresh clean state."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM response_logs WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM assessment_sessions WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM learning_roadmaps WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    sb = get_supabase()
    if sb:
        try:
            sb.table("response_logs").delete().eq("user_id", user_id).execute()
            sb.table("assessment_sessions").delete().eq("user_id", user_id).execute()
        except Exception:
            pass





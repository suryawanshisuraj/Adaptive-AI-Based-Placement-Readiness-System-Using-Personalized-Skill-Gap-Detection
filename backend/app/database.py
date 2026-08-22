import os
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

_supabase_client: Client = None


def get_supabase() -> Client:
    """Return a singleton Supabase client using the service key."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _supabase_client


def init_db():
    """Verify Supabase connection on startup. Tables must be created via supabase_schema.sql."""
    try:
        sb = get_supabase()
        sb.table("users").select("id").limit(1).execute()
        print("[OK] Supabase connection verified successfully.")
    except Exception as e:
        print(f"[WARN] Supabase connection warning: {e}")
        print("       Please run supabase_schema.sql in your Supabase SQL Editor.")




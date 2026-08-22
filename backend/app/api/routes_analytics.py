import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from ..database import get_supabase
from ..schemas import PlacementReadinessReport, XAIExplanation
from ..engine.readiness import calculate_placement_readiness
from ..engine.skill_gap import analyze_all_skill_gaps
from ..engine.xai import generate_xai_explanation
from ..data.role_profiles import get_all_roles, get_role_profile
from ..data.question_bank import get_all_questions

router = APIRouter(prefix="/api/analytics", tags=["Analytics & XAI"])

def _get_user_responses(user_id: str) -> List[Dict[str, Any]]:
    sb = get_supabase()
    result = sb.table("response_logs").select("*").eq("user_id", user_id).execute()
    return result.data or []

@router.get("/readiness/{user_id}", response_model=PlacementReadinessReport)
def get_readiness_report(user_id: str, target_role: str = None):
    sb = get_supabase()
    user_result = sb.table("users").select("*").eq("id", user_id).execute()
    user = user_result.data[0] if user_result.data else None
    effective_role = target_role or (user["target_role"] if user else "java_developer")
    responses = _get_user_responses(user_id)
    report = calculate_placement_readiness(user_id, effective_role, responses)
    return report

@router.get("/xai/{user_id}", response_model=XAIExplanation)
def get_xai_breakdown(user_id: str, target_role: str = None):
    sb = get_supabase()
    user_result = sb.table("users").select("*").eq("id", user_id).execute()
    user = user_result.data[0] if user_result.data else None
    effective_role = target_role or (user["target_role"] if user else "java_developer")
    responses = _get_user_responses(user_id)
    xai_data = generate_xai_explanation(user_id, effective_role, responses)
    return xai_data

@router.get("/skill-gaps/{user_id}")
def get_all_gaps(user_id: str):
    responses = _get_user_responses(user_id)
    diags = analyze_all_skill_gaps(responses)
    return list(diags.values())

@router.get("/role-comparison/{user_id}")
def get_role_comparison(user_id: str):
    sb = get_supabase()
    user_result = sb.table("users").select("*").eq("id", user_id).execute()
    user = user_result.data[0] if user_result.data else None
    current_role = user["target_role"] if user else "java_developer"
    responses = _get_user_responses(user_id)

    all_roles = get_all_roles()
    comparisons = []
    for r_id, r_info in all_roles.items():
        rep = calculate_placement_readiness(user_id, r_id, responses)
        comparisons.append({
            "role_id": r_id,
            "role_title": r_info["title"],
            "icon": r_info.get("icon", "💼"),
            "readiness_score": rep["overall_readiness_score"],
            "readiness_tier": rep["readiness_tier"],
            "is_current_target": (r_id == current_role),
            "critical_gap_count": len(rep["critical_skill_gaps"])
        })
    return comparisons

@router.post("/seed-demo-data/{user_id}")
def seed_demo_profile_data(user_id: str):
    """
    Seeds a representative diagnostic performance record:
    Java: 82%, OOP: 76%, SQL: 48%, DBMS: 55%, Aptitude: 71%, Coding: 42%, Communication: 68%
    """
    sb = get_supabase()

    # Ensure user exists
    sb.table("users").upsert({
        "id": user_id,
        "name": "Alex Rivera",
        "email": f"alex.rivera.{user_id}@campus.edu",
        "target_role": "java_developer"
    }).execute()

    # Clear existing logs for fresh demo seed
    sb.table("response_logs").delete().eq("user_id", user_id).execute()
    sb.table("skill_mastery").delete().eq("user_id", user_id).execute()

    session_id = f"sess_demo_{uuid.uuid4().hex[:6]}"
    sb.table("assessment_sessions").insert({
        "id": session_id,
        "user_id": user_id,
        "session_type": "diagnostic",
        "target_role": "java_developer",
        "status": "completed",
        "total_questions": 10
    }).execute()

    demo_log_seeds = [
        ("sql_join_001", 1, 0, 58.0, "SQL JOINs", "Relational Queries", "SQL", 2),
        ("sql_join_002", 0, 0, 62.0, "SQL JOINs", "Relational Queries", "SQL", 3),
        ("sql_sub_001", 0, 0, 52.0, "SQL Subqueries", "Advanced Queries", "SQL", 3),
        ("code_rec_001", 0, 0, 48.0, "Recursion", "Algorithms", "Coding", 2),
        ("code_rec_002", 1, 0, 50.0, "Recursion", "Algorithms", "Coding", 4),
        ("code_arr_002", 0, 0, 55.0, "Arrays & Sliding Window", "Data Structures", "Coding", 3),
        ("dbms_norm_001", 0, 0, 46.0, "Normalization", "Schema Design", "DBMS", 3),
        ("java_col_001", 1, 1, 28.0, "Collections Framework", "Collections & Core", "Java", 3),
        ("java_con_001", 1, 1, 32.0, "Multithreading & Concurrency", "Concurrency", "Java", 4),
        ("oop_poly_001", 1, 1, 24.0, "OOP Polymorphism", "Object Oriented Principles", "OOP", 2),
        ("oop_poly_002", 1, 1, 30.0, "OOP Polymorphism", "Object Oriented Principles", "OOP", 3),
        ("apt_prob_001", 0, 1, 35.0, "Aptitude & Probability", "Quantitative Reasoning", "Aptitude", 2),
        ("apt_work_001", 1, 1, 40.0, "Aptitude & Probability", "Quantitative Reasoning", "Aptitude", 3),
        ("comm_001",     1, 1, 22.0, "Technical Communication", "Professional Verbal", "Communication", 2)
    ]

    logs = []
    for q_id, s_idx, is_c, t_sec, sub, top, sk, diff in demo_log_seeds:
        logs.append({
            "id": f"log_{uuid.uuid4().hex[:8]}",
            "session_id": session_id,
            "user_id": user_id,
            "question_id": q_id,
            "selected_index": s_idx,
            "is_correct": is_c,
            "response_time_sec": t_sec,
            "subtopic": sub,
            "topic": top,
            "skill": sk,
            "difficulty": diff
        })
    sb.table("response_logs").insert(logs).execute()

    return {
        "status": "success",
        "message": "Demo diagnostic profile seeded successfully!",
        "user_id": user_id
    }

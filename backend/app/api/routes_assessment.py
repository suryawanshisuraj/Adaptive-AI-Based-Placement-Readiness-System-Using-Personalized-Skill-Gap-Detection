import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from ..database import get_supabase
from ..schemas import (
    StartAssessmentRequest, AnswerSubmissionRequest,
    AnswerEvaluationResponse, QuestionClientView
)
from ..data.question_bank import get_question_by_id, get_all_questions
from ..engine.skill_gap import compute_subtopic_mastery, calculate_response_time_factor
from ..engine.recommender import select_next_adaptive_question
from ..engine.readiness import calculate_placement_readiness

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])

# In-memory session tracking fallback
_local_sessions = {}
_local_logs = {}

@router.post("/start")
def start_assessment_session(payload: StartAssessmentRequest):
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    target_role = payload.target_role or "java_developer"
    responses = []

    try:
        sb = get_supabase()
        user_result = sb.table("users").select("*").eq("id", payload.user_id).execute()
        user = user_result.data[0] if user_result.data else None
        if user and not payload.target_role:
            target_role = user.get("target_role", "java_developer")

        sb.table("assessment_sessions").insert({
            "id": session_id,
            "user_id": payload.user_id,
            "session_type": payload.session_type,
            "target_role": target_role,
            "status": "in_progress",
            "total_questions": payload.num_questions
        }).execute()

        responses_result = sb.table("response_logs").select("*").eq("user_id", payload.user_id).execute()
        responses = responses_result.data or []
    except Exception:
        pass

    _local_sessions[session_id] = {
        "id": session_id,
        "user_id": payload.user_id,
        "session_type": payload.session_type,
        "target_role": target_role,
        "status": "in_progress",
        "total_questions": payload.num_questions
    }

    first_q = select_next_adaptive_question(target_role, responses)
    if not first_q:
        first_q = get_all_questions()[0]

    client_q = QuestionClientView(
        id=first_q["id"],
        skill=first_q["skill"],
        topic=first_q["topic"],
        subtopic=first_q["subtopic"],
        difficulty=first_q["difficulty"],
        question_text=first_q["question_text"],
        options=first_q["options"],
        expected_time_sec=first_q["expected_time_sec"],
        code_snippet=first_q.get("code_snippet"),
        tags=first_q.get("tags", [])
    )

    return {
        "session_id": session_id,
        "session_type": payload.session_type,
        "target_role": target_role,
        "total_questions": payload.num_questions,
        "current_question_index": 1,
        "question": client_q
    }

@router.post("/submit", response_model=AnswerEvaluationResponse)
def submit_answer(payload: AnswerSubmissionRequest):
    q_data = get_question_by_id(payload.question_id)
    is_correct = (payload.selected_index == q_data["correct_index"])
    
    session = _local_sessions.get(payload.session_id, {
        "id": payload.session_id,
        "user_id": payload.user_id,
        "target_role": "java_developer",
        "total_questions": 8
    })

    try:
        sb = get_supabase()
        session_result = sb.table("assessment_sessions").select("*").eq("id", payload.session_id).execute()
        if session_result.data:
            session = session_result.data[0]
    except Exception:
        pass

    target_role = session.get("target_role", "java_developer")
    log_id = f"log_{uuid.uuid4().hex[:8]}"

    log_entry = {
        "id": log_id,
        "session_id": payload.session_id,
        "user_id": payload.user_id,
        "question_id": payload.question_id,
        "selected_index": payload.selected_index,
        "is_correct": 1 if is_correct else 0,
        "response_time_sec": payload.response_time_sec,
        "subtopic": q_data["subtopic"],
        "topic": q_data["topic"],
        "skill": q_data["skill"],
        "difficulty": q_data["difficulty"]
    }

    if payload.session_id not in _local_logs:
        _local_logs[payload.session_id] = []
    _local_logs[payload.session_id].append(log_entry)

    try:
        sb = get_supabase()
        sb.table("response_logs").insert(log_entry).execute()
    except Exception:
        pass

    all_user_responses = _local_logs.get(payload.session_id, [])
    subtopic_diag = compute_subtopic_mastery(all_user_responses, q_data["subtopic"], 50.0)
    new_mastery = subtopic_diag["mastery_score"]

    session_answered_ids = [r["question_id"] for r in all_user_responses]
    total_limit = session.get("total_questions", 8)

    if len(session_answered_ids) >= total_limit:
        next_q_view = None
    else:
        next_q = select_next_adaptive_question(
            target_role=target_role,
            responses=all_user_responses,
            exclude_question_ids=session_answered_ids
        )
        if next_q:
            next_q_view = QuestionClientView(
                id=next_q["id"],
                skill=next_q["skill"],
                topic=next_q["topic"],
                subtopic=next_q["subtopic"],
                difficulty=next_q["difficulty"],
                question_text=next_q["question_text"],
                options=next_q["options"],
                expected_time_sec=next_q["expected_time_sec"],
                code_snippet=next_q.get("code_snippet"),
                tags=next_q.get("tags", [])
            )
        else:
            next_q_view = None

    if is_correct:
        feedback = f"Great work! Correct answer. Your subtopic mastery in '{q_data['subtopic']}' is now {new_mastery}%."
        next_diff = min(5, q_data["difficulty"] + 1)
    else:
        feedback = f"Incorrect. Notice the explanation below. Your subtopic mastery in '{q_data['subtopic']}' adjusted to {new_mastery}%."
        next_diff = max(1, q_data["difficulty"] - 1)

    return AnswerEvaluationResponse(
        is_correct=is_correct,
        correct_index=q_data["correct_index"],
        explanation=q_data["explanation"],
        updated_subtopic_mastery=new_mastery,
        feedback=feedback,
        next_recommended_difficulty=next_diff,
        next_question=next_q_view
    )

@router.get("/session/{session_id}/summary")
def get_session_summary(session_id: str):
    session = _local_sessions.get(session_id, {
        "id": session_id,
        "user_id": "default",
        "target_role": "java_developer"
    })
    responses = _local_logs.get(session_id, [])

    try:
        sb = get_supabase()
        session_result = sb.table("assessment_sessions").select("*").eq("id", session_id).execute()
        if session_result.data:
            session = session_result.data[0]
        logs_result = sb.table("response_logs").select("*").eq("session_id", session_id).execute()
        if logs_result.data:
            responses = logs_result.data
    except Exception:
        pass

    total = len(responses)
    correct = sum(1 for r in responses if r.get("is_correct") == 1)
    accuracy = (correct / total * 100.0) if total > 0 else 0.0

    readiness_rep = calculate_placement_readiness(
        session.get("user_id", "default"),
        session.get("target_role", "java_developer"),
        responses
    )

    return {
        "session_id": session_id,
        "user_id": session.get("user_id", "default"),
        "target_role": session.get("target_role", "java_developer"),
        "total_questions": total,
        "correct_count": correct,
        "accuracy": round(accuracy, 1),
        "readiness_report": readiness_rep
    }

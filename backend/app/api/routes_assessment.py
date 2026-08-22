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

@router.post("/start")
def start_assessment_session(payload: StartAssessmentRequest):
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    sb = get_supabase()

    user_result = sb.table("users").select("*").eq("id", payload.user_id).execute()
    user = user_result.data[0] if user_result.data else None
    target_role = payload.target_role or (user["target_role"] if user else "java_developer")

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
    sb = get_supabase()
    q_data = get_question_by_id(payload.question_id)
    is_correct = (payload.selected_index == q_data["correct_index"])

    session_result = sb.table("assessment_sessions").select("*").eq("id", payload.session_id).execute()
    if not session_result.data:
        raise HTTPException(status_code=404, detail="Assessment session not found")
    session = session_result.data[0]
    target_role = session["target_role"]

    log_id = f"log_{uuid.uuid4().hex[:8]}"
    sb.table("response_logs").insert({
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
    }).execute()

    mastery_result = sb.table("skill_mastery").select("*").eq("user_id", payload.user_id).eq("subtopic", q_data["subtopic"]).execute()
    existing_mastery = mastery_result.data[0] if mastery_result.data else None
    prior_score = existing_mastery["mastery_score"] if existing_mastery else 50.0

    all_responses_result = sb.table("response_logs").select("*").eq("user_id", payload.user_id).execute()
    all_user_responses = all_responses_result.data or []

    subtopic_diag = compute_subtopic_mastery(all_user_responses, q_data["subtopic"], prior_score)
    new_mastery = subtopic_diag["mastery_score"]

    if existing_mastery:
        sb.table("skill_mastery").update({
            "mastery_score": new_mastery,
            "attempts_count": existing_mastery["attempts_count"] + 1,
            "correct_count": existing_mastery["correct_count"] + (1 if is_correct else 0),
            "avg_response_time": subtopic_diag["avg_latency_sec"]
        }).eq("user_id", payload.user_id).eq("subtopic", q_data["subtopic"]).execute()
    else:
        mastery_id = f"mst_{uuid.uuid4().hex[:8]}"
        sb.table("skill_mastery").insert({
            "id": mastery_id,
            "user_id": payload.user_id,
            "skill": q_data["skill"],
            "topic": q_data["topic"],
            "subtopic": q_data["subtopic"],
            "mastery_score": new_mastery,
            "attempts_count": 1,
            "correct_count": 1 if is_correct else 0,
            "avg_response_time": payload.response_time_sec
        }).execute()

    session_logs_result = sb.table("response_logs").select("question_id").eq("session_id", payload.session_id).execute()
    session_answered_ids = [r["question_id"] for r in (session_logs_result.data or [])]

    total_limit = session["total_questions"]
    if len(session_answered_ids) >= total_limit:
        sb.table("assessment_sessions").update({"status": "completed"}).eq("id", payload.session_id).execute()
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
    sb = get_supabase()
    session_result = sb.table("assessment_sessions").select("*").eq("id", session_id).execute()
    if not session_result.data:
        raise HTTPException(status_code=404, detail="Session not found")
    session = session_result.data[0]

    logs_result = sb.table("response_logs").select("*").eq("session_id", session_id).execute()
    responses = logs_result.data or []

    total = len(responses)
    correct = sum(1 for r in responses if r["is_correct"] == 1)
    accuracy = (correct / total * 100.0) if total > 0 else 0.0

    readiness_rep = calculate_placement_readiness(
        session["user_id"],
        session["target_role"],
        responses
    )

    return {
        "session_id": session_id,
        "user_id": session["user_id"],
        "target_role": session["target_role"],
        "total_questions": total,
        "correct_count": correct,
        "accuracy": round(accuracy, 1),
        "readiness_report": readiness_rep
    }

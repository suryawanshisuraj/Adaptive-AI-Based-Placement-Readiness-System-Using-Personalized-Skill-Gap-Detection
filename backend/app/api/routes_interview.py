from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from ..engine.interview_engine import get_interview_questions_for_role, evaluate_interview_response

router = APIRouter(prefix="/api/interview", tags=["AI Mock Interview"])

class InterviewEvaluateRequest(BaseModel):
    user_id: str
    question_id: str
    candidate_answer: str

@router.get("/questions/{role_id}")
def get_role_interview_questions(role_id: str):
    return get_interview_questions_for_role(role_id)

@router.post("/evaluate")
def evaluate_response(payload: InterviewEvaluateRequest):
    return evaluate_interview_response(payload.question_id, payload.candidate_answer)

from fastapi import APIRouter
from pydantic import BaseModel
from ..engine.resume_analyzer import analyze_resume_text

router = APIRouter(prefix="/api/resume", tags=["Resume Analyzer"])

class ResumeAnalyzeRequest(BaseModel):
    user_id: str
    target_role: str
    resume_text: str

@router.post("/analyze")
def analyze_resume(payload: ResumeAnalyzeRequest):
    return analyze_resume_text(payload.resume_text, payload.target_role)

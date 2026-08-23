import uuid
from fastapi import APIRouter
from ..database import get_supabase, db_get_user, db_get_user_responses
from ..schemas import LearningRoadmapResponse, RoadmapStepSchema
from ..engine.recommender import generate_personalized_roadmap
from ..data.learning_resources import get_resource_for_subtopic

router = APIRouter(prefix="/api/roadmap", tags=["Learning Roadmap"])

@router.get("/generate/{user_id}", response_model=LearningRoadmapResponse)
def get_or_generate_roadmap(user_id: str, regenerate: bool = False):
    user = db_get_user(user_id)
    target_role = user["target_role"] if user else "java_developer"
    responses = db_get_user_responses(user_id)

    # Generate new dynamic roadmap
    raw_steps = generate_personalized_roadmap(user_id, target_role, responses)
    roadmap_id = f"rdm_{uuid.uuid4().hex[:8]}"

    try:
        sb = get_supabase()
        sb.table("learning_roadmaps").insert({
            "id": roadmap_id,
            "user_id": user_id,
            "target_role": target_role,
            "is_active": 1
        }).execute()
    except Exception:
        pass

    steps = []
    step_records = []
    for s in raw_steps:
        step_id = f"step_{uuid.uuid4().hex[:8]}"
        step_records.append({
            "id": step_id,
            "roadmap_id": roadmap_id,
            "day_number": s["day_number"],
            "skill": s["skill"],
            "topic": s["topic"],
            "subtopic": s["subtopic"],
            "action_title": s["action_title"],
            "explanation_summary": s["explanation_summary"],
            "target_questions_count": s["target_questions_count"],
            "is_completed": 0
        })
        steps.append(RoadmapStepSchema(
            id=step_id,
            day_number=s["day_number"],
            skill=s["skill"],
            topic=s["topic"],
            subtopic=s["subtopic"],
            action_title=s["action_title"],
            explanation_summary=s["explanation_summary"],
            target_questions_count=s["target_questions_count"],
            is_completed=False,
            score_achieved=None,
            recommended_resources=s.get("recommended_resources", [])
        ))

    try:
        if step_records:
            sb = get_supabase()
            sb.table("roadmap_steps").insert(step_records).execute()
    except Exception:
        pass

    return LearningRoadmapResponse(
        roadmap_id=roadmap_id,
        user_id=user_id,
        target_role=target_role,
        generated_at="Just now",
        steps=steps,
        completion_percentage=0.0
    )

@router.post("/step/{step_id}/toggle-complete")
def toggle_step_complete(step_id: str):
    sb = get_supabase()
    step_result = sb.table("roadmap_steps").select("*").eq("id", step_id).execute()
    if not step_result.data:
        raise HTTPException(status_code=404, detail="Step not found")
    step = step_result.data[0]
    new_status = 0 if step["is_completed"] == 1 else 1
    sb.table("roadmap_steps").update({"is_completed": new_status}).eq("id", step_id).execute()
    return {"step_id": step_id, "is_completed": bool(new_status)}

@router.get("/resource/{subtopic}")
def get_resource_details(subtopic: str):
    return get_resource_for_subtopic(subtopic)

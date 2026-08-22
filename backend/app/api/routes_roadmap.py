import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import get_supabase
from ..schemas import LearningRoadmapResponse, RoadmapStepSchema
from ..engine.recommender import generate_personalized_roadmap
from ..data.learning_resources import get_resource_for_subtopic

router = APIRouter(prefix="/api/roadmap", tags=["Learning Roadmap"])

@router.get("/generate/{user_id}", response_model=LearningRoadmapResponse)
def get_or_generate_roadmap(user_id: str, regenerate: bool = False):
    sb = get_supabase()

    user_result = sb.table("users").select("*").eq("id", user_id).execute()
    user = user_result.data[0] if user_result.data else None
    target_role = user["target_role"] if user else "java_developer"

    responses_result = sb.table("response_logs").select("*").eq("user_id", user_id).execute()
    responses = responses_result.data or []

    roadmap_result = sb.table("learning_roadmaps").select("*").eq("user_id", user_id).eq("is_active", 1).execute()
    roadmap_row = roadmap_result.data[0] if roadmap_result.data else None

    if roadmap_row and not regenerate:
        if roadmap_row["target_role"] == target_role:
            roadmap_id = roadmap_row["id"]
            steps_result = sb.table("roadmap_steps").select("*").eq("roadmap_id", roadmap_id).order("day_number").execute()
            step_rows = steps_result.data or []

            steps = []
            completed_count = 0
            for s in step_rows:
                is_comp = bool(s["is_completed"])
                if is_comp:
                    completed_count += 1
                res = get_resource_for_subtopic(s["subtopic"])
                steps.append(RoadmapStepSchema(
                    id=s["id"],
                    day_number=s["day_number"],
                    skill=s["skill"],
                    topic=s["topic"],
                    subtopic=s["subtopic"],
                    action_title=s["action_title"],
                    explanation_summary=s["explanation_summary"],
                    target_questions_count=s["target_questions_count"],
                    is_completed=is_comp,
                    score_achieved=s.get("score_achieved"),
                    recommended_resources=res.get("curated_links", [])
                ))
            comp_pct = (completed_count / len(steps) * 100.0) if steps else 0.0
            return LearningRoadmapResponse(
                roadmap_id=roadmap_id,
                user_id=user_id,
                target_role=target_role,
                generated_at=str(roadmap_row.get("generated_at", "")),
                steps=steps,
                completion_percentage=round(comp_pct, 1)
            )
        else:
            # Target role changed! Deactivate old active roadmap
            sb.table("learning_roadmaps").update({"is_active": 0}).eq("id", roadmap_row["id"]).execute()

    # Generate new dynamic roadmap
    raw_steps = generate_personalized_roadmap(user_id, target_role, responses)
    roadmap_id = f"rdm_{uuid.uuid4().hex[:8]}"

    sb.table("learning_roadmaps").insert({
        "id": roadmap_id,
        "user_id": user_id,
        "target_role": target_role,
        "is_active": 1
    }).execute()

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

    if step_records:
        sb.table("roadmap_steps").insert(step_records).execute()

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

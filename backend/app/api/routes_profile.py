import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Body
from ..database import get_supabase, db_get_user, db_upsert_user, db_save_user_skill_priors, db_get_user_skill_priors
from ..schemas import UserCreate, UserResponse, TargetRoleUpdate
from ..data.role_profiles import get_all_roles, get_role_profile

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("/roles")
def get_roles():
    return get_all_roles()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    new_id = user.id if hasattr(user, 'id') and user.id else f"usr_{uuid.uuid4().hex[:8]}"
    existing = db_get_user(new_id)
    if existing:
        return UserResponse(
            id=existing["id"],
            name=existing["name"],
            email=existing["email"],
            target_role=existing["target_role"],
            created_at=str(existing.get("created_at", ""))
        )

    user_dict = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "target_role": user.target_role
    }
    db_upsert_user(user_dict)

    return UserResponse(
        id=new_id,
        name=user.name,
        email=user.email,
        target_role=user.target_role
    )

@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: str):
    user = db_get_user(user_id)
    if user:
        return UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            target_role=user["target_role"],
            created_at=str(user.get("created_at", ""))
        )

    # Auto create if not found
    default_user = {
        "id": user_id,
        "name": "Candidate",
        "email": f"{user_id}@campus.edu",
        "target_role": "java_developer"
    }
    db_upsert_user(default_user)
    return UserResponse(
        id=user_id,
        name="Candidate",
        email=f"{user_id}@campus.edu",
        target_role="java_developer",
        created_at=""
    )

@router.put("/{user_id}/target-role")
def update_target_role(user_id: str, payload: TargetRoleUpdate):
    user = db_get_user(user_id) or {
        "id": user_id,
        "name": "Candidate",
        "email": f"{user_id}@campus.edu",
        "target_role": payload.target_role
    }
    user["target_role"] = payload.target_role
    db_upsert_user(user)

    return {
        "status": "success",
        "user_id": user_id,
        "target_role": payload.target_role,
        "role_info": get_role_profile(payload.target_role)
    }

@router.post("/{user_id}/skills")
def save_user_skills(user_id: str, skills_payload: Dict[str, float] = Body(...)):
    """Saves customized skill mastery priors for this candidate."""
    db_save_user_skill_priors(user_id, skills_payload)
    return {
        "status": "success",
        "user_id": user_id,
        "saved_skills": skills_payload
    }

@router.get("/{user_id}/skills")
def get_user_skills(user_id: str):
    """Retrieves candidate's customized skill mastery priors."""
    priors = db_get_user_skill_priors(user_id)
    return priors

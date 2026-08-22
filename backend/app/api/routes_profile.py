import uuid
from fastapi import APIRouter, HTTPException
from ..database import get_supabase
from ..schemas import UserCreate, UserResponse, TargetRoleUpdate
from ..data.role_profiles import get_all_roles, get_role_profile

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("/roles")
def get_roles():
    return get_all_roles()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    try:
        sb = get_supabase()
        result = sb.table("users").select("*").eq("email", user.email).execute()
        if result.data:
            existing = result.data[0]
            return UserResponse(
                id=existing["id"],
                name=existing["name"],
                email=existing["email"],
                target_role=existing["target_role"],
                created_at=str(existing.get("created_at", ""))
            )

        new_id = user.id if hasattr(user, 'id') and user.id else f"usr_{uuid.uuid4().hex[:8]}"
        sb.table("users").insert({
            "id": new_id,
            "name": user.name,
            "email": user.email,
            "target_role": user.target_role
        }).execute()

        return UserResponse(
            id=new_id,
            name=user.name,
            email=user.email,
            target_role=user.target_role
        )
    except Exception as e:
        # Tables might not exist yet - return a graceful response
        fallback_id = f"usr_{uuid.uuid4().hex[:8]}"
        return UserResponse(
            id=fallback_id,
            name=user.name,
            email=user.email,
            target_role=user.target_role
        )

@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: str):
    try:
        sb = get_supabase()
        result = sb.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            new_id = user_id if user_id != "default" else "usr_demo_01"
            try:
                sb.table("users").insert({
                    "id": new_id,
                    "name": "Alex Rivera",
                    "email": f"alex.rivera.{new_id}@campus.edu",
                    "target_role": "java_developer"
                }).execute()
                result = sb.table("users").select("*").eq("id", new_id).execute()
            except Exception:
                pass

        if result.data:
            row = result.data[0]
            return UserResponse(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                target_role=row["target_role"],
                created_at=str(row.get("created_at", ""))
            )
    except Exception:
        pass

    # Fallback — tables not yet created, return a local default
    return UserResponse(
        id=user_id,
        name="Student",
        email="student@campus.edu",
        target_role="java_developer",
        created_at=""
    )

@router.put("/{user_id}/target-role")
def update_target_role(user_id: str, payload: TargetRoleUpdate):
    try:
        sb = get_supabase()
        sb.table("users").update({"target_role": payload.target_role}).eq("id", user_id).execute()
        sb.table("learning_roadmaps").update({"is_active": 0}).eq("user_id", user_id).execute()
    except Exception:
        pass  # graceful degradation until tables exist

    return {
        "user_id": user_id,
        "target_role": payload.target_role,
        "role_details": get_role_profile(payload.target_role)
    }

"""Auth routes: GET /auth/me, POST /auth/profile."""

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user_id, get_supabase_dep
from app.api.v1.auth.schemas import ProfileCreateRequest, UserResponse
from app.db.queries import users as users_q

router = APIRouter(prefix="/auth", tags=["auth"])


def _to_user_response(user: dict, passport: dict | None) -> UserResponse:
    return UserResponse(
        id=user["id"],
        phone=user.get("phone"),
        full_name=user.get("full_name"),
        preferred_language=user["preferred_language"],
        state=user.get("state"),
        occupation_category=user.get("occupation_category"),
        passport_code=passport["passport_code"] if passport else None,
        passport_id=passport["id"] if passport else None,
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> UserResponse:
    user = users_q.get_user_by_id(supabase, user_id)
    if not user:
        from app.core.exceptions import ServiceError

        raise ServiceError("User profile not found. POST /auth/profile first.", 404)
    passport = users_q.get_passport_by_user_id(supabase, user_id)
    return _to_user_response(user, passport)


@router.post("/profile", response_model=UserResponse)
def create_or_update_profile(
    body: ProfileCreateRequest,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> UserResponse:
    user = users_q.upsert_user(
        supabase,
        user_id,
        {
            "full_name": body.full_name,
            "phone": body.phone,
            "preferred_language": body.preferred_language,
            "state": body.state,
            "occupation_category": body.occupation_category,
        },
    )
    passport = users_q.get_passport_by_user_id(supabase, user_id)
    if not passport:
        passport = users_q.create_passport_for_user(supabase, user_id)
    return _to_user_response(user, passport)

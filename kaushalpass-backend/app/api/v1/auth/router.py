from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.api.v1.auth.schemas import ProfileCreateRequest, UserResponse
from app.db.queries import passport as passport_queries
from app.db.queries import users as users_queries
from app.db.queries.users import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
_security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_security)],
) -> UUID:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = credentials.credentials
    settings = get_settings()
    try:
        if settings["supabase_jwt_secret"]:
            payload = jwt.decode(
                token,
                settings["supabase_jwt_secret"],
                algorithms=["HS256"],
                audience="authenticated",
            )
        else:
            payload = jwt.get_unverified_claims(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject"
        )
    return UUID(str(sub))


CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: CurrentUserId) -> UserResponse:
    user = await users_queries.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
    passport = await passport_queries.get_passport_by_user(user_id)
    return UserResponse(
        id=UUID(user["id"]),
        phone=user.get("phone"),
        full_name=user["full_name"],
        preferred_language=user["preferred_language"],
        state=user.get("state"),
        occupation_category=user.get("occupation_category"),
        passport_code=passport["passport_code"] if passport else None,
        passport_id=UUID(passport["id"]) if passport else None,
        created_at=user.get("created_at"),
    )


@router.post("/profile", response_model=UserResponse)
async def upsert_profile(
    body: ProfileCreateRequest,
    user_id: CurrentUserId,
) -> UserResponse:
    user = await users_queries.upsert_user(
        user_id,
        full_name=body.full_name,
        preferred_language=body.preferred_language,
        phone=body.phone,
        state=body.state,
        occupation_category=body.occupation_category,
    )
    passport = await passport_queries.get_passport_by_user(user_id)
    if not passport:
        passport = await users_queries.create_passport_for_user(user_id)

    return UserResponse(
        id=UUID(user["id"]),
        phone=user.get("phone"),
        full_name=user["full_name"],
        preferred_language=user["preferred_language"],
        state=user.get("state"),
        occupation_category=user.get("occupation_category"),
        passport_code=passport["passport_code"],
        passport_id=UUID(passport["id"]),
        created_at=user.get("created_at"),
    )

"""Passport routes."""

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user_id, get_supabase_dep
from app.api.v1.passport.schemas import (
    PassportResponse,
    SkillEntryCreate,
    SkillEntryResponse,
    SkillEntryUpdate,
)
from app.services import passport_service

router = APIRouter(prefix="/passport", tags=["passport"])


@router.get("/me", response_model=PassportResponse)
def get_my_passport(
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> PassportResponse:
    data = passport_service.get_passport_for_user(supabase, user_id)
    return PassportResponse(**data)


@router.post("/skills", response_model=SkillEntryResponse)
def add_skill(
    body: SkillEntryCreate,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> SkillEntryResponse:
    skill = passport_service.add_skill(supabase, user_id, body.model_dump())
    return SkillEntryResponse(**skill)


@router.put("/skills/{skill_id}", response_model=SkillEntryResponse)
def update_skill(
    skill_id: str,
    body: SkillEntryUpdate,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> SkillEntryResponse:
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    skill = passport_service.update_skill_entry(supabase, user_id, skill_id, updates)
    return SkillEntryResponse(**skill)


@router.delete("/skills/{skill_id}", response_model=SkillEntryResponse)
def delete_skill(
    skill_id: str,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> SkillEntryResponse:
    skill = passport_service.soft_delete_skill(supabase, user_id, skill_id)
    return SkillEntryResponse(**skill)

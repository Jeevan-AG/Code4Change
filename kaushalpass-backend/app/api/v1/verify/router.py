"""Public passport verification — no auth."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from supabase import Client

from app.api.deps import get_supabase_dep
from app.services import passport_service

router = APIRouter(prefix="/verify", tags=["verify"])


class PublicSkillItem(BaseModel):
    skill_name: str
    skill_level: str
    nsqf_level: int
    verification_status: str


class PublicVerifyResponse(BaseModel):
    passport_code: str
    holder_name: str
    issued_at: str
    skills: list[PublicSkillItem]


@router.get("/{passport_id}", response_model=PublicVerifyResponse)
def verify_passport(
    passport_id: str,
    supabase: Client = Depends(get_supabase_dep),
) -> PublicVerifyResponse:
    data = passport_service.get_public_verify_data(supabase, passport_id)
    return PublicVerifyResponse(**data)

"""Passport schemas."""

from typing import Literal

from pydantic import BaseModel, Field

SkillLevel = Literal["beginner", "intermediate", "expert"]
VerificationStatus = Literal["ai_provisional", "community_verified", "master_verified"]


class SkillEntryResponse(BaseModel):
    id: str
    passportId: str
    skillName: str
    skillLevel: SkillLevel
    nsqfLevel: int = Field(ge=1, le=8)
    confidenceScore: float = Field(ge=0, le=1)
    verificationStatus: VerificationStatus
    isVerified: bool
    archived: bool
    createdAt: str


class PassportResponse(BaseModel):
    id: str
    passport_code: str
    user_id: str
    is_active: bool
    total_skills: int
    issued_at: str
    skills: list[SkillEntryResponse]


class SkillEntryCreate(BaseModel):
    skill_name: str = Field(min_length=1)
    skill_level: SkillLevel
    nsqf_level: int | None = Field(default=None, ge=1, le=8)
    confidence_score: float = Field(default=0.7, ge=0, le=1)
    verification_status: VerificationStatus = "ai_provisional"
    is_verified: bool = False


class SkillEntryUpdate(BaseModel):
    skill_name: str | None = None
    skill_level: SkillLevel | None = None
    nsqf_level: int | None = Field(default=None, ge=1, le=8)
    confidence_score: float | None = Field(default=None, ge=0, le=1)
    verification_status: VerificationStatus | None = None
    is_verified: bool | None = None

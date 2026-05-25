from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class QueueItem(BaseModel):
    assessment_id: UUID
    user_id: UUID
    holder_name: str | None = None
    skill_name: str | None = None
    input_type: str
    language_code: str | None = None
    transcribed_text: str | None = None
    verification_status: str | None = None
    created_at: datetime | None = None


class VerifierSubmission(BaseModel):
    rubric_scores: dict = Field(default_factory=dict)
    overall_score: float = Field(ge=0.0, le=5.0)
    notes: str | None = None


class VerifierSubmitResponse(BaseModel):
    review_id: UUID
    assessment_id: UUID
    consensus_reached: bool
    verification_status: str | None = None
    escalated: bool = False

"""Verifier schemas."""

from typing import Any

from pydantic import BaseModel, Field


class QueueItem(BaseModel):
    id: str
    user_id: str
    skill_id: str | None
    language_code: str
    transcribed_text: str | None
    parsed_result: dict[str, Any] | None
    created_at: str


class VerifierSubmission(BaseModel):
    rubric_scores: dict[str, Any] = Field(default_factory=dict)
    overall_score: float = Field(ge=0, le=1)
    notes: str | None = None


class VerifierSubmitResponse(BaseModel):
    review_id: str
    review_count: int
    consensus: str | None

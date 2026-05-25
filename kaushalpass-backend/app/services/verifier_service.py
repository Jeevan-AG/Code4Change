"""Verifier consensus layer."""

from __future__ import annotations

from typing import Any

from supabase import Client

from app.core.exceptions import ServiceError
from app.db.queries import assessments as assessments_q
from app.db.queries import passport as passport_q


async def submit_verifier_review(
    supabase: Client,
    assessment_id: str,
    verifier_user_id: str,
    rubric_scores: dict[str, Any],
    overall_score: float,
    notes: str | None = None,
) -> dict[str, Any]:
    assessment = assessments_q.get_assessment_by_id(supabase, assessment_id)
    if not assessment:
        raise ServiceError("Assessment not found", 404)

    review = assessments_q.insert_verifier_review(
        supabase,
        assessment_id,
        verifier_user_id,
        rubric_scores,
        overall_score,
        notes,
    )

    reviews = assessments_q.get_assessment_reviews(supabase, assessment_id)
    consensus: str | None = None

    if len(reviews) >= 2:
        score_delta = abs(reviews[0]["overall_score"] - reviews[1]["overall_score"])
        skill_id = assessment.get("skill_id")
        if score_delta < 0.3 and skill_id:
            passport_q.update_skill_verification_status(
                supabase, str(skill_id), "community_verified", is_verified=True
            )
            consensus = "community_verified"
        else:
            assessments_q.flag_for_escalation(supabase, assessment_id)
            consensus = "escalated"

    return {
        "review": review,
        "review_count": len(reviews),
        "consensus": consensus,
    }

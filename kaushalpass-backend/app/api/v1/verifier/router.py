"""Verifier queue and submission routes."""

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user_id, get_supabase_dep
from app.api.v1.verifier.schemas import QueueItem, VerifierSubmission, VerifierSubmitResponse
from app.db.queries import assessments as assessments_q
from app.services import verifier_service

router = APIRouter(prefix="/verifier", tags=["verifier"])


@router.get("/queue", response_model=list[QueueItem])
def verifier_queue(
    _user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> list[QueueItem]:
    rows = assessments_q.get_pending_queue(supabase)
    return [
        QueueItem(
            id=r["id"],
            user_id=r["user_id"],
            skill_id=r.get("skill_id"),
            language_code=r["language_code"],
            transcribed_text=r.get("transcribed_text"),
            parsed_result=r.get("parsed_result"),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/submit/{assessment_id}", response_model=VerifierSubmitResponse)
async def submit_review(
    assessment_id: str,
    body: VerifierSubmission,
    verifier_user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> VerifierSubmitResponse:
    result = await verifier_service.submit_verifier_review(
        supabase,
        assessment_id,
        verifier_user_id,
        body.rubric_scores,
        body.overall_score,
        body.notes,
    )
    return VerifierSubmitResponse(
        review_id=result["review"]["id"],
        review_count=result["review_count"],
        consensus=result["consensus"],
    )

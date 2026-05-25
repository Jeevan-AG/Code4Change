from uuid import UUID

from fastapi import APIRouter

from app.api.v1.verifier.schemas import QueueItem, VerifierSubmission, VerifierSubmitResponse
from app.db.queries import assessments as assessments_queries
from fastapi import HTTPException

from app.api.v1.auth.router import CurrentUserId

router = APIRouter(prefix="/verifier", tags=["verifier"])

CONSENSUS_DELTA = 0.3


@router.get("/queue", response_model=list[QueueItem])
async def verifier_queue(_user_id: CurrentUserId) -> list[QueueItem]:
    rows = await assessments_queries.get_pending_queue()
    items: list[QueueItem] = []
    for row in rows:
        users = row.get("users") or {}
        skills = row.get("skills") or {}
        items.append(
            QueueItem(
                assessment_id=UUID(row["id"]),
                user_id=UUID(row["user_id"]),
                holder_name=users.get("full_name"),
                skill_name=skills.get("skill_name"),
                input_type=row["input_type"],
                language_code=row.get("language_code"),
                transcribed_text=row.get("transcribed_text"),
                verification_status=skills.get("verification_status"),
                created_at=row.get("created_at"),
            )
        )
    return items


@router.post("/submit/{assessment_id}", response_model=VerifierSubmitResponse)
async def submit_verification(
    assessment_id: UUID,
    body: VerifierSubmission,
    verifier_user_id: CurrentUserId,
) -> VerifierSubmitResponse:
    assessment = await assessments_queries.get_assessment_by_id(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    review = await assessments_queries.insert_verifier_review(
        assessment_id,
        verifier_user_id,
        rubric_scores=body.rubric_scores,
        overall_score=body.overall_score,
        notes=body.notes,
    )

    reviews = await assessments_queries.get_assessment_reviews(assessment_id)
    consensus_reached = False
    escalated = False
    verification_status: str | None = None

    if len(reviews) == 2:
        score_delta = abs(float(reviews[0]["overall_score"]) - float(reviews[1]["overall_score"]))
        skill_id = assessment.get("skill_id")
        if score_delta < CONSENSUS_DELTA and skill_id:
            await assessments_queries.update_skill_verification_status(
                UUID(skill_id), "community_verified"
            )
            consensus_reached = True
            verification_status = "community_verified"
        else:
            await assessments_queries.flag_for_escalation(assessment_id)
            escalated = True

    return VerifierSubmitResponse(
        review_id=UUID(review["id"]),
        assessment_id=assessment_id,
        consensus_reached=consensus_reached,
        verification_status=verification_status,
        escalated=escalated,
    )

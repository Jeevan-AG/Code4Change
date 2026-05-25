"""Assessment and verifier queries."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from supabase import Client


def get_assessment_by_id(supabase: Client, assessment_id: str) -> dict[str, Any] | None:
    result = (
        supabase.table("assessments")
        .select("*")
        .eq("id", assessment_id)
        .maybe_single()
        .execute()
    )
    return result.data if result.data else None


def get_pending_queue(supabase: Client, limit: int = 50) -> list[dict[str, Any]]:
    """Assessments linked to skills still ai_provisional, not escalated."""
    result = (
        supabase.table("assessments")
        .select("*, skills(skill_name, verification_status)")
        .not_.is_("skill_id", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    items = result.data or []
    queue: list[dict[str, Any]] = []
    for row in items:
        meta = row.get("parsed_result") or {}
        if isinstance(meta, dict) and meta.get("escalated"):
            continue
        skill = row.get("skills")
        if skill and skill.get("verification_status") == "ai_provisional":
            queue.append(row)
    return queue


def get_assessment_reviews(supabase: Client, assessment_id: str) -> list[dict[str, Any]]:
    result = (
        supabase.table("verifier_reviews")
        .select("*")
        .eq("assessment_id", assessment_id)
        .order("created_at")
        .execute()
    )
    return result.data or []


def insert_verifier_review(
    supabase: Client,
    assessment_id: str,
    verifier_user_id: str,
    rubric_scores: dict[str, Any],
    overall_score: float,
    notes: str | None = None,
) -> dict[str, Any]:
    row = {
        "assessment_id": assessment_id,
        "verifier_user_id": verifier_user_id,
        "rubric_scores": rubric_scores,
        "overall_score": overall_score,
        "notes": notes,
    }
    result = supabase.table("verifier_reviews").insert(row).execute()
    if not result.data:
        raise RuntimeError("Failed to insert verifier review")
    return result.data[0]


def flag_for_escalation(supabase: Client, assessment_id: str) -> None:
    assessment = get_assessment_by_id(supabase, assessment_id)
    if not assessment:
        return
    parsed = assessment.get("parsed_result") or {}
    if not isinstance(parsed, dict):
        parsed = {}
    parsed["escalated"] = True
    parsed["escalation_reason"] = "reviewer_score_conflict"
    supabase.table("assessments").update({"parsed_result": parsed}).eq("id", assessment_id).execute()

"""Passport and skills queries."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from supabase import Client


def get_passport_by_user(supabase: Client, user_id: str) -> dict[str, Any] | None:
    result = (
        supabase.table("passports")
        .select("*")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    return result.data if result.data else None


def get_passport_by_id(supabase: Client, passport_id: str) -> dict[str, Any] | None:
    result = (
        supabase.table("passports")
        .select("*")
        .eq("id", passport_id)
        .maybe_single()
        .execute()
    )
    return result.data if result.data else None


def get_skills(supabase: Client, passport_id: str, include_archived: bool = False) -> list[dict[str, Any]]:
    query = supabase.table("skills").select("*").eq("passport_id", passport_id)
    if not include_archived:
        query = query.eq("archived", False)
    result = query.order("created_at", desc=True).execute()
    return result.data or []


def get_skill_by_id(supabase: Client, skill_id: str) -> dict[str, Any] | None:
    result = supabase.table("skills").select("*").eq("id", skill_id).maybe_single().execute()
    return result.data if result.data else None


def insert_skill(supabase: Client, passport_id: str, skill: dict[str, Any]) -> dict[str, Any]:
    row = {
        "passport_id": passport_id,
        "skill_name": skill["skill_name"],
        "skill_level": skill["skill_level"],
        "nsqf_level": skill["nsqf_level"],
        "confidence_score": skill["confidence_score"],
        "verification_status": skill.get("verification_status", "ai_provisional"),
        "is_verified": skill.get("is_verified", False),
        "archived": False,
    }
    result = supabase.table("skills").insert(row).execute()
    if not result.data:
        raise RuntimeError("Failed to insert skill")
    _increment_total_skills(supabase, passport_id)
    return result.data[0]


def update_skill(supabase: Client, skill_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "skill_name",
        "skill_level",
        "nsqf_level",
        "confidence_score",
        "verification_status",
        "is_verified",
    }
    row = {k: v for k, v in updates.items() if k in allowed}
    row["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = supabase.table("skills").update(row).eq("id", skill_id).execute()
    if not result.data:
        raise RuntimeError("Skill not found")
    return result.data[0]


def soft_delete_skill(supabase: Client, skill_id: str, passport_id: str) -> dict[str, Any]:
    result = (
        supabase.table("skills")
        .update({"archived": True, "updated_at": datetime.now(timezone.utc).isoformat()})
        .eq("id", skill_id)
        .eq("passport_id", passport_id)
        .execute()
    )
    if not result.data:
        raise RuntimeError("Skill not found")
    _decrement_total_skills(supabase, passport_id)
    return result.data[0]


def _increment_total_skills(supabase: Client, passport_id: str) -> None:
    passport = get_passport_by_id(supabase, passport_id)
    if not passport:
        return
    total = int(passport.get("total_skills", 0)) + 1
    supabase.table("passports").update({"total_skills": total}).eq("id", passport_id).execute()


def _decrement_total_skills(supabase: Client, passport_id: str) -> None:
    passport = get_passport_by_id(supabase, passport_id)
    if not passport:
        return
    total = max(0, int(passport.get("total_skills", 0)) - 1)
    supabase.table("passports").update({"total_skills": total}).eq("id", passport_id).execute()


def update_skill_verification_status(
    supabase: Client,
    skill_id: str,
    status: str,
    *,
    is_verified: bool = True,
) -> dict[str, Any]:
    result = (
        supabase.table("skills")
        .update(
            {
                "verification_status": status,
                "is_verified": is_verified,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .eq("id", skill_id)
        .execute()
    )
    if not result.data:
        raise RuntimeError("Skill not found")
    return result.data[0]

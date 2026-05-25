"""Passport business logic."""

from __future__ import annotations

from typing import Any

from supabase import Client

from app.core.exceptions import ServiceError
from app.db.queries import passport as passport_q
from app.db.queries import users as users_q
from app.services.nsqf_mapper import map_skill_to_nsqf


def get_passport_for_user(supabase: Client, user_id: str) -> dict[str, Any]:
    passport = passport_q.get_passport_by_user(supabase, user_id)
    if not passport:
        raise ServiceError("Passport not found", 404)
    skills = passport_q.get_skills(supabase, passport["id"])
    return {
        "id": passport["id"],
        "passport_code": passport["passport_code"],
        "user_id": passport["user_id"],
        "is_active": passport["is_active"],
        "total_skills": passport["total_skills"],
        "issued_at": passport["issued_at"],
        "skills": [_format_skill(s) for s in skills],
    }


def _format_skill(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "passportId": row["passport_id"],
        "skillName": row["skill_name"],
        "skillLevel": row["skill_level"],
        "nsqfLevel": row["nsqf_level"],
        "confidenceScore": row["confidence_score"],
        "verificationStatus": row["verification_status"],
        "isVerified": row["is_verified"],
        "archived": row["archived"],
        "createdAt": row["created_at"],
    }


def add_skill(supabase: Client, user_id: str, skill_data: dict[str, Any]) -> dict[str, Any]:
    passport = passport_q.get_passport_by_user(supabase, user_id)
    if not passport:
        raise ServiceError("Passport not found", 404)

    nsqf_level = skill_data.get("nsqf_level")
    if nsqf_level is None:
        mapped = map_skill_to_nsqf(skill_data["skill_name"])
        if mapped:
            nsqf_level = mapped["nsqf_level"]
            if "skill_level" not in skill_data:
                skill_data["skill_level"] = mapped["level"]
        else:
            nsqf_level = 3

    row = {
        "skill_name": skill_data["skill_name"],
        "skill_level": skill_data["skill_level"],
        "nsqf_level": int(nsqf_level),
        "confidence_score": float(skill_data.get("confidence_score", 0.7)),
        "verification_status": skill_data.get("verification_status", "ai_provisional"),
        "is_verified": skill_data.get("is_verified", False),
    }
    inserted = passport_q.insert_skill(supabase, passport["id"], row)
    return _format_skill(inserted)


def update_skill_entry(
    supabase: Client,
    user_id: str,
    skill_id: str,
    updates: dict[str, Any],
) -> dict[str, Any]:
    passport = passport_q.get_passport_by_user(supabase, user_id)
    if not passport:
        raise ServiceError("Passport not found", 404)
    skill = passport_q.get_skill_by_id(supabase, skill_id)
    if not skill or skill["passport_id"] != passport["id"]:
        raise ServiceError("Skill not found", 404)
    updated = passport_q.update_skill(supabase, skill_id, updates)
    return _format_skill(updated)


def soft_delete_skill(supabase: Client, user_id: str, skill_id: str) -> dict[str, Any]:
    passport = passport_q.get_passport_by_user(supabase, user_id)
    if not passport:
        raise ServiceError("Passport not found", 404)
    deleted = passport_q.soft_delete_skill(supabase, skill_id, passport["id"])
    return _format_skill(deleted)


def get_public_verify_data(supabase: Client, passport_id: str) -> dict[str, Any]:
    """Public verify — no PII beyond name."""
    passport = passport_q.get_passport_by_id(supabase, passport_id)
    if not passport:
        raise ServiceError("Passport not found", 404)

    user = users_q.get_user_by_id(supabase, passport["user_id"])
    holder_name = (user or {}).get("full_name") or "Skill Holder"
    skills = passport_q.get_skills(supabase, passport["id"])

    return {
        "passport_code": passport["passport_code"],
        "holder_name": holder_name,
        "issued_at": passport["issued_at"],
        "skills": [
            {
                "skill_name": s["skill_name"],
                "skill_level": s["skill_level"],
                "nsqf_level": s["nsqf_level"],
                "verification_status": s["verification_status"],
            }
            for s in skills
        ],
    }

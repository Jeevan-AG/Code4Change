"""User and passport bootstrap queries."""

from __future__ import annotations

import secrets
import string
from datetime import datetime, timezone
from typing import Any

from supabase import Client

VALID_LANGS = frozenset({"hi-IN", "ta-IN", "te-IN", "kn-IN", "bn-IN", "en-IN"})


def _generate_passport_code() -> str:
    year = datetime.now(timezone.utc).year
    suffix = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return f"KP-{year}-{suffix}"


def get_user_by_id(supabase: Client, user_id: str) -> dict[str, Any] | None:
    result = supabase.table("users").select("*").eq("id", user_id).maybe_single().execute()
    return result.data if result.data else None


def upsert_user(supabase: Client, user_id: str, profile: dict[str, Any]) -> dict[str, Any]:
    row = {
        "id": user_id,
        "phone": profile.get("phone"),
        "full_name": profile.get("full_name"),
        "preferred_language": profile.get("preferred_language", "hi-IN"),
        "state": profile.get("state"),
        "occupation_category": profile.get("occupation_category"),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if row["preferred_language"] not in VALID_LANGS:
        row["preferred_language"] = "hi-IN"
    result = supabase.table("users").upsert(row, on_conflict="id").execute()
    if not result.data:
        raise RuntimeError("Failed to upsert user")
    return result.data[0]


def get_passport_by_user_id(supabase: Client, user_id: str) -> dict[str, Any] | None:
    result = (
        supabase.table("passports")
        .select("*")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    return result.data if result.data else None


def create_passport_for_user(supabase: Client, user_id: str) -> dict[str, Any]:
    for _ in range(5):
        code = _generate_passport_code()
        existing = (
            supabase.table("passports")
            .select("id")
            .eq("passport_code", code)
            .maybe_single()
            .execute()
        )
        if not existing.data:
            break
    else:
        raise RuntimeError("Could not generate unique passport code")

    row = {
        "user_id": user_id,
        "passport_code": code,
        "is_active": True,
        "total_skills": 0,
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    result = supabase.table("passports").insert(row).execute()
    if not result.data:
        raise RuntimeError("Failed to create passport")
    return result.data[0]

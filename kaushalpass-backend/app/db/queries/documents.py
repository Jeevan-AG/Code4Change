"""Document storage queries."""

from __future__ import annotations

from typing import Any

from supabase import Client


def insert_document(supabase: Client, doc: dict[str, Any]) -> dict[str, Any]:
    result = supabase.table("documents").insert(doc).execute()
    if not result.data:
        raise RuntimeError("Failed to insert document")
    return result.data[0]


def get_phashes_for_user(supabase: Client, user_id: str) -> list[str]:
    result = (
        supabase.table("documents")
        .select("phash")
        .eq("user_id", user_id)
        .not_.is_("phash", "null")
        .execute()
    )
    return [row["phash"] for row in (result.data or []) if row.get("phash")]


def get_document_by_id(supabase: Client, document_id: str) -> dict[str, Any] | None:
    result = (
        supabase.table("documents")
        .select("*")
        .eq("id", document_id)
        .maybe_single()
        .execute()
    )
    return result.data if result.data else None

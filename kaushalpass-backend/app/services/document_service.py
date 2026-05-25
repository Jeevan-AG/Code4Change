"""Document upload with pHash dedup and Nemotron analysis."""

from __future__ import annotations

import uuid
from typing import Any

from supabase import Client

from app.config import Settings, get_settings
from app.core.exceptions import DuplicateMediaError, ServiceError
from app.db.queries import documents as documents_q
from app.services import nemotron_service
from app.utils.media_preprocessor import check_phash_duplicate, compute_phash

IMAGE_TYPES = frozenset({"image/jpeg", "image/jpg", "image/png", "image/webp"})
VIDEO_TYPES = frozenset({"video/mp4", "video/webm", "video/quicktime", "video/ogg"})


async def upload_to_storage(
    supabase: Client,
    bucket: str,
    path: str,
    data: bytes,
    content_type: str,
    settings: Settings | None = None,
) -> str:
    supabase.storage.from_(bucket).upload(
        path,
        data,
        file_options={"content-type": content_type, "upsert": "false"},
    )
    signed = supabase.storage.from_(bucket).create_signed_url(
        path,
        (settings or get_settings()).STORAGE_SIGNED_URL_EXPIRY_SECONDS,
    )
    url = signed.get("signedURL") or signed.get("signedUrl") or ""
    if not url:
        raise ServiceError("Failed to create signed URL", 502)
    return url


async def process_and_upload_document(
    supabase: Client,
    user_id: str,
    file_bytes: bytes,
    content_type: str,
    filename: str,
    skill_id: str | None = None,
    *,
    settings: Settings | None = None,
) -> dict[str, Any]:
    s = settings or get_settings()
    phash = compute_phash(file_bytes)
    existing = documents_q.get_phashes_for_user(supabase, user_id)
    if check_phash_duplicate(phash, existing):
        raise DuplicateMediaError()

    ct = content_type.lower()
    if ct in VIDEO_TYPES or filename.lower().endswith((".mp4", ".webm", ".mov")):
        analysis = await nemotron_service.analyze_craft_video(file_bytes, settings=s)
        file_type = "video"
    elif ct in IMAGE_TYPES or filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        analysis = await nemotron_service.analyze_single_image(file_bytes, settings=s)
        file_type = "image"
    else:
        raise ServiceError(f"Unsupported file type: {content_type}", 400)

    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    storage_path = f"{user_id}/{uuid.uuid4()}.{ext}"
    bucket = s.DOCUMENTS_BUCKET

    upload_to_storage_sync(supabase, bucket, storage_path, file_bytes, content_type, s)

    doc_row = {
        "user_id": user_id,
        "skill_id": skill_id,
        "storage_path": storage_path,
        "file_type": file_type,
        "file_size_bytes": len(file_bytes),
        "phash": phash,
        "nemotron_analysis": analysis,
    }
    inserted = documents_q.insert_document(supabase, doc_row)
    return {
        "id": inserted["id"],
        "storage_path": storage_path,
        "file_type": file_type,
        "file_size_bytes": len(file_bytes),
        "phash": phash,
        "nemotron_analysis": analysis,
    }


def upload_to_storage_sync(
    supabase: Client,
    bucket: str,
    path: str,
    data: bytes,
    content_type: str,
    settings: Settings,
) -> None:
    supabase.storage.from_(bucket).upload(
        path,
        data,
        file_options={"content-type": content_type, "upsert": "false"},
    )


def get_document_signed_url(
    supabase: Client,
    document_id: str,
    user_id: str,
    *,
    settings: Settings | None = None,
) -> str:
    s = settings or get_settings()
    doc = documents_q.get_document_by_id(supabase, document_id)
    if not doc or doc["user_id"] != user_id:
        raise ServiceError("Document not found", 404)
    signed = supabase.storage.from_(s.DOCUMENTS_BUCKET).create_signed_url(
        doc["storage_path"],
        s.STORAGE_SIGNED_URL_EXPIRY_SECONDS,
    )
    url = signed.get("signedURL") or signed.get("signedUrl") or ""
    if not url:
        raise ServiceError("Failed to create signed URL", 502)
    return url

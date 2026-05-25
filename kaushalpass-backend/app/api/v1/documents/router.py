"""Document upload routes."""

from fastapi import APIRouter, Depends, File, Form, UploadFile
from supabase import Client

from app.api.deps import get_current_user_id, get_supabase_dep
from app.api.v1.documents.schemas import DocumentUploadResponse, DocumentUrlResponse
from app.services import document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    skill_id: str | None = Form(default=None),
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> DocumentUploadResponse:
    data = await file.read()
    result = await document_service.process_and_upload_document(
        supabase,
        user_id,
        data,
        file.content_type or "application/octet-stream",
        file.filename or "upload.bin",
        skill_id=skill_id,
    )
    return DocumentUploadResponse(**result)


@router.get("/{document_id}/url", response_model=DocumentUrlResponse)
def get_document_url(
    document_id: str,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> DocumentUrlResponse:
    url = document_service.get_document_signed_url(supabase, document_id, user_id)
    return DocumentUrlResponse(url=url)

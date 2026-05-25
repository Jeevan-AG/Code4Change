"""Certificate generation routes."""

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user_id, get_supabase_dep
from app.api.v1.certificate.schemas import (
    CertificateGenerateResponse,
    CertificateStatusResponse,
)
from app.services import certificate_service

router = APIRouter(prefix="/certificate", tags=["certificate"])


@router.post("/generate", response_model=CertificateGenerateResponse)
def generate_certificate(
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_dep),
) -> CertificateGenerateResponse:
    result = certificate_service.generate_certificate_pdf(supabase, user_id)
    return CertificateGenerateResponse(**result)


@router.get("/status/{certificate_id}", response_model=CertificateStatusResponse)
def certificate_status(certificate_id: str) -> CertificateStatusResponse:
    job = certificate_service.get_certificate_status(certificate_id)
    return CertificateStatusResponse(**job)

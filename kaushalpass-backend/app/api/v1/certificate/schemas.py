"""Certificate schemas."""

from pydantic import BaseModel


class CertificateGenerateResponse(BaseModel):
    id: str
    status: str
    download_url: str | None
    passport_code: str
    generated_at: str


class CertificateStatusResponse(BaseModel):
    id: str
    status: str
    download_url: str | None = None

"""Document schemas."""

from typing import Any

from pydantic import BaseModel


class NemotronAnalysis(BaseModel):
    skill_detected: str | None = None
    technique_quality: int | None = None
    hands_visible: bool = False
    active_work: bool = False
    fraud_signals: list[str] = []
    confidence: float = 0.0


class DocumentUploadResponse(BaseModel):
    id: str
    storage_path: str
    file_type: str
    file_size_bytes: int
    phash: str
    nemotron_analysis: dict[str, Any]


class DocumentUrlResponse(BaseModel):
    url: str

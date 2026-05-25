"""Auth schemas."""

from typing import Literal

from pydantic import BaseModel, Field

LangCode = Literal["hi-IN", "ta-IN", "te-IN", "kn-IN", "bn-IN", "en-IN"]


class ProfileCreateRequest(BaseModel):
    full_name: str = Field(min_length=1)
    phone: str | None = None
    preferred_language: LangCode = "hi-IN"
    state: str | None = None
    occupation_category: str | None = None


class UserResponse(BaseModel):
    id: str
    phone: str | None
    full_name: str | None
    preferred_language: str
    state: str | None
    occupation_category: str | None
    passport_code: str | None = None
    passport_id: str | None = None

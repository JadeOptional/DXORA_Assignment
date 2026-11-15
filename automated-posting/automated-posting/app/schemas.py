import re
from typing import Optional
from urllib.parse import urlsplit
from pydantic import AnyHttpUrl, BaseModel, Field, TypeAdapter, field_validator

URL_PATTERN = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
TRAILING_PUNCTUATION = ".,!?;:)]}>'\""

class PostingRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)

    @field_validator("message")
    @classmethod
    def validate_exactly_one_cta_url(cls, value: str) -> str:
        matches = URL_PATTERN.findall(value)
        urls = [match.rstrip(TRAILING_PUNCTUATION) for match in matches]
        if len(urls) != 1:
            raise ValueError("Message must contain exactly one HTTP or HTTPS CTA link")

        try:
            validated_url = TypeAdapter(AnyHttpUrl).validate_python(urls[0])
            hostname = urlsplit(str(validated_url)).hostname
            if not hostname or ("." not in hostname and hostname != "localhost"):
                raise ValueError("URL must include a valid hostname")
        except Exception as exc:
            raise ValueError("CTA link must be a valid HTTP or HTTPS URL") from exc
        return value

class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None

class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]

from pydantic import BaseModel, Field
from typing import List, Dict


class RedactionRequest(BaseModel):

    id: str = Field(
        ...,
        description="The incident ID",
    )

    input_text: str = Field(
        ...,
        description="The text to redact",
    )

    model: str = Field(
        default="redaction:4b",
        description="The base LLM to generate reasoning paths (e.g., deepseek-r1, gemma3:1b).",
    )

    add_to_db: bool = Field(
        default=False,
        description="Whether to add the redaction to the database",
    )


class RedactionResponse(BaseModel):

    id: str = Field(
        ...,
        description="The incident ID",
    )

    redacted_text: str = Field(
        ...,
        description="The redacted text",
    )

    redacted_cases: List[Dict] = Field(
        ...,
        description="The redacted cases",
    )

    total_duration_seconds: float = Field(
        ...,
        description="The total duration in seconds",
    )

    created_at: str = Field(
        ...,
        description="The timestamp",
    )

    model: str = Field(
        ...,
        description="The model used",
    )




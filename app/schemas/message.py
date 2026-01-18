from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MessageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def strip_and_validate(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("text must not be empty")
        return v2


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    text: str
    created_at: datetime

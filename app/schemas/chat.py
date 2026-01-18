from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.message import MessageOut

class ChatCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def strip_and_validate(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("title must not be empty")
        return v2


class ChatOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime



class ChatWithMessages(ChatOut):
    model_config = ConfigDict(from_attributes=True)

    messages: list[MessageOut]

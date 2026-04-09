from datetime import datetime

from pydantic import BaseModel, Field


class CitationItem(BaseModel):
    document_id: int
    document_name: str
    page_number: int
    chunk_id: int
    content: str
    score: float


class ChatAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    document_ids: list[int] = Field(default_factory=list)
    conversation_id: int | None = None


class ChatAnswerResponse(BaseModel):
    conversation_id: int
    answer: str
    citations: list[CitationItem]


class MessageItem(BaseModel):
    id: int
    role: str
    content: str
    citations: list
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationItem(BaseModel):
    id: int
    title: str
    scope_type: str
    scope_data: dict
    created_at: datetime
    messages: list[MessageItem] = []

    model_config = {"from_attributes": True}

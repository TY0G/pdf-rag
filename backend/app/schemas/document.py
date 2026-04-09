from datetime import datetime

from pydantic import BaseModel


class DocumentItem(BaseModel):
    id: int
    file_name: str
    file_size: int
    content_type: str
    parse_status: str
    parse_error: str | None = None
    page_count: int
    summary: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChunkItem(BaseModel):
    id: int
    page_number: int
    chunk_index: int
    content: str
    meta: dict

    model_config = {"from_attributes": True}


class DocumentDetail(DocumentItem):
    chunks: list[ChunkItem] = []


class UploadResponse(BaseModel):
    message: str
    document: DocumentItem

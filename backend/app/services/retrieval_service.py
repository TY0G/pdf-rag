from sqlalchemy import literal
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document, DocumentChunk
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.embedding_service = EmbeddingService()

    def search_chunks(
        self,
        *,
        user_id: int,
        question: str,
        document_ids: list[int],
        top_k: int | None = None,
    ) -> list[tuple[DocumentChunk, Document, float]]:
        top_k = top_k or settings.top_k
        query_vector = self.embedding_service.embed_text(question)

        query = (
            self.db.query(
                DocumentChunk,
                Document,
                (1 - DocumentChunk.embedding.cosine_distance(query_vector)).label("similarity"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .filter(Document.user_id == user_id, Document.parse_status == "ready")
        )

        if document_ids:
            query = query.filter(Document.id.in_(document_ids))

        rows = (
            query.order_by(DocumentChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
            .all()
        )
        return [(chunk, document, float(score or 0.0)) for chunk, document, score in rows]

from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk, DocumentPage


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_document(
        self,
        *,
        user_id: int,
        file_name: str,
        file_path: str,
        file_size: int,
        content_type: str,
    ) -> Document:
        document = Document(
            user_id=user_id,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def list_by_user(self, user_id: int) -> list[Document]:
        return (
            self.db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.id.desc())
            .all()
        )

    def get_user_document(self, document_id: int, user_id: int) -> Document | None:
        return (
            self.db.query(Document)
            .filter(Document.id == document_id, Document.user_id == user_id)
            .first()
        )

    def get_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def replace_pages(self, document: Document, pages: list[dict]) -> None:
        self.db.query(DocumentPage).filter(DocumentPage.document_id == document.id).delete()
        for item in pages:
            self.db.add(DocumentPage(document_id=document.id, **item))
        self.db.commit()

    def replace_chunks(self, document: Document, chunks: list[dict]) -> None:
        self.db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()
        for item in chunks:
            self.db.add(DocumentChunk(document_id=document.id, **item))
        self.db.commit()

    def list_chunks(self, document_id: int) -> list[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.page_number.asc(), DocumentChunk.chunk_index.asc())
            .all()
        )

    def set_status(
        self,
        document: Document,
        *,
        status: str,
        page_count: int | None = None,
        summary: str | None = None,
        parse_error: str | None = None,
    ) -> None:
        document.parse_status = status
        if page_count is not None:
            document.page_count = page_count
        if summary is not None:
            document.summary = summary
        document.parse_error = parse_error
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

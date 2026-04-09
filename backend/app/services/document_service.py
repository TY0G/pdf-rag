from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.services.parser_service import ParserService
from app.services.storage_service import StorageService


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = DocumentRepository(db)
        self.storage = StorageService()
        self.parser = ParserService()

    def upload_document(self, *, user_id: int, file: UploadFile) -> Document:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="当前仅支持 PDF 文件上传")

        file_path, file_size = self.storage.save_upload(file)
        return self.repo.create_document(
            user_id=user_id,
            file_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            content_type=file.content_type or "application/pdf",
        )

    def parse_document(self, document_id: int) -> None:
        document = self.repo.get_by_id(document_id)
        if not document:
            return
        try:
            self.repo.set_status(document, status="processing")
            result = self.parser.parse_pdf(document.file_path)
            self.repo.replace_pages(document, result["pages"])
            self.repo.replace_chunks(document, result["chunks"])
            self.repo.set_status(
                document,
                status="ready",
                page_count=result["page_count"],
                summary=result["summary"],
                parse_error=None,
            )
        except Exception as exc:
            self.repo.set_status(document, status="failed", parse_error=str(exc))

    def list_documents(self, user_id: int):
        return self.repo.list_by_user(user_id)

    def get_document_or_404(self, document_id: int, user_id: int) -> Document:
        document = self.repo.get_user_document(document_id, user_id)
        if not document:
            raise HTTPException(status_code=404, detail="文档不存在")
        return document

    def get_chunks(self, document_id: int, user_id: int):
        document = self.get_document_or_404(document_id, user_id)
        return self.repo.list_chunks(document.id)

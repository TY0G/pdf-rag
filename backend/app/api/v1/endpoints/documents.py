import os

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.db.session import SessionLocal
from app.schemas.document import ChunkItem, DocumentDetail, DocumentItem, UploadResponse
from app.services.document_service import DocumentService

router = APIRouter()


def run_parse_document(document_id: int) -> None:
    db = SessionLocal()
    try:
        service = DocumentService(db)
        service.parse_document(document_id)
    finally:
        db.close()


@router.post("/upload", response_model=UploadResponse)
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = DocumentService(db)
    document = service.upload_document(user_id=user.id, file=file)
    background_tasks.add_task(run_parse_document, document.id)
    return UploadResponse(message="上传成功，正在后台解析", document=document)


@router.get("", response_model=list[DocumentItem])
def list_documents(db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = DocumentService(db)
    return service.list_documents(user.id)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = DocumentService(db)
    document = service.get_document_or_404(document_id, user.id)
    chunks = service.get_chunks(document_id, user.id)
    payload = DocumentDetail.model_validate(document)
    payload.chunks = [ChunkItem.model_validate(item) for item in chunks]
    return payload


@router.post("/{document_id}/parse", response_model=UploadResponse)
def reparse_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = DocumentService(db)
    document = service.get_document_or_404(document_id, user.id)
    background_tasks.add_task(run_parse_document, document.id)
    return UploadResponse(message="已重新触发解析", document=document)


@router.get("/{document_id}/file")
def preview_file(document_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = DocumentService(db)
    document = service.get_document_or_404(document_id, user.id)
    media_type = document.content_type or "application/pdf"
    return FileResponse(
        path=document.file_path,
        filename=os.path.basename(document.file_name),
        media_type=media_type,
    )

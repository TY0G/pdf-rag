from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.models.document import Document
from app.models.user import User

router = APIRouter()


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), admin=Depends(require_admin)):
    user_count = db.query(User).count()
    document_count = db.query(Document).count()
    ready_count = db.query(Document).filter(Document.parse_status == "ready").count()
    failed_count = db.query(Document).filter(Document.parse_status == "failed").count()
    return {
        "user_count": user_count,
        "document_count": document_count,
        "ready_count": ready_count,
        "failed_count": failed_count,
    }

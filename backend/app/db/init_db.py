import time

from sqlalchemy import text

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.conversation import Conversation, Message
from app.models.document import Document, DocumentChunk, DocumentPage
from app.models.user import EmailCode, User


def wait_for_db(max_retries: int = 30, sleep_seconds: int = 2) -> None:
    for _ in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception:
            time.sleep(sleep_seconds)
    raise RuntimeError("数据库连接超时")


def init_db() -> None:
    wait_for_db()
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            db.add(
                User(
                    email="admin@example.com",
                    password_hash=get_password_hash("Admin123!"),
                    nickname="管理员",
                    role="admin",
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

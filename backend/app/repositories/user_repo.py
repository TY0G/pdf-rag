from sqlalchemy.orm import Session

from app.models.user import EmailCode, User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password_hash: str, nickname: str) -> User:
        user = User(email=email, password_hash=password_hash, nickname=nickname)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save_email_code(self, email: str, code: str, expires_at) -> EmailCode:
        row = EmailCode(email=email, code=code, expires_at=expires_at)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_latest_available_code(self, email: str) -> EmailCode | None:
        return (
            self.db.query(EmailCode)
            .filter(EmailCode.email == email, EmailCode.used.is_(False))
            .order_by(EmailCode.id.desc())
            .first()
        )

    def mark_code_used(self, code_row: EmailCode) -> None:
        code_row.used = True
        self.db.add(code_row)
        self.db.commit()

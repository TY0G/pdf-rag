from sqlalchemy.orm import Session

from app.models.conversation import Conversation, Message


class ConversationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_conversation(
        self,
        *,
        user_id: int,
        title: str,
        scope_type: str,
        scope_data: dict,
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title,
            scope_type=scope_type,
            scope_data=scope_data,
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def list_by_user(self, user_id: int) -> list[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.id.desc())
            .all()
        )

    def get_user_conversation(self, conversation_id: int, user_id: int) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .first()
        )

    def add_message(
        self,
        *,
        conversation_id: int,
        role: str,
        content: str,
        citations: list | None = None,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            citations=citations or [],
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

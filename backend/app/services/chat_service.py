from sqlalchemy.orm import Session

from app.repositories.conversation_repo import ConversationRepository
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.retrieval_service = RetrievalService(db)
        self.llm_service = LLMService()

    async def ask(
        self,
        *,
        user_id: int,
        question: str,
        document_ids: list[int],
        conversation_id: int | None,
    ) -> tuple[int, str, list[dict]]:
        scope_type = "multi_document" if len(document_ids) > 1 else "single_document"
        scope_data = {"document_ids": document_ids}

        conversation = None
        if conversation_id:
            conversation = self.conversation_repo.get_user_conversation(conversation_id, user_id)
        if not conversation:
            title = question[:30]
            conversation = self.conversation_repo.create_conversation(
                user_id=user_id,
                title=title,
                scope_type=scope_type,
                scope_data=scope_data,
            )

        self.conversation_repo.add_message(
            conversation_id=conversation.id,
            role="user",
            content=question,
            citations=[],
        )

        rows = self.retrieval_service.search_chunks(
            user_id=user_id,
            question=question,
            document_ids=document_ids,
        )
        citations = [
            {
                "document_id": document.id,
                "document_name": document.file_name,
                "page_number": chunk.page_number,
                "chunk_id": chunk.id,
                "content": chunk.content,
                "score": round(score, 4),
            }
            for chunk, document, score in rows
        ]
        answer = await self.llm_service.generate_answer(question=question, evidence=citations)
        self.conversation_repo.add_message(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            citations=citations,
        )
        return conversation.id, answer, citations

    def list_conversations(self, user_id: int):
        return self.conversation_repo.list_by_user(user_id)

    def get_conversation(self, conversation_id: int, user_id: int):
        return self.conversation_repo.get_user_conversation(conversation_id, user_id)

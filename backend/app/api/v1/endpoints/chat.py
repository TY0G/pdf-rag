from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.schemas.chat import ChatAnswerResponse, ChatAskRequest, ConversationItem
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService

router = APIRouter()


@router.post("/ask", response_model=ChatAnswerResponse)
async def ask_question(
    payload: ChatAskRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not payload.document_ids:
        raise HTTPException(status_code=400, detail="请至少选择一个文档")

    document_service = DocumentService(db)
    for document_id in payload.document_ids:
        document_service.get_document_or_404(document_id, user.id)

    service = ChatService(db)
    conversation_id, answer, citations = await service.ask(
        user_id=user.id,
        question=payload.question,
        document_ids=payload.document_ids,
        conversation_id=payload.conversation_id,
    )
    return ChatAnswerResponse(
        conversation_id=conversation_id,
        answer=answer,
        citations=citations,
    )


@router.get("/conversations", response_model=list[ConversationItem])
def list_conversations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = ChatService(db)
    items = service.list_conversations(user.id)
    return items


@router.get("/conversations/{conversation_id}", response_model=ConversationItem)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = ChatService(db)
    conversation = service.get_conversation(conversation_id, user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")
    return conversation

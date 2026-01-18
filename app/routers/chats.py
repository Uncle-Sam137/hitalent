from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatCreate, ChatOut, ChatWithMessages
from app.schemas.message import MessageCreate, MessageOut

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatOut, status_code=status.HTTP_201_CREATED)
async def create_chat(payload: ChatCreate, db: AsyncSession = Depends(get_db)) -> Chat:
    chat = Chat(title=payload.title)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.post("/{chat_id}/messages/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
) -> Message:
    chat = await db.scalar(select(Chat).where(Chat.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    msg = Message(chat_id=chat_id, text=payload.text)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg



@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: int,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: AsyncSession = Depends(get_db),
) -> dict:
    chat = await db.scalar(select(Chat).where(Chat.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    # последние limit сообщений, отсортированные по created_at (возрастающе)
    # берем последние по убыванию, потом разворачиваем
    res = await db.scalars(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
    )
    last_msgs = list(res.all())
    last_msgs.reverse()

    return {"id": chat.id, "title": chat.title, "created_at": chat.created_at, "messages": last_msgs}


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)) -> Response:
    chat = await db.scalar(select(Chat).where(Chat.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    await db.execute(delete(Chat).where(Chat.id == chat_id))
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

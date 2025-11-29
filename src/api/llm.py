from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel

from fastapi import APIRouter, Depends, WebSocket, Query
from pydantic_ai import Agent

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.utils import validate_session_key
from src.core.llm_models import  get_model, model_dicts
from src.models.conversations import ChatMessage, ChatSession
from src.db.utils import get_db_session


router = APIRouter(
    tags=['LLM']
)


def validate_model(model: str) -> str:
    if model not in model_dicts:
        raise ValueError(f'Invalid model: {model}')
    return model

def validate_user_prompt(prompt: str) -> str:
    if not prompt:
        raise ValueError('User prompt cannot be empty')
    return prompt


class ChatRequest(BaseModel):
    model: Annotated[str, AfterValidator(validate_model)]
    user_prompt: Annotated[str, AfterValidator(validate_user_prompt)]
    chat_session_id: int | None = None

class StreamFinish(BaseModel):
    message_id: int
    full_response: str

class StreamChunk(BaseModel):
    chunk: str

class ChatStreamResponse(BaseModel):
    chat_session_id: int
    response_chunk: str | StreamFinish | StreamChunk
    type: Literal['message', 'chunk', 'error', 'finish']

@router.websocket('/ws/chat')
async def chat(
    ws: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db_session),
):
    await ws.accept()

    try:
        user = validate_session_key(token, db)
    except Exception as e:
        await ws.send_text(ChatStreamResponse(chat_session_id=0, response_chunk=str(e), type='error').model_dump_json())
        await ws.close()
        return

    _chat_request = await ws.receive_text()
    chat_request = ChatRequest.model_validate_json(_chat_request)

    model = get_model(chat_request.model)

    if chat_request.chat_session_id:
        chat_session = db.scalar(select(ChatSession).where(ChatSession.id == chat_request.chat_session_id, ChatSession.user_id == user.id))

        if not chat_session:
            await ws.send_text(ChatStreamResponse(chat_session_id=chat_request.chat_session_id, response_chunk='chat session not found', type='error').model_dump_json())
            await ws.close()
            return
    else:
        chat_session = ChatSession(user_id=user.id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    agent = Agent(model=model)

    llm_chunks: list[str] = []

    async with agent.run_stream(user_prompt=chat_request.user_prompt) as stream:
        async for chunk in stream.stream_text():
            llm_chunks.append(chunk)
            resp = ChatStreamResponse(response_chunk=StreamChunk(chunk=chunk), type='chunk', chat_session_id=1)
            await ws.send_text(data=resp.model_dump_json())

    user_message = ChatMessage()
    user_message.role = 'user'
    user_message.session_id = chat_session.id
    user_message.content = chat_request.user_prompt

    assistant_message = ChatMessage()
    assistant_message.role = 'assistant'
    assistant_message.session_id = chat_session.id
    assistant_message.content = ''.join(llm_chunks)

    db.add_all([user_message, assistant_message])
    db.commit()

    db.refresh(user_message)
    db.refresh(assistant_message)

    await ws.send_text(
        ChatStreamResponse(
            response_chunk=StreamFinish(
                full_response=assistant_message.content,
                message_id=assistant_message.id
            ),
            type='chunk',
            chat_session_id=chat_session.id
        ).model_dump_json()
    )

    await ws.close()

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base

if TYPE_CHECKING:
    from src.models.users import User

class ChatSession(Base):
    __tablename__ = 'conversations__chat_sessions'

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('auth__users.id'), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now)
    updated_at = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user: 'Mapped[User]' = relationship(back_populates='chat_sessions')
    messages: 'Mapped[list[ChatMessage]]' = relationship(back_populates='session')

class ChatMessage(Base):
    __tablename__ = 'conversations__chat_messages'

    id = mapped_column(Integer, primary_key=True)

    # main
    role = mapped_column(String(255), nullable=False)
    content = mapped_column(Text(), nullable=False)

    # meta
    session_id = mapped_column(Integer, ForeignKey('conversations__chat_sessions.id'), nullable=False)
    timestamp = mapped_column(DateTime, default=datetime.now)

    session: 'Mapped[ChatSession]' = relationship(back_populates='messages')

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Message(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, index=True) # ID del usuario que envía (puede ser email o ID numérico)
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

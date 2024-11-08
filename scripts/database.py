from typing import List

import os

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.mutable import MutableList

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from sqlalchemy import create_engine

Base = declarative_base()


def get_engine():
    return create_engine(os.environ.get('DATABASE_URL'))


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    thread_id = Column(Integer, ForeignKey('threads.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    thread = relationship("Thread", back_populates="messages")
    user = relationship("User", back_populates="messages")

    transformed_messages = relationship("TransformedMessage", back_populates="original_message")


class TransformedMessage(Base):
    __tablename__ = 'transformed_messages'

    id = Column(Integer, primary_key=True)
    transformed_text = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    original_message_id = Column(Integer, ForeignKey('messages.id'))
    
    original_message = relationship("Message", back_populates="transformed_messages")
    prompt_id = Column(Integer, ForeignKey('prompts.id'))

    message_images = Column(MutableList.as_mutable(Integer), ForeignKey('message_images.id'))


class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("Message", back_populates="thread")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("Message", back_populates="user")


class Image(Base):
    __tablename__ = 'message_images'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    image_id = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())

    revised_prompt = Column(String, nullable=True)
    transformed_message_id = Column(Integer, ForeignKey('transformed_messages.id'))


class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())

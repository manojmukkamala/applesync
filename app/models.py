from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, nullable=False)
    created_at: datetime

class Device(SQLModel, table=True):
    device_id: Optional[int] = Field(default=None, primary_key=True)
    device_name: str = Field(unique=True, nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    created_at: datetime

class Message(SQLModel, table=True):
    guid: str = Field(primary_key=True)
    conversation_guid: str
    conversation_conversation: str
    conversation_display_name: str
    date: str
    sender_full_name: str
    sender_phone_numbers: str
    type: str
    body: str
    device_id: int = Field(foreign_key="device.device_id")
    created_at: datetime

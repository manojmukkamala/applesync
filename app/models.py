from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, nullable=False)
    password: str = Field(default=None)  # Add password field for authentication
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

class HealthData(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True, description="Auto increment UUID primary key")
    device_id: int = Field(foreign_key="device.device_id")
    name: str
    source: str
    duration: str
    startdate: datetime
    enddate: datetime
    unit: str
    value: str
    type: str
    created_at: datetime

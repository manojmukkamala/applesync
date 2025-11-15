from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import datetime
from typing import Optional
import uuid

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

class HealthData(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("device_id", "unit", "startdate"),
    )

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        nullable=False
    )

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

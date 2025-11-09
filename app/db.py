import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import select
from app.models import User, Device, Message
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Global database path
DB_PATH = './data/messages.db'

# Create the async database engine
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)
session_local = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initialize the database and create tables if they don't exist"""
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Use SQLModel to create tables
    from app.models import User, Device, Message
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)


# User database functions
async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(User).where(User.user_id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user.model_dump() if user else None


async def get_all_users() -> List[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()
        return [user.model_dump() for user in users]


async def create_user(user_name: str) -> Dict[str, Any]:
    created_at = datetime.now()
    async with session_local() as session:
        user = User(user_name=user_name, created_at=created_at)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.model_dump()


# Device database functions
async def get_device_by_id(device_id: int) -> Optional[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(Device).where(Device.device_id == device_id)
        result = await session.execute(statement)
        device = result.scalars().first()
        return device.model_dump() if device else None


async def get_devices_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(Device).where(Device.user_id == user_id)
        result = await session.execute(statement)
        devices = result.scalars().all()
        return [device.model_dump() for device in devices]


async def create_device(device_name: str, user_id: int) -> Dict[str, Any]:
    created_at = datetime.now()
    async with session_local() as session:
        device = Device(device_name=device_name, user_id=user_id, created_at=created_at)
        session.add(device)
        await session.commit()
        await session.refresh(device)
        return device.model_dump()


# Message database functions
async def get_message_by_guid(guid: str) -> Optional[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(Message).where(Message.guid == guid)
        result = await session.execute(statement)
        message = result.scalars().first()
        return message.model_dump() if message else None


async def get_messages_by_device_id(device_id: int, guid: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    async with session_local() as session:
        if guid:
            statement = select(Message).where(Message.device_id == device_id, Message.guid == guid)
            result = await session.execute(statement)
            message = result.scalars().first()
            return message.model_dump() if message else None
        else:
            statement = select(Message).where(Message.device_id == device_id)
            result = await session.execute(statement)
            messages = result.scalars().all()
            return [message.model_dump() for message in messages]


async def create_message(guid: str, conversation_guid: str, conversation_conversation: str, conversation_display_name: str, date: str, sender_full_name: str, sender_phone_numbers: str, type: str, body: str, device_id: int) -> Dict[str, Any]:
    created_at = datetime.now()
    async with session_local() as session:
        message = Message(
            guid=guid,
            conversation_guid=conversation_guid,
            conversation_conversation=conversation_conversation,
            conversation_display_name=conversation_display_name,
            date=date,
            sender_full_name=sender_full_name,
            sender_phone_numbers=sender_phone_numbers,
            type=type,
            body=body,
            device_id=device_id,
            created_at=created_at
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message.model_dump()

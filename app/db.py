import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import select
from app.models import User, Device, Message, HealthData, ScreenTime
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
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)
        await conn.run_sync(HealthData.metadata.create_all)
        await conn.run_sync(ScreenTime.metadata.create_all)


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


async def get_messages_by_device_id(device_id: int, guid: Optional[str] = None, startDate: Optional[str] = None, endDate: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    async with session_local() as session:
        if guid:
            statement = select(Message).where(Message.device_id == device_id, Message.guid == guid)
            result = await session.execute(statement)
            message = result.scalars().first()
            return message.model_dump() if message else None
        else:
            statement = select(Message).where(Message.device_id == device_id)
            
            # Apply date filtering if startDate and/or endDate are provided
            if startDate or endDate:

                # Parse date strings to datetime objects for comparison
                if startDate:
                    start_date = datetime.strptime(startDate, '%Y-%m-%d')
                    statement = statement.where(Message.date >= start_date)
                if endDate:
                    end_date = datetime.strptime(endDate, '%Y-%m-%d')
                    statement = statement.where(Message.date <= end_date)
            
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


# HealthData database functions
async def get_health_data_by_id(health_id: str) -> Optional[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(HealthData).where(HealthData.id == health_id)
        result = await session.execute(statement)
        health_data = result.scalars().first()
        return health_data.model_dump() if health_data else None


async def get_health_data_by_device_id(device_id: int, guid: Optional[str] = None, startDate: Optional[str] = None, endDate: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    async with session_local() as session:
        if guid:
            statement = select(HealthData).where(HealthData.device_id == device_id, HealthData.id == guid)
            result = await session.execute(statement)
            health_data = result.scalars().first()
            return health_data.model_dump() if health_data else None
        else:
            statement = select(HealthData).where(HealthData.device_id == device_id)
            
            # Apply date filtering if startDate and/or endDate are provided
            if startDate or endDate:
                # Parse date strings to datetime objects for comparison
                if startDate:
                    start_date = datetime.strptime(startDate, '%Y-%m-%d')
                    statement = statement.where(HealthData.startdate >= start_date)
                if endDate:
                    end_date = datetime.strptime(endDate, '%Y-%m-%d')
                    statement = statement.where(HealthData.startdate <= end_date)
            
            result = await session.execute(statement)
            health_data = result.scalars().all()
            return [data.model_dump() for data in health_data]


async def create_health_data(device_id: int, name: str, source: str, duration: str, startdate: str, enddate: str, unit: str, value: str, type: str) -> Dict[str, Any]:
    created_at = datetime.now()

    async with session_local() as session:

     # Normalize dates
     startdate_obj = datetime.fromisoformat(startdate.replace("Z", "+00:00"))
     enddate_obj = datetime.fromisoformat(enddate.replace("Z", "+00:00"))

    # 1) CHECK IF EXISTS (based on unique constraint)
    stmt = select(HealthData).where(
        HealthData.device_id == device_id,
        HealthData.type == type,
        HealthData.startdate == startdate_obj
    )

    result = await session.execute(stmt)
    existing = result.one_or_none()

    # 2) UPDATE IF EXISTS
    if existing:
        existing.name = name
        existing.source = source
        existing.duration = duration
        existing.enddate = enddate_obj
        existing.value = value
        existing.type = type
        existing.created_at = created_at

        session.add(existing)
        await session.commit()
        await session.refresh(existing)

        hd = existing

    # 3) INSERT NEW IF NOT EXISTS
    else:
        hd = HealthData(
            device_id=device_id,
            name=name,
            source=source,
            duration=duration,
            startdate=startdate_obj,
            enddate=enddate_obj,
            unit=unit,
            value=value,
            type=type,
            created_at=created_at
        )
        session.add(hd)
        await session.commit()
        await session.refresh(hd)

    # Prepare output
    data = hd.model_dump()
    data["startdate"] = hd.startdate.isoformat()
    data["enddate"] = hd.enddate.isoformat()

    return data


# ScreenTime database functions
async def get_screen_time_by_id(screen_time_id: str) -> Optional[Dict[str, Any]]:
    async with session_local() as session:
        statement = select(ScreenTime).where(ScreenTime.id == screen_time_id)
        result = await session.execute(statement)
        screen_time = result.scalars().first()
        return screen_time.model_dump() if screen_time else None


async def get_screen_time_by_device_id(device_id: int, app: Optional[str] = None, startDate: Optional[str] = None, endDate: Optional[str] = None) -> List[Dict[str, Any]]:
    async with session_local() as session:
        if app:
            statement = select(ScreenTime).where(ScreenTime.device_id == device_id, ScreenTime.app == app)
            result = await session.execute(statement)
            screen_time = result.scalars().first()
            return screen_time.model_dump() if screen_time else None
        else:
            statement = select(ScreenTime).where(ScreenTime.device_id == device_id)
            
            # Apply date filtering if startDate and/or endDate are provided
            if startDate or endDate:
                # Parse date strings to date objects for comparison
                if startDate:
                    start_date = datetime.strptime(startDate, '%Y-%m-%d')
                    statement = statement.where(ScreenTime.activity_date >= start_date)
                if endDate:
                    end_date = datetime.strptime(endDate, '%Y-%m-%d')
                    statement = statement.where(ScreenTime.activity_date <= end_date)
            
            result = await session.execute(statement)
            screen_time = result.scalars().all()
            return [st.model_dump() for st in screen_time]


async def create_screen_time(device_id: int, app: str, website: str, duration: str, description: str, activity_date: str) -> Dict[str, Any]:
    created_at = datetime.now()
    async with session_local() as session:
        # Convert string date to date object
        from datetime import date
        if isinstance(activity_date, str):
            # Parse the date string (assuming YYYY-MM-DD format)
            activity_date_obj = date.fromisoformat(activity_date)
        else:
            activity_date_obj = activity_date
            
        screen_time = ScreenTime(
            device_id=device_id,
            app=app,
            website=website,
            duration=duration,
            description=description,
            activity_date=activity_date_obj,
            created_at=created_at
        )
        session.add(screen_time)
        await session.commit()
        await session.refresh(screen_time)
        return screen_time.model_dump()

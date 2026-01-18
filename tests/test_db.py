import pytest
from datetime import datetime, date
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from app.models import User, Device, Message, HealthData, ScreenTime

# Create an in-memory database for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.mark.asyncio
async def test_init_db():
    """Test database initialization with in-memory database"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)
        await conn.run_sync(HealthData.metadata.create_all)
        await conn.run_sync(ScreenTime.metadata.create_all)
    
    # Test that tables were created
    async with engine.begin() as conn:
        # Use TextClause for raw SQL execution
        from sqlalchemy import text
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        table_names = [table[0] for table in tables]
        # Check for table names (note: SQLAlchemy may change the case)
        assert "user" in table_names or "User" in table_names
        assert "device" in table_names or "Device" in table_names
        assert "message" in table_names or "Message" in table_names
        assert "healthdata" in table_names or "health_data" in table_names
        assert "screentime" in table_names or "ScreenTime" in table_names

@pytest.mark.asyncio
async def test_create_and_get_user():
    """Test creating and retrieving a user"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
    
    # Create a user using SQL directly (avoiding datetime issues)
    async with engine.begin() as conn:
        # Insert user directly
        await conn.execute(
            User.__table__.insert(),
            {"user_name": "Test User", "created_at": datetime.now()}
        )
        
        # Retrieve the user
        result = await conn.execute(
            User.__table__.select().where(User.user_name == "Test User")
        )
        user = result.fetchone()
        assert user is not None
        assert user.user_name == "Test User"

@pytest.mark.asyncio
async def test_create_and_get_device():
    """Test creating and retrieving a device"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
    
    # Create a user first
    async with engine.begin() as conn:
        await conn.execute(
            User.__table__.insert(),
            {"user_name": "Test User", "created_at": datetime.now()}
        )
        
        # Get the user ID
        result = await conn.execute(
            User.__table__.select().where(User.user_name == "Test User")
        )
        user = result.fetchone()
        user_id = user.user_id
    
    # Create a device
    async with engine.begin() as conn:
        await conn.execute(
            Device.__table__.insert(),
            {
                "device_name": "Test Device",
                "user_id": user_id,
                "created_at": datetime.now()
            }
        )
        
        # Retrieve the device
        result = await conn.execute(
            Device.__table__.select().where(Device.device_name == "Test Device")
        )
        device = result.fetchone()
        assert device is not None
        assert device.device_name == "Test Device"
        assert device.user_id == user_id

@pytest.mark.asyncio
async def test_create_and_get_message():
    """Test creating and retrieving a message"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)
    
    # Create a user and device first
    async with engine.begin() as conn:
        await conn.execute(
            User.__table__.insert(),
            {"user_name": "Test User", "created_at": datetime.now()}
        )
        
        result = await conn.execute(
            User.__table__.select().where(User.user_name == "Test User")
        )
        user = result.fetchone()
        user_id = user.user_id
        
        await conn.execute(
            Device.__table__.insert(),
            {
                "device_name": "Test Device",
                "user_id": user_id,
                "created_at": datetime.now()
            }
        )
        
        result = await conn.execute(
            Device.__table__.select().where(Device.device_name == "Test Device")
        )
        device = result.fetchone()
        device_id = device.device_id
    
    # Create a message
    async with engine.begin() as conn:
        await conn.execute(
            Message.__table__.insert(),
            {
                "guid": "test-guid-123",
                "conversation_guid": "conv-guid-123",
                "conversation_conversation": "conv-conversation",
                "conversation_display_name": "conv-display",
                "date": "2023-01-01T00:00:00Z",
                "sender_full_name": "Test Sender",
                "sender_phone_numbers": "123-456-7890",
                "type": "text",
                "body": "Test message body",
                "device_id": device_id,
                "created_at": datetime.now()
            }
        )
        
        # Retrieve the message
        result = await conn.execute(
            Message.__table__.select().where(Message.guid == "test-guid-123")
        )
        message = result.fetchone()
        assert message is not None
        assert message.guid == "test-guid-123"
        assert message.body == "Test message body"
        assert message.device_id == device_id

@pytest.mark.asyncio
async def test_create_and_get_health_data():
    """Test creating and retrieving health data"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(HealthData.metadata.create_all)
    
    # Create a user and device first
    async with engine.begin() as conn:
        await conn.execute(
            User.__table__.insert(),
            {"user_name": "Test User", "created_at": datetime.now()}
        )
        
        result = await conn.execute(
            User.__table__.select().where(User.user_name == "Test User")
        )
        user = result.fetchone()
        user_id = user.user_id
        
        await conn.execute(
            Device.__table__.insert(),
            {
                "device_name": "Test Device",
                "user_id": user_id,
                "created_at": datetime.now()
            }
        )
        
        result = await conn.execute(
            Device.__table__.select().where(Device.device_name == "Test Device")
        )
        device = result.fetchone()
        device_id = device.device_id
    
    # Create health data
    async with engine.begin() as conn:
        await conn.execute(
            HealthData.__table__.insert(),
            {
                "device_id": device_id,
                "name": "Heart Rate",
                "source": "Apple Watch",
                "duration": "3600",
                "startdate": datetime.now(),
                "enddate": datetime.now(),
                "unit": "bpm",
                "value": "72",
                "type": "heart_rate",
                "created_at": datetime.now()
            }
        )
        
        # Retrieve the health data
        result = await conn.execute(
            HealthData.__table__.select().where(HealthData.name == "Heart Rate")
        )
        health_data = result.fetchone()
        assert health_data is not None
        assert health_data.name == "Heart Rate"
        assert health_data.type == "heart_rate"
        assert health_data.device_id == device_id

@pytest.mark.asyncio
async def test_create_and_get_screen_time():
    """Test creating and retrieving screen time data"""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(ScreenTime.metadata.create_all)
    
    # Create a user and device first
    async with engine.begin() as conn:
        await conn.execute(
            User.__table__.insert(),
            {"user_name": "Test User", "created_at": datetime.now()}
        )
        
        result = await conn.execute(
            User.__table__.select().where(User.user_name == "Test User")
        )
        user = result.fetchone()
        user_id = user.user_id
        
        await conn.execute(
            Device.__table__.insert(),
            {
                "device_name": "Test Device",
                "user_id": user_id,
                "created_at": datetime.now()
            }
        )
        
        result = await conn.execute(
            Device.__table__.select().where(Device.device_name == "Test Device")
        )
        device = result.fetchone()
        device_id = device.device_id
    
    # Create screen time data
    async with engine.begin() as conn:
        await conn.execute(
            ScreenTime.__table__.insert(),
            {
                "device_id": device_id,
                "app": "Test App",
                "website": "test.com",
                "duration": "3600",
                "description": "Test app usage",
                "activity_date": date(2023, 1, 1),
                "created_at": datetime.now()
            }
        )
        
        # Retrieve the screen time data
        result = await conn.execute(
            ScreenTime.__table__.select().where(ScreenTime.app == "Test App")
        )
        screen_time = result.fetchone()
        assert screen_time is not None
        assert screen_time.app == "Test App"
        assert screen_time.website == "test.com"
        assert screen_time.device_id == device_id
        assert screen_time.activity_date == date(2023, 1, 1)
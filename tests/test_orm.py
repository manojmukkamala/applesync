import asyncio
from app.db import init_db, create_user, get_all_users, create_device, get_all_devices, create_message, get_messages_for_device
from app.models import User, Device, Message

async def test_orm():
    # Initialize database
    await init_db()
    
    # Test creating a user
    user = await create_user("test_user_1")
    print(f"Created user: {user}")
    
    # Test getting all users
    users = await get_all_users()
    print(f"All users: {users}")
    
    # Test creating a device
    device = await create_device("test_device_1", user['user_id'])
    print(f"Created device: {device}")
    
    # Test getting all devices
    devices = await get_all_devices()
    print(f"All devices: {devices}")
    
    # Test creating a message
    message = await create_message(
        guid="test_guid_1",
        conversation_guid="conv_guid_1",
        conversation_conversation="conv_conv_1",
        conversation_display_name="display_name_1",
        date="2025-01-01",
        sender_full_name="Sender Name",
        sender_phone_numbers="123-456-7890",
        type="text",
        body="Test message body",
        device_id=device['device_id']
    )
    print(f"Created message: {message}")
    
    # Test getting messages for device
    messages = await get_messages_for_device(device['device_id'])
    print(f"Messages for device: {messages}")
    
    print("ORM implementation test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_orm())

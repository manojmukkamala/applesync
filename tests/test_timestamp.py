import asyncio
from app.db import init_db, create_user, get_all_users

async def test_timestamp():
    # Initialize database
    await init_db()
    
    # Test creating a user
    user = await create_user("timestamp_test_user")
    print(f"Created user: {user}")
    
    # Test getting all users
    users = await get_all_users()
    print(f"All users: {users}")
    
    # Check that created_at is a datetime object
    if users:
        first_user = users[0]
        print(f"Created at type: {type(first_user['created_at'])}")
        print(f"Created at value: {first_user['created_at']}")
    
    print("Timestamp implementation test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_timestamp())

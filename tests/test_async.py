import asyncio
from app.db import init_db, create_user, get_all_users

async def test_async():
    # Initialize database
    await init_db()
    
    # Test creating a user
    user = await create_user("async_test_user")
    print(f"Created user: {user}")
    
    # Test getting all users
    users = await get_all_users()
    print(f"All users: {users}")
    
    print("Async ORM implementation test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_async())

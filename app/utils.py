# scripts/create_user.py
import asyncio
from db import init_db, create_user

async def main():
    await init_db()
    user = await create_user("admin", "secret_password")
    print("Created user:", user)

if __name__ == "__main__":
    asyncio.run(main())
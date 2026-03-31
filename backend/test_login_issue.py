import asyncio
import sys
sys.path.insert(0, r'C:\Users\Make\Desktop\shamgp\backend')

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import verify_password

async def test():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == 'testuser1')
        )
        user = result.scalar_one_or_none()
        if user:
            print(f"Found user: {user.id}, {user.username}, status={user.status}")
            print(f"is_active: {user.is_active}")
            print(f"roles count: {len(user.roles)}")
            print(f"password hash: {user.password[:30]}...")
            ok = verify_password('Test123456', user.password)
            print(f"password verify: {ok}")
        else:
            print("User not found")
        await db.close()

asyncio.run(test())

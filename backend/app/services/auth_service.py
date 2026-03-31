from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import verify_password, create_access_token
from app.core.exceptions import AuthenticationError, ValidationError
from app.models.user import User


class AuthService:
    @staticmethod
    async def authenticate(db: AsyncSession, username: str, password: str) -> User:
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise AuthenticationError("Incorrect username or password")
        
        if not user.is_active:
            raise AuthenticationError("Inactive user")
        
        if not verify_password(password, user.password):
            raise AuthenticationError("Incorrect username or password")
        
        return user
    
    @staticmethod
    async def get_user_info(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.roles),
                selectinload(User.roles).selectinload('permissions')
            )
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise AuthenticationError("User not found")
        
        roles = [role.code for role in user.roles]
        permissions = []
        for role in user.roles:
            permissions.extend([perm.code for perm in role.permissions])
        
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "email": user.email,
            "phone": user.phone,
            "roles": roles,
            "permissions": list(set(permissions))
        }

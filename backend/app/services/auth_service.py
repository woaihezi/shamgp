from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import verify_password, create_access_token, get_password_hash
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
    async def register(db: AsyncSession, username: str, password: str, email: str = None, phone: str = None, nickname: str = None) -> User:
        result = await db.execute(select(User).where(User.username == username))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValidationError("Username already exists")
        
        if email:
            result = await db.execute(select(User).where(User.email == email))
            existing_email = result.scalar_one_or_none()
            if existing_email:
                raise ValidationError("Email already exists")
        
        user = User(
            username=username,
            password=get_password_hash(password),
            email=email,
            phone=phone,
            nickname=nickname or username,
            is_active=True,
            is_superuser=False
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def get_user_info(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise AuthenticationError("User not found")
        
        roles = [role.code for role in user.roles]
        
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "email": user.email,
            "phone": user.phone,
            "roles": roles,
            "permissions": []
        }

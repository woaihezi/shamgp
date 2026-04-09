from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash, verify_password
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate


class UserService:
    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.username == username, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def authenticate(db: AsyncSession, username: str, password: str) -> Optional[User]:
        user = await UserService.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    async def get_multi_paginated(db: AsyncSession, page: int = 1, page_size: int = 10) -> tuple[List[User], int]:
        offset = (page - 1) * page_size
        
        # 获取总数
        count_result = await db.execute(
            select(func.count(User.id)).where(User.is_deleted == False)
        )
        total = count_result.scalar()
        
        # 获取分页数据
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.is_deleted == False)
            .offset(offset)
            .limit(page_size)
        )
        items = list(result.scalars().all())
        
        return items, total
    
    @staticmethod
    async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.is_deleted == False)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def count(db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count(User.id)).where(User.is_deleted == False)
        )
        return result.scalar()
    
    @staticmethod
    async def create(db: AsyncSession, obj_in: UserCreate | dict) -> User:
        # 处理字典类型的输入
        if isinstance(obj_in, dict):
            username = obj_in.get('username')
            password = obj_in.get('password')
            email = obj_in.get('email')
            phone = obj_in.get('phone')
            nickname = obj_in.get('nickname')
            avatar = obj_in.get('avatar')
        else:
            username = obj_in.username
            password = obj_in.password
            email = obj_in.email
            phone = obj_in.phone
            nickname = obj_in.nickname
            avatar = obj_in.avatar
        
        existing = await UserService.get_by_username(db, username)
        if existing:
            raise ValidationError("Username already registered")
        
        db_obj = User(
            username=username,
            password=get_password_hash(password),
            email=email,
            phone=phone,
            nickname=nickname,
            avatar=avatar
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def update(db: AsyncSession, db_obj: User, obj_in: UserUpdate | dict) -> User:
        # 处理字典类型的输入
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def update_password(db: AsyncSession, user: User, obj_in: UserPasswordUpdate) -> User:
        if not verify_password(obj_in.old_password, user.password):
            raise ValidationError("Old password is incorrect")
        
        user.password = get_password_hash(obj_in.new_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def remove(db: AsyncSession, user_id: int) -> User:
        user = await UserService.get(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        
        user.is_deleted = True
        db.add(user)
        await db.commit()
        return user


user_service = UserService()

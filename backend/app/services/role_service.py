from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.role import Role
from app.models.menu import Menu
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    @staticmethod
    async def get(db: AsyncSession, role_id: int) -> Optional[Role]:
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.menus), selectinload(Role.permissions))
            .where(Role.id == role_id, Role.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Optional[Role]:
        result = await db.execute(
            select(Role).where(Role.code == code, Role.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.menus), selectinload(Role.permissions))
            .where(Role.is_deleted == False)
            .order_by(Role.sort)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def count(db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count(Role.id)).where(Role.is_deleted == False)
        )
        return result.scalar()
    
    @staticmethod
    async def create(db: AsyncSession, obj_in: RoleCreate) -> Role:
        existing = await RoleService.get_by_code(db, obj_in.code)
        if existing:
            raise ValidationError("Role code already exists")
        
        db_obj = Role(
            name=obj_in.name,
            code=obj_in.code,
            description=obj_in.description,
            sort=obj_in.sort or 0
        )
        
        if obj_in.menu_ids:
            menus_result = await db.execute(
                select(Menu).where(Menu.id.in_(obj_in.menu_ids))
            )
            db_obj.menus = list(menus_result.scalars().all())
        
        if obj_in.permission_ids:
            perms_result = await db.execute(
                select(Permission).where(Permission.id.in_(obj_in.permission_ids))
            )
            db_obj.permissions = list(perms_result.scalars().all())
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def update(db: AsyncSession, db_obj: Role, obj_in: RoleUpdate) -> Role:
        update_data = obj_in.model_dump(exclude_unset=True, exclude={"menu_ids", "permission_ids"})
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        if obj_in.menu_ids is not None:
            menus_result = await db.execute(
                select(Menu).where(Menu.id.in_(obj_in.menu_ids))
            )
            db_obj.menus = list(menus_result.scalars().all())
        
        if obj_in.permission_ids is not None:
            perms_result = await db.execute(
                select(Permission).where(Permission.id.in_(obj_in.permission_ids))
            )
            db_obj.permissions = list(perms_result.scalars().all())
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def remove(db: AsyncSession, role_id: int) -> Role:
        role = await RoleService.get(db, role_id)
        if not role:
            raise ResourceNotFoundError("Role not found")
        
        role.is_deleted = True
        db.add(role)
        await db.commit()
        return role

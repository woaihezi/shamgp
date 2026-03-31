from typing import Optional
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission, role_permission_association

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise AuthenticationError()

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise AuthenticationError()

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthenticationError()

    if not user.is_active:
        raise AuthenticationError()

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise AuthenticationError("Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if not getattr(current_user, "is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser permissions required"
        )
    return current_user


async def get_user_permissions(db: AsyncSession, user_id: int) -> set:
    """获取用户所有权限 code 集合"""
    result = await db.execute(
        select(User).where(User.id == user_id).options()
    )
    user = result.scalar_one_or_none()
    if not user:
        return set()

    # 查询用户的角色
    role_result = await db.execute(
        select(user.c.role).where(user.c.user_id == user_id)
    )
    role_ids = [row[0] for row in role_result.fetchall()]

    if not role_ids:
        return set()

    # 查询这些角色关联的权限
    perm_result = await db.execute(
        select(Permission.code)
        .join(role_permission_association, role_permission_association.c.permission_id == Permission.id)
        .where(role_permission_association.c.role_id.in_(role_ids))
    )
    return {row[0] for row in perm_result.fetchall()}


def require_permissions(*permission_codes: str):
    """
    权限校验装饰器工厂。
    用法：
        @router.get("/orders")
        async def get_orders(
            current_user: User = Depends(require_permissions("order:read")),
        ):
            ...
    """
    async def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        # 超级管理员拥有所有权限
        if getattr(current_user, "is_superuser", False):
            return current_user

        user_perms = await get_user_permissions(db, current_user.id)

        missing = [code for code in permission_codes if code not in user_perms]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}"
            )

        return current_user

    return permission_checker

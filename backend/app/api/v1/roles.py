from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.user import User, user_role_association
from app.models.role import Role
from app.models.permission import Permission, role_permission_association
from app.schemas.common import ResponseModel, ListResponseModel
from app.api.deps import get_current_active_user, require_permissions

router = APIRouter()


# ─── Permission CRUD ────────────────────────────────────────────────────────

@router.get("/permissions", response_model=ListResponseModel[dict])
async def list_permissions(
    type: Optional[str] = None,
    page: int = 1,
    page_size: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取权限列表"""
    query = select(Permission)
    if type:
        query = query.where(Permission.type == type)
    query = query.order_by(Permission.sort.asc(), Permission.id.asc())

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return ListResponseModel(
        data=[{
            "id": p.id, "name": p.name, "code": p.code, "type": p.type,
            "path": p.path, "method": p.method, "parent_id": p.parent_id or 0,
            "sort": p.sort, "description": p.description,
        } for p in items],
        total=total or 0
    )


@router.post("/permissions", response_model=ResponseModel[dict])
async def create_permission(
    perm_in: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建权限"""
    name = perm_in.get("name")
    code = perm_in.get("code")
    if not name or not code:
        raise HTTPException(status_code=400, detail="name and code required")

    existing = await db.execute(
        select(Permission).where(Permission.code == code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Permission code already exists")

    perm = Permission(
        name=name,
        code=code,
        type=perm_in.get("type", "api"),
        path=perm_in.get("path"),
        method=perm_in.get("method"),
        parent_id=perm_in.get("parent_id", 0),
        sort=perm_in.get("sort", 0),
        description=perm_in.get("description"),
    )
    db.add(perm)
    await db.commit()
    await db.refresh(perm)
    return ResponseModel(data={"id": perm.id, "name": perm.name, "code": perm.code})


@router.put("/permissions/{permission_id}", response_model=ResponseModel[dict])
async def update_permission(
    permission_id: int,
    perm_in: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新权限"""
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    perm = result.scalar_one_or_none()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")

    for key in ("name", "type", "path", "method", "parent_id", "sort", "description"):
        if key in perm_in and perm_in[key] is not None:
            setattr(perm, key, perm_in[key])

    await db.commit()
    await db.refresh(perm)
    return ResponseModel(data={"id": perm.id, "name": perm.name})


@router.delete("/permissions/{permission_id}", response_model=ResponseModel)
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """删除权限"""
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    perm = result.scalar_one_or_none()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")

    await db.delete(perm)
    await db.commit()
    return ResponseModel(message="Permission deleted successfully")


# ─── Role CRUD ──────────────────────────────────────────────────────────────

@router.get("/roles", response_model=ListResponseModel[dict])
async def list_roles(
    page: int = 1,
    page_size: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取角色列表"""
    query = select(Role)
    count_q = select(func.count()).select_from(Role)
    total = (await db.execute(count_q)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    roles = result.scalars().all()

    # 加载每个角色的权限
    role_data = []
    for r in roles:
        perm_result = await db.execute(
            select(Permission.code, Permission.name, Permission.id)
            .join(role_permission_association, role_permission_association.c.permission_id == Permission.id)
            .where(role_permission_association.c.role_id == r.id)
        )
        perms = [{"id": pid, "code": code, "name": name} for code, name, pid in perm_result.fetchall()]
        role_data.append({
            "id": r.id,
            "name": r.name,
            "code": r.code,
            "description": r.description,
            "sort": r.sort,
            "permissions": perms,
            "created_at": str(r.created_at) if r.created_at else None,
        })

    return ListResponseModel(data=role_data, total=total or 0)


@router.post("/roles", response_model=ResponseModel[dict])
async def create_role(
    role_in: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建角色"""
    code = role_in.get("code")
    name = role_in.get("name")
    if not code or not name:
        raise HTTPException(status_code=400, detail="name and code required")

    existing = await db.execute(select(Role).where(Role.code == code))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Role code already exists")

    permission_ids = role_in.get("permission_ids", [])
    role = Role(
        name=name,
        code=code,
        description=role_in.get("description"),
        sort=role_in.get("sort", 0),
    )
    db.add(role)
    await db.flush()

    if permission_ids:
        role.permissions = []  # 初始化空列表
        for pid in permission_ids:
            await db.execute(
                role_permission_association.insert().values(
                    role_id=role.id,
                    permission_id=pid
                )
            )

    await db.commit()
    await db.refresh(role)
    return ResponseModel(data={"id": role.id, "name": role.name, "code": role.code})


@router.put("/roles/{role_id}", response_model=ResponseModel[dict])
async def update_role(
    role_id: int,
    role_in: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新角色"""
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key in ("name", "description", "sort"):
        if key in role_in and role_in[key] is not None:
            setattr(role, key, role_in[key])

    if "permission_ids" in role_in:
        # 删除旧的关联
        await db.execute(
            role_permission_association.delete()
            .where(role_permission_association.c.role_id == role_id)
        )
        # 插入新的
        for pid in role_in["permission_ids"]:
            await db.execute(
                role_permission_association.insert().values(
                    role_id=role_id,
                    permission_id=pid
                )
            )

    await db.commit()
    await db.refresh(role)
    return ResponseModel(data={"id": role.id, "name": role.name})


@router.delete("/roles/{role_id}", response_model=ResponseModel)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """删除角色"""
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if role.code == "superadmin":
        raise HTTPException(status_code=400, detail="Cannot delete superadmin role")

    await db.execute(
        role_permission_association.delete()
        .where(role_permission_association.c.role_id == role_id)
    )
    await db.delete(role)
    await db.commit()
    return ResponseModel(message="Role deleted successfully")


# ─── 用户角色分配 ──────────────────────────────────────────────────────────

@router.get("/users/{user_id}/roles", response_model=ResponseModel[List[dict]])
async def get_user_roles(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取用户的角色"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_result = await db.execute(
        select(Role.id, Role.name, Role.code)
        .join(user_role_association, user_role_association.c.role_id == Role.id)
        .where(user_role_association.c.user_id == user_id)
    )
    roles = [{"id": r[0], "name": r[1], "code": r[2]} for r in role_result.fetchall()]
    return ResponseModel(data=roles)


@router.post("/users/{user_id}/roles", response_model=ResponseModel)
async def assign_user_roles(
    user_id: int,
    role_ids_body: dict = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """分配角色给用户"""
    if role_ids_body is None:
        role_ids_body = {}
    role_ids = role_ids_body.get("role_ids", [])

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 删除旧的角色关联
    await db.execute(
        user_role_association.delete()
        .where(user_role_association.c.user_id == user_id)
    )
    # 插入新的
    for rid in role_ids:
        await db.execute(
            user_role_association.insert().values(
                user_id=user_id,
                role_id=rid
            )
        )

    await db.commit()
    return ResponseModel(message=f"Assigned {len(role_ids)} role(s) to user")

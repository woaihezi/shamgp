from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_active_user, get_current_active_superuser
from app.schemas.common import ResponseModel, PaginationResult, PaginationParams
from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.services.role_service import RoleService
from app.models.user import User

router = APIRouter()


@router.get("", response_model=ResponseModel[PaginationResult[Role]])
async def get_roles(
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    skip = (params.page - 1) * params.page_size
    roles = await RoleService.get_multi(db, skip=skip, limit=params.page_size)
    total = await RoleService.count(db)
    return ResponseModel(
        data=PaginationResult(
            items=roles,
            total=total,
            page=params.page,
            page_size=params.page_size
        )
    )


@router.get("/{role_id}", response_model=ResponseModel[Role])
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    role = await RoleService.get(db, role_id)
    return ResponseModel(data=role)


@router.post("", response_model=ResponseModel[Role])
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    role = await RoleService.create(db, role_in)
    return ResponseModel(data=role)


@router.put("/{role_id}", response_model=ResponseModel[Role])
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    role = await RoleService.get(db, role_id)
    role = await RoleService.update(db, role, role_in)
    return ResponseModel(data=role)


@router.delete("/{role_id}", response_model=ResponseModel)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    await RoleService.remove(db, role_id)
    return ResponseModel(message="Role deleted successfully")

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_active_user, get_current_active_superuser
from app.schemas.common import ResponseModel, PaginationResult, PaginationParams
from app.schemas.user import User, UserCreate, UserUpdate, UserPasswordUpdate
from app.services.user_service import UserService
from app.models.user import User as UserModel

router = APIRouter()


@router.get("", response_model=ResponseModel[PaginationResult[User]])
async def get_users(
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_superuser)
):
    skip = (params.page - 1) * params.page_size
    users = await UserService.get_multi(db, skip=skip, limit=params.page_size)
    total = await UserService.count(db)
    return ResponseModel(
        data=PaginationResult(
            items=users,
            total=total,
            page=params.page,
            page_size=params.page_size
        )
    )


@router.get("/{user_id}", response_model=ResponseModel[User])
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    user = await UserService.get(db, user_id)
    return ResponseModel(data=user)


@router.post("", response_model=ResponseModel[User])
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_superuser)
):
    user = await UserService.create(db, user_in)
    return ResponseModel(data=user)


@router.put("/{user_id}", response_model=ResponseModel[User])
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    user = await UserService.get(db, user_id)
    user = await UserService.update(db, user, user_in)
    return ResponseModel(data=user)


@router.put("/{user_id}/password", response_model=ResponseModel[User])
async def update_user_password(
    user_id: int,
    password_in: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    if current_user.id != user_id and not current_user.is_superuser:
        from app.core.exceptions import AuthorizationError
        raise AuthorizationError()
    
    user = await UserService.get(db, user_id)
    user = await UserService.update_password(db, user, password_in)
    return ResponseModel(data=user)


@router.delete("/{user_id}", response_model=ResponseModel)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_superuser)
):
    await UserService.remove(db, user_id)
    return ResponseModel(message="User deleted successfully")

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.common import ResponseModel
from app.schemas.user import UserInfo
from app.schemas.menu import MenuTree, RouterItem
from app.services.auth_service import AuthService
from app.services.menu_service import MenuService
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=ResponseModel[LoginResponse])
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService.authenticate(db, login_data.username, login_data.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return ResponseModel(
        data=LoginResponse(access_token=access_token)
    )


@router.get("/userinfo", response_model=ResponseModel[UserInfo])
async def get_userinfo(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_info = await AuthService.get_user_info(db, current_user.id)
    return ResponseModel(data=UserInfo(**user_info))


@router.get("/menu-tree", response_model=ResponseModel[list[MenuTree]])
async def get_menu_tree(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    
    menus = await MenuService.get_by_user(db, user)
    menu_tree = MenuService.build_menu_tree(menus)
    return ResponseModel(data=menu_tree)


@router.get("/routers", response_model=ResponseModel[list[RouterItem]])
async def get_routers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    
    menus = await MenuService.get_by_user(db, user)
    routers = MenuService.build_router_tree(menus)
    return ResponseModel(data=routers)


@router.post("/logout", response_model=ResponseModel)
async def logout():
    return ResponseModel(message="Logout successful")

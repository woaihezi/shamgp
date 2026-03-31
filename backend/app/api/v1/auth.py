from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.common import ResponseModel
from app.schemas.user import UserInfo, UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=ResponseModel[LoginResponse])
async def register(
    register_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.create(db, register_data)
    access_token = create_access_token(data={"sub": str(user.id)})
    return ResponseModel(
        data=LoginResponse(access_token=access_token)
    )


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


@router.post("/logout", response_model=ResponseModel)
async def logout():
    return ResponseModel(message="Logout successful")

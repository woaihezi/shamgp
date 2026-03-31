from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from app.schemas.common import BaseSchema
from app.schemas.role import RoleSimple


class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=500, description="头像")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


class UserSimple(BaseSchema):
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class User(UserSimple):
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_superuser: bool
    roles: List[RoleSimple] = []


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []

from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema


class PermissionBase(BaseModel):
    name: str = Field(..., max_length=100, description="权限名称")
    code: str = Field(..., max_length=100, description="权限编码")
    type: str = Field("api", max_length=20, description="权限类型: api-接口, button-按钮")
    path: Optional[str] = Field(None, max_length=200, description="API路径")
    method: Optional[str] = Field(None, max_length=20, description="请求方法")
    description: Optional[str] = Field(None, description="权限描述")


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    description: Optional[str] = None


class Permission(BaseSchema):
    name: str
    code: str
    type: str
    path: Optional[str] = None
    method: Optional[str] = None
    description: Optional[str] = None

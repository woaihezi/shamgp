from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema


class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, description="角色名称")
    code: str = Field(..., max_length=50, description="角色编码")
    description: Optional[str] = Field(None, description="角色描述")
    sort: Optional[int] = Field(0, description="排序")


class RoleCreate(RoleBase):
    menu_ids: Optional[List[int]] = Field(default_factory=list, description="菜单ID列表")
    permission_ids: Optional[List[int]] = Field(default_factory=list, description="权限ID列表")


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    sort: Optional[int] = None
    menu_ids: Optional[List[int]] = None
    permission_ids: Optional[List[int]] = None


class RoleSimple(BaseSchema):
    name: str
    code: str


class Role(RoleSimple):
    description: Optional[str] = None
    sort: int

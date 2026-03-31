from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema


class MenuBase(BaseModel):
    parent_id: Optional[int] = Field(0, description="父菜单ID")
    name: str = Field(..., max_length=50, description="菜单名称")
    path: Optional[str] = Field(None, max_length=200, description="路由路径")
    component: Optional[str] = Field(None, max_length=200, description="组件路径")
    permission: Optional[str] = Field(None, max_length=100, description="权限标识")
    type: str = Field("menu", max_length=20, description="菜单类型: directory-目录, menu-菜单, button-按钮")
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标")
    sort: Optional[int] = Field(0, description="排序")
    is_visible: Optional[bool] = Field(True, description="是否显示")
    is_keep_alive: Optional[bool] = Field(False, description="是否缓存")
    is_iframe: Optional[bool] = Field(False, description="是否外链")
    redirect: Optional[str] = Field(None, max_length=200, description="重定向地址")


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    parent_id: Optional[int] = None
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    permission: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    sort: Optional[int] = None
    is_visible: Optional[bool] = None
    is_keep_alive: Optional[bool] = None
    is_iframe: Optional[bool] = None
    redirect: Optional[str] = None


class MenuSimple(BaseSchema):
    parent_id: int
    name: str
    path: Optional[str] = None
    component: Optional[str] = None
    permission: Optional[str] = None
    type: str
    icon: Optional[str] = None
    sort: int
    is_visible: bool
    is_keep_alive: bool
    is_iframe: bool
    redirect: Optional[str] = None


class MenuTree(MenuSimple):
    children: List['MenuTree'] = []


MenuTree.model_rebuild()


class RouterMeta(BaseModel):
    title: str
    icon: Optional[str] = None
    permission: Optional[str] = None
    is_keep_alive: bool = False
    is_iframe: bool = False
    is_visible: bool = True


class RouterItem(BaseModel):
    path: str
    name: Optional[str] = None
    component: Optional[str] = None
    redirect: Optional[str] = None
    meta: Optional[RouterMeta] = None
    children: List['RouterItem'] = []


RouterItem.model_rebuild()

from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.role import role_menu_association


class Menu(BaseModel):
    __tablename__ = "menu"
    
    parent_id = Column(Integer, default=0, nullable=False, index=True, comment="父菜单ID")
    name = Column(String(50), nullable=False, comment="菜单名称")
    path = Column(String(200), nullable=True, comment="路由路径")
    component = Column(String(200), nullable=True, comment="组件路径")
    permission = Column(String(100), nullable=True, comment="权限标识")
    type = Column(String(20), nullable=False, default="menu", comment="菜单类型: directory-目录, menu-菜单, button-按钮")
    icon = Column(String(100), nullable=True, comment="菜单图标")
    sort = Column(Integer, default=0, nullable=False, comment="排序")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否显示")
    is_keep_alive = Column(Boolean, default=False, nullable=False, comment="是否缓存")
    is_iframe = Column(Boolean, default=False, nullable=False, comment="是否外链")
    redirect = Column(String(200), nullable=True, comment="重定向地址")
    
    roles = relationship("Role", secondary=role_menu_association, back_populates="menus")

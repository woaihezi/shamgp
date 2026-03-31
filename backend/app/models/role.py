from sqlalchemy import Column, String, Integer, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.user import user_role_association


role_menu_association = Table(
    "role_menu",
    BaseModel.metadata,
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
    Column("menu_id", Integer, ForeignKey("menu.id"), primary_key=True)
)


role_permission_association = Table(
    "role_permission",
    BaseModel.metadata,
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True)
)


class Role(BaseModel):
    __tablename__ = "role"
    
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    description = Column(Text, nullable=True, comment="角色描述")
    sort = Column(Integer, default=0, nullable=False, comment="排序")
    
    users = relationship("User", secondary=user_role_association, back_populates="roles")
    menus = relationship("Menu", secondary=role_menu_association, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission_association, back_populates="roles")

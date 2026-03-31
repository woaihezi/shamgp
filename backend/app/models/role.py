from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.user import user_role_association


class Role(BaseModel):
    __tablename__ = "role"

    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    description = Column(Text, nullable=True, comment="角色描述")
    sort = Column(Integer, default=0, nullable=False, comment="排序")

    users = relationship("User", secondary=user_role_association, back_populates="roles")

    # permissions 由 Permission.role_permission_association 表通过 back_populates="roles" 反向引用
    # 不在此处定义 relationship，直接通过 Permission.role_permission_association 的反向引用访问

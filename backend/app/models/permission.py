from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.role import role_permission_association


class Permission(BaseModel):
    __tablename__ = "permission"
    
    name = Column(String(100), nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, comment="权限编码")
    type = Column(String(20), nullable=False, default="api", comment="权限类型: api-接口, button-按钮")
    path = Column(String(200), nullable=True, comment="API路径")
    method = Column(String(20), nullable=True, comment="请求方法")
    description = Column(Text, nullable=True, comment="权限描述")
    
    roles = relationship("Role", secondary=role_permission_association, back_populates="permissions")

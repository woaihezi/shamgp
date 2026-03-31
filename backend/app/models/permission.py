from sqlalchemy import Column, String, Integer, Text, Table, ForeignKey, UniqueConstraint
from app.models.base import BaseModel
from app.models.user import user_role_association


# 角色-权限关联表（多对多）
role_permission_association = Table(
    "role_permission",
    BaseModel.metadata,
    Column("role_id", Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
)


class Permission(BaseModel):
    __tablename__ = "permission"

    name = Column(String(100), nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, comment="权限编码")
    type = Column(String(20), nullable=False, default="api", comment="权限类型: api-接口, button-按钮, menu-菜单")
    path = Column(String(200), nullable=True, comment="API路径")
    method = Column(String(20), nullable=True, comment="请求方法: GET/POST/PUT/DELETE")
    parent_id = Column(Integer, nullable=True, default=0, comment="父级权限ID（菜单树）")
    sort = Column(Integer, default=0, nullable=False, comment="排序")
    description = Column(Text, nullable=True, comment="权限描述")

    # roles 由 Role.users 通过 role_permission_association 表反向引用
    # 不在此处定义 relationship，直接通过 Role.role_permission_association 的反向引用访问

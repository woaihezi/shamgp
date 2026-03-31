from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


user_role_association = Table(
    "user_role",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True)
)


class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True, index=True)
    phone = Column(String(20), nullable=True, index=True)
    nickname = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    gender = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=1, index=True)
    user_type = Column(SmallInteger, default=1)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    roles = relationship("Role", secondary=user_role_association, back_populates="users")
    
    @property
    def is_active(self):
        return self.status == 1


from sqlalchemy import Column, String, Text, Integer, Boolean
from .base import BaseModel


class SystemConfig(BaseModel):
    __tablename__ = "system_configs"
    __table_args__ = {"comment": "系统配置表"}
    
    config_key = Column(String(100), nullable=False, unique=True, index=True, comment="配置键")
    config_value = Column(Text, nullable=True, comment="配置值")
    config_type = Column(String(20), nullable=False, default="string", comment="配置类型(string,int,bool,json)")
    config_group = Column(String(50), nullable=True, index=True, comment="配置分组")
    description = Column(String(255), nullable=True, comment="配置描述")
    is_public = Column(Boolean, nullable=False, default=False, comment="是否公开(0否,1是)")
    sort = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(Integer, nullable=False, default=1, comment="状态(0禁用,1启用)")

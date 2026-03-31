
from pydantic import BaseModel, Field
from typing import Optional
from .common import BaseSchema, PageParams


class SystemConfigBase(BaseModel):
    config_key: str = Field(..., description="配置键")
    config_value: Optional[str] = Field(None, description="配置值")
    config_type: str = Field(default="string", description="配置类型")
    config_group: Optional[str] = Field(None, description="配置分组")
    description: Optional[str] = Field(None, description="配置描述")
    is_public: bool = Field(default=False, description="是否公开")
    sort: int = Field(default=0, description="排序")
    status: int = Field(default=1, description="状态")


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    config_value: Optional[str] = None
    config_type: Optional[str] = None
    config_group: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    sort: Optional[int] = None
    status: Optional[int] = None


class SystemConfigResponse(SystemConfigBase, BaseSchema):
    pass


class SystemConfigQuery(PageParams):
    config_key: Optional[str] = None
    config_group: Optional[str] = None
    status: Optional[int] = None

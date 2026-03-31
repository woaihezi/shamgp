
from pydantic import BaseModel, Field
from typing import Optional
from .common import BaseSchema, PageParams


class FileBase(BaseModel):
    filename: str = Field(..., description="原始文件名")
    storage_name: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: int = Field(default=0, description="文件大小")
    file_type: Optional[str] = None
    file_ext: Optional[str] = None
    upload_user_id: Optional[int] = None
    category: Optional[str] = None
    storage_type: str = Field(default="local", description="存储类型")
    status: int = Field(default=1, description="状态")


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    filename: Optional[str] = None
    category: Optional[str] = None
    status: Optional[int] = None


class FileResponse(FileBase, BaseSchema):
    pass


class FileQuery(PageParams):
    filename: Optional[str] = None
    file_type: Optional[str] = None
    category: Optional[str] = None
    upload_user_id: Optional[int] = None
    status: Optional[int] = None


class UploadResponse(BaseModel):
    file_id: int = Field(..., description="文件ID")
    filename: str = Field(..., description="文件名")
    file_url: str = Field(..., description="文件URL")
    file_size: int = Field(..., description="文件大小")


from sqlalchemy import Column, String, BigInteger, Integer
from .base import BaseModel


class File(BaseModel):
    __tablename__ = "files"
    __table_args__ = {"comment": "文件表"}
    
    filename = Column(String(255), nullable=False, comment="原始文件名")
    storage_name = Column(String(255), nullable=False, unique=True, comment="存储文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_url = Column(String(500), nullable=True, comment="文件访问URL")
    file_size = Column(BigInteger, nullable=False, default=0, comment="文件大小(字节)")
    file_type = Column(String(100), nullable=False, comment="文件类型(MIME)")
    file_ext = Column(String(20), nullable=True, comment="文件扩展名")
    upload_user_id = Column(BigInteger, nullable=True, index=True, comment="上传用户ID")
    category = Column(String(50), nullable=True, index=True, comment="文件分类")
    storage_type = Column(String(20), nullable=False, default="local", comment="存储类型(local,oss,minio)")
    status = Column(Integer, nullable=False, default=1, comment="状态(0禁用,1启用)")

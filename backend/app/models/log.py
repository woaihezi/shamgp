
from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, func
from .base import BaseModel


class OperationLog(BaseModel):
    __tablename__ = "operation_logs"
    __table_args__ = {"comment": "操作日志表"}
    
    user_id = Column(BigInteger, nullable=True, index=True, comment="操作用户ID")
    username = Column(String(50), nullable=True, comment="操作用户名")
    module = Column(String(50), nullable=False, index=True, comment="操作模块")
    operation = Column(String(100), nullable=False, comment="操作类型")
    method = Column(String(20), nullable=False, comment="请求方法")
    url = Column(String(255), nullable=False, comment="请求URL")
    ip = Column(String(50), nullable=True, comment="IP地址")
    params = Column(Text, nullable=True, comment="请求参数")
    result = Column(Text, nullable=True, comment="响应结果")
    status = Column(Integer, nullable=False, default=1, comment="状态(0失败,1成功)")
    error_msg = Column(Text, nullable=True, comment="错误信息")
    execution_time = Column(Integer, nullable=True, comment="执行时间(毫秒)")


class LoginLog(BaseModel):
    __tablename__ = "login_logs"
    __table_args__ = {"comment": "登录日志表"}
    
    user_id = Column(BigInteger, nullable=True, index=True, comment="用户ID")
    username = Column(String(50), nullable=False, index=True, comment="用户名")
    ip = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    status = Column(Integer, nullable=False, default=1, comment="状态(0失败,1成功)")
    error_msg = Column(String(255), nullable=True, comment="错误信息")

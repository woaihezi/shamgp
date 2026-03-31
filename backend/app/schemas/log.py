
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .common import BaseSchema, PageParams


class OperationLogBase(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    module: str
    operation: str
    method: str
    url: str
    ip: Optional[str] = None
    params: Optional[str] = None
    result: Optional[str] = None
    status: int = 1
    error_msg: Optional[str] = None
    execution_time: Optional[int] = None


class OperationLogCreate(OperationLogBase):
    pass


class OperationLogUpdate(BaseModel):
    pass


class OperationLogResponse(OperationLogBase, BaseSchema):
    pass


class OperationLogQuery(PageParams):
    user_id: Optional[int] = None
    username: Optional[str] = None
    module: Optional[str] = None
    operation: Optional[str] = None
    status: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class LoginLogBase(BaseModel):
    user_id: Optional[int] = None
    username: str
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    status: int = 1
    error_msg: Optional[str] = None


class LoginLogCreate(LoginLogBase):
    pass


class LoginLogResponse(LoginLogBase, BaseSchema):
    pass


class LoginLogQuery(PageParams):
    user_id: Optional[int] = None
    username: Optional[str] = None
    status: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

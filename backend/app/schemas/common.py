from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Generic, TypeVar, List

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class ListResponseModel(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: List[T] = []
    total: int = 0


class PageParams(BaseModel):
    page: int = 1
    page_size: int = 20


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BaseSchema(TimestampMixin):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None

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


class PageResult(BaseModel, Generic[T]):
    items: List[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 20


class PageParams(BaseModel):
    page: int = 1
    page_size: int = 20


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IDMixin(BaseModel):
    id: Optional[int] = None


class BaseSchema(TimestampMixin, IDMixin):
    model_config = ConfigDict(from_attributes=True)


# Backward-compatible aliases used by existing route/service code.
TimestampSchema = TimestampMixin
ResponseBase = ResponseModel
PaginationResult = PageResult
PageResponse = ListResponseModel
PaginationParams = PageParams
IdSchema = IDMixin


from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from ...core.database import get_db
from ...schemas.common import ResponseModel, PageResponse
from ...schemas.log import (
    OperationLogResponse,
    OperationLogQuery,
    LoginLogResponse,
    LoginLogQuery
)
from ...services.log_service import LogService

router = APIRouter(prefix="/logs", tags=["日志"])


@router.get("/operation", response_model=ResponseModel[PageResponse[OperationLogResponse]])
async def get_operation_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    module: Optional[str] = None,
    operation: Optional[str] = None,
    status: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    service = LogService(db)
    query = OperationLogQuery(
        page=page,
        page_size=page_size,
        user_id=user_id,
        username=username,
        module=module,
        operation=operation,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    result = await service.get_operation_logs(query)
    return ResponseModel(data=result)


@router.get("/login", response_model=ResponseModel[PageResponse[LoginLogResponse]])
async def get_login_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    status: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    service = LogService(db)
    query = LoginLogQuery(
        page=page,
        page_size=page_size,
        user_id=user_id,
        username=username,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    result = await service.get_login_logs(query)
    return ResponseModel(data=result)

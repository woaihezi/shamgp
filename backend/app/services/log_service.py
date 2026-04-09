
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from ..models.log import OperationLog, LoginLog
from ..schemas.log import (
    OperationLogCreate,
    OperationLogUpdate,
    OperationLogResponse,
    OperationLogQuery,
    LoginLogCreate,
    LoginLogResponse,
    LoginLogQuery
)
from ..schemas.common import PageResponse


class LogService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_operation_log(self, log_data: OperationLogCreate) -> OperationLogResponse:
        db_log = OperationLog(**log_data.model_dump())
        self.db.add(db_log)
        await self.db.commit()
        await self.db.refresh(db_log)
        return OperationLogResponse.model_validate(db_log)

    async def get_operation_logs(self, query: OperationLogQuery) -> PageResponse[OperationLogResponse]:
        stmt = select(OperationLog)
        
        if query.user_id:
            stmt = stmt.where(OperationLog.user_id == query.user_id)
        if query.username:
            stmt = stmt.where(OperationLog.username.contains(query.username))
        if query.module:
            stmt = stmt.where(OperationLog.module == query.module)
        if query.operation:
            stmt = stmt.where(OperationLog.operation.contains(query.operation))
        if query.status is not None:
            stmt = stmt.where(OperationLog.status == query.status)
        if query.start_date:
            stmt = stmt.where(OperationLog.created_at >= query.start_date)
        if query.end_date:
            stmt = stmt.where(OperationLog.created_at <= query.end_date)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        
        offset = (query.page - 1) * query.page_size
        stmt = stmt.order_by(desc(OperationLog.created_at)).offset(offset).limit(query.page_size)
        
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return PageResponse(
            total=total,
            page=query.page,
            page_size=query.page_size,
            items=[OperationLogResponse.model_validate(item) for item in items]
        )

    async def create_login_log(self, log_data: LoginLogCreate) -> LoginLogResponse:
        db_log = LoginLog(**log_data.model_dump())
        self.db.add(db_log)
        await self.db.commit()
        await self.db.refresh(db_log)
        return LoginLogResponse.model_validate(db_log)

    async def get_login_logs(self, query: LoginLogQuery) -> PageResponse[LoginLogResponse]:
        stmt = select(LoginLog)
        
        if query.user_id:
            stmt = stmt.where(LoginLog.user_id == query.user_id)
        if query.username:
            stmt = stmt.where(LoginLog.username.contains(query.username))
        if query.status is not None:
            stmt = stmt.where(LoginLog.status == query.status)
        if query.start_date:
            stmt = stmt.where(LoginLog.created_at >= query.start_date)
        if query.end_date:
            stmt = stmt.where(LoginLog.created_at <= query.end_date)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        
        offset = (query.page - 1) * query.page_size
        stmt = stmt.order_by(desc(LoginLog.created_at)).offset(offset).limit(query.page_size)
        
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return PageResponse(
            total=total,
            page=query.page,
            page_size=query.page_size,
            items=[LoginLogResponse.model_validate(item) for item in items]
        )

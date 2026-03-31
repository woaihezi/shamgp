
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from ..models.system_config import SystemConfig
from ..schemas.system_config import (
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigResponse,
    SystemConfigQuery
)
from ..schemas.common import PageResponse


class SystemConfigService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, config_data: SystemConfigCreate) -> SystemConfigResponse:
        db_config = SystemConfig(**config_data.model_dump())
        self.db.add(db_config)
        await self.db.commit()
        await self.db.refresh(db_config)
        return SystemConfigResponse.model_validate(db_config)

    async def get_by_id(self, config_id: int) -> Optional[SystemConfigResponse]:
        result = await self.db.execute(select(SystemConfig).where(SystemConfig.id == config_id))
        config = result.scalar_one_or_none()
        return SystemConfigResponse.model_validate(config) if config else None

    async def get_by_key(self, config_key: str) -> Optional[SystemConfigResponse]:
        result = await self.db.execute(select(SystemConfig).where(SystemConfig.config_key == config_key))
        config = result.scalar_one_or_none()
        return SystemConfigResponse.model_validate(config) if config else None

    async def update(self, config_id: int, config_data: SystemConfigUpdate) -> Optional[SystemConfigResponse]:
        result = await self.db.execute(select(SystemConfig).where(SystemConfig.id == config_id))
        db_config = result.scalar_one_or_none()
        
        if db_config:
            update_data = config_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_config, field, value)
            
            await self.db.commit()
            await self.db.refresh(db_config)
            return SystemConfigResponse.model_validate(db_config)
        
        return None

    async def delete(self, config_id: int) -> bool:
        result = await self.db.execute(select(SystemConfig).where(SystemConfig.id == config_id))
        db_config = result.scalar_one_or_none()
        
        if db_config:
            await self.db.delete(db_config)
            await self.db.commit()
            return True
        
        return False

    async def list(self, query: SystemConfigQuery) -> PageResponse[SystemConfigResponse]:
        stmt = select(SystemConfig)
        
        if query.config_key:
            stmt = stmt.where(SystemConfig.config_key.contains(query.config_key))
        if query.config_group:
            stmt = stmt.where(SystemConfig.config_group == query.config_group)
        if query.status is not None:
            stmt = stmt.where(SystemConfig.status == query.status)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        
        offset = (query.page - 1) * query.page_size
        stmt = stmt.order_by(SystemConfig.sort, desc(SystemConfig.created_at)).offset(offset).limit(query.page_size)
        
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return PageResponse(
            total=total,
            page=query.page,
            page_size=query.page_size,
            items=[SystemConfigResponse.model_validate(item) for item in items]
        )

    async def get_public_configs(self) -> List[SystemConfigResponse]:
        result = await self.db.execute(
            select(SystemConfig).where(and_(SystemConfig.is_public == True, SystemConfig.status == 1))
            .order_by(SystemConfig.sort)
        )
        items = result.scalars().all()
        return [SystemConfigResponse.model_validate(item) for item in items]

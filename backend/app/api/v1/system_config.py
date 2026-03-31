
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ...core.database import get_db
from ...schemas.common import ResponseModel, PageResponse, IdSchema
from ...schemas.system_config import (
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigResponse,
    SystemConfigQuery
)
from ...services.system_config_service import SystemConfigService

router = APIRouter(prefix="/system-config", tags=["系统配置"])


@router.post("", response_model=ResponseModel[SystemConfigResponse])
async def create_config(
    config_data: SystemConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    config = await service.create(config_data)
    return ResponseModel(data=config)


@router.get("/{config_id}", response_model=ResponseModel[SystemConfigResponse])
async def get_config(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    config = await service.get_by_id(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return ResponseModel(data=config)


@router.get("/key/{config_key}", response_model=ResponseModel[SystemConfigResponse])
async def get_config_by_key(
    config_key: str,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    config = await service.get_by_key(config_key)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return ResponseModel(data=config)


@router.put("/{config_id}", response_model=ResponseModel[SystemConfigResponse])
async def update_config(
    config_id: int,
    config_data: SystemConfigUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    config = await service.update(config_id, config_data)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return ResponseModel(data=config)


@router.delete("/{config_id}", response_model=ResponseModel[dict])
async def delete_config(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    success = await service.delete(config_id)
    if not success:
        raise HTTPException(status_code=404, detail="配置不存在")
    return ResponseModel(data={"message": "删除成功"})


@router.get("", response_model=ResponseModel[PageResponse[SystemConfigResponse]])
async def list_configs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    config_key: Optional[str] = None,
    config_group: Optional[str] = None,
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    service = SystemConfigService(db)
    query = SystemConfigQuery(
        page=page,
        page_size=page_size,
        config_key=config_key,
        config_group=config_group,
        status=status
    )
    result = await service.list(query)
    return ResponseModel(data=result)


@router.get("/public/list", response_model=ResponseModel[list[SystemConfigResponse]])
async def get_public_configs(db: AsyncSession = Depends(get_db)):
    service = SystemConfigService(db)
    configs = await service.get_public_configs()
    return ResponseModel(data=configs)

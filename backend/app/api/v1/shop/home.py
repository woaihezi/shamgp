from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ResponseModel
from app.schemas.banner import Banner
from app.schemas.coupon import Coupon
from app.schemas.recommend import Floor
from app.services.banner_service import banner_service
from app.services.coupon_service import coupon_service
from app.services.recommend_service import floor_service, ad_service, ad_space_service

router = APIRouter(prefix="/home", tags=["shop-home"])


@router.get("/banners", response_model=ResponseModel[list[Banner]])
async def get_home_banners(
    platform: Optional[int] = Query(1, description="平台：1-PC端，2-移动端"),
    db: AsyncSession = Depends(get_db),
):
    banners = await banner_service.get_active_banners(db, platform=platform)
    return ResponseModel(data=banners)


@router.get("/coupons/available", response_model=ResponseModel[list[Coupon]])
async def get_available_coupons(
    db: AsyncSession = Depends(get_db),
):
    coupons = await coupon_service.get_available_coupons(db)
    return ResponseModel(data=coupons)


@router.get("/floors", response_model=ResponseModel[list[dict]])
async def get_home_floors(
    db: AsyncSession = Depends(get_db),
):
    floors = await floor_service.get_active_floors(db)
    
    result = []
    for floor in floors:
        product_ids = []
        floor_data = {
            "id": floor.id,
            "name": floor.name,
            "code": floor.code,
            "title": floor.title,
            "subtitle": floor.subtitle,
            "style": floor.style,
            "product_ids": product_ids,
        }
        result.append(floor_data)
    
    return ResponseModel(data=result)


@router.get("/config", response_model=ResponseModel[dict])
async def get_home_config(
    platform: Optional[int] = Query(1, description="平台：1-PC端，2-移动端"),
    db: AsyncSession = Depends(get_db),
):
    banners = await banner_service.get_active_banners(db, platform=platform)
    floors = await floor_service.get_active_floors(db)
    
    config = {
        "banners": banners,
        "floors": floors,
    }
    return ResponseModel(data=config)

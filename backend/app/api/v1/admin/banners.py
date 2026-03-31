from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.banner import Banner, BannerCreate, BannerUpdate, BannerPageResult
from app.schemas.common import ResponseModel
from app.services.banner_service import banner_service
from app.services.recommend_service import (
    ad_space_service, ad_service, floor_service, floor_product_service
)
from app.schemas.recommend import (
    AdSpace, AdSpaceCreate, AdSpaceUpdate, AdSpacePageResult,
    Ad, AdCreate, AdUpdate, AdPageResult,
    Floor, FloorCreate, FloorUpdate, FloorPageResult,
    FloorProduct, FloorProductCreate, FloorProductUpdate
)

router = APIRouter(prefix="/banners", tags=["admin-banners"])


@router.get("", response_model=ResponseModel[BannerPageResult])
async def get_banners(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    platform: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await banner_service.get_multi_paginated(
        db, page=page, page_size=page_size, status=status, platform=platform
    )
    return ResponseModel(
        data=BannerPageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )


@router.get("/{banner_id}", response_model=ResponseModel[Banner])
async def get_banner(banner_id: int, db: AsyncSession = Depends(get_db)):
    banner = await banner_service.get(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return ResponseModel(data=banner)


@router.post("", response_model=ResponseModel[Banner])
async def create_banner(banner_in: BannerCreate, db: AsyncSession = Depends(get_db)):
    banner = await banner_service.create(db, banner_in.model_dump())
    return ResponseModel(data=banner)


@router.put("/{banner_id}", response_model=ResponseModel[Banner])
async def update_banner(
    banner_id: int,
    banner_in: BannerUpdate,
    db: AsyncSession = Depends(get_db),
):
    banner = await banner_service.get(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    banner = await banner_service.update(db, banner, banner_in.model_dump(exclude_unset=True))
    return ResponseModel(data=banner)


@router.delete("/{banner_id}", response_model=ResponseModel[dict])
async def delete_banner(banner_id: int, db: AsyncSession = Depends(get_db)):
    banner = await banner_service.remove(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return ResponseModel(data={"message": "Banner deleted successfully"})


ad_space_router = APIRouter(prefix="/ad-spaces", tags=["admin-ad-spaces"])


@ad_space_router.get("", response_model=ResponseModel[AdSpacePageResult])
async def get_ad_spaces(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await ad_space_service.get_multi_paginated(
        db, page=page, page_size=page_size, status=status
    )
    return ResponseModel(
        data=AdSpacePageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )


@ad_space_router.get("/{ad_space_id}", response_model=ResponseModel[AdSpace])
async def get_ad_space(ad_space_id: int, db: AsyncSession = Depends(get_db)):
    ad_space = await ad_space_service.get(db, ad_space_id)
    if not ad_space:
        raise HTTPException(status_code=404, detail="AdSpace not found")
    return ResponseModel(data=ad_space)


@ad_space_router.post("", response_model=ResponseModel[AdSpace])
async def create_ad_space(ad_space_in: AdSpaceCreate, db: AsyncSession = Depends(get_db)):
    ad_space = await ad_space_service.create(db, ad_space_in.model_dump())
    return ResponseModel(data=ad_space)


@ad_space_router.put("/{ad_space_id}", response_model=ResponseModel[AdSpace])
async def update_ad_space(
    ad_space_id: int,
    ad_space_in: AdSpaceUpdate,
    db: AsyncSession = Depends(get_db),
):
    ad_space = await ad_space_service.get(db, ad_space_id)
    if not ad_space:
        raise HTTPException(status_code=404, detail="AdSpace not found")
    ad_space = await ad_space_service.update(db, ad_space, ad_space_in.model_dump(exclude_unset=True))
    return ResponseModel(data=ad_space)


@ad_space_router.delete("/{ad_space_id}", response_model=ResponseModel[dict])
async def delete_ad_space(ad_space_id: int, db: AsyncSession = Depends(get_db)):
    ad_space = await ad_space_service.remove(db, ad_space_id)
    if not ad_space:
        raise HTTPException(status_code=404, detail="AdSpace not found")
    return ResponseModel(data={"message": "AdSpace deleted successfully"})


ad_router = APIRouter(prefix="/ads", tags=["admin-ads"])


@ad_router.get("", response_model=ResponseModel[AdPageResult])
async def get_ads(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    ad_space_id: Optional[int] = None,
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await ad_service.get_multi_paginated(
        db, page=page, page_size=page_size, ad_space_id=ad_space_id, status=status
    )
    return ResponseModel(
        data=AdPageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )


@ad_router.get("/{ad_id}", response_model=ResponseModel[Ad])
async def get_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await ad_service.get(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ResponseModel(data=ad)


@ad_router.post("", response_model=ResponseModel[Ad])
async def create_ad(ad_in: AdCreate, db: AsyncSession = Depends(get_db)):
    ad = await ad_service.create(db, ad_in.model_dump())
    return ResponseModel(data=ad)


@ad_router.put("/{ad_id}", response_model=ResponseModel[Ad])
async def update_ad(
    ad_id: int,
    ad_in: AdUpdate,
    db: AsyncSession = Depends(get_db),
):
    ad = await ad_service.get(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad = await ad_service.update(db, ad, ad_in.model_dump(exclude_unset=True))
    return ResponseModel(data=ad)


@ad_router.delete("/{ad_id}", response_model=ResponseModel[dict])
async def delete_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await ad_service.remove(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ResponseModel(data={"message": "Ad deleted successfully"})


floor_router = APIRouter(prefix="/floors", tags=["admin-floors"])


@floor_router.get("", response_model=ResponseModel[FloorPageResult])
async def get_floors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await floor_service.get_multi_paginated(
        db, page=page, page_size=page_size, status=status
    )
    return ResponseModel(
        data=FloorPageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )


@floor_router.get("/{floor_id}", response_model=ResponseModel[Floor])
async def get_floor(floor_id: int, db: AsyncSession = Depends(get_db)):
    floor = await floor_service.get(db, floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return ResponseModel(data=floor)


@floor_router.post("", response_model=ResponseModel[Floor])
async def create_floor(floor_in: FloorCreate, db: AsyncSession = Depends(get_db)):
    floor = await floor_service.create(db, floor_in.model_dump())
    return ResponseModel(data=floor)


@floor_router.put("/{floor_id}", response_model=ResponseModel[Floor])
async def update_floor(
    floor_id: int,
    floor_in: FloorUpdate,
    db: AsyncSession = Depends(get_db),
):
    floor = await floor_service.get(db, floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    floor = await floor_service.update(db, floor, floor_in.model_dump(exclude_unset=True))
    return ResponseModel(data=floor)


@floor_router.delete("/{floor_id}", response_model=ResponseModel[dict])
async def delete_floor(floor_id: int, db: AsyncSession = Depends(get_db)):
    floor = await floor_service.remove(db, floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return ResponseModel(data={"message": "Floor deleted successfully"})


floor_product_router = APIRouter(prefix="/floor-products", tags=["admin-floor-products"])


@floor_product_router.get("/floor/{floor_id}", response_model=ResponseModel[list[FloorProduct]])
async def get_floor_products(floor_id: int, db: AsyncSession = Depends(get_db)):
    items = await floor_product_service.get_by_floor_id(db, floor_id)
    return ResponseModel(data=items)


@floor_product_router.post("", response_model=ResponseModel[FloorProduct])
async def create_floor_product(floor_product_in: FloorProductCreate, db: AsyncSession = Depends(get_db)):
    floor_product = await floor_product_service.create(db, floor_product_in.model_dump())
    return ResponseModel(data=floor_product)


@floor_product_router.delete("/{floor_product_id}", response_model=ResponseModel[dict])
async def delete_floor_product(floor_product_id: int, db: AsyncSession = Depends(get_db)):
    floor_product = await floor_product_service.remove(db, floor_product_id)
    if not floor_product:
        raise HTTPException(status_code=404, detail="FloorProduct not found")
    return ResponseModel(data={"message": "FloorProduct deleted successfully"})

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.schemas.order import (
    OrderCreate, OrderUpdate, OrderSchema, OrderDetailSchema,
    OrderStatusUpdate, RefundCreate, RefundSchema
)
from app.schemas.address import AddressCreate, AddressUpdate, AddressSchema
from app.services.order_service import OrderService
from app.services.address_service import AddressService
from app.schemas.common import ResponseModel, ListResponseModel, PageParams
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/addresses", response_model=ResponseModel[List[AddressSchema]])
async def get_addresses(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = AddressService(db)
    addresses = await service.get_addresses(current_user.id)
    return ResponseModel(data=[AddressSchema.model_validate(addr) for addr in addresses])


@router.get("/addresses/default", response_model=ResponseModel[AddressSchema])
async def get_default_address(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = AddressService(db)
    address = await service.get_default_address(current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Default address not found")
    return ResponseModel(data=AddressSchema.model_validate(address))


@router.post("/addresses", response_model=ResponseModel[AddressSchema])
async def create_address(
    address_in: AddressCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = AddressService(db)
    address = await service.create_address(current_user.id, address_in)
    return ResponseModel(data=AddressSchema.model_validate(address))


@router.put("/addresses/{address_id}", response_model=ResponseModel[AddressSchema])
async def update_address(
    address_id: int,
    address_in: AddressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = AddressService(db)
    address = await service.update_address(current_user.id, address_id, address_in)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return ResponseModel(data=AddressSchema.model_validate(address))


@router.delete("/addresses/{address_id}", response_model=ResponseModel)
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = AddressService(db)
    success = await service.delete_address(current_user.id, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return ResponseModel(message="Address deleted successfully")


@router.post("/", response_model=ResponseModel[OrderSchema])
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    try:
        order = await service.create_order(current_user.id, order_in)
        return ResponseModel(data=OrderSchema.model_validate(order))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ListResponseModel[OrderSchema])
async def get_orders(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    orders, total = await service.get_orders(user_id=current_user.id, status=status, page=page, page_size=page_size)
    return ListResponseModel(
        data=[OrderSchema.model_validate(order) for order in orders],
        total=total
    )


@router.get("/{order_id}", response_model=ResponseModel[OrderDetailSchema])
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.get_order(order_id, user_id=current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=OrderDetailSchema.model_validate(order))


@router.put("/{order_id}/status", response_model=ResponseModel[OrderSchema])
async def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.update_order_status(order_id, status_in.status, user_id=current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=OrderSchema.model_validate(order))


@router.post("/{order_id}/cancel", response_model=ResponseModel[OrderSchema])
async def cancel_order(
    order_id: int,
    cancel_reason: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.cancel_order(order_id, cancel_reason, user_id=current_user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    return ResponseModel(data=OrderSchema.model_validate(order))


@router.post("/refunds", response_model=ResponseModel[RefundSchema])
async def create_refund(
    refund_in: RefundCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    try:
        refund = await service.create_refund(current_user.id, refund_in)
        return ResponseModel(data=RefundSchema.model_validate(refund))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/refunds", response_model=ResponseModel[List[RefundSchema]])
async def get_refunds(
    order_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    refunds = await service.get_refunds(user_id=current_user.id, order_id=order_id)
    return ResponseModel(data=[RefundSchema.model_validate(refund) for refund in refunds])


@router.get("/refunds/{refund_id}", response_model=ResponseModel[RefundSchema])
async def get_refund(
    refund_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    refund = await service.get_refund(refund_id, user_id=current_user.id)
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    return ResponseModel(data=RefundSchema.model_validate(refund))


@router.get("/admin/", response_model=ListResponseModel[OrderSchema])
async def admin_get_orders(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    orders, total = await service.get_orders(status=status, page=page, page_size=page_size)
    return ListResponseModel(
        data=[OrderSchema.model_validate(order) for order in orders],
        total=total
    )


@router.get("/admin/{order_id}", response_model=ResponseModel[OrderDetailSchema])
async def admin_get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=OrderDetailSchema.model_validate(order))


@router.put("/admin/{order_id}/status", response_model=ResponseModel[OrderSchema])
async def admin_update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.update_order_status(order_id, status_in.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=OrderSchema.model_validate(order))

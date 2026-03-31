from fastapi import APIRouter
from app.api.v1.admin import coupons as admin_coupons
from app.api.v1.admin import banners as admin_banners
from app.api.v1.shop import home as shop_home
from app.api.v1.shop import coupons as shop_coupons
from app.api.v1 import (
    auth, carts, categories, dashboard, inventory,
    logs, menus, orders, products, roles, shop_products,
    system_config, uploads, users
)

api_router = APIRouter()

admin_router = APIRouter(prefix="/admin", tags=["admin"])
admin_router.include_router(admin_coupons.router)
admin_router.include_router(admin_banners.router)
if hasattr(admin_banners, 'ad_space_router'):
    admin_router.include_router(admin_banners.ad_space_router)
if hasattr(admin_banners, 'ad_router'):
    admin_router.include_router(admin_banners.ad_router)
if hasattr(admin_banners, 'floor_router'):
    admin_router.include_router(admin_banners.floor_router)
if hasattr(admin_banners, 'floor_product_router'):
    admin_router.include_router(admin_banners.floor_product_router)

shop_router = APIRouter(prefix="/shop", tags=["shop"])
shop_router.include_router(shop_home.router)
shop_router.include_router(shop_coupons.router)

api_router.include_router(admin_router)
api_router.include_router(shop_router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(shop_products.router, prefix="/shop-products", tags=["shop-products"])
api_router.include_router(system_config.router, prefix="/system-config", tags=["system-config"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

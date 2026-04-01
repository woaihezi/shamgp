from importlib import import_module
from fastapi import APIRouter
import os

api_router = APIRouter()

# 严格模式：开发环境下路由导入失败时抛出异常
STRICT_MODE = os.getenv("API_STRICT_MODE", "true").lower() == "true"


def _include_router(module_path: str, prefix: str, tags: list[str]) -> None:
    try:
        module = import_module(module_path)
        router = getattr(module, "router", None)
        if router is not None:
            api_router.include_router(router, prefix=prefix, tags=tags)
            print(f"[router-loaded] {module_path}")
        else:
            print(f"[router-warning] {module_path}: No 'router' attribute found")
            if STRICT_MODE:
                raise RuntimeError(f"Module {module_path} has no 'router' attribute")
    except Exception as exc:
        print(f"[router-error] {module_path}: {type(exc).__name__}: {exc}")
        import traceback
        traceback.print_exc()
        if STRICT_MODE:
            raise


_include_router("app.api.v1.auth", "/auth", ["auth"])
_include_router("app.api.v1.carts", "/carts", ["carts"])
_include_router("app.api.v1.orders", "/orders", ["orders"])
_include_router("app.api.v1.products", "/products", ["products"])
_include_router("app.api.v1.shop_products", "/shop-products", ["shop-products"])
_include_router("app.api.v1.categories", "/categories", ["categories"])
_include_router("app.api.v1.users", "/users", ["users"])
_include_router("app.api.v1.dashboard", "/dashboard", ["dashboard"])
_include_router("app.api.v1.inventory", "/inventory", ["inventory"])
_include_router("app.api.v1.logs", "/logs", ["logs"])
_include_router("app.api.v1.menus", "/menus", ["menus"])
_include_router("app.api.v1.system_config", "/system-config", ["system-config"])
_include_router("app.api.v1.uploads", "/uploads", ["uploads"])
_include_router("app.api.v1.roles", "/roles", ["roles"])
_include_router("app.api.v1.payments", "/payments", ["payments"])
_include_router("app.api.v1.coupons", "/coupons", ["coupons"])
_include_router("app.api.v1.admin.banners", "/admin/banners", ["admin-banners"])
_include_router("app.api.v1.admin.coupons", "/admin/coupons", ["admin-coupons"])
_include_router("app.api.v1.shop.coupons", "/shop/coupons", ["shop-coupons"])
_include_router("app.api.v1.shop.home", "/shop/home", ["shop-home"])
_include_router("app.api.v1.favorites", "/favorites", ["favorites"])
_include_router("app.api.v1.browse_history", "/browse-history", ["browse-history"])

from .base import Base
from .user import User, user_role_association
from .role import Role
from .product import Product
from .category import ProductCategory
from .brand import Brand
from .product_spu import ProductSpu
from .product_sku import ProductSku
from .product_image import ProductImage
from .inventory_record import InventoryRecord
from .cart import CartItem
from .order import Order, OrderItem

# Backward-compatible alias for services still importing Category.
Category = ProductCategory

__all__ = [
    "Base",
    "User",
    "user_role_association",
    "Role",
    "Product",
    "ProductCategory",
    "Category",
    "Brand",
    "ProductSpu",
    "ProductSku",
    "ProductImage",
    "InventoryRecord",
    "CartItem",
    "Order",
    "OrderItem",
]

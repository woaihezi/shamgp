"""
ShamGP 后端开发环境数据库初始化脚本
用法: cd backend && python scripts/init_dev_db.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash
from app.models import (
    User, Role, Permission,
    ProductCategory, Brand,
    Product, ProductSpu, ProductSku, ProductImage,
    CartItem, Order, OrderItem, Address,
    Favorite, BrowseHistory,
    Coupon, UserCoupon, ShippingRule,
    AdSpace, Ad, Floor, FloorProduct,
    InventoryRecord, user_role_association,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] 所有数据表已创建")


async def create_test_user():
    async with AsyncSessionLocal() as session:
        user = User(
            username="testuser",
            password=get_password_hash("user123"),
            nickname="测试用户",
            email="test@example.com",
            status=1,
            is_superuser=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"[OK] 测试用户已创建: username=testuser, password=user123")
        return user


async def create_admin_user():
    async with AsyncSessionLocal() as session:
        admin = User(
            username="admin",
            password=get_password_hash("admin123"),
            nickname="管理员",
            email="admin@example.com",
            status=1,
            is_superuser=True,
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        print(f"[OK] 管理员用户已创建: username=admin, password=admin123")
        return admin


async def create_test_category():
    async with AsyncSessionLocal() as session:
        cat = ProductCategory(
            name="测试分类",
            code="test",
            level=1,
            status=1,
            sort=1,
        )
        session.add(cat)
        await session.commit()
        await session.refresh(cat)
        print(f"[OK] 测试分类已创建: id={cat.id}")
        return cat


async def main():
    print("=== ShamGP 开发环境数据库初始化 ===\n")
    await create_tables()
    await create_test_user()
    await create_admin_user()
    await create_test_category()
    print("\n=== 初始化完成 ===")
    print("现在可以启动后端: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")


if __name__ == "__main__":
    asyncio.run(main())

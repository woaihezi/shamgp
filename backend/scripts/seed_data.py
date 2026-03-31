import asyncio
import sys
import os
from sqlalchemy import select

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models import (
    User,
    Role,
    ProductCategory,
    Product,
    CartItem,
    Order,
    OrderItem
)


async def seed_data():
    async with AsyncSessionLocal() as session:
        print("Seeding data...")
        
        # 1. 检查是否已存在管理员角色
        result = await session.execute(select(Role).where(Role.code == "admin"))
        admin_role = result.scalar_one_or_none()
        
        if not admin_role:
            admin_role = Role(
                name="管理员",
                code="admin",
                description="系统管理员",
                sort=1
            )
            session.add(admin_role)
            await session.flush()
            print("Created admin role")
        else:
            print("Admin role already exists")
        
        # 2. 创建管理员用户 (密码: admin123)
        admin_user = User(
            username="admin",
            password=get_password_hash("admin123"),
            nickname="系统管理员",
            email="admin@shamgp.com",
            phone="13800138000",
            status=1,
            user_type=1
        )
        admin_user.roles.append(admin_role)
        session.add(admin_user)
        
        # 3. 创建测试用户 (密码: user123)
        test_user = User(
            username="testuser",
            password=get_password_hash("user123"),
            nickname="测试用户",
            email="test@shamgp.com",
            phone="13900139000",
            status=1,
            user_type=2
        )
        session.add(test_user)
        await session.flush()
        
        # 4. 创建商品分类
        category1 = ProductCategory(
            name="数码产品",
            code="digital",
            description="数码电子产品",
            sort=1,
            level=1,
            status=1
        )
        category2 = ProductCategory(
            name="服装鞋帽",
            code="clothing",
            description="服装鞋类",
            sort=2,
            level=1,
            status=1
        )
        category3 = ProductCategory(
            name="食品饮料",
            code="food",
            description="食品和饮料",
            sort=3,
            level=1,
            status=1
        )
        session.add_all([category1, category2, category3])
        await session.flush()
        
        # 5. 创建商品数据
        products = [
            Product(
                category_id=category1.id,
                name="iPhone 15 Pro Max",
                code="IPHONE15PM",
                brief="苹果最新旗舰手机，钛金属设计，A17 Pro芯片",
                description="iPhone 15 Pro Max 采用钛金属设计，配备 A17 Pro 芯片，支持 USB-C 接口，提供卓越的性能和拍照体验。",
                cover_image="https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
                price=9999.00,
                original_price=10999.00,
                stock=100,
                sales=50,
                is_hot=True,
                is_new=True,
                status=1,
                sort=1
            ),
            Product(
                category_id=category1.id,
                name="MacBook Pro 14\"",
                code="MBP14M3",
                brief="M3 Pro芯片，专业级性能",
                description="搭载 M3 Pro 芯片的 MacBook Pro，提供出色的性能和超长续航，是专业工作者的理想选择。",
                cover_image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop",
                price=14999.00,
                original_price=16999.00,
                stock=50,
                sales=30,
                is_hot=True,
                status=1,
                sort=2
            ),
            Product(
                category_id=category2.id,
                name="经典款运动鞋",
                code="SNEAKER001",
                brief="舒适百搭，时尚之选",
                description="采用优质面料制作，舒适透气，适合日常穿着和运动健身。",
                cover_image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
                price=599.00,
                original_price=899.00,
                stock=200,
                sales=150,
                is_hot=True,
                is_recommend=True,
                status=1,
                sort=1
            ),
            Product(
                category_id=category2.id,
                name="纯棉休闲T恤",
                code="TSHIRT001",
                brief="100%纯棉，亲肤舒适",
                description="精选优质纯棉面料，手感柔软，透气吸湿，四季皆宜。",
                cover_image="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
                price=129.00,
                original_price=199.00,
                stock=300,
                sales=280,
                is_new=True,
                status=1,
                sort=2
            ),
            Product(
                category_id=category3.id,
                name="有机坚果礼盒",
                code="NUTS001",
                brief="精选6种有机坚果，健康美味",
                description="包含杏仁、腰果、核桃、夏威夷果、碧根果、开心果，营养丰富，送礼佳品。",
                cover_image="https://images.unsplash.com/photo-1536816579748-4ecb145459ec?w=400&h=400&fit=crop",
                price=268.00,
                original_price=328.00,
                stock=80,
                sales=45,
                is_recommend=True,
                status=1,
                sort=1
            ),
            Product(
                category_id=category3.id,
                name="进口咖啡豆",
                code="COFFEE001",
                brief="哥伦比亚单品咖啡豆，中度烘焙",
                description="精选哥伦比亚咖啡豆，中度烘焙，带有坚果和巧克力风味，酸度适中。",
                cover_image="https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=400&fit=crop",
                price=168.00,
                original_price=198.00,
                stock=120,
                sales=90,
                status=1,
                sort=2
            )
        ]
        session.add_all(products)
        await session.flush()
        
        # 6. 创建购物车数据
        cart_item1 = CartItem(
            user_id=test_user.id,
            product_id=products[0].id,
            quantity=1,
            selected=True
        )
        cart_item2 = CartItem(
            user_id=test_user.id,
            product_id=products[2].id,
            quantity=2,
            selected=True
        )
        session.add_all([cart_item1, cart_item2])
        
        # 7. 创建订单数据
        order1 = Order(
            order_no="ORD202503310001",
            user_id=test_user.id,
            total_amount=1199.00,
            pay_amount=1199.00,
            status="completed",
            pay_status=1,
            consignee_name="张三",
            consignee_phone="13800138001",
            consignee_address="北京市朝阳区xxx街道xxx号"
        )
        session.add(order1)
        await session.flush()
        
        order_item1 = OrderItem(
            order_id=order1.id,
            product_id=products[2].id,
            product_name=products[2].name,
            product_image=products[2].cover_image,
            price=products[2].price,
            quantity=2,
            total_amount=products[2].price * 2
        )
        session.add(order_item1)
        
        await session.commit()
        print("Data seeded successfully!")
        print(f"\nDefault admin account:")
        print(f"  Username: admin")
        print(f"  Password: admin123")
        print(f"\nTest user account:")
        print(f"  Username: testuser")
        print(f"  Password: user123")


if __name__ == "__main__":
    asyncio.run(seed_data())

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.services.user_service import user_service
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

# 测试数据库引擎
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
)

# 测试会话工厂
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def setup_db():
    """设置测试数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def teardown_db():
    """清理测试数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user():
    """测试创建用户"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            
            user = await user_service.create(db, user_data.model_dump())
            
            assert user is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.nickname == "Test User"
            assert user.phone == "13800138000"
            assert user.password is not None
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_get_user_by_id():
    """测试通过ID获取用户"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            test_user = await user_service.create(db, user_data.model_dump())
            
            # 测试通过ID获取用户
            user = await user_service.get(db, test_user.id)
            
            assert user is not None
            assert user.id == test_user.id
            assert user.username == test_user.username
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_get_user_by_username():
    """测试通过用户名获取用户"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            test_user = await user_service.create(db, user_data.model_dump())
            
            # 测试通过用户名获取用户
            user = await user_service.get_by_username(db, test_user.username)
            
            assert user is not None
            assert user.username == test_user.username
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_get_user_by_email():
    """测试通过邮箱获取用户"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            test_user = await user_service.create(db, user_data.model_dump())
            
            # 测试通过邮箱获取用户
            user = await user_service.get_by_email(db, test_user.email)
            
            assert user is not None
            assert user.email == test_user.email
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_update_user():
    """测试更新用户信息"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            test_user = await user_service.create(db, user_data.model_dump())
            
            # 测试更新用户信息
            update_data = UserUpdate(
                nickname="Updated Test User",
                phone="13900139000"
            )
            
            updated_user = await user_service.update(db, test_user, update_data.model_dump(exclude_unset=True))
            
            assert updated_user is not None
            assert updated_user.nickname == "Updated Test User"
            assert updated_user.phone == "13900139000"
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_authenticate_user():
    """测试用户认证"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            test_user = await user_service.create(db, user_data.model_dump())
            
            # 测试正确的密码
            authenticated_user = await user_service.authenticate(db, test_user.username, "password123")
            assert authenticated_user is not None
            assert authenticated_user.username == test_user.username
            
            # 测试错误的密码
            wrong_password_user = await user_service.authenticate(db, test_user.username, "wrongpassword")
            assert wrong_password_user is None
            
            # 测试不存在的用户
            non_existent_user = await user_service.authenticate(db, "nonexistent", "password123")
            assert non_existent_user is None
    finally:
        await teardown_db()


@pytest.mark.asyncio
async def test_get_multi_paginated():
    """测试分页获取用户列表"""
    await setup_db()
    try:
        async with TestingSessionLocal() as db:
            # 创建测试用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                nickname="Test User",
                phone="13800138000"
            )
            await user_service.create(db, user_data.model_dump())
            
            # 创建更多用户用于测试分页
            for i in range(5):
                user_data = UserCreate(
                    username=f"user{i}",
                    email=f"user{i}@example.com",
                    password="password123",
                    nickname=f"User {i}",
                    phone=f"138001380{i}"
                )
                await user_service.create(db, user_data.model_dump())
            
            # 测试分页获取
            users, total = await user_service.get_multi_paginated(db, page=1, page_size=3)
            
            assert len(users) == 3
            assert total >= 6  # 包括测试用户和5个新创建的用户
    finally:
        await teardown_db()
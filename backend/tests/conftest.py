import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.config import settings
from app.main import app
from fastapi.testclient import TestClient
import asyncio

# 测试数据库引擎
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
)

# 测试会话工厂
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """创建一个会话范围的事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_database():
    """设置测试数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db():
    """创建一个测试数据库会话"""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client():
    """创建一个测试客户端"""
    return TestClient(app)


@pytest.fixture
async def test_user(db):
    """创建一个测试用户"""
    from app.services.user_service import user_service
    from app.schemas.user import UserCreate
    
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123",
        nickname="Test User",
        phone="13800138000"
    )
    user = await user_service.create(db, user_data.model_dump())
    return user


@pytest.fixture
async def test_token(client, test_user):
    """获取测试用户的令牌"""
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    return response.json()["data"]["access_token"]
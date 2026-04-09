import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    """测试用户注册"""
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "nickname": "New User",
        "phone": "13800138001"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "data" in data
    assert "user" in data["data"]
    assert data["data"]["user"]["username"] == "newuser"
    assert data["data"]["user"]["email"] == "newuser@example.com"


def test_login():
    """测试用户登录"""
    # 先注册一个用户
    client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "password123",
        "nickname": "Login User",
        "phone": "13800138002"
    })
    
    # 测试登录
    response = client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "data" in data
    assert "access_token" in data["data"]
    assert "token_type" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_login_with_wrong_password():
    """测试使用错误密码登录"""
    # 先注册一个用户
    client.post("/api/v1/auth/register", json={
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "password123",
        "nickname": "Wrong Pass User",
        "phone": "13800138003"
    })
    
    # 测试使用错误密码登录
    response = client.post("/api/v1/auth/login", json={
        "username": "wrongpassuser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401
    assert "message" in data


def test_login_with_nonexistent_user():
    """测试登录不存在的用户"""
    response = client.post("/api/v1/auth/login", json={
        "username": "nonexistentuser",
        "password": "password123"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401
    assert "message" in data


@pytest.mark.asyncio
async def test_get_current_user(client, test_token):
    """测试获取当前用户信息"""
    response = client.get("/api/v1/users/me", headers={
        "Authorization": f"Bearer {test_token}"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "data" in data
    assert data["data"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(client):
    """测试使用无效令牌获取当前用户信息"""
    response = client.get("/api/v1/users/me", headers={
        "Authorization": "Bearer invalidtoken"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401
    assert "message" in data
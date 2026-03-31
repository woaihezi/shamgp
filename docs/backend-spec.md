# 后端开发规范

## 1. 项目结构规范

### 1.1 目录命名
- 目录名：小写字母 + 下划线（snake_case），如 `user_manage`
- 模块文件：小写字母 + 下划线，如 `user_service.py`

### 1.2 包模块组织
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # 路由聚合
│   │       ├── admin/          # 后台管理 API
│   │       └── shop/           # 商城 API
│   ├── core/                   # 核心配置
│   ├── models/                 # 数据库模型
│   ├── schemas/                # Pydantic 模型
│   ├── services/               # 业务逻辑层
│   ├── utils/                  # 工具函数
│   └── tests/                  # 测试
├── alembic/                    # 数据库迁移
└── requirements.txt
```

---

## 2. 代码风格规范

### 2.1 命名规范
- 类名：大驼峰（PascalCase），如 `UserService`
- 函数/方法：小写字母 + 下划线（snake_case），如 `get_user_list`
- 常量：全大写 + 下划线，如 `MAX_PAGE_SIZE`
- 私有变量/方法：单下划线前缀，如 `_internal_method`

### 2.2 类型注解
- 所有函数必须添加类型注解
- 使用 `typing` 模块或 Python 3.9+ 内置类型

```python
from typing import List, Optional
from datetime import datetime

def get_users(
    page: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None
) -> tuple[List[dict], int]:
    pass
```

### 2.3 导入顺序
```python
# 标准库
import os
from datetime import datetime

# 第三方库
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 本地模块
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
```

---

## 3. 数据库模型规范

### 3.1 基础模型

```python
# app/models/base.py
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
```

### 3.2 模型定义

```python
# app/models/user.py
from sqlalchemy import Column, BigInteger, String, SmallInteger
from .base import Base, TimestampMixin, SoftDeleteMixin

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), index=True)
    phone = Column(String(20), index=True)
    nickname = Column(String(50))
    avatar = Column(String(255))
    gender = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=1, index=True)
    user_type = Column(SmallInteger, default=1)
```

---

## 4. Pydantic Schema 规范

### 4.1 通用响应模型

```python
# app/schemas/common.py
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[T] = Field(None, description="数据")
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))

class PageResponse(BaseModel, Generic[T]):
    list: List[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
```

### 4.2 业务模型

```python
# app/schemas/user.py
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    role_ids: Optional[List[int]] = Field(None, description="角色ID列表")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    status: Optional[int] = None
    role_ids: Optional[List[int]] = None

class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    gender: int = 0
    status: int = 1
    user_type: int = 1
    created_at: datetime

    class Config:
        from_attributes = True

class UserListQuery(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    keyword: Optional[str] = Field(None, description="关键词")
    status: Optional[int] = Field(None, description="状态")
```

---

## 5. API 路由规范

### 5.1 路由定义

```python
# app/api/v1/admin/users.py
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db, get_current_admin_user
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserListQuery
)
from app.schemas.common import Response, PageResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("", response_model=Response[PageResponse[UserResponse]])
async def get_users(
    query: UserListQuery = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    users, total = await UserService.get_list(db, query)
    total_pages = (total + query.page_size - 1) // query.page_size
    return Response(
        data=PageResponse(
            list=users,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages
        )
    )

@router.get("/{user_id}", response_model=Response[UserResponse])
async def get_user(
    user_id: int = Path(..., description="用户ID"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    user = await UserService.get_by_id(db, user_id)
    return Response(data=user)

@router.post("", response_model=Response[UserResponse])
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    user = await UserService.create(db, user_in)
    return Response(data=user, message="创建成功")

@router.put("/{user_id}", response_model=Response[UserResponse])
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    user = await UserService.update(db, user_id, user_in)
    return Response(data=user, message="更新成功")

@router.delete("/{user_id}", response_model=Response)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    await UserService.delete(db, user_id)
    return Response(message="删除成功")
```

### 5.2 路由聚合

```python
# app/api/v1/api.py
from fastapi import APIRouter
from .admin import users, roles, menus, products, orders
from .shop import auth, products as shop_products, cart, orders as shop_orders

api_router = APIRouter()

api_router.include_router(users.router, prefix="/admin")
api_router.include_router(roles.router, prefix="/admin")
api_router.include_router(menus.router, prefix="/admin")
api_router.include_router(products.router, prefix="/admin")
api_router.include_router(orders.router, prefix="/admin")

api_router.include_router(auth.router, prefix="/shop")
api_router.include_router(shop_products.router, prefix="/shop")
api_router.include_router(cart.router, prefix="/shop")
api_router.include_router(shop_orders.router, prefix="/shop")
```

---

## 6. Service 层规范

### 6.1 基础 Service

```python
# app/services/base.py
from typing import TypeVar, Type, Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import class_mapper

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        *,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        order_dir: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[ModelType], int]:
        query = select(self.model)
        
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if value is not None:
                    if isinstance(value, str):
                        filter_conditions.append(getattr(self.model, key).contains(value))
                    else:
                        filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        if order_by:
            order_column = getattr(self.model, order_by)
            if order_dir == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        items = result.scalars().all()
        
        return items, total

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        obj_data = obj_in.model_dump(exclude_unset=True)
        query = update(self.model).where(self.model.id == id).values(**obj_data)
        await db.execute(query)
        await db.commit()
        return await self.get_by_id(db, id)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        query = update(self.model).where(self.model.id == id).values(is_deleted=True)
        await db.execute(query)
        await db.commit()
        return True
```

### 6.2 业务 Service

```python
# app/services/user_service.py
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from passlib.context import CryptContext

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserUpdate, UserListQuery
from .base import BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        query: UserListQuery
    ) -> Tuple[List[User], int]:
        filters = {}
        if query.keyword:
            filters["username"] = query.keyword
        if query.status is not None:
            filters["status"] = query.status
        
        return await super().get_list(
            db,
            filters=filters,
            order_by="created_at",
            order_dir="desc",
            page=query.page,
            page_size=query.page_size
        )

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        obj_data = obj_in.model_dump()
        role_ids = obj_data.pop("role_ids", [])
        
        obj_data["password"] = self.get_password_hash(obj_data["password"])
        user = User(**obj_data)
        db.add(user)
        await db.flush()
        
        if role_ids:
            for role_id in role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                db.add(user_role)
        
        await db.commit()
        await db.refresh(user)
        return user

user_service = UserService()
```

---

## 7. 依赖注入规范

### 7.1 数据库会话

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### 7.2 当前用户

```python
# app/api/deps.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.services.user_service import user_service

security = HTTPBearer()

async def get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    return credentials.credentials

async def get_current_user(
    token: str = Depends(get_token_from_header),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_service.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    if user.status != 1:
        raise HTTPException(status_code=403, detail="用户已被禁用")
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.user_type != 2:
        raise HTTPException(status_code=403, detail="权限不足")
    return current_user
```

---

## 8. 异常处理规范

### 8.1 自定义异常

```python
# app/core/exceptions.py
from fastapi import HTTPException, status

class BusinessException(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={"code": code, "message": message}
        )

class NotFoundException(BusinessException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message)

class ValidationException(BusinessException):
    def __init__(self, message: str = "参数验证失败"):
        super().__init__(code=400, message=message)

class AuthException(BusinessException):
    def __init__(self, message: str = "认证失败"):
        super().__init__(code=401, message=message)

class PermissionException(BusinessException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=403, message=message)
```

### 8.2 全局异常处理

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import BusinessException

app = FastAPI()

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.detail["code"],
            "message": exc.detail["message"],
            "data": None,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
    )
```

---

## 9. 配置管理规范

### 9.1 配置类

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DEBUG: bool = True
    
    API_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/shamgp"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 10. 日志规范

### 10.1 日志配置

```python
# app/utils/logger.py
import logging
import sys
from datetime import datetime

def setup_logger(name: str = "shamgp") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()
```

---

## 11. 代码提交规范

### 11.1 Commit Message 格式
```
<type>(<scope>): <subject>

<type>:
  feat: 新功能
  fix: 修复bug
  docs: 文档更新
  style: 代码格式
  refactor: 重构
  test: 测试相关
  chore: 构建/工具

示例:
feat(backend): 添加用户管理 Service
fix(backend): 修复 JWT Token 验证错误
```

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


WEAK_JWT_SECRETS = {
    "",
    "secret",
    "changeme",
    "change-me",
    "default",
    "your-secret-key-here-change-in-production",
    "your-secret-key-here",
}


class Settings(BaseSettings):
    PROJECT_NAME: str = "ShamGP E-commerce"
    API_V1_STR: str = "/api/v1"
    
    DB_TYPE: str = "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "shop_db"
    
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "postgresql":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001"
    CORS_ALLOW_CREDENTIALS: bool = True
    
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        secret = (value or "").strip()
        if secret.lower() in WEAK_JWT_SECRETS:
            raise ValueError("SECRET_KEY 使用了弱密钥/占位值，请通过环境变量设置强随机值。")
        if len(secret) < 32:
            raise ValueError("SECRET_KEY 长度至少 32 位。")
        return secret

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, value: str) -> str:
        origins = [item.strip() for item in (value or "").split(",") if item.strip()]
        if not origins:
            raise ValueError("CORS_ORIGINS 不能为空。")
        if "*" in origins:
            raise ValueError("CORS_ORIGINS 不允许使用通配符 '*'。")
        return ",".join(origins)

    @property
    def cors_origins_list(self) -> List[str]:
        return [item.strip() for item in self.CORS_ORIGINS.split(",") if item.strip()]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

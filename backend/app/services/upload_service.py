
import os
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from fastapi import UploadFile
from ..models.file import File
from ..schemas.file import (
    FileCreate,
    FileUpdate,
    FileResponse,
    FileQuery,
    UploadResponse
)
from ..schemas.common import PageResponse
from ..core.config import settings


class UploadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_file(
        self,
        file: UploadFile,
        category: Optional[str] = None,
        upload_user_id: Optional[int] = None
    ) -> UploadResponse:
        upload_dir = settings.UPLOAD_DIR
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        if file_ext and file_ext not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型: {file_ext}")
        
        storage_name = f"{uuid.uuid4().hex}.{file_ext}" if file_ext else uuid.uuid4().hex
        file_path = os.path.join(upload_dir, storage_name)
        
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"文件大小超过限制: {settings.MAX_UPLOAD_SIZE} bytes")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        file_url = f"/uploads/{storage_name}"
        
        file_data = FileCreate(
            filename=file.filename,
            storage_name=storage_name,
            file_path=file_path,
            file_url=file_url,
            file_size=len(content),
            file_type=file.content_type or "application/octet-stream",
            file_ext=file_ext,
            upload_user_id=upload_user_id,
            category=category,
            storage_type="local"
        )
        
        db_file = File(**file_data.model_dump())
        self.db.add(db_file)
        await self.db.commit()
        await self.db.refresh(db_file)
        
        return UploadResponse(
            file_id=db_file.id,
            filename=db_file.filename,
            file_url=db_file.file_url,
            file_size=db_file.file_size
        )

    async def get_file(self, file_id: int) -> Optional[FileResponse]:
        result = await self.db.execute(select(File).where(File.id == file_id))
        file = result.scalar_one_or_none()
        return FileResponse.model_validate(file) if file else None

    async def update_file(self, file_id: int, file_data: FileUpdate) -> Optional[FileResponse]:
        result = await self.db.execute(select(File).where(File.id == file_id))
        db_file = result.scalar_one_or_none()
        
        if db_file:
            update_data = file_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_file, field, value)
            
            await self.db.commit()
            await self.db.refresh(db_file)
            return FileResponse.model_validate(db_file)
        
        return None

    async def delete_file(self, file_id: int) -> bool:
        result = await self.db.execute(select(File).where(File.id == file_id))
        db_file = result.scalar_one_or_none()
        
        if db_file:
            if os.path.exists(db_file.file_path):
                os.remove(db_file.file_path)
            
            await self.db.delete(db_file)
            await self.db.commit()
            return True
        
        return False

    async def list_files(self, query: FileQuery) -> PageResponse[FileResponse]:
        stmt = select(File)
        
        if query.filename:
            stmt = stmt.where(File.filename.contains(query.filename))
        if query.file_type:
            stmt = stmt.where(File.file_type.contains(query.file_type))
        if query.category:
            stmt = stmt.where(File.category == query.category)
        if query.upload_user_id:
            stmt = stmt.where(File.upload_user_id == query.upload_user_id)
        if query.status is not None:
            stmt = stmt.where(File.status == query.status)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        
        offset = (query.page - 1) * query.page_size
        stmt = stmt.order_by(desc(File.created_at)).offset(offset).limit(query.page_size)
        
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return PageResponse(
            total=total,
            page=query.page,
            page_size=query.page_size,
            items=[FileResponse.model_validate(item) for item in items]
        )

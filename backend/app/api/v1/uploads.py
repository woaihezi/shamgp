
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ...core.database import get_db
from ...schemas.common import ResponseModel, PageResponse
from ...schemas.file import (
    FileResponse,
    FileUpdate,
    FileQuery,
    UploadResponse
)
from ...services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["文件上传"])


@router.post("", response_model=ResponseModel[UploadResponse])
async def upload_file(
    file: UploadFile = File(...),
    category: Optional[str] = Query(None, description="文件分类"),
    upload_user_id: Optional[int] = Query(None, description="上传用户ID"),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = UploadService(db)
        result = await service.upload_file(file, category, upload_user_id)
        return ResponseModel(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{file_id}", response_model=ResponseModel[FileResponse])
async def get_file(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = UploadService(db)
    file = await service.get_file(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return ResponseModel(data=file)


@router.put("/{file_id}", response_model=ResponseModel[FileResponse])
async def update_file(
    file_id: int,
    file_data: FileUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = UploadService(db)
    file = await service.update_file(file_id, file_data)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return ResponseModel(data=file)


@router.delete("/{file_id}", response_model=ResponseModel[dict])
async def delete_file(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = UploadService(db)
    success = await service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="文件不存在")
    return ResponseModel(data={"message": "删除成功"})


@router.get("", response_model=ResponseModel[PageResponse[FileResponse]])
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    filename: Optional[str] = None,
    file_type: Optional[str] = None,
    category: Optional[str] = None,
    upload_user_id: Optional[int] = None,
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    service = UploadService(db)
    query = FileQuery(
        page=page,
        page_size=page_size,
        filename=filename,
        file_type=file_type,
        category=category,
        upload_user_id=upload_user_id,
        status=status
    )
    result = await service.list_files(query)
    return ResponseModel(data=result)


@router.post("/excel/import", tags=["Excel导入导出(预留)"])
async def excel_import():
    return ResponseModel(data={"message": "Excel导入接口预留"})


@router.get("/excel/export", tags=["Excel导入导出(预留)"])
async def excel_export():
    return ResponseModel(data={"message": "Excel导出接口预留"})

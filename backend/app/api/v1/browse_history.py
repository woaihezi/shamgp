from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, text
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.browse_history import BrowseHistory
from sqlalchemy import select

router = APIRouter()


@router.post("/browse", response_model=dict)
async def add_browse_history(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 同一用户同一商品，更新浏览时间（保留最新浏览时间）
    result = await db.execute(
        select(BrowseHistory).where(
            BrowseHistory.user_id == current_user.id,
            BrowseHistory.product_id == product_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        # 直接用 SQL 更新 browse_time
        await db.execute(
            text("UPDATE browse_histories SET browse_time = NOW() WHERE id = :id"),
            {"id": existing.id}
        )
        await db.commit()
    else:
        history = BrowseHistory(user_id=current_user.id, product_id=product_id)
        db.add(history)
        await db.commit()
    return {"code": 200, "message": "浏览记录已保存"}

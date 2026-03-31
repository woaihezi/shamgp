from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_active_user, get_current_active_superuser
from app.schemas.common import ResponseModel, PaginationResult, PaginationParams
from app.schemas.menu import MenuSimple, MenuCreate, MenuUpdate, MenuTree
from app.services.menu_service import MenuService
from app.models.user import User

router = APIRouter()


@router.get("", response_model=ResponseModel[PaginationResult[MenuSimple]])
async def get_menus(
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    skip = (params.page - 1) * params.page_size
    menus = await MenuService.get_multi(db, skip=skip, limit=params.page_size)
    total = len(await MenuService.get_all(db))
    return ResponseModel(
        data=PaginationResult(
            items=menus,
            total=total,
            page=params.page,
            page_size=params.page_size
        )
    )


@router.get("/tree", response_model=ResponseModel[list[MenuTree]])
async def get_all_menu_tree(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    menus = await MenuService.get_all(db)
    menu_tree = MenuService.build_menu_tree(menus)
    return ResponseModel(data=menu_tree)


@router.get("/{menu_id}", response_model=ResponseModel[MenuSimple])
async def get_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    menu = await MenuService.get(db, menu_id)
    return ResponseModel(data=menu)


@router.post("", response_model=ResponseModel[MenuSimple])
async def create_menu(
    menu_in: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    menu = await MenuService.create(db, menu_in)
    return ResponseModel(data=menu)


@router.put("/{menu_id}", response_model=ResponseModel[MenuSimple])
async def update_menu(
    menu_id: int,
    menu_in: MenuUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    menu = await MenuService.get(db, menu_id)
    menu = await MenuService.update(db, menu, menu_in)
    return ResponseModel(data=menu)


@router.delete("/{menu_id}", response_model=ResponseModel)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    await MenuService.remove(db, menu_id)
    return ResponseModel(message="Menu deleted successfully")

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.exceptions import ResourceNotFoundError
from app.models.menu import Menu
from app.models.user import User
from app.schemas.menu import MenuCreate, MenuUpdate, MenuTree, RouterItem, RouterMeta


class MenuService:
    @staticmethod
    async def get(db: AsyncSession, menu_id: int) -> Optional[Menu]:
        result = await db.execute(
            select(Menu).where(Menu.id == menu_id, Menu.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Menu]:
        result = await db.execute(
            select(Menu)
            .where(Menu.is_deleted == False)
            .order_by(Menu.sort)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List[Menu]:
        result = await db.execute(
            select(Menu)
            .where(Menu.is_deleted == False)
            .order_by(Menu.sort)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_user(db: AsyncSession, user: User) -> List[Menu]:
        if user.is_superuser:
            return await MenuService.get_all(db)
        
        menu_ids = set()
        for role in user.roles:
            menu_ids.update([menu.id for menu in role.menus])
        
        if not menu_ids:
            return []
        
        result = await db.execute(
            select(Menu)
            .where(Menu.id.in_(menu_ids), Menu.is_deleted == False)
            .order_by(Menu.sort)
        )
        return list(result.scalars().all())
    
    @staticmethod
    def build_menu_tree(menus: List[Menu]) -> List[MenuTree]:
        menu_dict = {}
        root_menus = []
        
        for menu in menus:
            menu_dict[menu.id] = MenuTree(
                id=menu.id,
                parent_id=menu.parent_id,
                name=menu.name,
                path=menu.path,
                component=menu.component,
                permission=menu.permission,
                type=menu.type,
                icon=menu.icon,
                sort=menu.sort,
                is_visible=menu.is_visible,
                is_keep_alive=menu.is_keep_alive,
                is_iframe=menu.is_iframe,
                redirect=menu.redirect,
                created_at=menu.created_at,
                updated_at=menu.updated_at,
                is_deleted=menu.is_deleted,
                children=[]
            )
        
        for menu_id, menu_tree in menu_dict.items():
            if menu_tree.parent_id == 0:
                root_menus.append(menu_tree)
            else:
                parent = menu_dict.get(menu_tree.parent_id)
                if parent:
                    parent.children.append(menu_tree)
        
        return root_menus
    
    @staticmethod
    def build_router_tree(menus: List[Menu]) -> List[RouterItem]:
        routers = []
        menu_dict = {}
        
        for menu in menus:
            if menu.type == 'button':
                continue
            
            menu_dict[menu.id] = RouterItem(
                path=menu.path or '',
                name=menu.path.replace('/', '-').strip('-') if menu.path else None,
                component=menu.component,
                redirect=menu.redirect,
                meta=RouterMeta(
                    title=menu.name,
                    icon=menu.icon,
                    permission=menu.permission,
                    is_keep_alive=menu.is_keep_alive,
                    is_iframe=menu.is_iframe,
                    is_visible=menu.is_visible
                ),
                children=[]
            )
        
        for menu_id, router in menu_dict.items():
            menu = next((m for m in menus if m.id == menu_id), None)
            if not menu:
                continue
            
            if menu.parent_id == 0:
                routers.append(router)
            else:
                parent = menu_dict.get(menu.parent_id)
                if parent:
                    parent.children.append(router)
        
        return routers
    
    @staticmethod
    async def create(db: AsyncSession, obj_in: MenuCreate) -> Menu:
        db_obj = Menu(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def update(db: AsyncSession, db_obj: Menu, obj_in: MenuUpdate) -> Menu:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def remove(db: AsyncSession, menu_id: int) -> Menu:
        menu = await MenuService.get(db, menu_id)
        if not menu:
            raise ResourceNotFoundError("Menu not found")
        
        menu.is_deleted = True
        db.add(menu)
        await db.commit()
        return menu

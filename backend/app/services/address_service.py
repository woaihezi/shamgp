from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from ..models.address import Address
from ..schemas.address import AddressCreate, AddressUpdate, AddressSchema


class AddressService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_addresses(self, user_id: int) -> List[Address]:
        result = await self.db.execute(
            select(Address).where(Address.user_id == user_id, Address.is_deleted == False)
        )
        return list(result.scalars().all())

    async def get_address(self, user_id: int, address_id: int) -> Optional[Address]:
        result = await self.db.execute(
            select(Address).where(
                Address.id == address_id,
                Address.user_id == user_id,
                Address.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def get_default_address(self, user_id: int) -> Optional[Address]:
        result = await self.db.execute(
            select(Address).where(
                Address.user_id == user_id,
                Address.is_default == True,
                Address.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def create_address(self, user_id: int, address_in: AddressCreate) -> Address:
        if address_in.is_default:
            await self.db.execute(
                update(Address)
                .where(Address.user_id == user_id, Address.is_deleted == False)
                .values(is_default=False)
            )

        address = Address(
            user_id=user_id,
            **address_in.model_dump()
        )
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def update_address(self, user_id: int, address_id: int, address_in: AddressUpdate) -> Optional[Address]:
        address = await self.get_address(user_id, address_id)
        if not address:
            return None

        if address_in.is_default:
            await self.db.execute(
                update(Address)
                .where(Address.user_id == user_id, Address.is_deleted == False)
                .values(is_default=False)
            )

        update_data = address_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(address, field, value)

        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def delete_address(self, user_id: int, address_id: int) -> bool:
        address = await self.get_address(user_id, address_id)
        if not address:
            return False

        address.is_deleted = True
        await self.db.commit()
        return True

    async def set_default_address(self, user_id: int, address_id: int) -> Optional[Address]:
        address = await self.get_address(user_id, address_id)
        if not address:
            return None

        await self.db.execute(
            update(Address)
            .where(Address.user_id == user_id, Address.is_deleted == False)
            .values(is_default=False)
        )

        address.is_default = True
        await self.db.commit()
        await self.db.refresh(address)
        return address

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .common import BaseSchema


class AddressBase(BaseModel):
    consignee_name: str = Field(..., min_length=1, max_length=50)
    consignee_phone: str = Field(..., min_length=1, max_length=20)
    province: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=50)
    district: str = Field(..., min_length=1, max_length=50)
    detail_address: str = Field(..., min_length=1, max_length=200)
    zip_code: Optional[str] = Field(None, max_length=10)
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    consignee_name: Optional[str] = Field(None, min_length=1, max_length=50)
    consignee_phone: Optional[str] = Field(None, min_length=1, max_length=20)
    province: Optional[str] = Field(None, min_length=1, max_length=50)
    city: Optional[str] = Field(None, min_length=1, max_length=50)
    district: Optional[str] = Field(None, min_length=1, max_length=50)
    detail_address: Optional[str] = Field(None, min_length=1, max_length=200)
    zip_code: Optional[str] = Field(None, max_length=10)
    is_default: Optional[bool] = None


class AddressSchema(BaseSchema, AddressBase):
    user_id: int
    
    @property
    def full_address(self) -> str:
        return f"{self.province}{self.city}{self.district}{self.detail_address}"

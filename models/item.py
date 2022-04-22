from pydantic import BaseModel, Field
from typing import Optional
from beanie import Document, Link, PydanticObjectId
from models.user import User


class Item(BaseModel):
    name: str
    price: float = Field(gt=0, le=100)
    is_offer: Optional[bool] = None


class ItemDocument(Document):
    name: str
    price: float = Field(gt=0, le=100)
    is_offer: Optional[bool] = None
    user_id: PydanticObjectId

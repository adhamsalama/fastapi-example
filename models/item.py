from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId


class Item(BaseModel):
    name: str
    price: float = Field(gt=0, le=100)
    is_offer: bool | None = None


class ItemDocument(Document):
    name: str
    price: float = Field(gt=0, le=100)
    is_offer: bool | None = None
    user_id: PydanticObjectId

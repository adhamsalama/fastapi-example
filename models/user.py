from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from beanie import Document, Insert, Replace, before_event


class UserIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class User(Document, UserIn):
    created_at: datetime = datetime.now()
    # @before_event(Insert)
    # def hash_password(self):
    #     if self.is_changed


class UserOut(BaseModel):
    email: str

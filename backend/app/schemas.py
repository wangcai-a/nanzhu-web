from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    description: str
    image: str
    specs: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    name: str
    email: str
    phone: str
    content: str
    status: Optional[str] = "pending"

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    status: str

class Message(MessageBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdminCreate(BaseModel):
    username: str
    password: str

class Stats(BaseModel):
    product_count: int
    pending_messages: int

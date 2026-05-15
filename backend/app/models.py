from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category = Column(String(100))
    price = Column(Float)
    description = Column(Text)
    image = Column(String(500))
    specs = Column(Text)
    created_at = Column(DateTime, default=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(200))
    phone = Column(String(20))
    content = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=func.now())

class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

SECRET_KEY = "nanzhu_bamboo_secret_key_for_jwt_token_generation_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SQLALCHEMY_DATABASE_URL = "sqlite:///./nanzhu.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category = Column(String(100))
    price = Column(Float)
    description = Column(Text)
    image = Column(String(500))
    specs = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(200))
    phone = Column(String(20))
    content = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class AdminDB(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="南竹竹制品管理系统 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: float
    description: str
    image: str
    specs: Optional[str] = None

class Message(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    content: str
    status: Optional[str] = "pending"
    created_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def get_admin(db: Session, username: str):
    return db.query(AdminDB).filter(AdminDB.username == username).first()

def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin or not verify_password(password, admin.hashed_password):
        return False
    return admin

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    admin = get_admin(db, username=token_data.username)
    if admin is None:
        raise credentials_exception
    return admin

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/register")
async def register_admin(username: str, password: str, db: Session = Depends(get_db)):
    if get_admin(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    db_admin = AdminDB(username=username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return {"message": "Admin registered successfully"}

@app.get("/api/products", response_model=List[Product])
async def get_products(db: Session = Depends(get_db), category: Optional[str] = None):
    query = db.query(ProductDB)
    if category:
        query = query.filter(ProductDB.category == category)
    return query.all()

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products", response_model=Product)
async def create_product(product: Product, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/api/messages", response_model=List[Message])
async def get_messages(db: Session = Depends(get_db), status: Optional[str] = None):
    query = db.query(MessageDB)
    if status:
        query = query.filter(MessageDB.status == status)
    return query.all()

@app.get("/api/messages/{message_id}", response_model=Message)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.post("/api/messages", response_model=Message)
async def create_message(message: Message, db: Session = Depends(get_db)):
    db_message = MessageDB(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.put("/api/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, status: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    db_message.status = status
    db.commit()
    db.refresh(db_message)
    return db_message

@app.delete("/api/messages/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully"}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    product_count = db.query(ProductDB).count()
    message_count = db.query(MessageDB).filter(MessageDB.status == "pending").count()
    return {
        "product_count": product_count,
        "pending_messages": message_count
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

def init_admin(db: Session):
    if not db.query(AdminDB).filter(AdminDB.username == "admin").first():
        hashed_password = get_password_hash("admin123")
        db_admin = AdminDB(username="admin", hashed_password=hashed_password)
        db.add(db_admin)
        db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    init_admin(db)
    db.close()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
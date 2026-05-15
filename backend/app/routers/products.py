from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Product
from ..schemas import ProductCreate, ProductUpdate, Product as ProductSchema
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/api/products", tags=["产品管理"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "nanzhu_bamboo_secret_key_for_jwt_token_generation_2024"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    from datetime import timedelta, datetime
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
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
    except JWTError:
        raise credentials_exception
    from ..models import Admin
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        raise credentials_exception
    return admin

@router.get("", response_model=List[ProductSchema])
async def get_products(db: Session = Depends(get_db), category: Optional[str] = None):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.all()

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductSchema)
async def create_product(product: ProductCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

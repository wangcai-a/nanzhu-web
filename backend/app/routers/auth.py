from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Admin
from ..schemas import Token
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["认证管理"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "nanzhu_bamboo_secret_key_for_jwt_token_generation_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_admin(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin or not verify_password(password, admin.hashed_password):
        return False
    return admin

def create_access_token(data: dict, expires_delta: timedelta = None):
    from datetime import datetime
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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

@router.post("/register")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    if get_admin(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    db_admin = Admin(username=username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return {"message": "Admin registered successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await login(form_data, db)

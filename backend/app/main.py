from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from .routers import products, messages, auth
from .models import Settings, Product, Message, Admin
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="南竹竹制品管理系统 API",
    description="长汀县南竹竹制品有限公司后台管理系统API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(messages.router)
app.include_router(auth.router)

DEFAULT_SETTINGS = [
    {"key": "site_name", "value": "南竹竹制品", "description": "网站名称"},
    {"key": "stat_product_count", "value": "500+", "description": "产品种类统计"},
    {"key": "stat_sales_amount", "value": "3000万+", "description": "年销售额统计"},
    {"key": "stat_dealer_count", "value": "50+", "description": "合作经销商统计"},
    {"key": "contact_address", "value": "福建省龙岩市长汀县工业园区", "description": "公司地址"},
    {"key": "contact_phone", "value": "0597-1234567", "description": "联系电话"},
    {"key": "contact_email", "value": "contact@nanzhu-bamboo.com", "description": "电子邮箱"},
    {"key": "contact_hours", "value": "周一至周六 8:00-18:00", "description": "营业时间"},
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "南竹竹制品管理系统 API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    product_count = db.query(Product).count()
    pending_messages = db.query(Message).filter(Message.status == "pending").count()
    return {
        "product_count": product_count,
        "pending_messages": pending_messages
    }

@app.get("/api/settings")
async def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Settings).all()
    result = {}
    for s in settings:
        result[s.key] = s.value
    return result

@app.put("/api/settings")
async def update_settings(updates: dict, db: Session = Depends(get_db)):
    for key, value in updates.items():
        setting = db.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = str(value)
        else:
            setting = Settings(key=key, value=str(value))
            db.add(setting)
    db.commit()
    return {"status": "success"}

def init_admin(db: Session):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not db.query(Admin).filter(Admin.username == "admin").first():
        hashed_password = pwd_context.hash("admin123")
        db_admin = Admin(username="admin", hashed_password=hashed_password)
        db.add(db_admin)
        db.commit()
        print("默认管理员账号已创建")

def init_settings(db: Session):
    for item in DEFAULT_SETTINGS:
        if not db.query(Settings).filter(Settings.key == item["key"]).first():
            setting = Settings(
                key=item["key"],
                value=item["value"],
                description=item.get("description", "")
            )
            db.add(setting)
    db.commit()
    print("默认网站设置已创建")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_admin(db)
        init_settings(db)
    finally:
        db.close()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

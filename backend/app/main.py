from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import products, messages, auth

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

@app.get("/")
async def root():
    return {"message": "南竹竹制品管理系统 API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/stats")
async def get_stats():
    from .database import SessionLocal
    from .models import Product, Message
    
    db = SessionLocal()
    try:
        product_count = db.query(Product).count()
        pending_messages = db.query(Message).filter(Message.status == "pending").count()
        return {
            "product_count": product_count,
            "pending_messages": pending_messages
        }
    finally:
        db.close()

def init_admin():
    from .database import SessionLocal
    from .models import Admin
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    db = SessionLocal()
    try:
        if not db.query(Admin).filter(Admin.username == "admin").first():
            hashed_password = pwd_context.hash("admin123")
            db_admin = Admin(username="admin", hashed_password=hashed_password)
            db.add(db_admin)
            db.commit()
            print("默认管理员账号已创建")
    finally:
        db.close()

if __name__ == "__main__":
    init_admin()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Depends, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from .database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from .routers import products, messages, auth
from .models import Settings, Product, Message, Admin
import bcrypt
import os
import uuid
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="南竹竹制品管理系统 API",
    description="长汀县南竹制品有限公司后台管理系统API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)
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

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "public")

uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

class NoCacheFileResponse(FileResponse):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
    
    @property
    def cache_control(self):
        return "no-cache, no-store, must-revalidate"

app.mount("/assets", NoCacheStaticFiles(directory=frontend_dir), name="static")
app.mount("/uploads", NoCacheStaticFiles(directory=uploads_dir), name="uploads")

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
    return FileResponse(
        os.path.join(frontend_dir, "index.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/admin")
async def admin():
    return FileResponse(
        os.path.join(frontend_dir, "admin.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/admin.html")
async def admin_html():
    return FileResponse(
        os.path.join(frontend_dir, "admin.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/product.html")
async def product_html():
    return FileResponse(
        os.path.join(frontend_dir, "product.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/contact")
async def contact():
    return FileResponse(
        os.path.join(frontend_dir, "contact.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/contact.html")
async def contact_html():
    return FileResponse(
        os.path.join(frontend_dir, "contact.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    if file.content_type not in allowed_types:
        return {"error": "不支持的文件类型，仅支持 JPG、PNG、GIF、WebP 格式"}
    
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    if not file_ext:
        file_ext = ".jpg"
    
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
    file_path = os.path.join(uploads_dir, filename)
    
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        file_url = f"/uploads/{filename}"
        return {"url": file_url, "filename": filename}
    except Exception as e:
        return {"error": f"文件上传失败: {str(e)}"}

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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        redoc_url="https://unpkg.com/redoc@next/bundle.js",
        openapi_url=app.openapi_url
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

def init_admin(db: Session):
    try:
        if not db.query(Admin).filter(Admin.username == "admin").first():
            password = "admin123"
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            db_admin = Admin(username="admin", hashed_password=hashed_password.decode('utf-8'))
            db.add(db_admin)
            db.commit()
            print("默认管理员账号已创建")
    except Exception as e:
        print(f"初始化管理员时出错: {e}")

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

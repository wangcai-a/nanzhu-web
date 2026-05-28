from app.database import SessionLocal, engine, Base
from app.models import Admin, Settings, Product, Message
import bcrypt

# 创建所有表
Base.metadata.create_all(bind=engine)

# 初始化默认设置
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

db = SessionLocal()

try:
    # 创建默认管理员账号
    if not db.query(Admin).filter(Admin.username == "admin").first():
        # 使用 bcrypt 直接哈希密码
        password = "admin123".encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        db_admin = Admin(username="admin", hashed_password=hashed_password.decode('utf-8'))
        db.add(db_admin)
        print("✓ 默认管理员账号已创建")
        print("  用户名: admin")
        print("  密码: admin123")
    else:
        print("✓ 管理员账号已存在")

    # 创建默认设置
    for item in DEFAULT_SETTINGS:
        if not db.query(Settings).filter(Settings.key == item["key"]).first():
            setting = Settings(
                key=item["key"],
                value=item["value"],
                description=item.get("description", "")
            )
            db.add(setting)
            print(f"✓ 添加设置: {item['key']}")

    db.commit()
    print("\n✓ 数据库初始化完成！")

finally:
    db.close()

# 南竹竹制品管理系统

前后端分离架构企业官网系统

## 项目结构

```
d:\code\web\
├── frontend/                 # 前端资源目录
│   ├── public/               # 公开静态资源
│   │   ├── index.html       # 企业官网首页
│   │   ├── admin.html       # 管理后台页面
│   │   ├── styles.css       # 官网样式
│   │   ├── admin-styles.css # 后台样式
│   │   ├── script.js        # 官网脚本
│   │   └── admin-script.js  # 后台脚本
│   └── src/                 # 前端源代码（如需）
├── backend/                  # 后端服务目录
│   ├── app/                 # 应用代码
│   │   ├── routers/        # API路由
│   │   │   ├── __init__.py
│   │   │   ├── auth.py     # 认证接口
│   │   │   ├── products.py  # 产品接口
│   │   │   └── messages.py  # 留言接口
│   │   ├── __init__.py
│   │   ├── main.py         # 应用入口
│   │   ├── database.py     # 数据库配置
│   │   ├── models.py       # 数据模型
│   │   └── schemas.py      # Pydantic模型
│   ├── requirements.txt    # Python依赖
│   └── start.bat           # 启动脚本
├── start.bat               # 一键启动脚本
└── README.md               # 项目说明
```

## 快速开始

### 方式一：一键启动（推荐）

双击运行项目根目录的 `start.bat`

### 方式二：分别启动

**1. 启动后端**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**2. 访问应用**
- 企业官网：http://localhost:8000
- 管理后台：http://localhost:8000/admin.html

## 默认账号

- 用户名：`admin`
- 密码：`admin123`

## 技术栈

### 前端
- HTML5 + CSS3 + JavaScript
- 响应式设计
- 苹果风格极简UI

### 后端
- **框架**: FastAPI
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **认证**: JWT Token + BCrypt

## API接口

### 认证接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 登录获取Token |
| POST | /api/auth/register | 注册管理员 |
| POST | /token | OAuth2兼容登录 |

### 产品接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/products | 获取产品列表 |
| GET | /api/products/{id} | 获取单个产品 |
| POST | /api/products | 创建产品（需认证） |
| PUT | /api/products/{id} | 更新产品（需认证） |
| DELETE | /api/products/{id} | 删除产品（需认证） |

### 留言接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/messages | 获取留言列表 |
| POST | /api/messages | 提交留言 |
| PUT | /api/messages/{id} | 更新状态（需认证） |
| DELETE | /api/messages/{id} | 删除留言（需认证） |

### 其他接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/stats | 获取统计数据 |
| GET | /api/health | 健康检查 |

## 数据库

SQLite数据库文件：`backend/nanzhu.db`

### 数据表

**products** - 产品表
- id, name, category, price, description, image, specs, created_at

**messages** - 留言表
- id, name, email, phone, content, status, created_at

**admin** - 管理员表
- id, username, hashed_password

## 安全特性

- ✅ JWT Token认证
- ✅ BCrypt密码加密
- ✅ CORS跨域保护
- ✅ 管理员权限控制

## 浏览器支持

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- 移动端浏览器

---

© 2024 长汀县南竹竹制品有限公司

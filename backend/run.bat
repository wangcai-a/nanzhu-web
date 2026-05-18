@echo off
chcp 65001 >nul
echo ========================================
echo   南竹竹制品管理系统 - 完整启动
echo ========================================
echo.

set PYTHON_PATH=D:\miniconda3
set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PYTHON_PATH%\Library\bin;%PATH%

echo [检查环境]
echo.
python --version
if errorlevel 1 (
    echo ✗ Python未找到！
    pause
    exit /b 1
)
echo ✓ Python已就绪
echo.

echo [步骤 1/4] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo.
    echo [步骤 1/4] 安装Python依赖...
    pip install -r requirements.txt
)
echo ✓ 依赖已就绪
echo.

echo [步骤 2/4] 初始化数据库...
python -c "from app.main import init_admin; from app.database import SessionLocal, engine; from app import models; models.Base.metadata.create_all(bind=engine); db = SessionLocal(); init_admin(db); db.close()" 2>nul
echo ✓ 数据库已就绪
echo.

echo [步骤 3/4] 启动前端...
cd ..\frontend\public
start "" index.html
start "" admin.html
cd ..\..\backend
echo ✓ 前端页面已打开
echo.

echo [步骤 4/4] 启动后端服务...
echo.
echo ========================================
echo   服务信息
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 管理后台: admin.html
echo.
echo 默认账号: admin / admin123
echo.
echo ========================================
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
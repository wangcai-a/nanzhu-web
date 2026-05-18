@echo off
chcp 65001 >nul
echo ========================================
echo   等待依赖安装并启动服务
echo ========================================
echo.

set PYTHON_PATH=D:\miniconda3
set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PYTHON_PATH%\Library\bin;%PATH%

echo [1/5] 检查Python环境...
python --version
echo.

echo [2/5] 等待依赖安装完成...
echo 正在检查uvicorn模块...

:check_uvicorn
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo  - 等待中... (请确保之前的依赖安装命令已完成)
    timeout /t 3 /nobreak >nul
    goto check_uvicorn
)

echo   ✓ uvicorn已安装
echo.

echo [3/5] 打开前端页面...
cd ..\frontend\public
start "" index.html
start "" admin.html
echo   ✓ 前端页面已打开
echo.

echo [4/5] 初始化数据库...
cd ..\..\backend
python -c "from app.main import init_admin; from app.database import SessionLocal; db = SessionLocal(); init_admin(db); db.close()"
echo   ✓ 数据库已就绪
echo.

echo [5/5] 启动后端服务...
echo.
echo ========================================
echo   服务已启动！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.
echo 默认账号: admin / admin123
echo.
echo ========================================
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
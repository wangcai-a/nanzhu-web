@echo off
chcp 65001 >nul
echo ========================================
echo   南竹竹制品管理系统 - 后端服务启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [2/3] 安装依赖...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查requirements.txt
    pause
    exit /b 1
)

echo [3/3] 启动服务...
echo.
echo 服务地址: http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
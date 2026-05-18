@echo off
chcp 65001 >nul
echo ========================================
echo   南竹竹制品 - 快速启动指南
echo ========================================
echo.

echo 请选择启动方式：
echo.
echo [1] 启动前端（打开官网）
echo [2] 启动后端（需要Python）
echo [3] 同时启动前端和后端
echo [0] 退出
echo.

set /p choice="请输入选项 (0-3): "

if "%choice%"=="1" goto start_frontend
if "%choice%"=="2" goto start_backend
if "%choice%"=="3" goto start_both
if "%choice%"=="0" goto end

echo 无效选项！
goto end

:start_frontend
echo.
echo ========================================
echo   启动前端服务...
echo ========================================
echo.
cd frontend\public
echo 正在打开企业官网...
start "" index.html
echo.
echo 官网已在浏览器中打开！
echo.
echo 如果需要本地服务器：
echo   请在当前目录运行: python -m http.server 8000
echo.
pause
goto end

:start_backend
echo.
echo ========================================
echo   启动后端服务...
echo ========================================
echo.
cd backend
if exist "requirements.txt" (
    echo [1/3] 检查依赖...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ✗ Python未找到！请先安装Python 3.8+
        pause
        goto end
    )
    echo ✓ Python已找到
    
    echo.
    echo [2/3] 安装依赖...
    pip install -r requirements.txt
    
    echo.
    echo [3/3] 启动FastAPI服务...
    echo.
    echo 后端地址: http://localhost:8000
    echo API文档: http://localhost:8000/docs
    echo.
    echo 按 Ctrl+C 停止服务
    echo.
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
)
goto end

:start_both
echo.
echo ========================================
echo   启动完整服务...
echo ========================================
echo.

echo [步骤 1/2] 启动后端服务...
cd backend
start "后端服务" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [步骤 2/2] 等待2秒后打开前端...
timeout /t 2 /nobreak >nul
cd ..\frontend\public
start "" index.html

echo.
echo ========================================
echo   服务已启动！
echo ========================================
echo.
echo 前端地址: http://localhost:8000
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 管理后台: admin.html
echo.
echo 默认账号: admin / admin123
echo.
pause

:end
echo.
echo 再见！
@echo off
chcp 65001 >nul
echo ========================================
echo   南竹竹制品管理系统 - 完整启动
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤1] 启动后端服务...
start "后端服务" cmd /k "cd /d %~dp0\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [步骤2] 启动前端服务...
start "前端服务" cmd /k "python -m http.server 8080"

echo.
echo ========================================
echo   服务已启动！
echo ========================================
echo.
echo 前端地址: http://localhost:8080
echo 后端地址: http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.
echo 管理后台: http://localhost:8080/admin.html
echo.
echo 默认账号: admin / admin123
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:8080
start http://localhost:8080/admin.html
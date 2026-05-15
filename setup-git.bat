@echo off
chcp 65001 >nul
echo ========================================
echo   Git环境变量设置脚本
echo ========================================
echo.

set GIT_PATH=D:\Git\bin
if not exist "%GIT_PATH%\git.exe (
    set GIT_PATH=D:\Git\cmd
)

echo [1/3] 检查Git安装路径...
if exist "%GIT_PATH%\git.exe" (
    echo   ✓ 找到Git: %GIT_PATH%
) else (
    echo   ✗ 未找到Git，请检查路径是否正确！
    pause
    exit /b 1
)

echo.
echo [2/3] 临时设置当前会话的PATH环境变量...
set PATH=%GIT_PATH%;%PATH%

echo.
echo [3/3] 验证Git是否可用...
git --version
if errorlevel 1 (
    echo   ✗ Git命令仍然无法识别！
    pause
    exit /b 1
) else (
    echo   ✓ Git命令可用！
)

echo.
echo ========================================
echo   设置完成！
echo ========================================
echo.
echo 提示：此设置仅对当前会话有效。
echo.
echo 如需永久设置，请：
echo 1. 右键"此电脑" -^> 属性 -^> 高级系统设置
echo 2. 环境变量 -^> 系统变量 -^> 编辑Path
echo 3. 添加：%GIT_PATH%
echo.
echo 现在可以在当前窗口使用Git命令了！
echo.

cmd /k
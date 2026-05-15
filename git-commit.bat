@echo off
chcp 65001 >nul
echo ========================================
echo   Git提交脚本
echo ========================================
echo.

echo [1/5] 检查Git状态...
git status
if errorlevel 1 (
    echo.
    echo [错误] Git命令无法识别！
    echo 请确保已安装Git并重启终端，或在Git Bash中运行此脚本。
    pause
    exit /b 1
)

echo.
echo [2/5] 添加所有文件...
git add .

echo.
echo [3/5] 检查变更...
git status

echo.
echo [4/5] 创建提交...
git commit -m "Initial commit: 南竹竹制品企业官网和管理系统"
if errorlevel 1 (
    echo.
    echo [提示] 可能没有需要提交的变更，或需要配置Git用户信息。
    echo 如果是第一次使用Git，请运行以下命令：
    echo   git config --global user.name "你的名字"
    echo   git config --global user.email "你的邮箱"
    pause
    exit /b 1
)

echo.
echo [5/5] 完成！
echo.
echo ========================================
echo   提交成功！
echo ========================================
echo.
git log --oneline -1

echo.
echo 提示：如需推送到远程仓库，请添加远程地址后运行 git push
pause
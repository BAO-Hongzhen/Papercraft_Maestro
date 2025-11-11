@echo off
chcp 65001 >nul
echo ════════════════════════════════════════════════════════════
echo          🎲 Syntax Roulette - 语法轮盘 🎲
echo ════════════════════════════════════════════════════════════
echo.
echo 正在检查环境...
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请安装Python 3.8或更高版本
    echo 下载: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 检查依赖
python -c "import gradio" >nul 2>&1
if errorlevel 1 (
    echo 📦 首次运行，正在安装依赖...
    echo 这可能需要几分钟...
    echo.
    pip install -r requirements.txt
    echo.
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        echo 请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已就绪
)
echo.

echo ════════════════════════════════════════════════════════════
echo   正在启动应用...
echo   浏览器会自动打开 http://localhost:7860
echo ════════════════════════════════════════════════════════════
echo.
echo 💡 提示:
echo   - 演示模式: 直接使用，生成预览动画
echo   - ComfyUI模式: 需要先启动ComfyUI服务
echo.
echo 按 Ctrl+C 停止应用
echo ════════════════════════════════════════════════════════════
echo.

REM 启动应用
python main.py

pause

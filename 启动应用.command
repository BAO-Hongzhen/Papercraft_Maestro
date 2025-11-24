#!/bin/bash

# 剪纸大师启动脚本
# 双击此文件即可启动应用

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================="
echo "🎨 剪纸大师 - 启动脚本"
echo "=========================================="

# 激活虚拟环境(如果存在)
if [ -d ".venv" ]; then
    echo "📦 激活虚拟环境..."
    source .venv/bin/activate
fi

# 清理可能存在的旧进程
echo "🧹 清理端口 5001..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true

# 启动应用
echo "🚀 启动 Flask 服务器..."
python3 app.py

# 脚本结束
echo ""
echo "👋 应用已关闭"
echo "=========================================="

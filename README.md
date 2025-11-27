# 剪纸大师 (Papercraft Maestro)

一个基于 AI 技术的中国传统剪纸艺术生成器，使用 Flask 框架构建。

## 🎨 功能特点

- 🖼️ AI 驱动的剪纸图案生成（基于 ComfyUI + Flux 模型）
- 🎯 精确还原 Figma 设计的用户界面
- 🔄 流畅的页面切换动画
- 💾 图片下载功能
- 🎭 占位符模式支持（无需 AI 即可测试界面）

## 🚀 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装 Flask 依赖
pip install -r requirements_flask.txt
```
### 2. 配置ComfyUI

flux1-dev-fp8.safetensors
下载链接：https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors
部署位置：ComfyUI所在位置/models/diffusion_models

clip_l.safetensors
下载链接：https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors
部署位置：ComfyUI所在位置/models/clip

t5xxl_fp8_e4m3fn.safetensors
下载链接：https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors
部署位置：ComfyUI所在位置/models/clip

ae.safetensors
下载链接：https://huggingface.co/lovis93/testllm/blob/ed9cf1af7465cebca4649157f118e331cf2a084f/ae.safetensors
部署位置：ComfyUI所在位置/models/VAE

大觉新春剪纸_V1.safetensors
下载链接：https://www.liblib.art/modelinfo/8714482561d4481d96113ae95e539e28?from=search&versionUuid=a69bec3ddfec4d0bae33c567001fd04f
部署位置：ComfyUI所在位置/models/loras

### 3. 启动应用

```bash
# 方法 1: 直接运行
python app.py

# 方法 2: 使用启动脚本
./start_flask.sh
```

### 4. 访问应用

打开浏览器访问：http://localhost:5001

## 📁 项目结构

```
Syntax_Roulette/
├── app.py                      # Flask 后端主文件
├── templates/
│   └── index.html             # 前端 HTML 模板
├── static/
│   ├── css/
│   │   └── style.css          # 样式文件
│   ├── js/
│   │   └── script.js          # 前端 JavaScript
│   └── images/                # UI 图片资源
├── ComfyUI_api.py             # ComfyUI 接口（可选）
├── Image_Processing.py        # 图像处理模块（可选）
└── requirements_flask.txt     # Python 依赖
```

## 🛠️ 运行模式

### 占位符模式（默认）
当 ComfyUI 模块不可用时，应用会自动进入占位符模式，返回示例图片用于测试界面。

### 真实生成模式
1. 确保 ComfyUI 服务运行在 http://127.0.0.1:8188
2. 确保 `ComfyUI_api.py` 和 `Image_Processing.py` 在项目目录中
3. 重启 Flask 应用

## 📝 API 端点

- `GET /` - 主页面
- `POST /api/generate` - 生成剪纸图案
- `GET /api/health` - 健康检查
- `GET /output/<filename>` - 获取生成的图片
- `GET /api/download/<filename>` - 下载图片

## 🎯 使用说明

1. 在搜索框中输入创意描述（例如：dragon, phoenix, superman）
2. 点击 Generate 按钮
3. 等待生成过程（显示 5 个处理步骤）
4. 查看生成的剪纸作品
5. 可选择：
   - **Try Again**: 返回主页重新生成
   - **Render in Scene**: 场景渲染（待开发）
   - **Download**: 下载生成的图片

## 📚 技术栈

- **后端**: Flask 3.0.0
- **前端**: HTML5 + CSS3 + JavaScript (纯原生)
- **AI 模型**: ComfyUI + Flux
- **图像处理**: Pillow

## 🔧 开发说明

详细的项目结构和开发指南请参考：
- [Flask 项目文档](README_FLASK.md)
- [项目结构说明](FLASK_PROJECT_STRUCTURE.md)

## 📄 许可证

本项目仅供学习和研究使用。

## 👥 贡献者

SD5913 课程项目 - Group Project: Master of China Cut

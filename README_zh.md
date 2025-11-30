# 剪纸大师 (Papercraft Maestro)

[English](README.md) | [中文](README_zh.md)

[](https://www.python.org/downloads/)
[](https://streamlit.io/)
[](https://github.com/comfyanonymous/ComfyUI)

**Papercraft Maestro** 是一个基于 AI 技术的中国传统剪纸艺术生成平台。本项目采用 **Streamlit** 构建交互式前端，结合 **Flux 图像生成模型** 与传统的图像处理算法，能够将用户简单的创意描述瞬间转化为精美的红色剪纸图案，并提供多种场景的模拟展示。

本项目是 **SD5913 Group Project** 的成果。

-----

## 效果展示

![](readmedoc/Papercraft%20Maestro%20-%20Google%20Chrome.gif)

-----

## 主要功能

  * **AI 智能生成**: 利用 ComfyUI 后端和 Flux 模型生成高质量剪纸图像。
  * **全版本自动连接 (Auto-Connect)**:
      * **零配置启动**: 无论您使用的是 **ComfyUI 标准版 (Web)**、**ComfyUI Desktop (桌面版)** 还是 **ComfyUI Portable (便携版)**，系统都能自动识别并连接。
      * **智能扫描**: 自动扫描本地环境中的常用端口（如 8188, 8000, 8189, 3000 等），无需手动修改配置文件。
  * **智能提示词系统**: **无需学习复杂的 Prompt！** 我们已内置经过精心调试的风格化提示词。用户只需输入想要生成的**主体**（例如："a rabbit" 或 "a dragon"），系统会自动补充“中国传统剪纸”、“红色纸张”、“复杂纹样”等风格描述。
  * **自动工艺处理**: 内置图像处理管线（去饱和、高对比度增强、智能去底、中国红着色），模拟真实剪纸的视觉效果。
  * **场景模拟 (Mockup)**: 支持将生成的剪纸一键合成到窗花、墙壁、门饰等真实场景中，预览实际装饰效果。
  * **便捷下载**: 支持生成的高清剪纸原图及场景合成图的下载。

## 核心技术解析

本项目通过两个核心模块实现了从 AI 生成到最终视觉呈现的自动化流程：

### 1\. 图像后期处理 (Image\_Processing.py)

该模块利用 **Pillow (PIL)** 和 **NumPy** 对 AI 生成的初始图像进行一系列计算机视觉处理，以模拟真实的剪纸质感：

  * **去饱和与对比度增强**: 使用 `ImageEnhance` 对生成的图像进行去色处理，并大幅提升对比度，确保剪纸纹理的清晰度。
  * **智能去底 (Alpha Masking)**: 将图像转换为 NumPy 数组，通过像素级阈值（Thresholding）检测白色背景区域，并将其 Alpha 通道设为透明，实现高精度的自动抠图。
  * **矢量化着色**: 实现了 `convert_to_red` 函数，将非透明的像素点统一映射为标准的“中国红”色值，同时保留原有的透明度层级，使边缘过渡自然。
  * **场景合成**: 使用 **Lanczos 重采样**算法高质量缩放剪纸图像，根据预设的坐标系统将剪纸精确贴合到窗户、墙壁或门等背景图中。

### 2\. ComfyUI 自动化接口 (ComfyUI\_api.py)

该模块封装了与 ComfyUI 后端的通信逻辑，实现了零配置的连接体验：

  * **端口自动发现机制**: 内置了 `find_comfyui_address` 函数，利用 Python 的 `socket` 库快速扫描本地常用端口（包括 Web 版默认的 8188、桌面版的 8000 以及其他备用端口）。一旦 TCP 连接建立，立即发送 HTTP 请求验证 `/system_stats` 端点，确保服务可用。
  * **动态工作流注入**: 系统加载 JSON 格式的工作流模板，在内存中动态修改 `CLIPTextEncodeFlux` 节点的输入参数，将用户的提示词与内置风格词（Prompt Template）拼接。
  * **任务队列管理**: 通过 API 将生成任务推送到 ComfyUI 队列，并实时轮询生成状态，直到获取最终生成的图像数据流。

## 硬件要求

由于本项目使用了 Flux.1-dev (FP8) 模型，请确保您的硬件满足以下要求：

  * **显卡 (GPU)**: NVIDIA 显卡，显存 (VRAM) ≥ 8GB (推荐 12GB 以上以获得更快速度)。
  * **内存 (RAM)**: 16GB 或更高。
  * **硬盘空间**: 预留至少 20GB 空间用于存放模型文件。

## 快速开始

### 1\. 环境准备

确保你的电脑上安装了 Python 3.8+ 以及 Git。

克隆项目到本地：

```bash
git clone https://github.com/BAO-Hongzhen/Papercraft_Maestro.git
cd Papercraft_Maestro
```

### 2\. 安装 Python 依赖

建议使用虚拟环境：

```bash
# 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3\. 配置 ComfyUI (关键步骤)

本项目依赖本地运行的 ComfyUI 服务。请确保你已安装 ComfyUI 并下载了以下必要的模型文件，放置在 ComfyUI 对应的目录下：

| 模型类型 | 文件名 | 下载链接 (示例) | 存放路径 (ComfyUI根目录起) |
| :--- | :--- | :--- | :--- |
| **UNET (Flux)** | `flux1-dev-fp8.safetensors` | [HuggingFace](https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors) | `models/diffusion_models/` |
| **CLIP** | `clip_l.safetensors` | [HuggingFace](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors) | `models/clip/` |
| **CLIP (T5)** | `t5xxl_fp8_e4m3fn.safetensors` | [HuggingFace](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors) | `models/clip/` |
| **VAE** | `ae.safetensors` | [HuggingFace](https://www.google.com/search?q=https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/ae.safetensors) | `models/vae/` |
| **LoRA** | `大觉新春剪纸_V1.safetensors` | [Google Drive](https://drive.google.com/file/d/1eXedHyMzIk0YYvr7jLChjj7yMlRA_dUA/view?usp=sharing) | `models/loras/` |

> **注意**: 如果你的模型文件名与上述不同，请修改 `ComfyUI_Workflow/paper_cut.json` 文件中对应的节点名称。

### 4\. 启动服务

**第一步：启动 ComfyUI**
无论是 Web 版、桌面版还是便携版，只要启动服务即可。无需关心具体的端口号。

**第二步：启动剪纸大师应用**

在项目根目录下运行：

```bash
streamlit run main.py
```

启动成功后，浏览器会自动打开应用的访问地址（通常为 `http://localhost:8501`）。终端会显示类似 `✅ 发现 ComfyUI 服务于: http://127.0.0.1:xxxx` 的成功连接信息。

## 使用指南

1.  **输入创意**: 在输入框中简单描述你想要生成的物体（建议使用英文，例如 `tiger`、`flower`、`superman`）。
      * *提示：你不需要输入“red paper cut style”等词汇，系统会自动添加。*
2.  **生成 (Generate)**: 点击 **GENERATE** 按钮。
      * **首次生成**: 大约需要 **70-90 秒**（需要加载模型到显存）。
      * **后续生成**: 大约需要 **40-60 秒**（取决于显卡性能）。
3.  **结果预览**: 生成完成后，你将看到处理好的红色剪纸图案。你可以点击 **Download PNG** 下载原图。
4.  **场景渲染 (Render in Scene)**:
      * 在右侧选择想要模拟的场景（Window, Wall, Door）。
      * 点击 **RENDER IN SCENE** 按钮。
      * 预览剪纸贴在真实场景中的效果并下载。

## 项目结构

```
Papercraft_Maestro/
├── main.py                     # Streamlit 应用主入口
├── comfy_api.py                # ComfyUI API 适配器（含多版本端口自动扫描逻辑）
├── Image_Processing.py         # 图像后期处理算法 (去底、上色、合成)
├── requirements.txt            # 项目依赖列表
├── comfyui_workflow/
│   └── paper_cut.json          # ComfyUI 工作流配置文件
├── ui_assets/                  # 静态资源
│   ├── background/             # streamlit背景图
│   └── prototype_images/       # 场景原型图（Window, Wall, Door等）
├── image_raw/                  # 存放生成的原始剪纸图片
├── image_processed/            # 存放处理后的图片
├── image_rendered/             # 存放场景合成后的图片
└── previous_work/              # 在此之前的测试与尝试
```

## 贡献者

感谢以下成员对本项目做出的贡献：

<a href="https://github.com/BAO-Hongzhen/Papercraft_Maestro/graphs/contributors">
 <img src="https://contrib.rocks/image?repo=BAO-Hongzhen/Papercraft_Maestro" alt="contrib.rocks image" />
</a>

## 许可证

本项目仅供学习与研究使用。所使用的 AI 模型及 LoRA 遵循其各自的许可协议。

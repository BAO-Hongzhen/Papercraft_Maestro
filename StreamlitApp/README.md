# 剪纸大师 (Streamlit 版)

这是一个基于 Streamlit 的传统剪纸生成器应用。它复刻了原项目的核心功能，并采用了全新的中国传统风格 UI。

## 功能特点

*   **AI 剪纸生成**: 连接 ComfyUI (Flux 模型) 生成精美的剪纸图案。
*   **自动图像处理**: 自动进行去底、上色（中国红）、增强对比度等处理。
*   **场景模拟**: 可将生成的剪纸合成到窗花或墙壁场景中预览。
*   **传统风格 UI**: 优美典雅的界面设计。

## 运行方法

1.  确保已安装 Python 依赖 (在项目根目录下运行):
    ```bash
    pip install streamlit requests pillow numpy
    ```

2.  确保 ComfyUI 正在运行:
    *   地址: `127.0.0.1:8188`
    *   确保已加载 Flux 模型和相关节点。

3.  启动应用:
    ```bash
    streamlit run StreamlitApp/app.py
    ```

## 注意事项

*   本应用依赖本地 ComfyUI 服务，请确保服务可用。
*   生成的图片将保存在内存中，可直接下载。

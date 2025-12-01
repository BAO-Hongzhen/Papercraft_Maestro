# Papercraft Maestro

[English](README.md) | [中文](README_zh.md)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B)](https://streamlit.io/)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Backend-4285F4)](https://github.com/comfyanonymous/ComfyUI)

**Papercraft Maestro** is an AI-powered platform for generating traditional Chinese paper cutting art. Built with **Streamlit** for an interactive frontend, it combines the **Flux image generation model** with traditional image processing algorithms to instantly transform simple creative descriptions into exquisite red paper cut patterns, offering various scene simulations for preview.

This project is a result of the **SD5913 Group Project**.

-----

## Demo

![](readmedoc/Papercraft%20Maestro%20-%20Google%20Chrome.gif)

-----

## Key Features

  * **AI Smart Generation**: Utilizes ComfyUI backend and Flux model to generate high-quality paper cut images.
  * **Auto-Connect**:
      * **Zero Configuration**: Whether you are using **ComfyUI Standard (Web)**, **ComfyUI Desktop**, or **ComfyUI Portable**, the system automatically identifies and connects.
      * **Smart Scanning**: Automatically scans common ports in the local environment (e.g., 8188, 8000, 8189, 3000, etc.), eliminating the need for manual configuration files.
  * **Smart Prompt System**: **No need to learn complex Prompts!** We have built-in carefully tuned stylized prompts. Users only need to input the **subject** they want to generate (e.g., "a rabbit" or "a dragon"), and the system automatically fills it into the preset style template:
    * **Prefix**: "A vibrant red Chinese paper"
    * **User Input**: [Subject]
    * **Suffix**: "complex Chinese patterns, stand proudly among the swirling clouds and stylized clouds. The background is pure white, emphasizing a bold traditional design"
    By automatically concatenating these, the system ensures that every generated image maintains a unified and authentic traditional Chinese paper cut style.
  * **Automatic Craft Processing**: Built-in image processing pipeline (desaturation, high contrast enhancement, smart background removal, Chinese red coloring) to simulate the visual effect of real paper cuts.
  * **Scene Simulation (Mockup)**: Supports one-click synthesis of generated paper cuts into real scenes like windows, walls, and door decorations to preview the actual decorative effect.
  * **Easy Download**: Supports downloading high-definition original paper cut images and scene synthesis images.

## Core Technology Analysis

This project implements an automated process from AI generation to final visual presentation through two core modules:

### 1. Image Post-Processing (Image_Processing.py)

This module uses **Pillow (PIL)** and **NumPy** to perform a series of computer vision processing on the initial AI-generated images to simulate real paper cut texture:

  * **Desaturation & Contrast Enhancement**: Uses `ImageEnhance` to desaturate the generated image and significantly increase contrast to ensure the clarity of paper cut textures.
  * **Smart Background Removal (Alpha Masking)**: Converts the image to a NumPy array, detects white background areas via pixel-level thresholding, and sets their Alpha channel to transparent, achieving high-precision automatic matting.
  * **Vectorized Coloring**: Implements the `convert_to_red` function to map non-transparent pixels to standard "Chinese Red" color values while preserving original transparency levels for natural edge transitions.
  * **Scene Synthesis**: Uses **Lanczos resampling** algorithm to high-quality scale paper cut images and accurately fit them onto background images like windows, walls, or doors based on a preset coordinate system.

### 2. ComfyUI Automation Interface (comfy_api.py)

This module encapsulates communication logic with the ComfyUI backend, achieving a zero-configuration connection experience:

  * **Port Auto-Discovery Mechanism**: Built-in `find_comfyui_address` function uses Python's `socket` library to quickly scan local common ports (including Web default 8188, Desktop 8000, and other backup ports). Once a TCP connection is established, it immediately sends an HTTP request to verify the `/system_stats` endpoint to ensure service availability.
  * **Dynamic Workflow Injection**: The system loads the JSON format workflow template and dynamically modifies the input parameters of the `CLIPTextEncodeFlux` node in memory, concatenating user prompts with built-in style words (Prompt Template).
  * **Task Queue Management**: Pushes generation tasks to the ComfyUI queue via API and polls generation status in real-time until the final generated image data stream is obtained.

## Hardware Requirements

Since this project uses the Flux.1-dev (FP8) model, please ensure your hardware meets the following requirements:

  * **GPU**: NVIDIA Graphics Card, VRAM ≥ 8GB (12GB+ recommended for faster speed).
  * **RAM**: 16GB or higher.
  * **Disk Space**: Reserve at least 20GB of space for storing model files.

## Quick Start

### 1. Environment Preparation

Ensure Python 3.8+ and Git are installed on your computer.

Clone the project locally:

```bash
git clone https://github.com/BAO-Hongzhen/Papercraft_Maestro.git
cd Papercraft_Maestro
```

### 2. Install Python Dependencies

Using a virtual environment is recommended:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure ComfyUI (Critical Step)

This project relies on a locally running ComfyUI service. Please ensure you have installed ComfyUI and downloaded the following necessary model files, placing them in the corresponding ComfyUI directories:

| Model Type | Filename | Download Link | Path (from ComfyUI root) |
| :--- | :--- | :--- | :--- |
| **UNET (Flux)** | `flux1-dev-fp8.safetensors` | [HuggingFace](https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors) | `models/diffusion_models/` |
| **CLIP** | `clip_l.safetensors` | [HuggingFace](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors) | `models/clip/` |
| **CLIP (T5)** | `t5xxl_fp8_e4m3fn.safetensors` | [HuggingFace](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors) | `models/clip/` |
| **VAE** | `ae.safetensors` | [HuggingFace](https://www.google.com/search?q=https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/ae.safetensors) | `models/vae/` |
| **LoRA** | `大觉新春剪纸_V1.safetensors` | [Google Drive](https://drive.google.com/file/d/1eXedHyMzIk0YYvr7jLChjj7yMlRA_dUA/view?usp=sharing) | `models/loras/` |

> **Note**: If your model filenames differ from the above, please modify the corresponding node names in the `ComfyUI_Workflow/paper_cut.json` file.

### 4. Start Service

**Step 1: Start ComfyUI**
Whether it's the Web version, Desktop version, or Portable version, just start the service. No need to worry about specific port numbers.

**Step 2: Start Papercraft Maestro App**

Run in the project root directory:

```bash
streamlit run main.py
```

After successful startup, the browser will automatically open the app access address (usually `http://localhost:8501`). The terminal will display a success connection message like `✅ Found ComfyUI service at: http://127.0.0.1:xxxx`.

## User Guide

1.  **Input Idea**: Simply describe the object you want to generate in the input box (English recommended, e.g., `tiger`, `flower`, `superman`).
      * *Tip: You don't need to input words like "red paper cut style", the system adds them automatically.*
2.  **Generate**: Click the **GENERATE** button.
      * **First Generation**: Takes about **70-90 seconds** (needs to load model into VRAM).
      * **Subsequent Generations**: Takes about **40-60 seconds** (depending on GPU performance).
3.  **Result Preview**: After generation is complete, you will see the processed red paper cut pattern. You can click **Download PNG** to download the original image.
4.  **Render in Scene**:
      * Select the scene you want to simulate on the right (Window, Wall, Door).
      * Click the **RENDER IN SCENE** button.
      * Preview the effect of the paper cut pasted in the real scene and download.

## Project Structure

```
Papercraft_Maestro/
├── main.py                     # Streamlit App Entry Point
├── comfy_api.py                # ComfyUI API Adapter (with multi-version port auto-scan logic)
├── Image_Processing.py         # Image Post-Processing Algorithms (Background Removal, Coloring, Synthesis)
├── requirements.txt            # Project Dependencies List
├── comfyui_workflow/
│   └── paper_cut.json          # ComfyUI Workflow Configuration File
├── ui_assets/                  # Static Assets
│   ├── background/             # Streamlit Background Images
│   └── prototype_images/       # Scene Prototype Images (Window, Wall, Door, etc.)
├── image_raw/                  # Stores Generated Raw Paper Cut Images
├── image_processed/            # Stores Processed Images
├── image_rendered/             # Stores Scene Synthesized Images
└── previous_work/              # Previous Tests and Attempts
```

## Contributors

Thanks to the following members for their contributions to this project:

<a href="https://github.com/BAO-Hongzhen/Papercraft_Maestro/graphs/contributors">
 <img src="https://contrib.rocks/image?repo=BAO-Hongzhen/Papercraft_Maestro" alt="contrib.rocks image" />
</a>

## License

This project is for learning and research purposes only. The AI models and LoRA used follow their respective license agreements.

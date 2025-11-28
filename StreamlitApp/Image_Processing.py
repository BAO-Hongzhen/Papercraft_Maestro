"""
图片处理脚本 - 去饱和、增强对比度、抠白色、转红色
"""

import os
from PIL import Image, ImageEnhance
import numpy as np
import time


def desaturate_image(image: Image.Image) -> Image.Image:
    """将图片饱和度设为0（转为灰度，但保留RGB通道）"""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(0.0)


def increase_contrast(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """增强图片对比度"""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def remove_white_background(image: Image.Image, threshold: int = 240) -> Image.Image:
    """移除白色背景，将白色部分变为透明"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    img_array = np.array(image)
    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]
    
    # 创建白色掩码：所有RGB通道都大于阈值的像素
    white_mask = (r > threshold) & (g > threshold) & (b > threshold)
    
    # 将白色像素的alpha通道设为0（完全透明）
    img_array[white_mask, 3] = 0
    
    return Image.fromarray(img_array, 'RGBA')


def convert_to_red(image: Image.Image, color: tuple = (255, 0, 0), opacity: float = 1.0) -> Image.Image:
    """
    将图片所有像素转换为指定颜色，保留alpha通道并设置透明度
    
    Args:
        image: 输入图片
        color: RGB颜色元组，默认为(255, 0, 0) = 纯红色
        opacity: 透明度，0.0-1.0，默认为1.0 (完全不透明)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    img_array = np.array(image)
    a = img_array[:, :, 3]
    
    # 将所有非透明像素设为指定颜色
    non_transparent = a > 0
    
    img_array[:, :, 0] = np.where(non_transparent, color[0], 0)  # R
    img_array[:, :, 1] = np.where(non_transparent, color[1], 0)  # G
    img_array[:, :, 2] = np.where(non_transparent, color[2], 0)  # B
    
    # 调整透明度：将原alpha值乘以opacity
    img_array[:, :, 3] = np.where(non_transparent, (a * opacity).astype(np.uint8), 0)
    
    return Image.fromarray(img_array, 'RGBA')


def process_image_for_papercut(image_path: str) -> str:
    """
    完整的剪纸图像处理流程
    
    Args:
        image_path: 原始图片路径
        
    Returns:
        str: 处理后的图片路径
    """
    try:
        # 加载图片
        image = Image.open(image_path)
        
        # 步骤1: 去饱和
        image = desaturate_image(image)
        
        # 步骤2: 增强对比度 (factor=3.0)
        image = increase_contrast(image, factor=3.0)
        
        # 步骤3: 抠除白色背景 (threshold=230)
        image = remove_white_background(image, threshold=230)
        
        # 步骤4: 转换为红色
        image = convert_to_red(image)
        
        # 确定输出路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "output")
        if not os.path.exists(output_dir):
            # 尝试在当前目录下找 output
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
            
        timestamp = int(time.time())
        output_filename = f"papercut_{timestamp}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        image.save(output_path, 'PNG')
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def render_on_window(papercut_path: str, scene_path: str, output_path: str) -> bool:
    """
    渲染到窗户场景
    """
    try:
        papercut = Image.open(papercut_path).convert('RGBA')
        scene = Image.open(scene_path).convert('RGB')
        
        # 准备剪纸图片用于窗户场景合成
        # 1. 调整尺寸为 1736x1736
        papercut = papercut.resize((1736, 1736), Image.Resampling.LANCZOS)
        # 2. 应用特定颜色 (#980015) 和透明度 (75%)
        processed_papercut = convert_to_red(papercut, color=(152, 0, 21), opacity=0.75)
        
        # Window coordinates
        x, y = 2890, 137
        
        scene_rgba = scene.convert('RGBA')
        scene_rgba.paste(processed_papercut, (x, y), processed_papercut)
        
        final_image = scene_rgba.convert('RGB')
        final_image.save(output_path)
        return True
    except Exception as e:
        print(f"Error rendering on window: {e}")
        return False


def render_on_wall(papercut_path: str, scene_path: str, output_path: str) -> bool:
    """
    渲染到墙壁场景 (暂未实现)
    """
    print("Render on wall not implemented yet.")
    return False


def render_on_door(papercut_path: str, scene_path: str, output_path: str) -> bool:
    """
    渲染到门场景 (暂未实现)
    """
    print("Render on door not implemented yet.")
    return False


def main():
    # 读取图片
    input_path = 'examples/input/d411ec41e95fa45c38c5ab852495a5b1.png'
    output_path = 'examples/output/d411ec41e95fa45c38c5ab852495a5b1.png'
    
    print("📂 正在处理图片...")
    image = Image.open(input_path)
    print(f"✅ 图片已加载: {image.size[0]}x{image.size[1]}")
    
    # 步骤1: 饱和度设为0
    print("🎨 步骤1: 饱和度设为0...")
    image = desaturate_image(image)
    
    # 步骤2: 对比度拉满
    print("🎨 步骤2: 对比度拉满...")
    image = increase_contrast(image, factor=10.0)
    
    # 步骤3: 抠除白色
    print("✂️  步骤3: 抠除白色背景...")
    image = remove_white_background(image, threshold=200)
    
    # 步骤4: 转为红色
    print("🔴 步骤4: 转换为红色...")
    image = convert_to_red(image)
    
    # 创建输出目录（如果不存在）
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存结果
    image.save(output_path, 'PNG')
    print(f"✅ 处理完成！输出位置: {output_path}")


if __name__ == "__main__":
    main()


"""
图片处理脚本 - 去饱和、增强对比度、抠白色、转红色
"""

import os
from PIL import Image, ImageEnhance
import numpy as np


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


def convert_to_red(image: Image.Image) -> Image.Image:
    """将图片所有像素转换为纯红色，保留alpha通道"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    img_array = np.array(image)
    a = img_array[:, :, 3]
    
    # 将所有非透明像素设为纯红色（255, 0, 0）
    non_transparent = a > 0
    
    img_array[:, :, 0] = np.where(non_transparent, 255, 0)
    img_array[:, :, 1] = 0
    img_array[:, :, 2] = 0
    
    return Image.fromarray(img_array, 'RGBA')


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


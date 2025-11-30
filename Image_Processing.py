"""
Image Processing Script - Desaturate, Increase Contrast, Remove White Background, Convert to Red
"""

import os
from PIL import Image, ImageEnhance
import numpy as np
import time


def desaturate_image(image: Image.Image) -> Image.Image:
    """Set image saturation to 0 (convert to grayscale, but keep RGB channels)"""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(0.0)


def increase_contrast(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """Increase image contrast"""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def remove_white_background(image: Image.Image, threshold: int = 240) -> Image.Image:
    """Remove white background, make white parts transparent"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    img_array = np.array(image)
    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]
    
    # Create white mask: pixels where all RGB channels are greater than threshold
    white_mask = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Set alpha channel of white pixels to 0 (fully transparent)
    img_array[white_mask, 3] = 0
    
    return Image.fromarray(img_array, 'RGBA')


def convert_to_red(image: Image.Image, color: tuple = (255, 0, 0), opacity: float = 1.0) -> Image.Image:
    """
    Convert all pixels of the image to the specified color, preserving the alpha channel and setting opacity
    
    Args:
        image: Input image
        color: RGB color tuple, default is (255, 0, 0) = Pure Red
        opacity: Opacity, 0.0-1.0, default is 1.0 (fully opaque)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    img_array = np.array(image)
    a = img_array[:, :, 3]
    
    # Set all non-transparent pixels to the specified color
    non_transparent = a > 0
    
    img_array[:, :, 0] = np.where(non_transparent, color[0], 0)  # R
    img_array[:, :, 1] = np.where(non_transparent, color[1], 0)  # G
    img_array[:, :, 2] = np.where(non_transparent, color[2], 0)  # B
    
    # Adjust opacity: multiply original alpha value by opacity
    img_array[:, :, 3] = np.where(non_transparent, (a * opacity).astype(np.uint8), 0)
    
    return Image.fromarray(img_array, 'RGBA')


def apply_color_effect(base_img: Image.Image, color: tuple) -> Image.Image:
    """
    Simulate layer blending mode 'Color': 
    Use Luminance/Value of base_img
    Use Hue and Saturation of color
    """
    # Ensure base_img is in RGB mode for conversion
    if base_img.mode != 'RGB':
        base_img = base_img.convert('RGB')
        
    # 1. Convert base to HSV to get V
    base_hsv = base_img.convert('HSV')
    base_np = np.array(base_hsv)
    v_channel = base_np[:, :, 2]
    
    # 2. Create solid color image and convert to HSV to get H, S
    color_layer = Image.new('RGB', base_img.size, color)
    color_hsv = color_layer.convert('HSV')
    color_np = np.array(color_hsv)
    
    h_channel = color_np[:, :, 0]
    s_channel = color_np[:, :, 1]
    
    # 3. Combine new HSV image
    new_hsv_np = np.dstack((h_channel, s_channel, v_channel))
    new_hsv_img = Image.fromarray(new_hsv_np, 'HSV')
    
    return new_hsv_img.convert('RGB')


def process_image_for_papercut(image_path: str) -> str:
    """
    Complete papercut image processing pipeline
    
    Args:
        image_path: Original image path
        
    Returns:
        str: Processed image path
    """
    try:
        # Load image
        image = Image.open(image_path)
        
        # Step 1: Desaturate
        image = desaturate_image(image)
        
        # Step 2: Increase contrast (factor=3.0)
        image = increase_contrast(image, factor=3.0)
        
        # Step 3: Remove white background (threshold=230)
        image = remove_white_background(image, threshold=230)
        
        # Step 4: Convert to red
        image = convert_to_red(image)
        
        # Determine output path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "image_processed")
        if not os.path.exists(output_dir):
            # Try to find output in current directory
            output_dir = os.path.join(os.getcwd(), "image_processed")
            os.makedirs(output_dir, exist_ok=True)
            
        timestamp = int(time.time())
        output_filename = f"papercut_{timestamp}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        image.save(output_path, 'PNG')
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def render_on_window(papercut_input, scene_input, output_path=None) -> Image.Image:
    """
    Render to window scene
    Args:
        papercut_input: Papercut image path (str) or PIL.Image object
        scene_input: Scene image path (str) or PIL.Image object
        output_path: (Optional) Output path, save if provided
    Returns:
        PIL.Image: Composited image
    """
    try:
        # Load Papercut
        if isinstance(papercut_input, str):
            papercut = Image.open(papercut_input).convert('RGBA')
        else:
            papercut = papercut_input.convert('RGBA')

        # Load Scene
        if isinstance(scene_input, str):
            scene = Image.open(scene_input).convert('RGB')
        else:
            scene = scene_input.convert('RGB')
        
        # Prepare papercut image for window scene composition
        # 1. Resize to 1736x1736 (Base_Window.jpg 5760x3840)
        papercut = papercut.resize((1736, 1736), Image.Resampling.LANCZOS)
        # 2. Apply specific color (#980015) and opacity (75%)
        processed_papercut = convert_to_red(papercut, color=(152, 0, 21), opacity=0.75)
        
        # Window coordinates
        x, y = 2890, 137
        
        scene_rgba = scene.convert('RGBA')
        scene_rgba.paste(processed_papercut, (x, y), processed_papercut)
        
        final_image = scene_rgba.convert('RGB')
        
        if output_path:
            final_image.save(output_path)
            
        return final_image
    except Exception as e:
        print(f"Error rendering on window: {e}")
        return None


def render_on_wall(papercut_input, scene_input, output_path=None) -> Image.Image:
    """
    Render to wall scene
    """
    try:
        # Load Papercut
        if isinstance(papercut_input, str):
            papercut = Image.open(papercut_input).convert('RGBA')
        else:
            papercut = papercut_input.convert('RGBA')

        # Load Scene
        if isinstance(scene_input, str):
            scene = Image.open(scene_input).convert('RGB')
        else:
            scene = scene_input.convert('RGB')
            
        # Base_wall.jpeg (768x768)
        # Scale papercut image to 49.48% of background height
        target_height = int(scene.height * 0.4948)
        aspect_ratio = papercut.width / papercut.height
        target_width = int(target_height * aspect_ratio)
        
        papercut = papercut.resize((target_width, target_height), Image.Resampling.LANCZOS)
        processed_papercut = convert_to_red(papercut, color=(152, 0, 21), opacity=0.9) 
        
        # Image center point at Height 37.3%, Width 66.67%
        center_x = int(scene.width * 0.6667)
        center_y = int(scene.height * 0.373)
        
        x = center_x - target_width // 2
        y = center_y - target_height // 2
        
        scene_rgba = scene.convert('RGBA')
        scene_rgba.paste(processed_papercut, (x, y), processed_papercut)
        
        final_image = scene_rgba.convert('RGB')
        
        if output_path:
            final_image.save(output_path)
            
        return final_image
    except Exception as e:
        print(f"Error rendering on wall: {e}")
        return None


def render_on_door(papercut_input, scene_input, output_path=None) -> Image.Image:
    """
    Render to door scene
    """
    try:
        # Load Papercut
        if isinstance(papercut_input, str):
            papercut = Image.open(papercut_input).convert('RGBA')
        else:
            papercut = papercut_input.convert('RGBA')

        # Load Scene
        if isinstance(scene_input, str):
            scene = Image.open(scene_input).convert('RGB')
        else:
            scene = scene_input.convert('RGB')
            
        # Base_door.jpg (799x799)
        # Scale papercut image to 18% of background height
        target_height = int(scene.height * 0.18)
        aspect_ratio = papercut.width / papercut.height
        target_width = int(target_height * aspect_ratio)
        
        papercut = papercut.resize((target_width, target_height), Image.Resampling.LANCZOS)
        processed_papercut = convert_to_red(papercut, color=(152, 0, 21), opacity=0.9)
        
        # Image center point at Height 36.3%, Width 62.45%
        center_x = int(scene.width * 0.6245)
        center_y = int(scene.height * 0.363)
        
        x = center_x - target_width // 2
        y = center_y - target_height // 2
        
        scene_rgba = scene.convert('RGBA')
        scene_rgba.paste(processed_papercut, (x, y), processed_papercut)
        
        final_image = scene_rgba.convert('RGB')
        
        if output_path:
            final_image.save(output_path)
            
        return final_image
    except Exception as e:
        print(f"Error rendering on door: {e}")
        return None


def render_on_package(papercut_input, scene_input, output_path=None) -> Image.Image:
    """
    Render to package scene
    """
    try:
        # Load Papercut
        if isinstance(papercut_input, str):
            papercut = Image.open(papercut_input).convert('RGBA')
        else:
            papercut = papercut_input.convert('RGBA')

        # Load Scene
        if isinstance(scene_input, str):
            scene = Image.open(scene_input).convert('RGB')
        else:
            scene = scene_input.convert('RGB')
            
        # Base_package.jpg (4032x2688)
        # Scale papercut image size to about 25% of background image (width)
        target_width = int(scene.width * 0.25)
        aspect_ratio = papercut.height / papercut.width
        target_height = int(target_width * aspect_ratio)
        
        papercut = papercut.resize((target_width, target_height), Image.Resampling.LANCZOS)
        # Simulate printing texture: slightly reduce opacity
        processed_papercut = convert_to_red(papercut, color=(152, 0, 21), opacity=0.85)
        
        # Rotate 33 degrees (counter-clockwise)
        processed_papercut = processed_papercut.rotate(33, expand=True, resample=Image.Resampling.BICUBIC)
        
        # Image center point position at Height 48.33%, Width 48%
        center_x = int(scene.width * 0.48)
        center_y = int(scene.height * 0.4833)
        
        # Size changes after rotation, need to re-acquire size
        new_width, new_height = processed_papercut.size
        
        x = center_x - new_width // 2
        y = center_y - new_height // 2
        
        scene_rgba = scene.convert('RGBA')
        scene_rgba.paste(processed_papercut, (x, y), processed_papercut)
        
        final_image = scene_rgba.convert('RGB')
        
        if output_path:
            final_image.save(output_path)
            
        return final_image
    except Exception as e:
        print(f"Error rendering on package: {e}")
        return None


def main():
    # Read image
    input_path = 'examples/input/d411ec41e95fa45c38c5ab852495a5b1.png'
    output_path = 'examples/output/d411ec41e95fa45c38c5ab852495a5b1.png'
    
    print("📂 Processing image...")
    image = Image.open(input_path)
    print(f"✅ Image loaded: {image.size[0]}x{image.size[1]}")
    
    # Step 1: Setting saturation to 0
    print("🎨 Step 1: Setting saturation to 0...")
    image = desaturate_image(image)
    
    # Step 2: Maximizing contrast
    print("🎨 Step 2: Maximizing contrast...")
    image = increase_contrast(image, factor=10.0)
    
    # Step 3: Removing white background
    print("✂️  Step 3: Removing white background...")
    image = remove_white_background(image, threshold=200)
    
    # Step 4: Converting to red
    print("🔴 Step 4: Converting to red...")
    image = convert_to_red(image)
    
    # Create output directory (if not exists)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save result
    image.save(output_path, 'PNG')
    print(f"✅ Processing complete! Output location: {output_path}")


if __name__ == "__main__":
    main()


import streamlit as st
import os
import time
import sys
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ComfyUI_api import FluxComfyUI_Generator
    from Image_Processing import desaturate_image, increase_contrast, remove_white_background, convert_to_red
except ImportError:
    pass # Will handle gracefully later

# Page Configuration
st.set_page_config(
    page_title="剪纸大师 - 传统艺术生成器",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Functions ---

def img_to_base64(img):
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    return base64.b64encode(buff.getvalue()).decode()

def create_seamless_pattern():
    """Create a distinct tiled background with placeholder images"""
    # Create a tile with 4 distinct "images" to simulate a collage
    w, h = 256, 256  # Reduced size for better performance
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Helper to draw a "framed picture"
    def draw_frame(x, y, color, shape_type):
        # Frame
        draw.rectangle([x, y, x+118, y+118], outline='#8B0000', width=3)
        # Content
        cx, cy = x + 59, y + 59
        if shape_type == 'circle':
            draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=color)
        elif shape_type == 'square':
            draw.rectangle([cx-40, cy-40, cx+40, cy+40], fill=color)
        elif shape_type == 'diamond':
            draw.polygon([(cx, cy-45), (cx+45, cy), (cx, cy+45), (cx-45, cy)], fill=color)
        elif shape_type == 'flower':
            for i in range(0, 360, 45):
                import math
                rad = math.radians(i)
                ox = cx + 25 * math.cos(rad)
                oy = cy + 25 * math.sin(rad)
                draw.ellipse([ox-15, oy-15, ox+15, oy+15], fill=color)
    
    # Draw 4 quadrants
    draw_frame(5, 5, '#980015', 'circle')      # Top-Left: Red Circle
    draw_frame(133, 5, '#DAA520', 'square')     # Top-Right: Gold Square
    draw_frame(5, 133, '#5C4033', 'flower')     # Bottom-Left: Brown Flower
    draw_frame(133, 133, '#191970', 'diamond')   # Bottom-Right: Blue Diamond
    
    return img

def create_placeholder_scene(width=1024, height=1024, type="window"):
    img = Image.new('RGB', (width, height), color='#F0F0F0')
    draw = ImageDraw.Draw(img)
    
    if type == "window":
        # Draw a simple lattice pattern
        step = 100
        for x in range(0, width, step):
            draw.line([(x, 0), (x, height)], fill='#5C4033', width=10)
        for y in range(0, height, step):
            draw.line([(0, y), (width, y)], fill='#5C4033', width=10)
        # Draw frame
        draw.rectangle([(0,0), (width, height)], outline='#3E2723', width=30)
        
    elif type == "wall":
        # Draw brick pattern
        img = Image.new('RGB', (width, height), color='#E0E0E0')
        draw = ImageDraw.Draw(img)
        brick_width = 200
        brick_height = 100
        for i, y in enumerate(range(0, height, brick_height)):
            offset = 0 if i % 2 == 0 else brick_width // 2
            for x in range(offset - brick_width, width, brick_width):
                draw.rectangle([(x, y), (x + brick_width, y + brick_height)], outline='#C0C0C0', width=2)
                
    return img

# --- CSS Styling ---
# Generate background pattern
bg_pattern = create_seamless_pattern()
bg_b64 = img_to_base64(bg_pattern)

st.markdown(f"""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

    /* 1. Hide Streamlit Header and Footer */
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}

    /* 2. Moving Background */
    /* Ensure the root container allows our background to show */
    .stApp {{
        background: #F9F7F2; /* Fallback color */
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 200vw;
        height: 200vh;
        background-image: url("data:image/png;base64,{bg_b64}");
        background-repeat: repeat;
        background-size: 256px 256px;
        opacity: 0.8; /* High opacity to ensure visibility */
        z-index: 0; /* Place at base level */
        animation: slide 30s linear infinite;
        pointer-events: none; /* Allow clicks to pass through */
    }}
    
    @keyframes slide {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(-128px, -128px); }}
    }}

    /* Content Container Overlay */
    .block-container {{
        position: relative;
        z-index: 1; /* Ensure content is above background */
        background-color: rgba(249, 247, 242, 0.9); /* Opaque enough to read text */
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 2rem;
        max-width: 1000px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(212, 197, 176, 0.5);
    }}

    /* 3. Title Styling */
    .title-container {{
        text-align: center;
        padding: 1rem 0 2rem 0;
    }}
    
    h1 {{
        font-family: 'Ma Shan Zheng', cursive;
        color: #252121 !important; /* Force Black */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-size: 4.5rem !important;
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }}
    
    /* 4. Unified Button Styling (Including Download Button) */
    .stButton > button, .stDownloadButton > button {{
        background-color: #B22222 !important;
        color: #FFF !important;
        border: 2px solid #FFF !important;
        border-radius: 8px !important;
        font-family: 'Ma Shan Zheng', cursive !important;
        font-size: 1.4rem !important; /* Slightly reduced font size */
        padding: 0.8rem 1rem !important; /* Reduced horizontal padding */
        white-space: nowrap !important; /* Force single line */
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        margin-top: 10px !important;
    }}

    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #980015 !important;
        color: #FFD700 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
        border-color: #FFD700 !important;
    }}
    
    /* Inputs */
    .stTextArea textarea {{
        border: 2px solid #8B0000 !important;
        border-radius: 8px !important;
        background-color: #FFFDF5 !important;
        font-family: 'Noto Serif SC', serif !important;
        font-size: 1.2rem !important;
        color: #333 !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        border: 2px solid #8B0000 !important;
        border-radius: 8px !important;
        background-color: #FFFDF5 !important;
    }}

    /* Success/Error Messages */
    .stSuccess, .stError, .stInfo {{
        font-family: 'Noto Serif SC', serif;
        border-radius: 8px;
    }}

</style>
""", unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    # Initialize Session State
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None
    
    # Title Section
    st.markdown("""
        <div class="title-container">
            <h1>🏮 剪 纸 大 师 🏮</h1>
        </div>
    """, unsafe_allow_html=True)

    # Input Section
    prompt = st.text_area("✍️ 请输入您的创意描述", height=100, placeholder="例如：一只站在梅花枝头的喜鹊，背景是祥云纹样...", label_visibility="collapsed")
    
    # Generate Button (Centered)
    # Use a narrower middle column for better visual centering
    col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
    with col_btn2:
        # Dynamic button label
        btn_label = "🔄 重 新 生 成" if st.session_state.processed_image else "🎨 开 始 创 作"
        generate_btn = st.button(btn_label)

    # Create a placeholder for results to allow explicit clearing
    results_placeholder = st.empty()

    if generate_btn:
        if not prompt:
            st.warning("⚠️ 请先输入描述！")
        else:
            # Clear previous results immediately
            st.session_state.processed_image = None
            st.session_state.generated_image = None
            results_placeholder.empty() # Explicitly clear the UI
            
            status_container = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Initialize Generator
                status_container.info("🔌 正在连接 ComfyUI 服务...")
                progress_bar.progress(10)
                
                try:
                    generator = FluxComfyUI_Generator()
                    connection_ok = generator.test_connection()
                except Exception:
                    connection_ok = False
                
                if not connection_ok:
                    status_container.error("❌ 无法连接到 ComfyUI，请确保服务已启动 (127.0.0.1:8188)")
                else:
                    # Generate (Using default parameters)
                    status_container.info("🎨 正在绘制剪纸图案 (这可能需要几十秒)...")
                    progress_bar.progress(30)
                    
                    first_part = "A vibrant red Chinese paper"
                    second_part = "complex Chinese patterns, stand proudly among the swirling clouds and stylized clouds. The background is pure white, emphasizing a bold traditional design"
                    
                    result = generator.generate_image(
                        first_part=first_part,
                        user_prompt=prompt,
                        second_part=second_part,
                        steps=30, # Default
                        cfg=1.0,  # Default
                        seed=None # Random
                    )
                    
                    if result['success']:
                        progress_bar.progress(70)
                        status_container.info("✂️ 正在进行剪纸工艺处理 (去底、上色)...")
                        
                        # Process
                        original_path = result['filename']
                        img = Image.open(original_path)
                        st.session_state.generated_image = img
                        
                        # Processing steps
                        img = desaturate_image(img)
                        img = increase_contrast(img, factor=3.0)
                        img = remove_white_background(img, threshold=230)
                        img = convert_to_red(img)
                        
                        st.session_state.processed_image = img
                        
                        progress_bar.progress(100)
                        status_container.success("✅ 创作完成！")
                        time.sleep(1)
                        status_container.empty()
                        progress_bar.empty()
                        
                        # Rerun to update button state
                        st.rerun()
                        
                    else:
                        status_container.error(f"❌ 生成失败: {result.get('error')}")
            
            except Exception as e:
                status_container.error(f"❌ 发生错误: {e}")

    # Results Display
    if st.session_state.processed_image:
        with results_placeholder.container():
            st.markdown("---")
            
            # Result Image (Larger - using wider column)
            col_res1, col_res2, col_res3 = st.columns([1, 8, 1]) # Much wider middle column
            with col_res2:
                st.markdown("<h3 style='text-align: center;'>🖼️ 剪纸成品</h3>", unsafe_allow_html=True)
                st.image(st.session_state.processed_image, use_container_width=True)
                
                # Download button (Centered under image)
                col_dl1, col_dl2, col_dl3 = st.columns([3, 2, 3])
                with col_dl2:
                    import io
                    buf = io.BytesIO()
                    st.session_state.processed_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 下载剪纸图片",
                        data=byte_im,
                        file_name=f"papercut_{int(time.time())}.png",
                        mime="image/png"
                    )
    
            # Scene Simulation
            st.markdown("---")
            st.markdown("<h3 style='text-align: center;'>🏠 场景模拟预览</h3>", unsafe_allow_html=True)
            
            col_scene1, col_scene2 = st.columns([1, 3])
            
            with col_scene1:
                st.markdown("<br>", unsafe_allow_html=True)
                scene_option = st.selectbox("选择展示场景", ["窗花 (Window)", "墙壁 (Wall)"])
                preview_btn = st.button("👀 生成预览")
                
            with col_scene2:
                if preview_btn:
                    with st.spinner("正在合成场景..."):
                        # Create background
                        bg_type = "window" if "Window" in scene_option else "wall"
                        bg_img = create_placeholder_scene(type=bg_type)
                        
                        # Composite
                        papercut = st.session_state.processed_image.copy()
                        target_size = int(bg_img.width * 0.6)
                        papercut = papercut.resize((target_size, target_size), Image.Resampling.LANCZOS)
                        
                        # Center position
                        x = (bg_img.width - papercut.width) // 2
                        y = (bg_img.height - papercut.height) // 2
                        
                        # Paste
                        bg_img.paste(papercut, (x, y), papercut)
                        
                        st.image(bg_img, caption=f"{scene_option}效果预览", use_container_width=True)

                    st.image(bg_img, caption=f"{scene_option}效果预览", use_container_width=True)

if __name__ == "__main__":
    main()

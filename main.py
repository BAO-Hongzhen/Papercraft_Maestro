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
    from comfy_api import ComfyUIManager
    from Image_Processing import desaturate_image, increase_contrast, remove_white_background, convert_to_red, render_on_window, render_on_wall, render_on_door, render_on_package
except ImportError:
    pass # Will handle gracefully later

# --- Path Settings ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOW_PATH = os.path.join(BASE_DIR, "comfyui_workflow", "paper_cut.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "image_raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "image_processed")
RENDERED_DIR = os.path.join(BASE_DIR, "image_rendered")

# Ensure output directories exist
for d in [OUTPUT_DIR, PROCESSED_DIR, RENDERED_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# Page Configuration
st.set_page_config(
    page_title="Papercraft Maestro",
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
    """Create a distinct tiled background using random papercuts from ui_assets/background with paper texture (3x3 grid)"""
    import random
    import numpy as np
    
    # 1. Try to load images from ui_assets/background
    assets_dir = os.path.join(BASE_DIR, 'ui_assets', 'background')
    
    papercuts = []
    if os.path.exists(assets_dir):
        for f in os.listdir(assets_dir):
            if f.endswith('.png') or f.endswith('.jpg'):
                papercuts.append(os.path.join(assets_dir, f))
    
    # 2. Setup Canvas (768x768 for 3x3 grid of 256x256 cells)
    cell_size = 256
    grid_size = 3
    w, h = cell_size * grid_size, cell_size * grid_size
    
    # Generate Paper Texture Background
    # Warm white base color (R, G, B, A)
    base_color = [253, 251, 247, 255] 
    img_array = np.full((h, w, 4), base_color, dtype=np.uint8)
    
    # Add random noise for texture
    noise = np.random.randint(-5, 5, (h, w, 4), dtype=np.int16)
    # Apply noise only to RGB channels, keep Alpha 255
    img_array[:, :, :3] = np.clip(img_array[:, :, :3] + noise[:, :, :3], 0, 255)
    
    img = Image.fromarray(img_array.astype(np.uint8), 'RGBA')
    
    # 3. If valid images found, add them to the collage
    if papercuts:
        # Select 9 unique random images (if enough exist)
        if len(papercuts) >= grid_size * grid_size:
            selected = random.sample(papercuts, k=grid_size * grid_size)
        else:
            # Fallback if not enough unique images
            selected = random.choices(papercuts, k=grid_size * grid_size)
        
        for idx, path in enumerate(selected):
            try:
                p_img = Image.open(path).convert('RGBA')
                
                # Resize to fit in cell (256x256) with LESS padding
                # Target size: 230x230 to reduce spacing
                p_img.thumbnail((230, 230), Image.Resampling.LANCZOS)
                
                # Calculate row and col
                row = idx // grid_size
                col = idx % grid_size
                
                # Cell top-left coordinates
                cell_x = col * cell_size
                cell_y = row * cell_size
                
                # No rotation
                # angle = 0 
                # p_img = p_img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
                
                # Calculate centered position in cell
                px = cell_x + (cell_size - p_img.width) // 2
                py = cell_y + (cell_size - p_img.height) // 2
                
                # Adjust opacity (make it subtle background)
                # Create a new image with adjusted alpha
                r, g, b, a = p_img.split()
                # Reduce alpha to 80%
                a = a.point(lambda x: x * 0.8) 
                p_img.putalpha(a)
                
                # Paste
                img.paste(p_img, (px, py), p_img)
                
            except Exception as e:
                print(f"Error loading background asset {path}: {e}")
                continue
                
        return img

    # 3. Fallback
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
        background-size: 768px 768px;
        opacity: 0.8; /* High opacity to ensure visibility */
        z-index: 0; /* Place at base level */
        animation: slide 180s linear infinite;
        pointer-events: none; /* Allow clicks to pass through */
    }}
    
    @keyframes slide {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(-768px, -768px); }}
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
        st.session_state.generated_image = None
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None
    if 'scene_previews' not in st.session_state:
        st.session_state.scene_previews = {}
    
    # Title Section
    st.markdown("""
        <div class="title-container">
            <h1>Papercraft Maestro</h1>
        </div>
    """, unsafe_allow_html=True)

    # Input Section
    prompt = st.text_area("Enter your creative description", height=100, placeholder="e.g., tiger, flower, superman or a sentence...", label_visibility="collapsed")
    
    # Generate Button (Centered)
    # Use a narrower middle column for better visual centering
    col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
    with col_btn2:
        # Dynamic button label
        btn_label = "Regen" if st.session_state.processed_image else "Generate"
        generate_btn = st.button(btn_label)

    # Create a placeholder for results to allow explicit clearing
    results_placeholder = st.empty()

    if generate_btn:
        if not prompt:
            st.warning("Please enter a description first!")
        else:
            # Clear previous results immediately
            st.session_state.processed_image = None
            st.session_state.generated_image = None
            st.session_state.scene_previews = {}
            results_placeholder.empty() # Explicitly clear the UI
            
            status_container = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Initialize Generator (Updated to use ComfyUIManager)
                status_container.info("Connecting to ComfyUI service...")
                progress_bar.progress(10)
                
                try:
                    # Use ComfyUIManager from root
                    manager = ComfyUIManager(WORKFLOW_PATH)
                    connection_ok = True
                except Exception as e:
                    print(f"Connection error: {e}")
                    connection_ok = False
                
                if not connection_ok:
                    status_container.error("Cannot connect to ComfyUI. Please ensure the service is running (127.0.0.1:8188)")
                else:
                    # Generate (Using default parameters)
                    status_container.info("Generating papercut pattern (this may take a few seconds)...")
                    progress_bar.progress(30)
                    
                    # Generate image using manager
                    raw_image_path = manager.generate_image(prompt, OUTPUT_DIR)
                    
                    if raw_image_path:
                        progress_bar.progress(70)
                        status_container.info("Processing papercut (removing background, coloring)...")
                        
                        # Process
                        img = Image.open(raw_image_path)
                        st.session_state.generated_image = img
                        
                        # Processing steps
                        img = desaturate_image(img)
                        img = increase_contrast(img, factor=3.0)
                        img = remove_white_background(img, threshold=230)
                        img = convert_to_red(img)
                        
                        st.session_state.processed_image = img
                        
                        # Save processed image
                        timestamp = int(time.time())
                        processed_filename = f"processed_{timestamp}.png"
                        processed_path = os.path.join(PROCESSED_DIR, processed_filename)
                        img.save(processed_path)
                        
                        # Generate Scene Previews
                        status_container.info("Generating scene previews...")
                        
                        # Use ui_assets/prototype_images for scene backgrounds
                        ui_assets_dir = os.path.join(BASE_DIR, 'ui_assets', 'prototype_images')
                        
                        # Window (Base_Window.jpg)
                        window_bg = os.path.join(ui_assets_dir, 'Base_Window.jpg')
                        if os.path.exists(window_bg):
                            output_path = os.path.join(RENDERED_DIR, f"window_{timestamp}.png")
                            st.session_state.scene_previews['window'] = render_on_window(img, window_bg, output_path)
                        
                        # Package (Base_package.jpg)
                        package_bg = os.path.join(ui_assets_dir, 'Base_package.jpg')
                        if os.path.exists(package_bg):
                            output_path = os.path.join(RENDERED_DIR, f"package_{timestamp}.png")
                            st.session_state.scene_previews['package'] = render_on_package(img, package_bg, output_path)
                            
                        # Door (Base_door.jpg)
                        door_bg = os.path.join(ui_assets_dir, 'Base_door.jpg')
                        if os.path.exists(door_bg):
                            output_path = os.path.join(RENDERED_DIR, f"door_{timestamp}.png")
                            st.session_state.scene_previews['door'] = render_on_door(img, door_bg, output_path)
                            
                        # Wall (Base_wall.jpeg)
                        wall_bg = os.path.join(ui_assets_dir, 'Base_wall.jpeg')
                        if os.path.exists(wall_bg):
                            output_path = os.path.join(RENDERED_DIR, f"wall_{timestamp}.png")
                            st.session_state.scene_previews['wall'] = render_on_wall(img, wall_bg, output_path)
                        
                        progress_bar.progress(100)
                        status_container.success("Creation complete!")
                        time.sleep(1)
                        status_container.empty()
                        progress_bar.empty()
                        
                        # Rerun to update button state
                        st.rerun()
                        
                    else:
                        status_container.error(f"Generation failed: ComfyUI did not return an image")
            
            except Exception as e:
                status_container.error(f"Error occurred: {e}")

    # Results Display
    if st.session_state.processed_image:
        with results_placeholder.container():
            st.markdown("---")
            
            # Result Image (Larger - using wider column)
            col_res1, col_res2, col_res3 = st.columns([1, 8, 1]) # Much wider middle column
            with col_res2:
                st.markdown("<h3 style='text-align: center;'>Papercut Result</h3>", unsafe_allow_html=True)
                st.image(st.session_state.processed_image, use_container_width=True)
                
                # Download button (Centered under image)
                col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                with col_dl2:
                    import io
                    buf = io.BytesIO()
                    st.session_state.processed_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="Download Papercut",
                        data=byte_im,
                        file_name=f"papercut_{int(time.time())}.png",
                        mime="image/png"
                    )
    
            # Scene Simulation
            st.markdown("---")
            st.markdown("<h3 style='text-align: center;'>Scene Preview</h3>", unsafe_allow_html=True)
            
            if st.session_state.scene_previews:
                # Row 1: Window & Package (Landscape 3:2)
                col_r1_1, col_r1_2 = st.columns(2)
                
                with col_r1_1:
                    if 'window' in st.session_state.scene_previews and st.session_state.scene_previews['window']:
                        st.image(st.session_state.scene_previews['window'], caption="Window Effect", use_container_width=True)
                    else:
                        st.info("Window preview failed")
                        
                with col_r1_2:
                    if 'package' in st.session_state.scene_previews and st.session_state.scene_previews['package']:
                        st.image(st.session_state.scene_previews['package'], caption="Package Effect", use_container_width=True)
                    else:
                        st.info("Package preview failed")
                
                # Row 2: Door & Wall (Square 1:1)
                col_r2_1, col_r2_2 = st.columns(2)
                
                with col_r2_1:
                    if 'door' in st.session_state.scene_previews and st.session_state.scene_previews['door']:
                        st.image(st.session_state.scene_previews['door'], caption="Door Effect", use_container_width=True)
                    else:
                        st.info("Door preview failed")
                        
                with col_r2_2:
                    if 'wall' in st.session_state.scene_previews and st.session_state.scene_previews['wall']:
                        st.image(st.session_state.scene_previews['wall'], caption="Wall Effect", use_container_width=True)
                    else:
                        st.info("Wall preview failed")
            else:
                st.warning("Preview generation failed. Please check resource files.")

if __name__ == "__main__":
    main()

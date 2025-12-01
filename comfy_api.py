import os
import random
import asyncio
import time
import socket
import requests

# Handle asyncio event loop issue (Streamlit compatibility)
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

def find_comfyui_address():
    """
    Automatically detect ComfyUI address
    Supports ComfyUI Desktop, command line version, and custom port configuration
    """
    print("Searching for ComfyUI service...")
    
    # 1. Prioritize checking environment variables
    env_addr = os.environ.get("COMFYUI_ADDRESS")
    if env_addr:
        print(f"Found address from environment variable: {env_addr}")
        return env_addr

    # 2. Define list of ports to scan (sorted by priority)
    # - 8000: ComfyUI Desktop default port
    # - 8188-8199: ComfyUI command line version common port range
    # - 3000, 3001: Ports that might be used by some configurations
    # - 7860, 7861: Gradio style ports (used by some integrated packages)
    priority_ports = [8000, 8188, 8189, 8190, 8191, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199]
    additional_ports = [3000, 3001, 7860, 7861, 8080, 8081, 9000, 9001]
    all_ports = priority_ports + additional_ports

    # 3. Scan ports
    for port in all_ports:
        if _check_comfyui_port(port):
            url = f"http://127.0.0.1:{port}"
            print(f"Found ComfyUI service at: {url}")
            return url
            
    print("No running ComfyUI found, using default address http://127.0.0.1:8188/")
    print("Tip: Please ensure ComfyUI or ComfyUI Desktop is started")
    return "http://127.0.0.1:8188/"


def _check_comfyui_port(port):
    """
    Check if ComfyUI service is running on the specified port
    
    Args:
        port: Port number to check
        
    Returns:
        bool: Returns True if ComfyUI is running on the port
    """
    try:
        # Perform quick TCP connection test first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            return False
            
        # TCP connection successful, verify if it is ComfyUI (check /system_stats endpoint)
        url = f"http://127.0.0.1:{port}"
        response = requests.get(f"{url}/system_stats", timeout=1)
        return response.status_code == 200
    except:
        return False

class ComfyUIManager:
    def __init__(self, workflow_path, server_address=None):
        if server_address is None:
            self.server_address = find_comfyui_address()
        else:
            self.server_address = server_address
            
        self.workflow_path = workflow_path
        print(f"Connecting to ComfyUI: {self.server_address}")
        self.api = ComfyApiWrapper(self.server_address)
        
    def generate_image(self, prompt, output_dir):
        """
        Execute ComfyUI generation task
        
        Args:
            prompt (str): User input prompt
            output_dir (str): Output directory
            
        Returns:
            str: Full path of the generated image, returns None if failed
        """
        try:
            # Reload workflow to ensure a clean state every time
            wf = ComfyWorkflowWrapper(self.workflow_path)
            
            # 1. Set random seed
            random_seed = random.randint(1, 2**48 - 1)
            wf.set_node_param("KSampler", "seed", random_seed)
            
            # 2. Build full prompt
            first_part = "A vibrant red Chinese paper"
            second_part = "complex Chinese patterns, stand proudly among the swirling clouds and stylized clouds. The background is pure white, emphasizing a bold traditional design"
            full_prompt = f"{first_part}, {prompt}, {second_part}"
            
            # 3. Update prompt node (CLIPTextEncodeFlux)
            # Flux models usually have two text inputs
            wf.set_node_param("CLIPTextEncodeFlux", "clip_l", full_prompt)
            wf.set_node_param("CLIPTextEncodeFlux", "t5xxl", full_prompt)
            
            # 4. Submit task and wait
            # "Save Image" is the Title of the save node in the workflow
            results = self.api.queue_and_wait_images(wf, "Save Image")
            
            if results:
                # Get the first image
                filename = list(results.keys())[0]
                image_data = results[filename]
                
                # Generate output filename
                timestamp = int(time.time())
                safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
                output_filename = f"flux_{safe_prompt}_{timestamp}.png"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save file
                with open(output_path, "wb") as f:
                    f.write(image_data)
                    
                return output_path
            else:
                print("Error: No images returned from ComfyUI.")
                return None
                
        except Exception as e:
            print(f"ComfyUI Generation Error: {e}")
            return None

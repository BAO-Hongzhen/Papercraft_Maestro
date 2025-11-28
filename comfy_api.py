import os
import random
import asyncio
import time
import socket
import requests

# 处理 asyncio 事件循环问题 (Streamlit 兼容性)
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

def find_comfyui_address(start_port=8188, max_attempts=10):
    """
    自动检测 ComfyUI 地址
    尝试连接本地常用端口
    """
    print("🔍 正在寻找 ComfyUI 服务...")
    
    # 1. 优先检查环境变量
    env_addr = os.environ.get("COMFYUI_ADDRESS")
    if env_addr:
        print(f"✅ 从环境变量找到地址: {env_addr}")
        return env_addr

    # 2. 扫描本地端口
    for port in range(start_port, start_port + max_attempts):
        try:
            # 简单的 TCP 连接测试
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                # 进一步验证是否是 ComfyUI (检查 /system_stats 端点)
                url = f"http://127.0.0.1:{port}"
                try:
                    response = requests.get(f"{url}/system_stats", timeout=1)
                    if response.status_code == 200:
                        print(f"✅ 发现 ComfyUI 服务于: {url}")
                        return url
                except:
                    pass
        except:
            continue
            
    print("⚠️ 未找到运行中的 ComfyUI，将使用默认地址 http://127.0.0.1:8188/")
    return "http://127.0.0.1:8188/"

class ComfyUIManager:
    def __init__(self, workflow_path, server_address=None):
        if server_address is None:
            self.server_address = find_comfyui_address()
        else:
            self.server_address = server_address
            
        self.workflow_path = workflow_path
        print(f"🔌 连接到 ComfyUI: {self.server_address}")
        self.api = ComfyApiWrapper(self.server_address)
        
    def generate_image(self, prompt, output_dir):
        """
        执行 ComfyUI 生成任务
        
        Args:
            prompt (str): 用户输入的提示词
            output_dir (str): 输出目录
            
        Returns:
            str: 生成图片的完整路径，如果失败则返回 None
        """
        try:
            # 重新加载工作流以确保每次都是干净的状态
            wf = ComfyWorkflowWrapper(self.workflow_path)
            
            # 1. 设置随机种子
            random_seed = random.randint(1, 2**48 - 1)
            wf.set_node_param("KSampler", "seed", random_seed)
            
            # 2. 构建完整提示词
            first_part = "A vibrant red Chinese paper"
            second_part = "complex Chinese patterns, stand proudly among the swirling clouds and stylized clouds. The background is pure white, emphasizing a bold traditional design"
            full_prompt = f"{first_part}, {prompt}, {second_part}"
            
            # 3. 更新提示词节点 (CLIPTextEncodeFlux)
            # Flux 模型通常有两个文本输入端
            wf.set_node_param("CLIPTextEncodeFlux", "clip_l", full_prompt)
            wf.set_node_param("CLIPTextEncodeFlux", "t5xxl", full_prompt)
            
            # 4. 提交任务并等待
            # "Save Image" 是工作流中保存节点的 Title
            results = self.api.queue_and_wait_images(wf, "Save Image")
            
            if results:
                # 获取第一张图片
                filename = list(results.keys())[0]
                image_data = results[filename]
                
                # 生成输出文件名
                timestamp = int(time.time())
                safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
                output_filename = f"flux_{safe_prompt}_{timestamp}.png"
                output_path = os.path.join(output_dir, output_filename)
                
                # 保存文件
                with open(output_path, "wb") as f:
                    f.write(image_data)
                    
                return output_path
            else:
                print("Error: No images returned from ComfyUI.")
                return None
                
        except Exception as e:
            print(f"ComfyUI Generation Error: {e}")
            return None

"""
ComfyUI API调用模块 - ComfyUI API Client
负责与本地ComfyUI服务通信，生成GIF动图
"""

import json
import requests
import websocket
import uuid
import urllib.request
import urllib.parse
import time
from io import BytesIO
from PIL import Image
from typing import Optional, Dict, List
import os


class ComfyUIClient:
    """ComfyUI API客户端"""
    
    def __init__(self, server_address: str = "127.0.0.1:8188"):
        """
        初始化ComfyUI客户端
        
        Args:
            server_address: ComfyUI服务器地址
        """
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.base_url = f"http://{server_address}"
    
    def queue_prompt(self, prompt: Dict) -> Optional[str]:
        """
        将提示词加入队列
        
        Args:
            prompt: 工作流提示词
            
        Returns:
            提示词ID
        """
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        
        try:
            req = urllib.request.Request(f"{self.base_url}/prompt", data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            return result.get('prompt_id')
        except Exception as e:
            print(f"❌ 提交提示词失败: {e}")
            return None
    
    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> Optional[bytes]:
        """
        从ComfyUI获取生成的图像
        
        Args:
            filename: 文件名
            subfolder: 子文件夹
            folder_type: 文件夹类型
            
        Returns:
            图像数据
        """
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        
        try:
            with urllib.request.urlopen(f"{self.base_url}/view?{url_values}") as response:
                return response.read()
        except Exception as e:
            print(f"❌ 获取图像失败: {e}")
            return None
    
    def get_history(self, prompt_id: str) -> Optional[Dict]:
        """
        获取生成历史
        
        Args:
            prompt_id: 提示词ID
            
        Returns:
            历史记录
        """
        try:
            with urllib.request.urlopen(f"{self.base_url}/history/{prompt_id}") as response:
                return json.loads(response.read())
        except Exception as e:
            print(f"❌ 获取历史失败: {e}")
            return None
    
    def track_progress(self, prompt_id: str, timeout: int = 300) -> Optional[Dict]:
        """
        跟踪生成进度
        
        Args:
            prompt_id: 提示词ID
            timeout: 超时时间（秒）
            
        Returns:
            完成的历史记录
        """
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                print(f"❌ 生成超时 ({timeout}秒)")
                return None
            
            history = self.get_history(prompt_id)
            if history and prompt_id in history:
                return history[prompt_id]
            
            time.sleep(1)
    
    def create_text2gif_workflow(self, prompt: str, negative_prompt: str = "",
                                  width: int = 512, height: int = 512,
                                  num_frames: int = 16, fps: int = 8) -> Dict:
        """
        创建文本到GIF的工作流
        
        Args:
            prompt: 正面提示词
            negative_prompt: 负面提示词
            width: 宽度
            height: 高度
            num_frames: 帧数
            fps: 帧率
            
        Returns:
            工作流字典
        """
        workflow = {
            "3": {
                "inputs": {
                    "seed": int(time.time()),
                    "steps": 20,
                    "cfg": 8,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": num_frames
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "syntax_roulette",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }
        
        return workflow
    
    def generate_gif(self, prompt: str, negative_prompt: str = "",
                    width: int = 512, height: int = 512,
                    num_frames: int = 16, fps: int = 8,
                    output_path: Optional[str] = None) -> Optional[str]:
        """
        生成GIF动图
        
        Args:
            prompt: 正面提示词
            negative_prompt: 负面提示词
            width: 宽度
            height: 高度
            num_frames: 帧数
            fps: 帧率
            output_path: 输出路径
            
        Returns:
            生成的GIF文件路径
        """
        print(f"🎨 开始生成GIF...")
        print(f"   提示词: {prompt}")
        print(f"   尺寸: {width}x{height}")
        print(f"   帧数: {num_frames}")
        
        # 创建工作流
        workflow = self.create_text2gif_workflow(
            prompt, negative_prompt, width, height, num_frames, fps
        )
        
        # 提交到队列
        prompt_id = self.queue_prompt(workflow)
        if not prompt_id:
            return None
        
        print(f"✅ 已提交到队列，ID: {prompt_id}")
        print(f"⏳ 等待生成完成...")
        
        # 跟踪进度
        history = self.track_progress(prompt_id)
        if not history:
            return None
        
        # 获取生成的图像
        outputs = history.get("outputs", {})
        images = []
        
        for node_id in outputs:
            node_output = outputs[node_id]
            if "images" in node_output:
                for image_data in node_output["images"]:
                    image_bytes = self.get_image(
                        image_data["filename"],
                        image_data.get("subfolder", ""),
                        image_data.get("type", "output")
                    )
                    if image_bytes:
                        images.append(Image.open(BytesIO(image_bytes)))
        
        if not images:
            print(f"❌ 未获取到图像")
            return None
        
        # 保存为GIF
        if output_path is None:
            timestamp = int(time.time())
            output_path = f"output/syntax_roulette_{timestamp}.gif"
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存GIF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=1000 // fps,
            loop=0
        )
        
        print(f"✅ GIF生成成功: {output_path}")
        return output_path
    
    def test_connection(self) -> bool:
        """
        测试与ComfyUI的连接
        
        Returns:
            连接是否成功
        """
        try:
            response = requests.get(f"{self.base_url}/system_stats", timeout=5)
            if response.status_code == 200:
                print(f"✅ ComfyUI连接成功: {self.base_url}")
                stats = response.json()
                print(f"   系统信息: {stats}")
                return True
            else:
                print(f"❌ ComfyUI连接失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ ComfyUI连接失败: {e}")
            print(f"   请确保ComfyUI正在运行于 {self.base_url}")
            return False


# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = ComfyUIClient()
    
    # 测试连接
    print("测试ComfyUI连接...")
    if client.test_connection():
        print("\n尝试生成GIF（需要ComfyUI运行）...")
        
        # 生成GIF
        gif_path = client.generate_gif(
            prompt="a cat jumping happily in a beautiful garden",
            negative_prompt="blurry, bad quality",
            width=512,
            height=512,
            num_frames=16,
            fps=8
        )
        
        if gif_path:
            print(f"\n🎉 GIF已保存到: {gif_path}")
    else:
        print("\n⚠️ 演示模式：请先启动ComfyUI服务")
        print("   启动命令: python main.py (在ComfyUI目录)")

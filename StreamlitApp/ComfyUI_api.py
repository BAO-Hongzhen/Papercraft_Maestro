"""
ComfyUI Flux 剪纸图片生成器
支持终端交互式输入
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class FluxComfyUI_Generator:
    """Flux ComfyUI 图片生成器"""
    
    def __init__(self, server_address: str = "127.0.0.1:8188"):
        """
        初始化生成器
        
        Args:
            server_address: ComfyUI 服务器地址
        """
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self._workflow_template = None  # 缓存工作流模板
        print(f"✅ 初始化 ComfyUI 客户端: {server_address}")
    
    def load_workflow_template(self) -> Dict[str, Any]:
        """加载 API 格式的工作流模板（带缓存）"""
        # 如果已经加载过，直接返回缓存
        if self._workflow_template is not None:
            return self._workflow_template.copy()  # 返回副本避免被修改
        
        workflow_path = 'ComfyUI_Workflow/paper_cut.json'
        
        if not os.path.exists(workflow_path):
            raise FileNotFoundError(
                f"工作流文件不存在: {workflow_path}"
            )
        
        with open(workflow_path, 'r', encoding='utf-8') as f:
            self._workflow_template = json.load(f)
        
        print(f"✅ 工作流加载成功: {len(self._workflow_template)} 个节点（已缓存）")
        return self._workflow_template.copy()
    
    def replace_prompts_in_workflow(self, 
                                  workflow: Dict[str, Any], 
                                  first_part: str,
                                  user_prompt: str,
                                  second_part: str) -> Dict[str, Any]:
        """
        替换工作流中的提示词
        
        Args:
            workflow: API 格式工作流
            first_part: 提示词第一部分
            user_prompt: 用户输入的提示词
            second_part: 提示词第二部分
            
        Returns:
            更新后的工作流
        """
        # 构建完整提示词
        full_prompt = f"{first_part}, {user_prompt}, {second_part}"
        
        # 在 API 格式工作流中找到 CLIPTextEncodeFlux 节点
        prompt_set = False
        for node_id, node_data in workflow.items():
            if node_data.get('class_type') == 'CLIPTextEncodeFlux':
                # 更新提示词
                node_data['inputs']['clip_l'] = full_prompt
                node_data['inputs']['t5xxl'] = full_prompt
                print(f"✅ 提示词已设置 (节点 {node_id})")
                print(f"   完整提示词: {full_prompt[:80]}...")
                prompt_set = True
                break
        
        if not prompt_set:
            print("⚠️ 警告: 未找到 CLIPTextEncodeFlux 节点")
        
        return workflow
    
    def update_sampler_parameters(self, 
                                workflow: Dict[str, Any], 
                                seed: int = None,
                                steps: int = None,
                                cfg: float = None,
                                width: int = None,
                                height: int = None) -> Dict[str, Any]:
        """
        更新采样器和图片参数
        
        Args:
            workflow: API 格式工作流
            seed: 随机种子
            steps: 采样步数
            cfg: CFG 值
            width: 图片宽度
            height: 图片高度
            
        Returns:
            更新后的工作流
        """
        # 更新 KSampler 参数
        for node_id, node_data in workflow.items():
            if node_data.get('class_type') == 'KSampler':
                if seed is not None:
                    node_data['inputs']['seed'] = seed
                if steps is not None:
                    node_data['inputs']['steps'] = steps
                if cfg is not None:
                    node_data['inputs']['cfg'] = cfg
                print(f"✅ KSampler 参数已更新: seed={seed}, steps={steps}, cfg={cfg}")
            
            # 更新图片尺寸
            if node_data.get('class_type') == 'EmptySD3LatentImage':
                if width is not None:
                    node_data['inputs']['width'] = width
                if height is not None:
                    node_data['inputs']['height'] = height
                print(f"✅ 图片尺寸已更新: {width}x{height}")
        
        return workflow
    
    def queue_prompt(self, prompt: Dict[str, Any]) -> str:
        """
        提交工作流到 ComfyUI 队列
        
        Args:
            prompt: API 格式的工作流
            
        Returns:
            任务 ID
        """
        url = f"http://{self.server_address}/prompt"
        
        # 保存调试信息（可选 - 仅用于开发调试）
        # debug_file = 'debug_prompt.json'
        # with open(debug_file, 'w', encoding='utf-8') as f:
        #     json.dump({"prompt": prompt, "client_id": self.client_id}, f, indent=2, ensure_ascii=False)
        # print(f"📝 调试信息已保存: {debug_file}")
        
        # 发送请求
        response = requests.post(url, json={"prompt": prompt, "client_id": self.client_id})
        
        # 检查响应
        if response.status_code != 200:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            response.raise_for_status()
        
        result = response.json()
        prompt_id = result.get("prompt_id")
        
        if not prompt_id:
            raise ValueError(f"未获取到任务 ID: {result}")
        
        return prompt_id
    
    def get_image(self, prompt_id: str, max_attempts: int = 300, check_interval: int = 2) -> Optional[bytes]:
        """
        等待并获取生成的图片
        
        Args:
            prompt_id: 任务 ID
            max_attempts: 最大尝试次数
            check_interval: 检查间隔（秒）
            
        Returns:
            图片数据（字节）
        """
        url = f"http://{self.server_address}/history/{prompt_id}"
        
        print(f"⏳ 等待图片生成... (最多等待 {max_attempts * check_interval} 秒)")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    history = response.json()
                    
                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})
                        
                        # 查找图片输出
                        for node_id, node_output in outputs.items():
                            if "images" in node_output:
                                images = node_output["images"]
                                if images:
                                    image_info = images[0]
                                    
                                    # 构建图片 URL
                                    filename = image_info['filename']
                                    subfolder = image_info.get('subfolder', '')
                                    folder_type = image_info.get('type', 'output')
                                    
                                    image_url = (
                                        f"http://{self.server_address}/view?"
                                        f"filename={filename}&subfolder={subfolder}&type={folder_type}"
                                    )
                                    
                                    # 下载图片
                                    print(f"📥 下载图片: {filename}")
                                    image_response = requests.get(image_url, timeout=30)
                                    image_response.raise_for_status()
                                    
                                    return image_response.content
                
                # 显示进度
                if attempt % 5 == 0:
                    print(f"   等待中... ({attempt + 1}/{max_attempts})")
                
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"⚠️ 检查状态时出错: {e}")
                time.sleep(check_interval)
        
        print(f"❌ 超时: 等待了 {max_attempts * check_interval} 秒仍未完成")
        return None
    
    def test_connection(self) -> bool:
        """
        测试与 ComfyUI 的连接
        
        Returns:
            连接是否成功
        """
        try:
            url = f"http://{self.server_address}/system_stats"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ ComfyUI 连接成功")
                return True
            else:
                print(f"❌ ComfyUI 连接失败: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到 ComfyUI: {self.server_address}")
            print(f"   请确保 ComfyUI 正在运行")
            return False
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def generate_image(self, 
                      first_part: str,
                      user_prompt: str,
                      second_part: str,
                      output_filename: str = None,
                      seed: int = None,
                      steps: int = 30,
                      cfg: float = 1.0,
                      width: int = 1024,
                      height: int = 1024) -> Dict[str, Any]:
        """
        生成图片 - 主函数
        
        Args:
            first_part: 提示词第一部分
            user_prompt: 用户输入的提示词
            second_part: 提示词第二部分
            output_filename: 输出文件名
            seed: 随机种子
            steps: 采样步数
            cfg: CFG 值
            width: 图片宽度
            height: 图片高度
            
        Returns:
            结果字典 {success, filename, prompt_id, error}
        """
        result = {
            "success": False,
            "filename": None,
            "prompt_id": None,
            "error": None
        }
        
        try:
            print("\n" + "="*60)
            print("🎨 开始生成图片")
            print("="*60)
            
            # 1. 加载工作流
            workflow = self.load_workflow_template()
            
            # 2. 设置提示词
            workflow = self.replace_prompts_in_workflow(
                workflow, first_part, user_prompt, second_part
            )
            
            # 3. 更新参数
            if seed is None:
                seed = int(time.time()) % 1000000
            
            workflow = self.update_sampler_parameters(
                workflow, seed, steps, cfg, width, height
            )
            
            # 4. 提交任务
            print("\n📤 提交到 ComfyUI...")
            prompt_id = self.queue_prompt(workflow)
            result["prompt_id"] = prompt_id
            print(f"✅ 任务已提交，ID: {prompt_id}")
            
            # 5. 等待并获取图片
            image_data = self.get_image(prompt_id)
            
            if image_data:
                # 6. 保存图片
                if not output_filename:
                    timestamp = int(time.time())
                    safe_prompt = "".join(
                        c for c in user_prompt[:20] 
                        if c.isalnum() or c in (' ', '-', '_')
                    ).strip().replace(' ', '_')
                    output_filename = f"flux_{safe_prompt}_{timestamp}.png"
                
                # 确保输出目录存在
                output_dir = os.path.dirname(output_filename)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                with open(output_filename, "wb") as f:
                    f.write(image_data)
                
                result["success"] = True
                result["filename"] = output_filename
                
                print("\n" + "="*60)
                print("✅ 图片生成成功！")
                print(f"📁 保存位置: {output_filename}")
                print(f"📊 文件大小: {len(image_data) / 1024:.1f} KB")
                print("="*60)
            else:
                result["error"] = "生成图片失败或超时"
                print("\n❌ 生成失败或超时")
                
        except FileNotFoundError as e:
            result["error"] = str(e)
            print(f"\n❌ 文件错误: {e}")
            
        except requests.exceptions.ConnectionError:
            error_msg = f"无法连接到 ComfyUI: {self.server_address}"
            result["error"] = error_msg
            print(f"\n❌ {error_msg}")
            print("   请确保 ComfyUI 正在运行")
            
        except Exception as e:
            error_msg = f"生成过程出错: {str(e)}"
            result["error"] = error_msg
            print(f"\n❌ {error_msg}")
            import traceback
            traceback.print_exc()
        
        return result


def get_user_input() -> Optional[str]:
    """从终端获取用户输入的提示词"""
    print("\n" + "="*60)
    print("请输入您的提示词 (输入 'quit' 或 'exit' 退出)")
    print("="*60)
    
    try:
        user_prompt = input("提示词: ").strip()
        
        if user_prompt.lower() in ['quit', 'exit', 'q']:
            return None
        
        if not user_prompt:
            print("⚠️ 提示词不能为空")
            return get_user_input()
        
        return user_prompt
        
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断")
        return None
    except EOFError:
        return None


def main():
    """主函数 - 交互式生成图片"""
    print("="*60)
    print("🎨 Flux ComfyUI 剪纸图片生成器")
    print("="*60)
    print()
    
    # 初始化生成器
    try:
        generator = FluxComfyUI_Generator("127.0.0.1:8188")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 测试连接
    print("\n🔗 测试 ComfyUI 连接...")
    if not generator.test_connection():
        print("\n❌ 无法连接到 ComfyUI，请检查：")
        print("   1. ComfyUI 是否正在运行？")
        print("   2. 地址是否正确？(127.0.0.1:8188)")
        return
    
    # 检查工作流文件
    if not os.path.exists('ComfyUI_Workflow/paper_cut.json'):
        print("\n❌ 缺少工作流文件: ComfyUI_Workflow/paper_cut.json")
        return
    
    # 配置提示词模板
    first_part = "A vibrant red Chinese paper"
    second_part = "complex Chinese patterns, stand proudly among the swirling clouds and stylized clouds. The background is pure white, emphasizing a bold traditional design."
    
    print("\n📝 提示词模板:")
    print(f"   第一部分: {first_part}")
    print(f"   第二部分: {second_part}")
    print(f"   格式: [第一部分], [用户输入], [第二部分]")
    
    # 交互式输入循环
    while True:
        user_prompt = get_user_input()
        
        if user_prompt is None:
            print("\n👋 感谢使用，再见！")
            break
        
        # 生成图片
        result = generator.generate_image(
            first_part=first_part,
            user_prompt=user_prompt,
            second_part=second_part,
            seed=None,  # 自动随机
            steps=30,   # 采样步数
            cfg=1.0,    # CFG 值
            width=1024,
            height=1024
        )
        
        # 显示结果
        if not result["success"]:
            print(f"\n❌ 生成失败")
            if result["error"]:
                print(f"   错误: {result['error']}")
        
        print("\n" + "-"*60)


if __name__ == "__main__":
    main()

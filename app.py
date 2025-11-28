"""
剪纸大师 (Papercraft Maestro) - Flask 后端
提供 Web API 和页面路由
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
from PIL import Image
import time
import webbrowser
import threading
import signal
import sys
from werkzeug.utils import secure_filename

# 导入剪纸生成模块
try:
    from comfy_api import ComfyUIManager, find_comfyui_address
    from Image_Processing import desaturate_image, increase_contrast, remove_white_background, convert_to_red
    MODULES_AVAILABLE = True
except ImportError:
    print("⚠️ ComfyUI 模块未找到，将使用占位符模式")
    MODULES_AVAILABLE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['GENERATED_FOLDER'] = 'image_generated'
app.config['SCENE_FOLDER'] = 'image_in_scene'

# 确保必要的文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
os.makedirs(app.config['SCENE_FOLDER'], exist_ok=True)

# 全局ComfyUI生成器实例（复用连接和工作流）
_comfyui_manager = None
WORKFLOW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ComfyUI_Workflow", "paper_cut.json")

def get_comfyui_manager():
    """获取全局ComfyUI客户端实例（单例模式）"""
    global _comfyui_manager
    if _comfyui_manager is None and MODULES_AVAILABLE:
        _comfyui_manager = ComfyUIManager(WORKFLOW_PATH)
        print("✅ 全局 ComfyUI 客户端已初始化")
    return _comfyui_manager


@app.route('/')
def index():
    """
    首页路由 - 显示 UI_1 主界面
    """
    return render_template('index.html')


@app.route('/result')
def result():
    """
    结果页路由 - 显示 UI_2 结果界面
    """
    return render_template('result.html')


@app.route('/api/generate', methods=['POST'])
def generate_papercut():
    """
    生成剪纸图案的 API
    
    接收参数：
    - prompt: 文字描述（必填）
    - scene: 场景类型，可选值：window, wall, door（可选）
    - scene_image: 场景图片文件（可选）
    
    返回：
    - success: 是否成功
    - message: 状态消息
    - image_url: 生成图片的 URL
    - steps: 处理步骤信息
    """
    try:
        # 获取请求参数
        data = request.form
        prompt = data.get('prompt', '').strip()
        scene_type = data.get('scene', 'none')  # window, wall, door, none
        
        # 验证输入
        if not prompt:
            return jsonify({
                'success': False,
                'message': '⚠️ 请输入创意描述！'
            }), 400
        
        print(f"\n{'='*60}")
        print(f"🔵 收到生成请求")
        print(f"📝 Prompt: {prompt}")
        print(f"🏠 Scene: {scene_type}")
        print(f"{'='*60}\n")
        
        # 处理上传的场景图片（如果有）
        scene_image_path = None
        if 'scene_image' in request.files:
            file = request.files['scene_image']
            if file.filename:
                filename = secure_filename(file.filename)
                timestamp = int(time.time())
                scene_image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 
                    f"scene_{timestamp}_{filename}"
                )
                file.save(scene_image_path)
                print(f"📸 场景图片已保存: {scene_image_path}")
        
        # 如果模块可用，执行实际生成
        if MODULES_AVAILABLE:
            result = _generate_with_comfyui(prompt, scene_type, scene_image_path)
        else:
            # 占位符模式 - 返回模拟结果
            result = _generate_placeholder(prompt, scene_type)
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ 生成失败: {error_detail}")
        return jsonify({
            'success': False,
            'message': f'❌ 生成失败: {str(e)}',
            'error': error_detail
        }), 500


def _generate_with_comfyui(prompt: str, scene_type: str, scene_image_path: str = None):
    """
    使用 ComfyUI 生成剪纸图案
    
    Args:
        prompt: 用户输入的文字描述
        scene_type: 场景类型
        scene_image_path: 场景图片路径
    
    Returns:
        dict: 包含生成结果的字典
    """
    steps_info = []
    
    try:
        # 获取全局 ComfyUI 客户端（复用实例）
        steps_info.append("🎨 连接 ComfyUI 服务...")
        manager = get_comfyui_manager()
        
        if manager is None:
            return {
                'success': False,
                'message': '❌ ComfyUI 模块未加载',
                'steps': steps_info
            }
        
        # 第1步：生成初始图像
        steps_info.append("⏳ 步骤 1/5: 调用 ComfyUI Flux 模型生成图像...")
        
        # 使用新的 ComfyUIManager 生成图片
        # 注意：generate_image 已经包含了提示词拼接和随机种子设置
        raw_image_path = manager.generate_image(prompt, app.config['GENERATED_FOLDER'])
        
        if not raw_image_path:
            return {
                'success': False,
                'message': "❌ 图像生成失败: ComfyUI 未返回图片",
                'steps': steps_info
            }
        
        generated_image = Image.open(raw_image_path)
        generated_filename = os.path.basename(raw_image_path)
        
        # 第2步：去饱和
        steps_info.append("⏳ 步骤 2/5: 去饱和处理...")
        processed_image = desaturate_image(generated_image)
        
        # 第3步：增强对比度
        steps_info.append("⏳ 步骤 3/5: 增强对比度...")
        processed_image = increase_contrast(processed_image, factor=3.0)
        
        # 第4步：抠白色背景
        steps_info.append("⏳ 步骤 4/5: 抠除白色背景...")
        processed_image = remove_white_background(processed_image, threshold=230)
        
        # 第5步：转为红色
        steps_info.append("⏳ 步骤 5/5: 转换为剪纸红色...")
        processed_image = convert_to_red(processed_image)
        
        # 保存最终结果到 output 文件夹
        timestamp = int(time.time())
        output_filename = f"papercut_{timestamp}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        processed_image.save(output_path)
        
        steps_info.append("✅ 剪纸图案生成成功！")
        
        return {
            'success': True,
            'message': '✅ 剪纸图案生成成功！',
            'image_url': f'/output/{output_filename}',
            'original_image': f'/generated/{generated_filename}',
            'prompt': prompt,
            'scene_type': scene_type,
            'steps': steps_info,
            'processing_info': {
                'comfyui_image': raw_image_path,
                'final_output': output_path,
                'steps_completed': 5
            }
        }
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        steps_info.append(f"❌ 错误: {str(e)}")
        return {
            'success': False,
            'message': f'❌ 生成失败: {str(e)}',
            'steps': steps_info,
            'error': error_detail
        }


def _generate_placeholder(prompt: str, scene_type: str):
    """
    占位符模式 - 返回模拟结果
    用于在没有 ComfyUI 模块时测试前端功能
    
    Args:
        prompt: 用户输入的文字描述
        scene_type: 场景类型
    
    Returns:
        dict: 模拟的生成结果
    """
    timestamp = int(time.time())
    
    # 模拟处理步骤
    steps_info = [
        "🎨 初始化 ComfyUI 客户端...",
        "⏳ 步骤 1/5: 调用 ComfyUI Flux 模型生成图像...",
        "⏳ 步骤 2/5: 去饱和处理...",
        "⏳ 步骤 3/5: 增强对比度...",
        "⏳ 步骤 4/5: 抠除白色背景...",
        "⏳ 步骤 5/5: 转换为剪纸红色...",
        "✅ 剪纸图案生成成功！（占位符模式）"
    ]
    
    return {
        'success': True,
        'message': '✅ 剪纸图案生成成功！（占位符模式 - 请接入真实 AI 模型）',
        'image_url': '/static/images/placeholder_result.png',
        'prompt': prompt,
        'scene_type': scene_type,
        'steps': steps_info,
        'placeholder_mode': True,
        'processing_info': {
            'note': '这是占位符模式，请接入 ComfyUI 模块以启用真实生成功能'
        }
    }


@app.route('/output/<filename>')
def serve_output(filename):
    """
    提供处理后的图片文件
    """
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], filename),
        mimetype='image/png'
    )


@app.route('/generated/<filename>')
def serve_generated(filename):
    """
    提供ComfyUI生成的原始图片文件
    """
    return send_file(
        os.path.join(app.config['GENERATED_FOLDER'], filename),
        mimetype='image/png'
    )


@app.route('/scene/<filename>')
def serve_scene(filename):
    """
    提供场景合成图片文件
    """
    return send_file(
        os.path.join(app.config['SCENE_FOLDER'], filename),
        mimetype='image/png'
    )


@app.route('/api/render_scene', methods=['POST'])
def render_scene():
    """
    将剪纸图片合成到场景图片上
    
    接收参数：
    - papercut_image: 剪纸图片的文件名或URL
    - scene_type: 场景类型 (window, wall, door)
    
    返回：
    - success: 是否成功
    - message: 状态消息
    - scene_image_url: 合成后的场景图片URL
    """
    try:
        data = request.json
        papercut_url = data.get('papercut_image', '')
        scene_type = data.get('scene_type', 'window')
        
        if not papercut_url:
            return jsonify({
                'success': False,
                'message': '⚠️ 缺少剪纸图片参数'
            }), 400
        
        print(f"\n{'='*60}")
        print(f"🎬 收到场景渲染请求")
        print(f"🖼️ 剪纸图片: {papercut_url}")
        print(f"🏠 场景类型: {scene_type}")
        print(f"{'='*60}\n")
        
        # 加载剪纸图片
        if papercut_url.startswith('/output/'):
            papercut_filename = papercut_url.replace('/output/', '')
            papercut_path = os.path.join(app.config['OUTPUT_FOLDER'], papercut_filename)
        else:
            return jsonify({
                'success': False,
                'message': '❌ 无效的图片路径'
            }), 400
        
        if not os.path.exists(papercut_path):
            return jsonify({
                'success': False,
                'message': '❌ 剪纸图片不存在'
            }), 404
        
        # 加载场景背景图片
        scene_filename = f'Prototype_Window.jpg' if scene_type == 'window' else f'{scene_type.capitalize()}.jpg'
        scene_path = os.path.join('Assets', 'Prototype_Images', scene_filename)
        
        if not os.path.exists(scene_path):
            return jsonify({
                'success': False,
                'message': f'❌ 场景图片不存在: {scene_filename}'
            }), 404
        
        # 合成图片
        print(f"🔧 开始合成图片...")
        result = _composite_scene(papercut_path, scene_path, scene_type)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ 场景渲染失败: {error_detail}")
        return jsonify({
            'success': False,
            'message': f'❌ 场景渲染失败: {str(e)}',
            'error': error_detail
        }), 500


def _apply_color_and_opacity(image: Image.Image, color: tuple = (152, 0, 21), opacity: float = 0.75) -> Image.Image:
    """
    应用指定颜色和透明度到图片
    
    Args:
        image: 输入图片（RGBA）
        color: RGB颜色元组，默认为(152, 0, 21) = #980015
        opacity: 透明度，0.0-1.0，默认为0.75 (75%)
    
    Returns:
        处理后的图片
    """
    import numpy as np
    
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


def _composite_scene(papercut_path: str, scene_path: str, scene_type: str):
    """
    合成剪纸图片到场景背景上
    
    Args:
        papercut_path: 剪纸图片路径
        scene_path: 场景背景图片路径
        scene_type: 场景类型
    
    Returns:
        dict: 包含合成结果的字典
    """
    try:
        # 加载图片
        papercut = Image.open(papercut_path).convert('RGBA')
        scene = Image.open(scene_path).convert('RGB')
        
        print(f"📐 原始剪纸尺寸: {papercut.size}")
        print(f"📐 场景尺寸: {scene.size}")
        
        # 调整剪纸尺寸为1736x1736
        print("🔄 调整剪纸尺寸到1736x1736...")
        papercut = papercut.resize((1736, 1736), Image.Resampling.LANCZOS)
        
        # 应用颜色和透明度处理：#980015, 75%透明度
        print("🎨 应用颜色(#980015)和透明度(75%)...")
        papercut = _apply_color_and_opacity(papercut, color=(152, 0, 21), opacity=0.75)
        
        print(f"📐 处理后剪纸尺寸: {papercut.size}")
        
        # 设置位置到右上部分
        x = 2890
        y = 137
        
        print(f"📍 放置位置: ({x}, {y})")
        print(f"📐 场景尺寸: {scene.size}")
        
        # 将场景转换为RGBA以支持透明度合成
        scene_rgba = scene.convert('RGBA')
        
        # 创建新图层用于合成
        composite = Image.new('RGBA', scene_rgba.size, (255, 255, 255, 0))
        composite.paste(scene_rgba, (0, 0))
        
        # 将剪纸粘贴到场景上（使用alpha通道）
        composite.paste(papercut, (x, y), papercut)
        
        # 转换回RGB保存
        final_image = composite.convert('RGB')
        
        # 保存合成图片
        timestamp = int(time.time())
        output_filename = f"scene_{scene_type}_{timestamp}.png"
        output_path = os.path.join(app.config['SCENE_FOLDER'], output_filename)
        final_image.save(output_path, 'PNG')
        
        print(f"✅ 场景合成成功")
        print(f"💾 保存位置: {output_path}")
        print(f"📊 文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
        
        return {
            'success': True,
            'message': '✅ 场景渲染成功！',
            'scene_image_url': f'/scene/{output_filename}',
            'scene_type': scene_type,
            'output_path': output_path
        }
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ 合成失败: {error_detail}")
        return {
            'success': False,
            'message': f'❌ 合成失败: {str(e)}',
            'error': error_detail
        }


@app.route('/api/download/<filename>')
def download_image(filename):
    """
    下载生成的剪纸图片
    """
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=f"papercut_{int(time.time())}.png"
            )
        else:
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'下载失败: {str(e)}'
        }), 500


@app.route('/api/health')
def health_check():
    """
    健康检查接口
    """
    return jsonify({
        'status': 'ok',
        'modules_available': MODULES_AVAILABLE,
        'comfyui_connected': _check_comfyui_connection() if MODULES_AVAILABLE else False
    })


@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """
    关闭服务器接口
    当浏览器标签页关闭时被调用
    """
    print("\n" + "="*60)
    print("🛑 收到关闭请求,正在停止服务器...")
    print("="*60)
    
    # 使用 werkzeug 的 shutdown 函数
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # 如果无法获取 shutdown 函数,使用 os._exit
        threading.Thread(target=lambda: (time.sleep(0.5), os._exit(0))).start()
    else:
        func()
    
    return jsonify({'success': True, 'message': '服务器即将关闭'})


def _check_comfyui_connection():
    """检查 ComfyUI 连接状态"""
    try:
        # 如果 manager 已初始化，使用它的地址
        if _comfyui_manager:
            target_url = _comfyui_manager.server_address
        else:
            # 否则尝试检测
            target_url = find_comfyui_address()
            
        # 验证连接
        import requests
        response = requests.get(f"{target_url}/system_stats", timeout=1)
        return response.status_code == 200
    except:
        return False


def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)  # 等待服务器启动
    webbrowser.open('http://localhost:5001')


def signal_handler(sig, frame):
    """处理 Ctrl+C 信号"""
    print("\n" + "="*60)
    print("👋 正在关闭服务器...")
    print("="*60)
    sys.exit(0)


if __name__ == '__main__':
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n" + "="*60)
    print("🎨 剪纸大师 (Papercraft Maestro) - Flask 服务器启动中...")
    print("="*60)
    print(f"📦 模块状态: {'✅ 已加载' if MODULES_AVAILABLE else '⚠️ 占位符模式'}")
    print(f"🌐 访问地址: http://localhost:5001")
    print(f"💡 提示: 关闭浏览器标签页后,请按 Ctrl+C 停止服务器")
    print("="*60 + "\n")
    
    # 在新线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动 Flask 服务器
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True,
        use_reloader=False  # 禁用重载器,避免浏览器被打开两次
    )

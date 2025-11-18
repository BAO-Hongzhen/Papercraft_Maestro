"""
Syntax Roulette - 主程序
语法轮盘：从词库抽取单词组成句子，AI生成GIF动图

架构：
- word_bank.py: 词库管理
- comfyui_api.py: ComfyUI API调用
- gradio_ui.py: Web界面
"""

from word_bank import WordBank
from comfyui_api import ComfyUIClient
from gradio_ui import GradioInterface


def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🎲 Syntax Roulette - 语法轮盘 🎲                 ║
║                                                              ║
║          Random Words → Creative Sentences → GIF Art        ║
║          随机词语 → 创意句子 → GIF动图                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    dependencies = {
        'gradio': 'Gradio',
        'PIL': 'Pillow',
        'requests': 'Requests'
    }
    
    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - 未安装")
            missing.append(name.lower())
    
    if missing:
        print(f"\n⚠️  缺少依赖，请运行: pip install {' '.join(missing)}")
        return False
    
    print("✅ 所有依赖已就绪\n")
    return True


def initialize_components():
    """初始化各个组件"""
    print("🚀 初始化组件...\n")
    
    # 1. 初始化词库
    print("📚 初始化词库...")
    word_bank = WordBank(data_dir="data")
    word_bank.print_statistics()
    
    # 2. 初始化ComfyUI客户端
    print("🔌 初始化ComfyUI客户端...")
    comfyui_client = ComfyUIClient(server_address="127.0.0.1:8000")
    print(f"   服务器地址: {comfyui_client.base_url}")
    print(f"   客户端ID: {comfyui_client.client_id}")
    
    # 测试连接（不阻塞启动）
    print("\n🔗 测试ComfyUI连接...")
    if comfyui_client.test_connection():
        print("   ✅ ComfyUI已连接，可以生成真实动图")
    else:
        print("   ⚠️  ComfyUI未运行，将使用演示模式")
        print("   💡 启动ComfyUI: 在ComfyUI目录运行 python main.py")
    
    print()
    
    # 3. 初始化Gradio界面
    print("🎨 初始化Web界面...")
    gradio_interface = GradioInterface(word_bank, comfyui_client)
    app = gradio_interface.create_interface()
    print("   ✅ 界面创建成功\n")
    
    return app


def main():
    """主函数"""
    # 打印横幅
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        input("\n按回车键退出...")
        return
    
    # 初始化组件
    try:
        app = initialize_components()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return
    
    # 启动应用
    print("=" * 64)
    print("🌐 启动Web服务器...")
    print("=" * 64)
    print()
    
    try:
        app.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True,
            quiet=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")


if __name__ == "__main__":
    main()

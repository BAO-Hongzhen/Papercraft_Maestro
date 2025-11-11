# 🎲 Syntax Roulette - 语法轮盘

> 从词库随机抽取单词，组成创意句子，AI生成GIF动图

## 🎯 项目概述

Syntax Roulette 是一个创意工具，它结合了随机语法生成和AI图像生成技术：

1. **随机抽词**: 从词库中随机抽取各类词语
2. **组成句子**: 按语法规则组合成完整句子
3. **生成动图**: 将句子作为提示词，AI生成GIF动画

## ✨ 功能特点

- 🎲 **随机句子生成**: 支持简单句式和详细句式
- 🎨 **AI动图创作**: 通过ComfyUI生成高质量GIF
- 🌐 **Web界面**: 美观易用的Gradio界面
- 📚 **词库管理**: 可自定义和扩展词库
- 🔄 **双模式**: 演示模式 + ComfyUI真实生成

## 🏗️ 项目架构

```
syntax_gif_generator/
├── main.py                    # 主程序入口
├── modules/                   # 功能模块
│   ├── word_bank.py          # 词库管理模块
│   ├── comfyui_api.py        # ComfyUI API调用模块
│   └── gradio_ui.py          # Gradio网页界面模块
├── data/                      # 词库数据目录
├── output/                    # 生成的GIF输出目录
└── requirements.txt           # 依赖包列表
```

### 架构说明

#### 模块化设计

1. **word_bank.py - 词库模块**
   - 管理各类词语（主语、动词、宾语等）
   - 提供随机抽取功能
   - 支持多种句式模板
   - 可扩展词库

2. **comfyui_api.py - API调用模块**
   - 封装ComfyUI API
   - 处理工作流提交
   - 跟踪生成进度
   - 获取生成结果

3. **gradio_ui.py - 界面模块**
   - 构建Web界面
   - 处理用户交互
   - 展示生成结果
   - 管理历史记录

4. **main.py - 主程序**
   - 初始化各模块
   - 协调模块交互
   - 启动Web服务

## 🚀 快速开始

### 方法1: 使用批处理文件（Windows推荐）

1. 双击 `启动应用.bat`
2. 等待自动安装依赖和启动
3. 浏览器自动打开应用

### 方法2: 命令行启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
python main.py
```

应用会在浏览器中自动打开：`http://localhost:7860`

## 📖 使用指南

### 基本流程

1. **生成句子**
   - 选择句式（简单/详细）
   - 点击"随机生成句子"
   - 查看生成的句子和结构

2. **生成GIF**
   - 调整参数（尺寸、帧数等）
   - 选择模式（演示/ComfyUI）
   - 点击"生成GIF动图"
   - 等待生成完成

### 两种模式

#### 演示模式（默认）
- ✅ 无需ComfyUI
- ✅ 快速生成预览动画
- ✅ 测试句子生成功能
- ⚠️ 非真实AI生成

#### ComfyUI模式
- ✅ 真实AI生成
- ✅ 高质量动图
- ⚠️ 需要本地ComfyUI运行
- ⚠️ 生成时间较长

### 使用ComfyUI

1. **安装ComfyUI**
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI
   cd ComfyUI
   pip install -r requirements.txt
   ```

2. **启动ComfyUI**
   ```bash
   python main.py
   ```

3. **在应用中启用**
   - 勾选"使用ComfyUI生成"
   - 开始生成

## 🎨 句式模板

### 简单句式
```
主语 + 动词 + 宾语
例: a cat is jumping a ball
```

### 详细句式
```
形容词 + 主语 + 副词 + 动词 + 形容词 + 宾语 + 地点 + 时间
例: beautiful cat happily is jumping colorful ball in the garden at sunset
```

## 📚 词库类别

- **subjects**: 主语（人物、动物等）
- **verbs**: 动词（动作）
- **objects**: 宾语（物品）
- **adjectives**: 形容词（修饰）
- **adverbs**: 副词（修饰动作）
- **places**: 地点
- **times**: 时间

## ⚙️ 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| 宽度 | GIF宽度（像素） | 512 |
| 高度 | GIF高度（像素） | 512 |
| 帧数 | 动画帧数 | 16 |
| 帧率 | 每秒帧数 | 8 FPS |
| 负面提示词 | 不想要的元素 | blurry, bad quality |

## 🔧 自定义词库

### 通过代码添加

```python
from modules.word_bank import WordBank

word_bank = WordBank()
word_bank.add_word("subjects", "a unicorn")
word_bank.add_word("verbs", "is flying")
word_bank.save_to_file("data/my_words.json")
```

### 通过JSON文件

创建 `data/custom_words.json`:

```json
{
  "subjects": ["a dragon", "a mermaid"],
  "verbs": ["is swimming", "is breathing fire"],
  "objects": ["treasure", "coral"]
}
```

然后在代码中加载:

```python
word_bank.load_from_file("data/custom_words.json")
```

## 📊 项目特色

### ✅ 优点

1. **模块化设计**
   - 清晰的职责分离
   - 易于维护和扩展
   - 可独立测试各模块

2. **灵活的架构**
   - 支持多种句式
   - 可扩展词库
   - 双模式运行

3. **用户友好**
   - 直观的Web界面
   - 实时反馈
   - 历史记录管理

4. **可扩展性**
   - 易于添加新句式
   - 支持自定义词库
   - 可接入其他AI服务

## 🛠️ 技术栈

- **Python 3.8+**
- **Gradio**: Web界面框架
- **Pillow**: 图像处理
- **Requests**: HTTP请求
- **ComfyUI**: AI图像生成（可选）

## 📝 开发路线图

- [x] 基础词库系统
- [x] 简单句式生成
- [x] ComfyUI集成
- [x] Gradio界面
- [x] 演示模式
- [ ] 更多句式模板
- [ ] 中文词库支持
- [ ] 词库可视化编辑
- [ ] 批量生成功能
- [ ] 导出分享功能

## ❓ 常见问题

### Q: 如何添加新的句式？

A: 在 `word_bank.py` 中添加新的生成函数：

```python
def generate_custom_sentence(self):
    # 自定义逻辑
    return {"sentence": "...", "pattern": "..."}
```

### Q: ComfyUI连接失败怎么办？

A: 
1. 确认ComfyUI正在运行
2. 检查端口是否为8188
3. 查看ComfyUI终端日志
4. 使用演示模式测试

### Q: 如何修改默认参数？

A: 在 `gradio_ui.py` 中修改slider的默认值。

### Q: 生成的GIF保存在哪里？

A: 保存在 `output/` 目录下。

## 📄 许可证

本项目遵循项目根目录的许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

<div align="center">

**🎲 开始你的创意之旅！**

[快速开始](#-快速开始) · [使用指南](#-使用指南) · [常见问题](#-常见问题)

Made with ❤️ using Gradio & ComfyUI

</div>

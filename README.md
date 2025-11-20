# 🎴 Syntax Roulette - AI Image Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)

**An interactive web application that creates AI-generated images from randomly selected English words!**

Shuffle card decks, pick words from 5 syntax categories, generate creative sentences, and watch as AI transforms them into stunning images using Stable Diffusion.

> 📚 **Documentation Guide:**  
> - 🆕 **New to programming?** Start with [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)  
> - ⚡ **Just need commands?** See [QUICK_START.md](QUICK_START.md)  
> - 📖 **Want details?** Keep reading this file!

---

## 📸 What Does It Do?

1. **🎴 Shuffle & Pick Cards**: Click a button to shuffle virtual card decks and randomly pick words from 5 categories
2. **📝 Build Sentences**: Automatically generate grammatically correct English sentences
3. **🎨 Generate AI Images**: Transform your sentence into beautiful AI-generated artwork
4. **💾 Save History**: Keep track of all your creations

Perfect for: Creative writing, English learning, art generation, or just having fun!

---

## ✨ Key Features

### 🎴 **150 Curated Words**
- 5 Syntax Categories (30 words each):
  - **Subject**: People, animals, characters (e.g., cat, robot, wizard)
  - **Predicate**: Action verbs (e.g., dance, fly, paint)
  - **Attributive**: Descriptive adjectives (e.g., happy, giant, mysterious)
  - **Adverbial**: Manner adverbs (e.g., quickly, gracefully, wildly)
  - **Complement**: Objects & places (e.g., a pizza, in the forest, under the moon)

### 🎨 **AI-Powered Image Generation**
- Uses **Stable Diffusion 1.5** for high-quality image generation
- Automatic GPU detection (NVIDIA CUDA, Apple Silicon MPS, or CPU)
- Real-time progress tracking with visual updates
- Customizable generation parameters (steps, guidance, resolution)

### 🌐 **User-Friendly Interface**
- Clean, modern web interface (no coding required!)
- Animated card shuffling with visual feedback
- History gallery to browse past generations
- Helpful tooltips and documentation

### 🖥️ **Cross-Platform Support**
- ✅ **Windows** (Windows 10/11)
- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Linux** (Ubuntu, Debian, etc.)

---

## 🚀 Quick Start Guide

### For Complete Beginners

Don't worry if you've never used Python before! Just follow these simple steps:

#### **Step 1: Install Python**

**Windows:**
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.11** (or newer)
3. Run the installer
4. ⚠️ **IMPORTANT**: Check ✅ "Add Python to PATH" before clicking Install

**macOS:**
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.11** (or newer)
3. Run the installer and follow the prompts

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### **Step 2: Download This Project**

**Option A - Using Git (Recommended):**
```bash
git clone https://github.com/BAO-Hongzhen/Syntax_Roulette.git
cd Syntax_Roulette
```

**Option B - Download ZIP:**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file
4. Open Terminal/Command Prompt and navigate to the folder:
   ```bash
   cd path/to/Syntax_Roulette
   ```

#### **Step 3: Run Setup (One Time Only)**

**Windows:**
```bash
setup_windows.bat
```
Just double-click `setup_windows.bat` or run it in Command Prompt.

**macOS/Linux:**
```bash
chmod +x setup_macos.sh run_macos.sh
./setup_macos.sh
```

This will:
- ✅ Create a virtual environment
- ✅ Install all required packages
- ✅ Download AI models (~4GB, takes 5-15 minutes on first run)

#### **Step 4: Start the Application**

**Windows:**
```bash
run_windows.bat
```
Double-click `run_windows.bat` or run it in Command Prompt.

**macOS/Linux:**
```bash
./run_macos.sh
```

The web interface will automatically open in your browser at:
```
http://localhost:7860
```

If it doesn't open automatically, just copy that URL into your browser!

---

## 📖 How to Use the App

### Basic Workflow

1. **🎴 Shuffle Cards**
   - Click "🎴 Shuffle & Pick Cards"
   - Watch as the app shuffles virtual decks and picks random words
   - See your selected words appear in 5 boxes

2. **✏️ Customize (Optional)**
   - Don't like a word? Just type a new one in any box!
   - Edit any category to personalize your sentence

3. **📝 Generate Sentence**
   - Click "📝 Generate Sentence"
   - The app creates a grammatically correct English sentence
   - Example: *"A happy robot is quickly dancing in a magical garden."*

4. **🎨 Generate Image**
   - Click "🎨 Generate Image"
   - Watch the progress bar as AI creates your image
   - **First time**: Takes 5-15 minutes to download models
   - **Subsequent runs**: Takes 30-60 seconds per image

5. **💾 View History**
   - All your creations are saved automatically
   - Click "📚 Generation History" to see past images
   - Each image shows the seed number for reproducibility

### Advanced Settings

Click "⚙️ Image Generation Settings" to customize:

- **Negative Prompt**: Tell AI what NOT to include (e.g., "blurry, ugly")
- **Width/Height**: Image size (512x512 recommended)
- **Inference Steps**: 
  - 20 steps = Fast (30 seconds)
  - 35 steps = High quality (60 seconds)
- **Guidance Scale**: How strictly to follow prompt (7.5 recommended)
- **Random Seed**: Uncheck to reproduce exact same image

---

## 🛠️ System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher (3.11 recommended)
- **RAM**: 8 GB (16 GB recommended)
- **Storage**: 10 GB free space (for models)
- **Internet**: Required for initial model download

### Recommended for Best Performance
- **GPU**: NVIDIA GPU with 6GB+ VRAM, or Apple Silicon Mac
- **RAM**: 16 GB or more
- **Storage**: SSD with 15 GB free space

### GPU Support
The app automatically detects and uses:
- ✅ **NVIDIA GPU** (CUDA) - Windows/Linux
- ✅ **Apple Silicon** (MPS) - M1/M2/M3 Macs
- ✅ **CPU Fallback** - Works on any computer (slower)

---

## 📁 Project Structure

```
Syntax_Roulette/
│
├── 📄 README.md                    # This file
├── 📄 QUICK_START.md              # Quick reference guide
├── 📄 BEGINNER_GUIDE.md           # Beginner's installation guide
│
├── 🐍 main.py                     # Main application
├── 🐍 word_banks.py              # Word categories (150 words)
├── 🐍 image_generator.py         # AI image generation
│
├── 📦 requirements.txt            # Python dependencies
│
├── 🪟 setup_windows.bat          # Windows setup script
├── 🪟 run_windows.bat            # Windows run script
│
├── 🍎 setup_macos.sh             # macOS/Linux setup script
├── 🍎 run_macos.sh               # macOS/Linux run script
│
├── 📁 output/                     # Generated images (auto-created)
├── 📁 .venv/                      # Virtual environment (auto-created)
└── 📁 .git/                       # Git repository files
```

---

## ❓ Troubleshooting

### Common Issues

#### **Problem: "Python is not recognized"**
**Solution**: 
- Reinstall Python and check ✅ "Add Python to PATH"
- Or add Python manually to PATH (Google: "add python to path [your OS]")

#### **Problem: Setup script fails**
**Solution**:
```bash
# Try manual installation
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### **Problem: "Out of memory" error**
**Solution**:
- Reduce image size to 256x256 or 384x384
- Reduce inference steps to 20
- Close other applications
- Restart your computer

#### **Problem: Very slow generation**
**Solution**:
- This is normal on CPU (can take 2-5 minutes)
- Consider using a GPU if available
- Reduce image size and steps for faster results

#### **Problem: macOS "command not found"**
**Solution**:
```bash
chmod +x setup_macos.sh run_macos.sh
./setup_macos.sh
```

#### **Problem: Windows "Access Denied"**
**Solution**:
- Right-click on `.bat` files
- Select "Run as Administrator"

#### **Problem: Black images on macOS**
**Solution**:
- This is automatically handled for Apple Silicon
- If issues persist, update to latest macOS version

### Getting Help

1. **Check Documentation**: Read `QUICK_START.md` and `DOCUMENTATION_SUMMARY.md`
2. **Search Issues**: Visit the [GitHub Issues](https://github.com/BAO-Hongzhen/Syntax_Roulette/issues) page
3. **Ask Questions**: Open a new issue with:
   - Your operating system
   - Python version (`python --version`)
   - Error messages (copy full text)
   - Steps you've tried

---

## 🎓 Usage Tips

### Creating Better Images

1. **Be Specific**: More details = better results
   - ❌ "cat"
   - ✅ "fluffy orange cat sitting on a velvet cushion"

2. **Use Style Keywords**: Add artistic styles
   - "photorealistic"
   - "oil painting"
   - "anime style"
   - "watercolor"
   - "3D render"

3. **Negative Prompts**: List what you DON'T want
   - "blurry, low quality, distorted, disfigured"
   - "extra limbs, mutated, bad anatomy"

4. **Experiment with Settings**:
   - More steps (30-40) = Better quality, slower
   - Higher guidance (10-12) = Follows prompt more strictly
   - Random seed = Get different variations

### Example Sentences

Here are some great example sentences:

1. *"A majestic dragon gracefully flies over ancient mountains at sunset."*
2. *"The wise wizard carefully creates magical crystals in a mystical forest."*
3. *"A cute robot happily dances with colorful balloons in a futuristic city."*
4. *"The brave knight quickly rides through dangerous caverns under the moon."*
5. *"A tiny fairy gently paints beautiful flowers in an enchanted garden."*

---

## 🔧 Advanced Configuration

### Changing AI Models

To use a different Stable Diffusion model:

1. Open `image_generator.py`
2. Find line ~22:
   ```python
   self.model_id = "runwayml/stable-diffusion-v1-5"
   ```
3. Replace with your preferred model:
   ```python
   self.model_id = "stabilityai/stable-diffusion-2-1"
   ```

Popular models:
- `runwayml/stable-diffusion-v1-5` (default, best compatibility)
- `stabilityai/stable-diffusion-2-1` (newer, higher quality)
- `dreamlike-art/dreamlike-photoreal-2.0` (photorealistic)

### Adding Custom Words

To add your own words:

1. Open `word_banks.py`
2. Find the category you want to edit (e.g., `self.subject`)
3. Add words to the list (keep 30 words per category)
4. Save and restart the application

### Performance Tuning

Edit these values in the web interface settings:

- **Fast Mode**: 256x256, 20 steps, 7.0 guidance (~15 seconds)
- **Balanced**: 512x512, 25 steps, 7.5 guidance (~30 seconds)
- **Quality Mode**: 768x768, 35 steps, 9.0 guidance (~90 seconds)

---

## 📝 Technical Details

### Dependencies

Main packages (automatically installed):
- `gradio` - Web interface
- `torch` - Deep learning framework
- `diffusers` - Stable Diffusion pipeline
- `transformers` - AI model support
- `Pillow` - Image processing
- `accelerate` - GPU optimization

### GPU Acceleration

The application automatically detects your hardware:

```python
# NVIDIA GPU (Windows/Linux)
if torch.cuda.is_available():
    device = "cuda"
    
# Apple Silicon (M1/M2/M3 Macs)
elif torch.backends.mps.is_available():
    device = "mps"
    
# CPU Fallback
else:
    device = "cpu"
```

### Platform-Specific Optimizations

- **Windows/NVIDIA**: Uses `torch.float16` for memory efficiency
- **macOS/Apple Silicon**: Uses `torch.float32` (required for MPS)
- **CPU**: Uses `torch.float32` with special attention mechanisms

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- Add more word categories
- Improve sentence generation logic
- Support for more languages
- Additional AI models
- UI/UX improvements
- Performance optimizations

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stable Diffusion** by Stability AI - Core image generation
- **Gradio** - Web interface framework
- **Hugging Face** - AI model hosting and diffusers library
- **PyTorch** - Deep learning framework

---

## 📮 Contact

- **GitHub**: [BAO-Hongzhen](https://github.com/BAO-Hongzhen)
- **Project**: [Syntax_Roulette](https://github.com/BAO-Hongzhen/Syntax_Roulette)
- **Issues**: [Report a bug](https://github.com/BAO-Hongzhen/Syntax_Roulette/issues)

---

## 🎉 Happy Creating!

Thank you for using Syntax Roulette! We hope you create amazing images and have fun exploring the intersection of language and AI art.

**Remember**: The first run takes longer (model download), but subsequent runs start instantly!

---

**Made with ❤️ by the Syntax Roulette Team**

*Last Updated: November 2025*

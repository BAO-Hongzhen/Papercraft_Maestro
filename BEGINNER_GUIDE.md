# 🎓 Beginner's Installation Guide

**New to programming? No problem!** This guide will walk you through every step.

---

## 📋 What You'll Need

- A computer (Windows, macOS, or Linux)
- Internet connection
- About 30 minutes for first-time setup
- 10 GB free disk space

---

## Step 1: Install Python

### Why Python?
Python is the programming language this application runs on. Think of it like installing Microsoft Office before you can use Word.

### Windows Installation

1. **Download Python**:
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click the big yellow "Download Python 3.11" button
   - Save the file (it's about 25 MB)

2. **Install Python**:
   - Find the downloaded file (usually in "Downloads" folder)
   - Double-click to run the installer
   - ⚠️ **IMPORTANT**: Check the box that says **"Add Python to PATH"**
   - Click "Install Now"
   - Wait for installation to complete (takes 2-3 minutes)
   - Click "Close" when done

3. **Verify Installation**:
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - In the black window, type: `python --version`
   - You should see something like: `Python 3.11.5`
   - If you see an error, restart your computer and try again

### macOS Installation

1. **Download Python**:
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click the big yellow "Download Python 3.11" button
   - Save the file

2. **Install Python**:
   - Find the downloaded `.pkg` file
   - Double-click to open
   - Click "Continue" through all the screens
   - Enter your Mac password when asked
   - Click "Install"
   - Wait for installation (takes 2-3 minutes)
   - Click "Close" when done

3. **Verify Installation**:
   - Open "Terminal" (Command + Space, type "Terminal", press Enter)
   - Type: `python3 --version`
   - You should see: `Python 3.11.5` (or similar)

### Linux Installation

Open Terminal and run:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

---

## Step 2: Download the Project

### Option A: Using Git (Recommended)

**What is Git?** It's a tool for downloading code projects.

1. **Install Git**:
   - **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
   - **macOS**: Open Terminal and type: `git --version` (it will auto-install)
   - **Linux**: `sudo apt install git`

2. **Download the Project**:
   ```bash
   # Open Terminal (macOS/Linux) or Command Prompt (Windows)
   cd Desktop
   git clone https://github.com/BAO-Hongzhen/Syntax_Roulette.git
   cd Syntax_Roulette
   ```

### Option B: Download ZIP (Easier for beginners)

1. Go to [github.com/BAO-Hongzhen/Syntax_Roulette](https://github.com/BAO-Hongzhen/Syntax_Roulette)
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to your Desktop
5. Remember where you extracted it!

---

## Step 3: Open Terminal/Command Prompt in Project Folder

This is where many beginners get stuck. Here's how:

### Windows

1. Open File Explorer
2. Navigate to where you extracted the project (e.g., `C:\Users\YourName\Desktop\Syntax_Roulette`)
3. Click in the address bar at the top
4. Type `cmd` and press Enter
5. A black window (Command Prompt) will open in that folder

**Alternative**:
- Right-click in the folder while holding Shift
- Select "Open PowerShell window here" or "Open in Terminal"

### macOS

1. Open Finder
2. Navigate to the project folder
3. Right-click the folder
4. Hold `Option` key
5. Select "Copy 'Syntax_Roulette' as Pathname"
6. Open Terminal (Command + Space, type "Terminal")
7. Type `cd ` (with a space after cd)
8. Press `Command + V` to paste the path
9. Press Enter

**Alternative**:
- Open Terminal
- Type `cd ` (with space)
- Drag the folder from Finder into Terminal
- Press Enter

### Linux

- Right-click in the folder
- Select "Open in Terminal"

---

## Step 4: Run the Setup Script

**This only needs to be done once!** The setup script will:
- Create a safe, isolated environment for the app
- Download all required libraries
- Download the AI model (~4GB)

### Windows

In the Command Prompt window from Step 3, type:
```bash
setup_windows.bat
```
Press Enter.

### macOS/Linux

In the Terminal window from Step 3, type:
```bash
chmod +x setup_macos.sh run_macos.sh
./setup_macos.sh
```

### What to Expect

- You'll see lots of text scrolling by - **this is normal!**
- The first download takes 5-15 minutes (downloading AI model)
- Total setup time: 10-20 minutes
- If you see errors about "permission denied", try running as administrator

**⚠️ Common Issues**:

- **"Python not found"**: You didn't check "Add Python to PATH" during installation. Reinstall Python.
- **"Permission denied"**: Right-click the script and select "Run as Administrator" (Windows) or use `sudo` (macOS/Linux)
- **Network error**: Check your internet connection

---

## Step 5: Run the Application

Every time you want to use the app:

### Windows
```bash
run_windows.bat
```

### macOS/Linux
```bash
./run_macos.sh
```

### What Happens

1. A web browser will open automatically
2. You'll see the Syntax Roulette interface
3. If the browser doesn't open, manually go to: `http://localhost:7860`

### First Run Only

- The **very first time**, the app downloads AI models (~4GB)
- This takes 5-15 minutes depending on your internet
- You'll see a progress bar
- **After the first time, the app starts in 10-30 seconds!**

---

## Step 6: Start Creating!

### Basic Workflow

1. **Click "🎴 Shuffle & Pick Cards"**
   - Randomly selects 5 words
   - Watch the fun animation

2. **Click "📝 Generate Sentence"**
   - Creates a grammatically correct sentence
   - Example: *"A happy robot is carefully dancing in a garden."*

3. **Click "🎨 Generate Image"**
   - Waits 30-60 seconds
   - Creates an AI image based on your sentence
   - Image appears below

4. **Save Your Work**
   - Images auto-save to the `output/` folder
   - Click "📚 Generation History" to see all past creations

---

## 🆘 Troubleshooting

### "Python is not recognized"

**Problem**: Windows can't find Python

**Solution**:
1. Uninstall Python
2. Reinstall Python
3. **Make sure to check ✅ "Add Python to PATH"**
4. Restart your computer

### "Virtual environment not found"

**Problem**: Setup didn't complete

**Solution**:
```bash
# Delete the .venv folder if it exists
# Then run setup again:
setup_windows.bat    # Windows
./setup_macos.sh     # macOS/Linux
```

### "Out of memory"

**Problem**: Your computer doesn't have enough RAM

**Solution**:
1. Close all other programs
2. Reduce image size in settings:
   - Change from 512x512 to 256x256
   - Reduce steps from 25 to 15
3. Restart your computer and try again

### Very Slow Image Generation

**Expected Behavior**:
- **With GPU** (NVIDIA or Apple Silicon): 10-30 seconds
- **Without GPU** (CPU only): 2-5 minutes

**This is normal!** AI image generation is computationally intensive.

**To Speed Up**:
- Reduce image size to 256x256
- Reduce steps to 15-20
- Close other programs

### Application Won't Start

**Solution**:
1. Make sure you're in the correct folder
2. Run the setup script again
3. Check for error messages and search them online
4. Ask for help (see below)

---

## 📞 Getting Help

### Before Asking for Help

1. Read this guide carefully
2. Check the error message
3. Try searching the error on Google
4. Restart your computer

### Where to Ask

**GitHub Issues**: [github.com/BAO-Hongzhen/Syntax_Roulette/issues](https://github.com/BAO-Hongzhen/Syntax_Roulette/issues)

When asking for help, include:
- Your operating system (Windows 10/11, macOS version, Linux distro)
- Python version (`python --version`)
- **Full error message** (copy all text)
- What you tried
- Screenshots (if applicable)

### Example Good Question

> **Title**: "Setup fails on Windows 11 with 'Permission denied' error"
> 
> **Description**:
> - OS: Windows 11
> - Python version: 3.11.5
> - Error: When I run `setup_windows.bat`, I get "Permission denied"
> - I tried: Running as Administrator
> - Screenshot: [attached]

---

## 🎉 You're Ready!

Congratulations! You've successfully installed Syntax Roulette. Now go create some amazing AI art!

### Quick Tips

- **First image is always slow** (5-15 min for model download)
- **Save your favorites** (check the `output/` folder)
- **Experiment with settings** (try different sizes and steps)
- **Share your creations** (tag us on social media!)

### Next Steps

- Read `README.md` for detailed features
- Check `QUICK_START.md` for quick reference
- Explore the settings to customize your images
- Join our community on GitHub

---

**Made with ❤️ for beginners by the Syntax Roulette Team**

*Remember: Everyone was a beginner once. Don't be afraid to ask questions!*

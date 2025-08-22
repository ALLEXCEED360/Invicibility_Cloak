# 🪄 Harry Potter Invisibility Cloak

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A real-time invisibility cloak effect using computer vision with OpenCV and Python. Step into the world of Harry Potter and experience magic through the power of programming!

![Invisibility Cloak Demo](Demo%20Gif/im-invisible-invisible.gif)

## ✨ Features

- 🎭 **Real-time Invisibility Effect** - Become invisible in real-time using your webcam
- 🎨 **Multiple Color Presets** - Support for red, blue, green, and yellow cloaks
- 🔧 **Live HSV Tuning** - Real-time color calibration with interactive sliders
- 🎥 **Video Recording** - Record your magical moments with timestamps
- 📊 **Performance Monitoring** - Built-in FPS counter and system status
- 🎮 **Interactive Controls** - Easy-to-use keyboard shortcuts
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 📱 **Smart Background Capture** - Intelligent background averaging for stability
- 🔊 **User-Friendly Interface** - Clear instructions and visual feedback

## 🎬 How It Works

The invisibility cloak uses computer vision techniques to create a real-time masking effect:

1. **Background Capture**: Records a clean background image by averaging multiple frames
2. **Color Detection**: Uses HSV color space to detect the cloak color with high precision
3. **Mask Creation**: Creates a binary mask identifying cloak areas using morphological operations
4. **Image Compositing**: Seamlessly replaces cloak pixels with the pre-recorded background
5. **Real-time Processing**: Applies the effect in real-time at 30+ FPS

```
Original Frame + Background → HSV Conversion → Color Masking → Morphological Ops → Final Composite
```

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Webcam (built-in or external)
- Good lighting conditions

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ALLEXCEED360/Invicibility_Cloak.git
cd Invisibility_Cloak
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python invisibility_cloak.py
```

4. **Start the magic!**
   - Press **'B'** to capture background (step out of frame first!)
   - Put on a **red cloth/shirt**
   - Watch yourself become invisible! ✨

## 🎮 Controls Reference

| Key | Action | Description |
|-----|--------|-------------|
| **B** | 📸 Capture Background | Step out of frame and press to record background |
| **R** | 🎥 Record Video | Start/stop recording (saves as MP4 with timestamp) |
| **C** | 🎨 Cycle Colors | Switch between red → blue → green → yellow |
| **T** | 🔧 HSV Tuner | Open color calibration window with sliders |
| **S** | 💾 Save Settings | Save current HSV settings to file |
| **SPACE** | 🔄 Reset Background | Clear current background |
| **Q/ESC** | 🚪 Quit | Exit the application |

## 🎯 Usage Guide

### Step 1: Setup Your Environment
- Position your camera at eye level
- Ensure good, even lighting (avoid harsh shadows)
- Choose a complex background (not a plain wall)

### Step 2: Capture Background
```bash
# The app will guide you through this process
1. Run: python invisibility_cloak.py
2. Step completely out of camera view
3. Press 'B' key
4. Wait for 3-2-1 countdown
5. Background captured! ✅
```

### Step 3: Put On Your Cloak
- Use **solid-colored cloth** (red works best)
- Avoid wrinkled or folded materials
- Cover the body parts you want to make invisible

### Step 4: Fine-tune (Optional)
- Press **'T'** to open HSV tuner
- Adjust sliders until your cloak appears white in the mask
- Press **'S'** to save your custom settings

## 🎨 Color Presets

The application comes with optimized presets for different cloak colors:

| Color | HSV Range | Best Use Case |
|-------|-----------|---------------|
| **Red** 🔴 | H: 0-10, 170-180 | Default, works in most lighting |
| **Blue** 🔵 | H: 100-130 | Good for outdoor scenes |
| **Green** 🟢 | H: 40-80 | Avoid green backgrounds |
| **Yellow** 🟡 | H: 20-30 | Bright lighting conditions |

## 🛠️ Advanced Usage

### Command Line Options

```bash
# Basic usage
python invisibility_cloak.py

# Use different camera
python invisibility_cloak.py --cam 1

# Start with blue preset
python invisibility_cloak.py --color blue

# Custom resolution (for performance tuning)
python invisibility_cloak.py --width 640 --height 480

# All options combined
python invisibility_cloak.py --cam 1 --color green --width 1920 --height 1080
```

### Custom Color Configuration

Create your own color presets by modifying the HSV ranges:

```python
# Add to COLOR_PRESETS in the code
"purple": {
    "ranges": [
        (np.array([120, 50, 50]), np.array([150, 255, 255]))
    ],
    "description": "Purple cloth/clothing"
}
```

### Performance Optimization

For older computers or lower-end hardware:

```bash
# Reduce resolution
python invisibility_cloak.py --width 640 --height 480

# Or even lower
python invisibility_cloak.py --width 320 --height 240
```

## 📁 Project Structure

```
invisibility-cloak/
├── 📄 invisibility_cloak.py    # Main application
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md               # This file
├── 📄 camera_test.py          #Test your webcam 
├── 📄 run_demo.py             #Run Project using optimal settings 
├── 📄 .gitignore             # Git ignore rules
├── 📄 LICENSE                # MIT license
├── 📂 Demo Gif/              # Demo materials
│   ├── 🎬 im-invisible-invisible.gif
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 🚫 "Cannot open camera"
```bash
# Try different camera indices
python invisibility_cloak.py --cam 1
python invisibility_cloak.py --cam 2

# Check available cameras
python test_setup.py
```

#### 📉 Low FPS / Poor Performance
```bash
# Use lower resolution
python invisibility_cloak.py --width 640 --height 480

# Close other applications using the camera
# Ensure good lighting to reduce processing load
```

#### 🎭 Cloak Not Detected Properly
1. **Lighting**: Ensure even lighting without harsh shadows
2. **Color**: Use solid, vibrant colors (avoid patterns)
3. **Tuning**: Press 'T' to open HSV tuner and adjust
4. **Material**: Avoid shiny or reflective materials

#### 🖥️ ImportError for OpenCV or NumPy
```bash
# Reinstall dependencies
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python

# For conda users
conda install opencv numpy
```

#### 🎥 Video Recording Issues
- Ensure you have write permissions in the directory
- Check available disk space
- Try different video codecs if issues persist

### System Requirements

**Minimum:**
- Python 3.6+
- 2GB RAM
- Basic webcam (480p)
- 1 GHz processor

**Recommended:**
- Python 3.8+
- 4GB+ RAM
- HD webcam (720p+)
- Multi-core processor
- Good lighting setup

## 🎓 Educational Value

This project demonstrates several important computer vision concepts:

- **Color Space Conversion** (BGR ↔ HSV)
- **Image Masking and Bitwise Operations**
- **Morphological Operations** (Opening, Dilation)
- **Real-time Video Processing**
- **Background Subtraction Techniques**
- **Contour Detection and Filtering**

Perfect for:
- 📚 Computer Vision students
- 👩‍💻 OpenCV beginners
- 🎭 Interactive art projects
- 🎃 Halloween enthusiasts
- 📹 Content creators

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Bug Reports
- Use the issue tracker to report bugs
- Include Python version, OS, and camera details
- Provide steps to reproduce the issue

### 💡 Feature Requests
- Suggest new features or improvements
- Explain the use case and expected behavior
- Check existing issues to avoid duplicates

### 🔧 Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with proper documentation
4. Test thoroughly across different environments
5. Submit a pull request with clear description

### 💭 Ideas for Contributions
- 🌈 Additional visual effects (color changing, transparency)
- 📱 Mobile app version (Android/iOS)
- 🌐 Web-based version using WebRTC
- 🤖 Machine learning-based color detection
- 👥 Multiple person support
- 🖐️ Hand gesture controls
- 🎵 Audio-reactive effects

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 📚 **OpenCV Community** - For the amazing computer vision library
- 🐍 **Python Foundation** - For the versatile programming language  
- ⚡ **NumPy Developers** - For efficient numerical computing
- 🪄 **J.K. Rowling** - For inspiring the magic of invisibility cloaks
- 🎓 **Computer Vision Researchers** - For foundational algorithms
- 🌟 **Open Source Community** - For making this possible


## 🎬 Showcase

Share your creations! Tag us on social media:

- 🧑‍💼 LinkedIn [@Fardeen Alam ](https://www.linkedin.com/in/fardeen-alam-1b3832319/)
- 📸 Instagram: [@fardeen_alam11](https://www.instagram.com/fardeen_alam11/)

Use hashtags: `#InvisibilityCloak #OpenCV #Python #ComputerVision #HarryPotter`

---

<div align="center">

**Made with ❤️ and a touch of magic ✨**

[⭐ Star this repo](https://github.com/ALLEXCEED360/Invicibility_Cloak.git) | [🍴 Fork it](https://github.com/ALLEXCEED360/Invicibility_Cloak.git/fork)

</div>

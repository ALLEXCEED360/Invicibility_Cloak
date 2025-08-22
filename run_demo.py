#!/usr/bin/env python3
"""
Quick demo launcher for Invisibility Cloak
This script provides an easy way to run the demo with optimal settings
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if requirements are installed"""
    try:
        import cv2
        import numpy
        return True
    except ImportError:
        return False

def main():
    print("🪄 Invisibility Cloak Demo Launcher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements not installed!")
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            print("Please run: pip install -r requirements.txt")
            return 1
    
    # Run the main program
    print("🚀 Launching Invisibility Cloak...")
    print("\nInstructions:")
    print("1. Press 'B' to capture background (step out of frame first!)")
    print("2. Put on red cloth/shirt")  
    print("3. Enjoy the magic! ✨")
    print("\nPress Ctrl+C to stop this launcher\n")
    
    try:
        # Run with optimal settings for demo
        subprocess.run([sys.executable, "invisibility_cloak.py", "--color", "red"])
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except FileNotFoundError:
        print("❌ invisibility_cloak.py not found!")
        print("Make sure you're in the correct directory")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
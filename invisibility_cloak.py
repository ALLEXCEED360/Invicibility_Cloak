#!/usr/bin/env python3
"""
Harry Potter Invisibility Cloak (OpenCV + NumPy)
------------------------------------------------
Features:
  • Real-time webcam capture with mirror effect
  • HSV-based color detection for the cloak (multiple color presets)
  • Advanced noise removal with morphological operations
  • Smart background capture with averaging and visual feedback
  • Bitwise compositing for realistic cloaking effect
  • On-screen HUD with FPS, status, and controls
  • Video recording with timestamp
  • Real-time HSV tuner for custom color calibration

Keyboard Controls:
  b       : Capture background (step out of frame first!)
  r       : Start/Stop video recording (saves as MP4)
  t       : Toggle HSV tuner window (for custom colors)
  c       : Cycle through color presets (red -> blue -> green)
  s       : Save current HSV settings to file
  SPACE   : Reset background
  q/ESC   : Quit application

Setup Instructions:
  1. Install dependencies: pip install opencv-python numpy
  2. Run: python invisibility_cloak.py
  3. Position camera and press 'b' to capture background
  4. Put on red cloth/shirt and watch the magic happen!

Tips for Best Results:
  • Use solid colored cloth (red works best)
  • Ensure good, even lighting
  • Avoid background colors similar to your cloak
  • Keep the cloak wrinkle-free for better detection
  • Stand still for a few seconds after capturing background

Author: Enhanced for GitHub
Version: 2.0
"""

import cv2
import numpy as np
import time
import json
import os
from collections import deque
from datetime import datetime

# ---------------------- FPS Counter Utility ----------------------
class FPSCounter:
    """Efficient FPS counter with rolling average"""
    def __init__(self, buffer_size=30):
        self.frame_times = deque(maxlen=buffer_size)
        self.last_time = None

    def update(self):
        current_time = time.perf_counter()
        if self.last_time is not None:
            frame_time = current_time - self.last_time
            self.frame_times.append(frame_time)
        self.last_time = current_time

    def get_fps(self):
        if not self.frame_times:
            return 0.0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0

# ---------------------- HSV Color Presets ----------------------
# Note: OpenCV uses H: 0-179, S,V: 0-255
COLOR_PRESETS = {
    "red": {
        "ranges": [
            # Red wraps around 0 in HSV, so we need two ranges
            (np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))
        ],
        "description": "Bright red cloth/clothing"
    },
    "blue": {
        "ranges": [
            (np.array([100, 150, 50]), np.array([130, 255, 255]))
        ],
        "description": "Blue cloth/clothing"
    },
    "green": {
        "ranges": [
            (np.array([40, 40, 40]), np.array([80, 255, 255]))
        ],
        "description": "Green cloth/clothing"
    },
    "yellow": {
        "ranges": [
            (np.array([20, 100, 100]), np.array([30, 255, 255]))
        ],
        "description": "Yellow cloth/clothing"
    }
}

# ---------------------- Real-time HSV Tuner ----------------------
class HSVTuner:
    """Interactive HSV range tuner with trackbars"""
    def __init__(self, window_name="HSV Tuner"):
        self.window_name = window_name
        self.is_active = False
        self.is_initialized = False

    def toggle(self):
        """Toggle the HSV tuner window"""
        self.is_active = not self.is_active
        
        if self.is_active and not self.is_initialized:
            self._create_window()
        elif not self.is_active and self.is_initialized:
            cv2.destroyWindow(self.window_name)

    def _create_window(self):
        """Create trackbar window with default values"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 400, 300)
        
        # Create trackbars
        trackbars = [
            ("H_Min", 179, 0), ("S_Min", 255, 120), ("V_Min", 255, 70),
            ("H_Max", 179, 10), ("S_Max", 255, 255), ("V_Max", 255, 255)
        ]
        
        for name, max_val, default in trackbars:
            cv2.createTrackbar(name, self.window_name, default, max_val, lambda x: None)
        
        self.is_initialized = True

    def get_hsv_range(self):
        """Get current HSV range from trackbars"""
        if not self.is_active or not self.is_initialized:
            return None
        
        h_min = cv2.getTrackbarPos("H_Min", self.window_name)
        s_min = cv2.getTrackbarPos("S_Min", self.window_name)
        v_min = cv2.getTrackbarPos("V_Min", self.window_name)
        h_max = cv2.getTrackbarPos("H_Max", self.window_name)
        s_max = cv2.getTrackbarPos("S_Max", self.window_name)
        v_max = cv2.getTrackbarPos("V_Max", self.window_name)
        
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        return (lower, upper)

    def save_settings(self, filename="custom_hsv.json"):
        """Save current HSV settings to file"""
        hsv_range = self.get_hsv_range()
        if hsv_range is None:
            return False
        
        lower, upper = hsv_range
        settings = {
            "custom": {
                "ranges": [(lower.tolist(), upper.tolist())],
                "description": "Custom HSV range",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"✅ HSV settings saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save settings: {e}")
            return False

# ---------------------- Main Invisibility Cloak Class ----------------------
class InvisibilityCloak:
    def __init__(self, camera_index=0, width=1280, height=720):
        self.cap = None
        self.background = None
        self.fps_counter = FPSCounter()
        self.hsv_tuner = HSVTuner()
        
        # Video recording
        self.video_writer = None
        self.is_recording = False
        
        # Current color preset
        self.color_names = list(COLOR_PRESETS.keys())
        self.current_color_index = 0
        
        # Morphological kernel (cached for performance)
        self.morph_kernel = np.ones((3, 3), np.uint8)
        
        # Initialize camera
        self._initialize_camera(camera_index, width, height)
        
    def _initialize_camera(self, camera_index, width, height):
        """Initialize camera with error handling"""
        try:
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"Cannot open camera {camera_index}")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Get actual properties
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            print(f"📷 Camera initialized:")
            print(f"   Resolution: {actual_width}x{actual_height}")
            print(f"   FPS: {actual_fps}")
            print()
            
        except Exception as e:
            raise RuntimeError(f"Camera initialization failed: {e}")

    def create_color_mask(self, hsv_frame):
        """Create binary mask for the current cloak color"""
        # Check if HSV tuner is active
        if self.hsv_tuner.is_active:
            hsv_range = self.hsv_tuner.get_hsv_range()
            if hsv_range is not None:
                lower, upper = hsv_range
                return cv2.inRange(hsv_frame, lower, upper)
        
        # Use preset colors
        current_color = self.color_names[self.current_color_index]
        color_info = COLOR_PRESETS[current_color]
        
        # Create mask from multiple ranges (for colors like red)
        masks = []
        for lower, upper in color_info["ranges"]:
            mask = cv2.inRange(hsv_frame, lower, upper)
            masks.append(mask)
        
        # Combine all masks
        final_mask = masks[0]
        for mask in masks[1:]:
            final_mask = cv2.bitwise_or(final_mask, mask)
        
        return final_mask

    def refine_mask(self, mask):
        """Clean up mask using morphological operations"""
        # Remove noise with opening (erosion followed by dilation)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.morph_kernel, iterations=2)
        
        # Fill small gaps with dilation
        mask = cv2.dilate(mask, self.morph_kernel, iterations=1)
        
        # Optional: Remove small contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Remove small areas
                cv2.fillPoly(mask, [contour], 0)
        
        return mask

    def capture_background(self, num_frames=30):
        """Capture stable background by averaging multiple frames"""
        print("🟡 Capturing background... Please step out of the frame!")
        print("   This will take about 3 seconds...")
        
        frames = []
        countdown_frames = 60  # 2 seconds at 30fps for countdown
        
        # Countdown phase
        for i in range(countdown_frames):
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            frame = cv2.flip(frame, 1)
            countdown = 3 - (i // 20)  # 3, 2, 1
            
            if countdown > 0:
                # Draw countdown
                font_scale = 3
                thickness = 5
                text = str(countdown)
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2
                
                cv2.putText(frame, text, (text_x, text_y), 
                          cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), thickness)
                cv2.putText(frame, "Step out of frame!", (50, 50), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            cv2.imshow("Invisibility Cloak", frame)
            cv2.waitKey(33)  # ~30fps
        
        # Actual capture phase
        for i in range(num_frames):
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            frame = cv2.flip(frame, 1)
            frames.append(frame.astype(np.float32))
            
            # Show progress
            progress = f"Capturing: {i+1}/{num_frames}"
            cv2.putText(frame, progress, (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Invisibility Cloak", frame)
            cv2.waitKey(33)
        
        if frames:
            # Average all frames and apply slight blur
            self.background = np.mean(frames, axis=0).astype(np.uint8)
            self.background = cv2.GaussianBlur(self.background, (5, 5), 0)
            print("✅ Background captured successfully!")
            return True
        else:
            print("❌ Failed to capture background")
            return False

    def cycle_color(self):
        """Cycle to next color preset"""
        self.current_color_index = (self.current_color_index + 1) % len(self.color_names)
        current_color = self.color_names[self.current_color_index]
        print(f"🎨 Switched to: {current_color} ({COLOR_PRESETS[current_color]['description']})")

    def toggle_recording(self):
        """Start or stop video recording"""
        if not self.is_recording:
            # Start recording
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"invisibility_cloak_{timestamp}.mp4"
            
            # Get frame dimensions
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Cannot start recording - no frame available")
                return
            
            height, width = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
            
            if self.video_writer.isOpened():
                self.is_recording = True
                print(f"⏺️  Recording started: {filename}")
            else:
                print("❌ Failed to initialize video writer")
                self.video_writer = None
        else:
            # Stop recording
            self.is_recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            print("⏹️  Recording stopped")

    def draw_hud(self, frame):
        """Draw heads-up display with status and controls"""
        height, width = frame.shape[:2]
        
        # Semi-transparent background for text
        overlay = frame.copy()
        
        # Status information
        fps = self.fps_counter.get_fps()
        current_color = self.color_names[self.current_color_index]
        
        texts = [
            f"FPS: {fps:.1f}",
            f"Background: {'SET' if self.background is not None else 'NOT SET'}",
            f"Recording: {'ON' if self.is_recording else 'OFF'}",
            f"Color: {current_color.upper()}",
            f"HSV Tuner: {'ON' if self.hsv_tuner.is_active else 'OFF'}"
        ]
        
        # Draw status
        for i, text in enumerate(texts):
            color = (0, 255, 0) if 'SET' in text or 'ON' in text else (100, 100, 100)
            if 'Recording: ON' in text:
                color = (0, 0, 255)  # Red for recording
            
            cv2.putText(frame, text, (10, 30 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Control instructions
        controls = [
            "Controls:",
            "B - Capture background",
            "R - Record video",
            "C - Change color",
            "T - HSV tuner",
            "S - Save HSV",
            "SPACE - Reset",
            "Q/ESC - Quit"
        ]
        
        for i, control in enumerate(controls):
            y_pos = height - 200 + i * 20
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            font_scale = 0.6 if i == 0 else 0.5
            cv2.putText(frame, control, (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 1)

    def apply_invisibility_effect(self, frame):
        """Apply the main invisibility effect"""
        if self.background is None:
            return frame
        
        # Convert to HSV for color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create and refine mask
        mask = self.create_color_mask(hsv)
        mask = self.refine_mask(mask)
        
        # Create inverse mask
        inv_mask = cv2.bitwise_not(mask)
        
        # Extract cloak area from background
        background_part = cv2.bitwise_and(self.background, self.background, mask=mask)
        
        # Extract non-cloak area from current frame
        frame_part = cv2.bitwise_and(frame, frame, mask=inv_mask)
        
        # Combine both parts
        result = cv2.add(background_part, frame_part)
        
        return result

    def run(self):
        """Main application loop"""
        print("🪄 Harry Potter Invisibility Cloak")
        print("=" * 40)
        print("Instructions:")
        print("1. Press 'B' to capture background (step out of frame first)")
        print("2. Put on a red cloth/shirt")
        print("3. Watch the magic happen!")
        print("4. Use other keys for more features")
        print("=" * 40)
        print()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("⚠️  Failed to read frame from camera")
                    break
                
                # Mirror the frame for natural webcam experience
                frame = cv2.flip(frame, 1)
                
                # Update FPS counter
                self.fps_counter.update()
                
                # Apply invisibility effect
                processed_frame = self.apply_invisibility_effect(frame)
                
                # Draw HUD
                self.draw_hud(processed_frame)
                
                # Show frame
                cv2.imshow("Invisibility Cloak", processed_frame)
                
                # Record if needed
                if self.is_recording and self.video_writer:
                    self.video_writer.write(processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key in [ord('q'), ord('Q'), 27]:  # Q or ESC
                    break
                elif key in [ord('b'), ord('B')]:
                    self.capture_background()
                elif key in [ord('r'), ord('R')]:
                    self.toggle_recording()
                elif key in [ord('c'), ord('C')]:
                    self.cycle_color()
                elif key in [ord('t'), ord('T')]:
                    self.hsv_tuner.toggle()
                elif key in [ord('s'), ord('S')]:
                    self.hsv_tuner.save_settings()
                elif key == ord(' '):  # SPACE
                    self.background = None
                    print("🔄 Background reset")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("🧹 Cleaning up...")
        
        if self.is_recording and self.video_writer:
            self.video_writer.release()
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        print("✅ Cleanup complete")

# ---------------------- Main Entry Point ----------------------
def main():
    """Main function with command line argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Harry Potter Invisibility Cloak using OpenCV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python invisibility_cloak.py                    # Use default settings
  python invisibility_cloak.py --cam 1            # Use camera 1
  python invisibility_cloak.py --color blue       # Start with blue preset
  python invisibility_cloak.py --width 640 --height 480  # Lower resolution
        """
    )
    
    parser.add_argument('--color', 
                       choices=list(COLOR_PRESETS.keys()), 
                       default='red',
                       help='Initial color preset (default: red)')
    
    parser.add_argument('--cam', 
                       type=int, 
                       default=0,
                       help='Camera index (default: 0)')
    
    parser.add_argument('--width', 
                       type=int, 
                       default=1280,
                       help='Camera width (default: 1280)')
    
    parser.add_argument('--height', 
                       type=int, 
                       default=720,
                       help='Camera height (default: 720)')
    
    args = parser.parse_args()
    
    try:
        # Create and run the invisibility cloak
        cloak = InvisibilityCloak(
            camera_index=args.cam,
            width=args.width,
            height=args.height
        )
        
        # Set initial color
        if args.color in COLOR_PRESETS:
            cloak.current_color_index = list(COLOR_PRESETS.keys()).index(args.color)
        
        # Run the application
        cloak.run()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your camera is not being used by other applications")
        print("2. Try a different camera index with --cam 1")
        print("3. Check if OpenCV is properly installed: pip install opencv-python")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
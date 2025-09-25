"""
Camera capture class for PyQt integration
Simplified version of realtime_capture_system for GUI use
"""

import cv2
import numpy as np
import pyrealsense2 as rs
import os
import sys
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

# Add current directory to path for pose_detector import
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)
from pose_detector import PoseDetector


class CameraCapture(QThread):
    # Signals to emit frames and capture status to the GUI
    frame_ready = pyqtSignal(np.ndarray)
    countdown_update = pyqtSignal(int)  # countdown seconds remaining
    capture_started = pyqtSignal()
    capture_progress = pyqtSignal(int, int)  # current_frame, total_frames
    capture_finished = pyqtSignal(str)  # path where data was saved
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.detector = PoseDetector()
        self.pipeline = None
        
        # Capture settings
        self.is_capturing = False
        self.is_countdown = False
        self.countdown_seconds = 0
        self.capture_frames = 0
        self.FRAME_RATE = 30
        self.CAPTURE_SECONDS = 5
        self.COUNTDOWN_SECONDS = 5
        self.max_capture_frames = self.FRAME_RATE * self.CAPTURE_SECONDS  # 5 seconds at 30 FPS
        self.capture_path = None
        self.captured_data = []
        
        # For countdown timing
        self.countdown_frame_count = 0
        self.frames_per_countdown = self.FRAME_RATE  # 1 second = 30 frames
        
        self.setup_camera()
    
    def setup_camera(self):
        """Initialize RealSense camera"""
        try:
            self.pipeline = rs.pipeline()
            config = rs.config()
            
            # Configure streams
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            
            # Start pipeline
            self.pipeline.start(config)
            print("Camera initialized successfully")
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.pipeline = None
    
    def run(self):
        """Main thread loop for capturing frames"""
        self.running = True
        
        while self.running and self.pipeline:
            try:
                # Get frames
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                
                if not color_frame:
                    continue
                
                # Convert to numpy array
                color_image = np.asanyarray(color_frame.get_data())
                
                # Detect pose
                pose_image, skeleton_image = self.detector.findPose(color_image)
                lmList = self.detector.getPosition(pose_image)
                
                # Handle countdown
                if self.is_countdown:
                    self.handle_countdown()
                
                # Process 3D coordinates if capturing
                if self.is_capturing and len(lmList) != 0:
                    self.process_capture_data(lmList, depth_frame, pose_image, skeleton_image)
                
                # Create combined view (similar to original)
                combined = np.concatenate((pose_image, skeleton_image), axis=1)
                
                # Add status indicators
                if self.is_countdown:
                    cv2.putText(combined, f'PREPARATE! {self.countdown_seconds} SEGUNDOS', 
                               (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3, cv2.LINE_AA)
                elif self.is_capturing:
                    cv2.putText(combined, f'CAPTURANDO: {self.capture_frames}/{self.max_capture_frames}', 
                               (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Emit frame to GUI
                self.frame_ready.emit(combined)
                
            except Exception as e:
                print(f"Error in capture loop: {e}")
                break
    
    def handle_countdown(self):
        """Handle countdown logic"""
        self.countdown_frame_count += 1
        
        # Check if a second has passed (30 frames = 1 second at 30 FPS)
        if self.countdown_frame_count >= self.frames_per_countdown:
            self.countdown_frame_count = 0
            self.countdown_seconds -= 1
            
            # Emit countdown update
            self.countdown_update.emit(self.countdown_seconds)
            
            # If countdown finished, start actual capture
            if self.countdown_seconds <= 0:
                self.is_countdown = False
                self.is_capturing = True
                self.capture_frames = 0
                self.capture_started.emit()
                print("Countdown finished! Starting capture...")
    
    def process_capture_data(self, lmList, depth_frame, pose_image, skeleton_image):
        """Process and save capture data - Using EXACT logic from realtime_capture_system.py"""
        try:
            # Use the EXACT same logic as in the reference file
            object_to_track = range(0, 33)
            
            if len(lmList) != 0:
                # Modify lmList in place like the reference code
                for objet in object_to_track:
                    if objet < len(lmList):
                        _, x, y = lmList[objet]
                        
                        # Validate coordinates are within frame bounds (EXACT same validation)
                        if (x < 0 or x >= 640):  # RESOLUTION[0] = 640
                            lmList[objet] = [0, 0, 0, 0]
                            continue
                        if (y < 0 or y >= 480):  # RESOLUTION[1] = 480
                            lmList[objet] = [0, 0, 0, 0]
                            continue
                        
                        # Get depth value
                        z = depth_frame.get_distance(x, y) if depth_frame else 0
                        if (z <= 0):
                            lmList[objet] = [0, 0, 0, 0]
                            continue
                        
                        # Append z coordinate to existing landmark (EXACT same as reference)
                        lmList[objet].append(z)
                
                # Delete invalid points (EXACT same logic)
                lmList = [v for v in lmList if v != [0, 0, 0, 0]]
            
            # Save data immediately (like reference code does per frame)
            self.save_frame_data(lmList, pose_image, skeleton_image, self.capture_frames)
            
            self.capture_frames += 1
            
            # Emit progress
            self.capture_progress.emit(self.capture_frames, self.max_capture_frames)
            
            # Check if capture is complete (EXACT same condition as reference)
            if self.capture_frames >= self.max_capture_frames:
                self.finish_capture()
                
        except Exception as e:
            print(f"Error processing capture data: {e}")
    
    def save_frame_data(self, lmList, pose_image, skeleton_image, frame_number):
        """Save only CSV data directly in action folder (simplified)"""
        try:
            if self.capture_path:
                # Save only the CSV points directly in the action folder
                print(f"Saving frame {frame_number + 1} to {self.capture_path}")
                np.savetxt(
                    fname=os.path.join(self.capture_path, f"capture_{frame_number + 1}.csv"),
                    X=lmList,
                    delimiter=","
                )
                
        except Exception as e:
            print(f"Error saving frame {frame_number}: {e}")
    
    def start_capture(self, action_name="unknown_action"):
        """Start capturing data for 5 seconds - Using EXACT logic from reference code"""
        if not self.is_capturing:
            # Create timestamp like reference code
            now = datetime.now()
            timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
            
            # Get project root directory (go up from src/capture to root)
            current_file = os.path.abspath(__file__)  # Get absolute path of this file
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))  # Go up 3 levels: capture -> src -> root
            self.capture_path = os.path.join(project_root, "data", "raw", f"{action_name}_{timestamp}")
            
            print(f"Creating capture directory: {self.capture_path}")
            
            # Create only the main action directory (simplified)
            if not os.path.exists(self.capture_path):
                os.makedirs(self.capture_path)
            
            # Reset capture variables
            self.is_capturing = True
            self.capture_frames = 0
            
            self.capture_started.emit()
            print(f"Started capture: {self.capture_path}")
    
    def start_capture_with_countdown(self, action_name="unknown_action"):
        """Start capture with 5-second countdown"""
        if not self.is_capturing and not self.is_countdown:
            # Setup capture path
            now = datetime.now()
            timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
            
            # Get project root directory
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            self.capture_path = os.path.join(project_root, "data", "raw", f"{action_name}_{timestamp}")
            
            print(f"Creating capture directory: {self.capture_path}")
            
            # Create only the main action directory (simplified)
            if not os.path.exists(self.capture_path):
                os.makedirs(self.capture_path)
            
            # Start countdown
            self.is_countdown = True
            self.countdown_seconds = self.COUNTDOWN_SECONDS
            self.countdown_frame_count = 0
            
            # Emit initial countdown
            self.countdown_update.emit(self.countdown_seconds)
            print(f"Starting countdown for {action_name} capture...")
    
    def finish_capture(self):
        """Finish capture - data already saved per frame (like reference code)"""
        try:
            self.is_capturing = False
            self.is_countdown = False
            
            if self.capture_path:
                print(f"Capture finished! Saved {self.capture_frames} frames to: {self.capture_path}")
                self.capture_finished.emit(self.capture_path)
            
            # Reset for next capture (like reference code resets imgsCount and path)
            self.capture_frames = 0
            self.capture_path = None
            self.countdown_seconds = 0
            self.countdown_frame_count = 0
            
        except Exception as e:
            print(f"Error finishing capture: {e}")
    
    def stop(self):
        """Stop the capture thread"""
        self.running = False
        if self.pipeline:
            self.pipeline.stop()
        self.wait()  # Wait for thread to finish
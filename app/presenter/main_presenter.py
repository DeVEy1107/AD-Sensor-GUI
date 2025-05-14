from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import cv2
import os
import numpy as np
from datetime import datetime


class Presenter(QObject):
    # Custom signals for thread-safe UI updates
    image_update_signal = pyqtSignal(object)
    status_update_signal = pyqtSignal(dict)
    progress_update_signal = pyqtSignal(int, str)
    
    def __init__(self, model, view):
        super().__init__()
        self.view = view
        self.model = model
        self.camera = None
        self.video_recorder = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_recording_progress)
        
        # Recording state
        self.is_recording = False
        self.recording_start_time = None
        self.recording_duration = 0
        
        # Connect signals
        self.image_update_signal.connect(self.update_image_view)
        self.status_update_signal.connect(self.update_status_view)
        self.progress_update_signal.connect(self.update_progress_view)
        
        # Connect UI signals
        self.connect_ui_signals()
        
        # Initialize camera model
        self.init_camera_model()
        
    def init_camera_model(self):
        """Initialize camera model with default settings"""
        if self.model is not None:
            # Use the model passed from main.py
            self.camera = self.model['camera']
            self.video_recorder = self.model['video_recorder']
            
            # Update camera combo box with available camera types
            self.view.camera_panel.camera_combo.clear()
            self.view.camera_panel.camera_combo.addItems(self.camera.camera_types)
            
            print("使用傳入的相機模組")
        else:
            # Fallback to creating camera model internally
            from app.model.camera import CameraDevice, VideoRecorder
            
            try:
                self.camera = CameraDevice(camera_type="Webcam")
                self.video_recorder = VideoRecorder()
                
                # Update camera combo box with available camera types
                self.view.camera_panel.camera_combo.clear()
                self.view.camera_panel.camera_combo.addItems(self.camera.camera_types)
                
                print("內部初始化相機模組")
            except Exception as e:
                print(f"相機初始化失敗: {str(e)}")
                QMessageBox.critical(self.view, "錯誤", f"無法初始化相機: {str(e)}")
    
    def connect_ui_signals(self):
        """Connect all UI signals to presenter methods"""
        # Camera panel signals - 移除重複的連接
        if not self.view.camera_panel.open_camera_btn.receivers(self.view.camera_panel.open_camera_btn.clicked):
            self.view.camera_panel.open_camera_btn.clicked.connect(self.toggle_camera)
        if not self.view.camera_panel.camera_combo.receivers(self.view.camera_panel.camera_combo.currentTextChanged):
            self.view.camera_panel.camera_combo.currentTextChanged.connect(self.switch_camera)
        if not self.view.camera_panel.resolution_combo.receivers(self.view.camera_panel.resolution_combo.currentTextChanged):
            self.view.camera_panel.resolution_combo.currentTextChanged.connect(self.change_resolution)
        if not self.view.camera_panel.save_video_btn.receivers(self.view.camera_panel.save_video_btn.clicked):
            self.view.camera_panel.save_video_btn.clicked.connect(self.toggle_recording)
        
        print("UI 信號連接完成")
        
    def toggle_camera(self):
        """Toggle camera on/off"""
        try:
            if self.view.camera_panel.open_camera_btn.text() == '開啟相機':
                print("正在開啟相機...")
                self.start_camera()
            else:
                print("正在關閉相機...")
                self.stop_camera()
        except Exception as e:
            print(f"相機操作錯誤: {str(e)}")
            QMessageBox.critical(self.view, "錯誤", f"相機操作失敗: {str(e)}")
    
    def start_camera(self):
        """Start camera and update UI"""
        if self.camera:
            try:
                self.camera.start()
                self.timer.start(30)  # 30ms interval for ~33fps
                self.view.camera_panel.open_camera_btn.setText('關閉相機')
                self.view.camera_panel.progress_bar.setFormat('相機已開啟')
                self.update_camera_status()
                print("相機已開啟")
            except Exception as e:
                print(f"開啟相機失敗: {str(e)}")
                QMessageBox.critical(self.view, "錯誤", f"開啟相機失敗: {str(e)}")
    
    def stop_camera(self):
        """Stop camera and update UI"""
        if self.is_recording:
            self.stop_recording()
        
        self.timer.stop()
        if self.camera:
            self.camera.stop()
        
        self.view.camera_panel.open_camera_btn.setText('開啟相機')
        self.view.camera_panel.progress_bar.setFormat('就緒')
        self.view.image_viewer.update_view(None)
        self.update_camera_status()
        print("相機已關閉")
    
    def switch_camera(self, camera_type):
        """Switch between different camera types"""
        if not camera_type or not self.camera:
            return
            
        was_running = self.timer.isActive()
        if was_running:
            self.timer.stop()
        
        try:
            self.camera.switch_camera(camera_type)
            if was_running:
                self.timer.start(30)
            self.update_camera_status()
            print(f"已切換到 {camera_type}")
        except Exception as e:
            print(f"切換相機錯誤: {str(e)}")
            QMessageBox.critical(self.view, "錯誤", f"切換相機失敗: {str(e)}")
    
    def change_resolution(self, resolution_text):
        """Change camera resolution"""
        if not resolution_text or not self.camera:
            return
            
        # Parse resolution from text
        try:
            if 'x' in resolution_text:
                res_part = resolution_text.split('(')[0].strip()
                width, height = map(int, res_part.split('x'))
                
                # For RealSense camera, reinitialize with new resolution
                if self.camera.camera_type == "RealSense":
                    was_running = self.timer.isActive()
                    if was_running:
                        self.timer.stop()
                    self.camera.camera.reset(width=width, height=height)
                    if was_running:
                        self.camera.start()
                        self.timer.start(30)
                
                # Update video recorder resolution
                if self.video_recorder:
                    self.video_recorder.width = width
                    self.video_recorder.height = height
                
                self.update_camera_status()
                print(f"解析度已更改為 {width}x{height}")
        except Exception as e:
            print(f"更改解析度錯誤: {str(e)}")
            QMessageBox.warning(self.view, "警告", f"無法更改解析度: {str(e)}")
    
    def update_frame(self):
        """Update camera frame in the UI"""
        if self.camera:
            try:
                frame = self.camera.get_frame()
                if frame is not None:
                    # Convert BGR to RGB for display
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.image_update_signal.emit(rgb_frame)
                    
                    # Record frame if recording
                    if self.is_recording and self.video_recorder and self.video_recorder.is_recording:
                        self.video_recorder.record_frame(frame)
            except Exception as e:
                print(f"更新畫面錯誤: {str(e)}")
    
    def update_image_view(self, frame):
        """Update the image viewer with new frame"""
        self.view.image_viewer.update_view(frame)
    
    def toggle_recording(self):
        """Toggle video recording"""
        if self.view.camera_panel.save_video_btn.text() == '開始錄影':
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start video recording"""
        if not self.camera or not self.timer.isActive():
            QMessageBox.warning(self.view, "警告", "請先開啟相機")
            return
        
        # Get filename from dialog
        videos_dir = os.path.expanduser('~/Videos')
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
            
        filename, _ = QFileDialog.getSaveFileName(
            self.view, 
            "儲存影片", 
            os.path.join(videos_dir, f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"),
            "影片檔案 (*.mp4);;所有檔案 (*.*)"
        )
        
        if not filename:
            return
        
        # Ensure .mp4 extension
        if not filename.endswith('.mp4'):
            filename += '.mp4'
        
        # Get duration from UI
        duration = self.view.camera_panel.duration_spinbox.value()
        
        # Get current resolution
        resolution_text = self.view.camera_panel.resolution_combo.currentText()
        width, height = 640, 480  # Default
        if 'x' in resolution_text:
            res_part = resolution_text.split('(')[0].strip()
            width, height = map(int, res_part.split('x'))
        
        try:
            # Configure and start recording
            self.video_recorder.set_config(filename, width, height, 30, duration)
            self.video_recorder.start()
            
            self.is_recording = True
            self.recording_start_time = datetime.now()
            self.recording_duration = duration
            
            self.view.camera_panel.save_video_btn.setText('停止錄影')
            self.recording_timer.start(100)  # Update progress every 100ms
            
            self.update_camera_status()
            print(f"開始錄影: {filename}")
        except Exception as e:
            print(f"開始錄影錯誤: {str(e)}")
            QMessageBox.critical(self.view, "錯誤", f"開始錄影失敗: {str(e)}")
    
    def stop_recording(self):
        """Stop video recording"""
        if self.video_recorder and self.video_recorder.is_recording:
            self.video_recorder.stop()
        
        self.is_recording = False
        self.recording_timer.stop()
        
        self.view.camera_panel.save_video_btn.setText('開始錄影')
        self.progress_update_signal.emit(100, '錄影已完成並儲存')
        
        self.update_camera_status()
        print("錄影已停止")
    
    def update_recording_progress(self):
        """Update recording progress bar"""
        if not self.is_recording or not self.recording_start_time:
            return
        
        elapsed = (datetime.now() - self.recording_start_time).total_seconds()
        progress = min(int((elapsed / self.recording_duration) * 100), 100)
        
        self.progress_update_signal.emit(progress, f'正在錄影... {progress}%')
        
        # Auto-stop if duration reached
        if progress >= 100:
            self.stop_recording()
    
    def update_progress_view(self, value, text):
        """Update progress bar in UI"""
        self.view.camera_panel.progress_bar.setValue(value)
        self.view.camera_panel.progress_bar.setFormat(text)
    
    def update_camera_status(self):
        """Update camera status in the status view"""
        if not self.camera:
            return
        
        status = {
            'resolution': self.view.camera_panel.resolution_combo.currentText().split('(')[0].strip(),
            'camera': self.camera.camera_type,
            'fps': '30 FPS',
            'output': os.path.expanduser('~/Videos')
        }
        
        self.status_update_signal.emit(status)
    
    def update_status_view(self, status):
        """Update status view with camera information"""
        self.view.status_panel.resolution_value.setText(status['resolution'])
        self.view.status_panel.camera_value.setText(status['camera'])
        self.view.status_panel.fps_value.setText(status['fps'])
        self.view.status_panel.output_value.setText(status['output'])
    
    def cleanup(self):
        """Clean up resources when closing"""
        if self.is_recording:
            self.stop_recording()
        
        if self.camera:
            self.stop_camera()
            self.camera.release()
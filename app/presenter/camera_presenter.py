# presenter/camera_presenter.py
from .base_presenter import BasePresenter
from ..interactor.camera_interactor import CameraInteractor
from ..common.events import CameraEvents, UIEvents
from PyQt6.QtCore import QTimer, pyqtSignal
from typing import Optional
import numpy as np


class CameraPresenter(BasePresenter):
    """相機功能 Presenter"""
    
    # Qt 信號
    frame_ready = pyqtSignal(np.ndarray)
    status_update = pyqtSignal(dict)
    
    def __init__(self, camera_interactor: CameraInteractor):
        super().__init__()
        self.camera_interactor = camera_interactor
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self._update_frame)
        self._camera_running = False
    
    def _setup_view_connections(self) -> None:
        """設定 View 連接"""
        if hasattr(self._view, 'open_camera_btn'):
            self._view.open_camera_btn.clicked.connect(self._on_camera_toggle)
        if hasattr(self._view, 'camera_combo'):
            self._view.camera_combo.currentTextChanged.connect(self._on_camera_change)
        if hasattr(self._view, 'resolution_combo'):
            self._view.resolution_combo.currentTextChanged.connect(self._on_resolution_change)
    
    def _subscribe_events(self) -> None:
        """訂閱事件"""
        self.event_bus.subscribe(CameraEvents.CAMERA_STARTED, self._handle_camera_started)
        self.event_bus.subscribe(CameraEvents.CAMERA_STOPPED, self._handle_camera_stopped)
        self.event_bus.subscribe(CameraEvents.CAMERA_ERROR, self._handle_camera_error)
        self.event_bus.subscribe(CameraEvents.FRAME_CAPTURED, self._handle_frame_captured)
    
    def _on_camera_toggle(self) -> None:
        """處理相機開關"""
        if self._camera_running:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self) -> None:
        """啟動相機"""
        if self.camera_interactor.start_camera():
            self.frame_timer.start(30)  # 30ms 間隔
            self._camera_running = True
            self.publish_event(UIEvents.UPDATE_BUTTON_TEXT, {
                "button": "open_camera_btn",
                "text": "關閉相機"
            })
    
    def stop_camera(self) -> None:
        """停止相機"""
        self.frame_timer.stop()
        self.camera_interactor.stop_camera()
        self._camera_running = False
        self.publish_event(UIEvents.UPDATE_BUTTON_TEXT, {
            "button": "open_camera_btn",
            "text": "開啟相機"
        })
    
    def _update_frame(self) -> None:
        """更新影格"""
        frame = self.camera_interactor.get_frame()
        if frame is not None:
            self.frame_ready.emit(frame)
    
    def _on_camera_change(self, camera_type: str) -> None:
        """處理相機切換"""
        if camera_type and self._camera_running:
            was_running = self._camera_running
            if was_running:
                self.stop_camera()
            
            if self.camera_interactor.initialize_camera(camera_type):
                if was_running:
                    self.start_camera()
    
    def _on_resolution_change(self, resolution_text: str) -> None:
        """處理解析度變更"""
        if not resolution_text:
            return
        
        try:
            # 解析解析度文字
            res_part = resolution_text.split('(')[0].strip()
            width, height = map(int, res_part.split('x'))
            self.camera_interactor.change_resolution(width, height)
        except Exception as e:
            self.publish_event(UIEvents.SHOW_MESSAGE, {
                "type": "warning",
                "title": "警告",
                "message": f"無法更改解析度: {str(e)}"
            })
    
    def _handle_camera_started(self, event) -> None:
        """處理相機啟動事件"""
        self.status_update.emit({
            "status": "running",
            "camera_type": event.data.get("camera_type", "Unknown")
        })
    
    def _handle_camera_stopped(self, event) -> None:
        """處理相機停止事件"""
        self.status_update.emit({
            "status": "stopped"
        })
    
    def _handle_camera_error(self, event) -> None:
        """處理相機錯誤"""
        error_msg = event.data.get("error", "Unknown error")
        self.publish_event(UIEvents.SHOW_MESSAGE, {
            "type": "error",
            "title": "相機錯誤",
            "message": error_msg
        })
    
    def _handle_frame_captured(self, event) -> None:
        """處理影格捕獲事件"""
        # 這裡可以添加額外的影格處理邏輯
        pass
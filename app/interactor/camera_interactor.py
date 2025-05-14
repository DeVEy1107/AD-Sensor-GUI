# interactor/camera_interactor.py
from typing import Optional, Tuple
from ..model.camera import CameraDevice
from ..common.event_bus import Event, get_event_bus
from ..common.events import CameraEvents
import cv2
import numpy as np


class CameraInteractor:
    """相機業務邏輯處理器"""
    
    def __init__(self, camera_device: CameraDevice):
        self.camera_device = camera_device
        self.event_bus = get_event_bus()
        self._is_running = False
    
    def initialize_camera(self, camera_type: str) -> bool:
        """初始化相機"""
        try:
            self.camera_device.switch_camera(camera_type)
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.CAMERA_INITIALIZED,
                data={"camera_type": camera_type},
                source="CameraInteractor"
            ))
            return True
        except Exception as e:
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.CAMERA_ERROR,
                data={"error": str(e)},
                source="CameraInteractor"
            ))
            return False
    
    def start_camera(self) -> bool:
        """啟動相機"""
        try:
            self.camera_device.start()
            self._is_running = True
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.CAMERA_STARTED,
                data={},
                source="CameraInteractor"
            ))
            return True
        except Exception as e:
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.CAMERA_ERROR,
                data={"error": str(e)},
                source="CameraInteractor"
            ))
            return False
    
    def stop_camera(self) -> None:
        """停止相機"""
        self.camera_device.stop()
        self._is_running = False
        self.event_bus.publish(Event.create(
            event_type=CameraEvents.CAMERA_STOPPED,
            data={},
            source="CameraInteractor"
        ))
    
    def get_frame(self) -> Optional[np.ndarray]:
        """獲取當前影格"""
        if not self._is_running:
            return None
        
        frame = self.camera_device.get_frame()
        if frame is not None:
            # 轉換為 RGB 格式供顯示使用
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.FRAME_CAPTURED,
                data={"frame": rgb_frame, "original_frame": frame},
                source="CameraInteractor"
            ))
            return rgb_frame
        return None
    
    def change_resolution(self, width: int, height: int) -> bool:
        """改變解析度"""
        try:
            # 實現解析度更改邏輯
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.RESOLUTION_CHANGED,
                data={"width": width, "height": height},
                source="CameraInteractor"
            ))
            return True
        except Exception as e:
            self.event_bus.publish(Event.create(
                event_type=CameraEvents.CAMERA_ERROR,
                data={"error": str(e)},
                source="CameraInteractor"
            ))
            return False
    
    def get_available_cameras(self) -> list:
        """獲取可用的相機列表"""
        return self.camera_device.camera_types
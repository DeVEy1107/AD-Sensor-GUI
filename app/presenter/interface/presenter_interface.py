# presenter/interfaces/presenter_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict


class PresenterInterface(ABC):
    """基礎 Presenter 介面定義"""
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化 Presenter"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """清理資源"""
        pass
    
    @abstractmethod
    def handle_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """處理事件"""
        pass


class CameraPresenterInterface(PresenterInterface):
    """相機 Presenter 介面"""
    
    @abstractmethod
    def start_camera(self) -> None:
        pass
    
    @abstractmethod
    def stop_camera(self) -> None:
        pass
    
    @abstractmethod
    def switch_camera(self, camera_type: str) -> None:
        pass
    
    @abstractmethod
    def update_frame(self) -> None:
        pass


class RecordingPresenterInterface(PresenterInterface):
    """錄影 Presenter 介面"""
    
    @abstractmethod
    def start_recording(self, config: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def stop_recording(self) -> None:
        pass
    
    @abstractmethod
    def update_recording_progress(self) -> None:
        pass
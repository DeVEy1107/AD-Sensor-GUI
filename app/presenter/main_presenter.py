# presenter/main_presenter.py
from .base_presenter import BasePresenter
from .camera_presenter import CameraPresenter
from .recording_presenter import RecordingPresenter
from .status_presenter import StatusPresenter
from ..interactor.camera_interactor import CameraInteractor
from ..interactor.recording_interactor import RecordingInteractor
from ..common.events import UIEvents
from PyQt6.QtWidgets import QMessageBox


class MainPresenter(BasePresenter):
    """主要 Presenter - 協調其他 Presenter"""
    
    def __init__(self, model):
        super().__init__()
        
        # 初始化 Interactors
        self.camera_interactor = CameraInteractor(model['camera'])
        self.recording_interactor = RecordingInteractor(model['video_recorder'])
        
        # 初始化子 Presenters
        self.camera_presenter = CameraPresenter(self.camera_interactor)
        self.recording_presenter = RecordingPresenter(self.recording_interactor)
        self.status_presenter = StatusPresenter()
        
        self._presenters = [
            self.camera_presenter,
            self.recording_presenter,
            self.status_presenter
        ]
    
    def set_view(self, view) -> None:
        """設定主視窗並分配子視圖給對應的 Presenter"""
        super().set_view(view)
        
        # 分配子視圖
        self.camera_presenter.set_view(view.camera_panel)
        self.recording_presenter.set_view(view.camera_panel)
        self.status_presenter.set_view(view.status_panel)
        
        # 連接主要視圖信號
        self._setup_view_connections()
    
    def activate(self) -> None:
        """啟動所有 Presenter"""
        super().activate()
        for presenter in self._presenters:
            presenter.activate()
    
    def deactivate(self) -> None:
        """停用所有 Presenter"""
        for presenter in self._presenters:
            presenter.deactivate()
        super().deactivate()
    
    def _subscribe_events(self) -> None:
        """訂閱 UI 事件"""
        self.event_bus.subscribe(UIEvents.SHOW_MESSAGE, self._handle_show_message)
        self.event_bus.subscribe(UIEvents.UPDATE_BUTTON_TEXT, self._handle_update_button)
    
    def _handle_show_message(self, event) -> None:
        """處理顯示訊息事件"""
        data = event.data
        msg_type = data.get("type", "info")
        title = data.get("title", "訊息")
        message = data.get("message", "")
        
        if msg_type == "error":
            QMessageBox.critical(self._view, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self._view, title, message)
        else:
            QMessageBox.information(self._view, title, message)
    
    def _handle_update_button(self, event) -> None:
        """處理更新按鈕文字事件"""
        data = event.data
        button_name = data.get("button")
        text = data.get("text")
        
        if button_name and text:
            button = getattr(self._view.camera_panel, button_name, None)
            if button:
                button.setText(text)
    
    def cleanup(self) -> None:
        """清理資源"""
        self.deactivate()
        # 清理所有子 Presenter
        for presenter in self._presenters:
            if hasattr(presenter, 'cleanup'):
                presenter.cleanup()
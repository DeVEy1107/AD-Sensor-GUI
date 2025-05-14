# presenter/base_presenter.py
from abc import ABC
from PyQt6.QtCore import QObject
from ..common.event_bus import EventBus, get_event_bus
from typing import Dict, Any


class BasePresenter(QObject, ABC):
    """基礎 Presenter 類別"""
    
    def __init__(self):
        super().__init__()
        self.event_bus: EventBus = get_event_bus()
        self._view = None
        self._active = False
    
    def set_view(self, view: Any) -> None:
        """設定對應的 View"""
        self._view = view
        self._setup_view_connections()
    
    def activate(self) -> None:
        """啟動 Presenter"""
        self._active = True
        self._subscribe_events()
    
    def deactivate(self) -> None:
        """停用 Presenter"""
        self._active = False
        self._unsubscribe_events()
    
    def _setup_view_connections(self) -> None:
        """設定 View 的事件連接"""
        pass
    
    def _subscribe_events(self) -> None:
        """訂閱事件"""
        pass
    
    def _unsubscribe_events(self) -> None:
        """取消訂閱事件"""
        pass
    
    def handle_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """處理事件的通用方法"""
        if self._active:
            handler_name = f"_handle_{event_type}"
            handler = getattr(self, handler_name, None)
            if handler:
                handler(data)
    
    def publish_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """發布事件"""
        from ..common.event_bus import Event
        event = Event.create(
            event_type=event_type,
            data=data,
            source=self.__class__.__name__
        )
        self.event_bus.publish(event)
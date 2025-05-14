# common/event_bus.py
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    """事件物件"""
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str

    @classmethod
    def create(cls, event_type: str, data: Dict[str, Any], source: str) -> 'Event':
        return cls(
            event_type=event_type,
            data=data,
            timestamp=datetime.now(),
            source=source
        )


class EventBus:
    """事件總線 - 中央事件處理器"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """訂閱事件"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """取消訂閱"""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)
    
    def publish(self, event: Event) -> None:
        """發布事件"""
        self._event_history.append(event)
        
        if event.event_type in self._subscribers:
            for handler in self._subscribers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error handling event {event.event_type}: {e}")
    
    def get_history(self, event_type: str = None) -> List[Event]:
        """獲取事件歷史"""
        if event_type:
            return [e for e in self._event_history if e.event_type == event_type]
        return self._event_history.copy()


# 單例模式
_event_bus = EventBus()

def get_event_bus() -> EventBus:
    """獲取事件總線實例"""
    return _event_bus
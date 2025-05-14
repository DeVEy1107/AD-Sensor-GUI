# common/events.py
"""事件類型定義"""


class CameraEvents:
    """相機相關事件"""
    CAMERA_INITIALIZED = "camera.initialized"
    CAMERA_STARTED = "camera.started"
    CAMERA_STOPPED = "camera.stopped"
    CAMERA_ERROR = "camera.error"
    CAMERA_SWITCHED = "camera.switched"
    FRAME_CAPTURED = "camera.frame_captured"
    RESOLUTION_CHANGED = "camera.resolution_changed"


class RecordingEvents:
    """錄影相關事件"""
    RECORDING_STARTED = "recording.started"
    RECORDING_STOPPED = "recording.stopped"
    RECORDING_PROGRESS = "recording.progress"
    RECORDING_ERROR = "recording.error"
    RECORDING_COMPLETED = "recording.completed"


class UIEvents:
    """UI 相關事件"""
    SHOW_MESSAGE = "ui.show_message"
    UPDATE_BUTTON_TEXT = "ui.update_button_text"
    UPDATE_STATUS = "ui.update_status"
    UPDATE_PROGRESS = "ui.update_progress"
    ENABLE_CONTROL = "ui.enable_control"
    DISABLE_CONTROL = "ui.disable_control"


class SystemEvents:
    """系統相關事件"""
    APPLICATION_STARTED = "system.app_started"
    APPLICATION_CLOSING = "system.app_closing"
    ERROR_OCCURRED = "system.error"
    CONFIGURATION_CHANGED = "system.config_changed"
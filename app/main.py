import sys
import os
# 將 app 目錄加入到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from presenter.main_presenter import Presenter
from view.main_window import MainWindow
from model.camera import CameraDevice, VideoRecorder


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize main window
    main_window = MainWindow()
    main_window.show()
    
    # Initialize camera model
    try:
        camera_model = {
            'camera': CameraDevice(camera_type="Webcam"),
            'video_recorder': VideoRecorder()
        }
        print("相機模組初始化成功")
    except Exception as e:
        print(f"相機模組初始化失敗: {str(e)}")
        camera_model = None
    
    # Initialize presenter with model and view
    presenter = Presenter(camera_model, main_window)
    
    sys.exit(app.exec())
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QGridLayout, 
    QWidget, QTabWidget
)
from .image_view import ImageViewer
from .camera_status_view import CameraStatusInterface
from .camera_panel_view import CameraInterface
from .info_entry_view import InfoEntryPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AD Sensor Application")
        # self.resize(1200, 400)
        # Fullscreen
        self.resize(1920, 1080)
        
        # Create main layout widget
        main_widget = QWidget()
        main_layout = QGridLayout(main_widget)
        self.setCentralWidget(main_widget)
        
        # Create image viewer (camera feed will be displayed here)
        self.image_viewer = ImageViewer()
        main_layout.addWidget(self.image_viewer, 0, 0, 1, 1)
        
        # Create tab widget for different operational panels
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget, 0, 1, 1, 1)
        
        # Create info panel as the first tab
        self.info_panel = InfoEntryPanel()
        self.tab_widget.addTab(self.info_panel, "個人資料")
        
        self.camera_panel = CameraInterface()
        camera_layout = QVBoxLayout(self.camera_panel)
        camera_layout.addWidget(QLabel("攝影機畫面將在此處顯示"))
        self.tab_widget.addTab(self.camera_panel, "攝影機")

        # Example: Add a status panel
        self.status_panel = CameraStatusInterface()
        status_layout = QVBoxLayout(self.status_panel)
        status_layout.addWidget(QLabel("相機狀態將在此處顯示"))
        self.tab_widget.addTab(self.status_panel, "相機狀態")

        # Example: Add an analysis panel
        analysis_panel = QWidget()
        analysis_layout = QVBoxLayout(analysis_panel)
        analysis_layout.addWidget(QLabel("分析結果將在此處顯示"))
        self.tab_widget.addTab(analysis_panel, "分析")

        # Example: Add a settings panel
        settings_panel = QWidget()
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.addWidget(QLabel("設定選項將在此處顯示"))
        self.tab_widget.addTab(settings_panel, "設定")
        

        # Focus on tab 1
        self.tab_widget.setCurrentIndex(0)  # Set the first tab as the current tab
        # Set tab widget properties

        # Add additional tabs as needed
        
        # # Set column stretch to give image viewer more space
        main_layout.setColumnStretch(0, 3)  # Image viewer gets more horizontal space
        main_layout.setColumnStretch(1, 2)  # Tab panel gets less horizontal space
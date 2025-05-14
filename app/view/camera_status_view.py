from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QGridLayout
)



class CameraStatusInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('相機狀態')
        self.setGeometry(500, 100, 400, 300)
        
        # Set widget background to white
        self.setStyleSheet("background-color: white;")
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 標題
        title_label = QLabel('相機狀態')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title_label)
        
        # 基本狀態群組
        basic_status_group = QGroupBox('基本狀態')
        basic_status_group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #495057;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        basic_layout = QGridLayout()
        basic_layout.setSpacing(20)
        basic_layout.setContentsMargins(20, 20, 20, 20)
        
        # 目前解析度
        resolution_label = self.create_status_label('目前解析度：')
        self.resolution_value = self.create_value_label('1920 x 1080')
        basic_layout.addWidget(resolution_label, 0, 0)
        basic_layout.addWidget(self.resolution_value, 0, 1)
        
        # 目前使用的鏡頭
        camera_label = self.create_status_label('使用鏡頭：')
        self.camera_value = self.create_value_label('後置鏡頭')
        basic_layout.addWidget(camera_label, 1, 0)
        basic_layout.addWidget(self.camera_value, 1, 1)
        
        # 目前幀率
        fps_label = self.create_status_label('目前幀率：')
        self.fps_value = self.create_value_label('30 FPS')
        basic_layout.addWidget(fps_label, 2, 0)
        basic_layout.addWidget(self.fps_value, 2, 1)
        
        # 輸出資料夾位置
        output_label = self.create_status_label('輸出位置：')
        self.output_value = self.create_value_label('C:/Users/Videos/Camera')
        self.output_value.setWordWrap(True)
        basic_layout.addWidget(output_label, 3, 0)
        basic_layout.addWidget(self.output_value, 3, 1)
        
        basic_status_group.setLayout(basic_layout)
        main_layout.addWidget(basic_status_group)
        
        # 新增彈性空間
        main_layout.addStretch()
        
    def create_status_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                font-weight: normal;
                padding: 8px;
            }
        """)
        return label
    
    def create_value_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: #212529;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background-color: white;
                border-radius: 4px;
                border: 1px solid #e9ecef;
                min-width: 150px;
            }
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
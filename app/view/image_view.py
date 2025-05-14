from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QLabel, QFrame


class ImageViewer(QLabel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(QSize(640, 480))
        self.setFrameShape(QFrame.Shape.Box)
        self.setStyleSheet("background-color: #000;")
        self.setText("No Camera Feed")
        self.setScaledContents(False) 
        self.original_pixmap = None
        # Fill the label with a gray color
        self.setStyleSheet("background-color: rgb(200, 200, 200);")

    def resizeEvent(self, event):
        """Handle resize events to scale the image appropriately."""
        super().resizeEvent(event)
        if self.original_pixmap is not None:
            self.setPixmap(self._scale_pixmap())
    
    def _scale_pixmap(self):
        """Scale the pixmap to fit the widget while maintaining aspect ratio."""
        if self.original_pixmap is None:
            return QPixmap()
            
        return self.original_pixmap.scaled(
            self.width(), 
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    
    def update_view(self, frame):
        """Update the displayed frame.
        
        Args:
            frame: NumPy array containing the image data (BGR format)
        """
        if frame is None:
            self.setText("No Camera Feed")
            self.original_pixmap = None
            return
        # Update pixmap from the QImage
        self.original_pixmap = self._narr2pixmap(frame)
        # Apply scaled pixmap
        self.setPixmap(self._scale_pixmap())

    @staticmethod
    def _narr2pixmap(narr): 
        height, width, channel = narr.shape
        q_img = QImage(narr.data, width, height, channel * width, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_img)
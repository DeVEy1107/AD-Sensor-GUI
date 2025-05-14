from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QLabel, QFrame
import numpy as np


class ImageViewer(QLabel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(QSize(640, 480))
        self.setFrameShape(QFrame.Shape.Box)
        self.setText("No Camera Feed")
        self.setScaledContents(True)  # Changed to True for better display
        self.original_pixmap = None
        # Set initial background
        self.setStyleSheet("background-color: #333; color: white; font-size: 16px;")

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
            self.size(),  # Use self.size() instead of width() and height()
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    
    def update_view(self, frame):
        """Update the displayed frame.
        
        Args:
            frame: NumPy array containing the image data (RGB format)
        """
        if frame is None:
            self.setText("No Camera Feed")
            self.original_pixmap = None
            print("Frame is None")
            return
            
        try:
            print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")
            
            # Ensure frame is in the correct format
            if frame.dtype != np.uint8:
                frame = frame.astype(np.uint8)
                print("Converted frame to uint8")
            
            # Create pixmap from the frame
            self.original_pixmap = self._narr2pixmap(frame)
            
            if self.original_pixmap.isNull():
                print("Pixmap is null!")
                self.setText("Error: Invalid pixmap")
                return
                
            # Set the pixmap
            self.setPixmap(self._scale_pixmap())
            print(f"Pixmap set: {self.original_pixmap.width()}x{self.original_pixmap.height()}")
            
        except Exception as e:
            print(f"Error updating view: {e}")
            import traceback
            traceback.print_exc()
            self.setText(f"Error: {str(e)}")

    @staticmethod
    def _narr2pixmap(narr): 
        """Convert numpy array to QPixmap
        
        Args:
            narr: numpy array in RGB format
            
        Returns:
            QPixmap object
        """
        if narr is None:
            return QPixmap()
            
        try:
            height, width, channel = narr.shape
            
            # Ensure the array is contiguous
            if not narr.flags['C_CONTIGUOUS']:
                narr = np.ascontiguousarray(narr)
                print("Made array contiguous")
            
            bytes_per_line = channel * width
            
            # Create QImage with the correct format
            if channel == 3:
                q_img = QImage(narr.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            elif channel == 4:
                q_img = QImage(narr.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)
            else:
                raise ValueError(f"Unsupported number of channels: {channel}")
            
            # Convert to pixmap
            pixmap = QPixmap.fromImage(q_img)
            print(f"Created pixmap: {pixmap.width()}x{pixmap.height()}, null: {pixmap.isNull()}")
            
            return pixmap
            
        except Exception as e:
            print(f"Error in _narr2pixmap: {e}")
            import traceback
            traceback.print_exc()
            return QPixmap()
import cv2
import numpy as np
import pyrealsense2 as rs


class WebcamCamera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = None

    def start(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(self.camera_index)
        else:
            self.capture.open(self.camera_index)

    def stop(self):
        if self.capture:
            self.capture.release()

    def get_frame(self):
        if self.capture is None:
            return None
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        self.stop()


class RealSenseCamera:
    def __init__(self, width=640, height=480, fps=30):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        self.width = width
        self.height = height
        self.fps = fps

    def reset(self, width=640, height=480, fps=30):
        self.stop()
        self.__init__(width, height, fps)

    def start(self):
        try:
            self.pipeline.start(self.config)
        except Exception as e:
            print(f"Error starting RealSense camera: {e}")
            raise

    def stop(self):
        try:
            self.pipeline.stop()
        except:
            pass

    def get_frame(self):
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                return None
            frame = np.asanyarray(color_frame.get_data())
            return frame
        except:
            return None
    
    def release(self):
        self.stop()


class CameraDevice:
    def __init__(self, camera_type="Webcam"):
        self.camera_types = ["Webcam", "RealSense"]
        
        # Initialize cameras lazily
        self.camera_devices = {
            "Webcam": None,
            "RealSense": None
        }
        
        self.camera_type = camera_type
        self.camera = None
        self._initialize_camera(camera_type)

    def _initialize_camera(self, camera_type):
        if camera_type not in self.camera_types:
            raise ValueError(f"Invalid camera type: {camera_type}")
        
        # Create camera instance if not exists
        if self.camera_devices[camera_type] is None:
            if camera_type == "Webcam":
                self.camera_devices[camera_type] = WebcamCamera()
            else:  # RealSense
                try:
                    self.camera_devices[camera_type] = RealSenseCamera()
                except:
                    # Fallback to webcam if RealSense is not available
                    print("RealSense camera not available, falling back to Webcam")
                    camera_type = "Webcam"
                    if self.camera_devices["Webcam"] is None:
                        self.camera_devices["Webcam"] = WebcamCamera()
        
        self.camera = self.camera_devices[camera_type]
        self.camera_type = camera_type

    def switch_camera(self, camera_type):
        if camera_type not in self.camera_types:
            raise ValueError(f"Invalid camera type: {camera_type}")
        
        # Stop current camera
        if self.camera:
            self.camera.stop()
        
        # Initialize and start new camera
        self._initialize_camera(camera_type)
        self.camera.start()

    def start(self):
        if self.camera:
            self.camera.start()

    def stop(self):
        if self.camera:
            self.camera.stop()

    def get_frame(self):
        if self.camera:
            return self.camera.get_frame()
        return None

    def release(self):
        for camera in self.camera_devices.values():
            if camera:
                camera.release()


class VideoRecorder:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.writer = None
        self.is_recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.duration_count = 0
        self.filename = None
        self.duration = None

    def set_config(self, filename, width=640, height=480, fps=30, duration=None):
        self.filename = filename
        self.fps = fps
        self.width = width
        self.height = height
        self.duration = duration * fps if duration else None

    def start(self):
        if self.filename:
            self.writer = cv2.VideoWriter(
                self.filename, self.fourcc, self.fps, (self.width, self.height)
            )
            self.is_recording = True
            self.duration_count = 0
        else:
            raise ValueError("Filename not set. Use set_config first.")

    def stop(self):
        if self.writer:
            self.writer.release()
        self.is_recording = False

    def record_frame(self, frame):
        if not self.is_recording or not self.writer:
            return
            
        if frame is None:
            raise ValueError("Frame is None.")
            
        # Resize frame if necessary
        if frame.shape[:2] != (self.height, self.width):
            frame = cv2.resize(frame, (self.width, self.height))
        
        if self.duration is None:
            self.writer.write(frame)
        else:
            if self.duration_count < self.duration:
                self.writer.write(frame)
                self.duration_count += 1
            else:
                self.stop()
    

if __name__ == "__main__":
    # Test code
    camera = CameraDevice(camera_type="Webcam")
    video_recorder = VideoRecorder()
    video_recorder.set_config(filename="output.mp4", width=640, height=480, fps=30, duration=3)
    
    try:
        camera.start()
        print("Camera started. Press 'q' to quit, 's' to start recording, 'c' to switch camera")
        
        camera_idx = 0
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            # Display the frame
            cv2.imshow("Camera Test", frame)
            
            if video_recorder.is_recording:
                video_recorder.record_frame(frame)
                
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                camera_idx = (camera_idx + 1) % len(camera.camera_types)
                try:
                    camera.switch_camera(camera.camera_types[camera_idx])
                    print(f"Switched to {camera.camera_types[camera_idx]}")
                except Exception as e:
                    print(f"Error switching camera: {e}")
            elif key == ord('s'):
                if not video_recorder.is_recording:
                    video_recorder.start()
                    print("Recording started")
                else:
                    video_recorder.stop()
                    print("Recording stopped")
    finally:
        camera.stop()
        if video_recorder.is_recording:
            video_recorder.stop()
        cv2.destroyAllWindows()
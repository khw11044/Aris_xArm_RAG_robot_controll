import cv2

class CameraService:
    def __init__(self):
        self.cameras = {}

    def open_camera(self, camera_id):
        """카메라를 열고 스트림을 시작합니다."""
        if camera_id not in self.cameras:
            cap = cv2.VideoCapture(camera_id)
            if cap.isOpened():
                self.cameras[camera_id] = cap
            else:
                raise RuntimeError(f"Failed to open camera {camera_id}")

    def close_camera(self, camera_id):
        """카메라 스트림을 종료하고 리소스를 해제합니다."""
        if camera_id in self.cameras:
            self.cameras[camera_id].release()
            del self.cameras[camera_id]

    async def get_frame(self, camera_id):
        """지정된 카메라의 프레임을 캡처하여 반환합니다."""
        if camera_id not in self.cameras:
            self.open_camera(camera_id)
        cap = self.cameras[camera_id]
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        return None

    def __del__(self):
        """서비스 종료 시 모든 카메라 스트림을 종료합니다."""
        for cap in self.cameras.values():
            cap.release()

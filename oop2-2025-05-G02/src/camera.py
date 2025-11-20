import cv2
import threading

class CameraViewer:
    def __init__(self, delay=10):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("カメラが開けません")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.DELAY = delay
        self.running = True
        self.capture_flag = False
        self.captured_img = None
        self.frame_for_gui = None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            self.frame_for_gui = frame.copy()
            if self.capture_flag:
                self.captured_img = frame.copy()
                print("📸 写真をキャプチャしました！")
                self.capture_flag = False
            cv2.waitKey(self.DELAY)

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
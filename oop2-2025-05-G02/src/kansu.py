import cv2
import os
from ivent import TakePhotoButton
import uuid

class CameraCapture:
    """カメラを起動して写真を撮る。GUIからフラグで制御可能"""

    DELAY: int = 100  # フレーム表示間隔(ms)

    def __init__(self, camera_id: int = 0, save_dir: str = "captured"):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img = None
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir

    def run(self, picturenisite):
        """
        picturenisite(path) : GUIに画像を渡すコールバック関数
        """
        while True:
            TakePhotoButton.ok_flag = False
            TakePhotoButton.retry_flag = False

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                img = frame.copy()
                rows, cols, _ = img.shape
                center = (cols//2, rows//2)

                # ターゲットマーク
                img = cv2.circle(img, center, 30, (0,0,255), 3)
                img = cv2.circle(img, center, 60, (0,0,255), 3)
                img = cv2.line(img, (center[0], center[1]-80), (center[0], center[1]+80), (0,0,255),3)
                img = cv2.line(img, (center[0]-80, center[1]), (center[0]+80, center[1]), (0,0,255),3)

                img = cv2.flip(img,1)
                cv2.imshow("Camera", img)

                if TakePhotoButton.cancel_capture_flag:
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return

                if TakePhotoButton.ok_flag:
                    self.captured_img = frame
                    filename = f"{uuid.uuid4().hex}.png"
                    path = os.path.join(self.save_dir, filename)
                    cv2.imwrite(path, frame)
                    picturenisite(path)  # GUIに送る
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return

                if TakePhotoButton.retry_flag:
                    break  # 撮り直し

                if cv2.waitKey(self.DELAY) & 0xFF == ord('q'):
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return

            # 内側ループ終了で再撮影

    def get_img(self):
        return self.captured_img

    def __del__(self):
        if hasattr(self,'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
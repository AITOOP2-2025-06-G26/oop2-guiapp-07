import cv2
from PySide6.QtGui import QImage, QPixmap
import threading

def setup_capture_event(camera, captured_label):
    """撮影ボタンが押されたときのイベント設定"""
    camera.capture_flag = True

    # 撮影完了後プレビュー更新
    def update_preview():
        while camera.capture_flag:
            pass
        if camera.captured_img is not None:
            rgb = cv2.cvtColor(camera.captured_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            pixmap = pixmap.scaled(
                captured_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            captured_label.setPixmap(pixmap)

    threading.Thread(target=update_preview, daemon=True).start()
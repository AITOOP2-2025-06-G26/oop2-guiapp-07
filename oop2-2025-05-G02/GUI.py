from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
import threading
import cv2

class CameraViewer:
    """カメラ映像の取得・撮影管理クラス"""
    def __init__(self, delay: int = 10):
        self.cap = cv2.VideoCapture(0)  # デバイスIDを変更して試す
        if not self.cap.isOpened():
            print("カメラが初期化されていません")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.DELAY = delay
        self.running = True

        self.capture_flag = False      # GUIからの撮影指示フラグ
        self.captured_img = None       # 最後のキャプチャ画像
        self.frame_for_gui = None      # GUI に渡す最新フレーム

    def run(self):
        """カメラ映像を取得し続け、GUIスレッドに最新フレームを渡す"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("カメラからフレームを取得できませんでした")
                continue

            print("フレーム取得成功")  # デバッグ用ログ

            # GUI用に保存（表示はGUI側で行う）
            self.frame_for_gui = frame.copy()

            # 撮影フラグが立った瞬間に元画像を保存
            if self.capture_flag:
                self.captured_img = frame.copy()
                print("📸 写真をキャプチャしました！")
                self.capture_flag = False

            # 軽く待機
            cv2.waitKey(self.DELAY)

    def stop(self):
        """カメラ終了処理"""
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

class MainWindow(QWidget):
    """GUIメインウィンドウ"""
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.setWindowTitle("PySide6 Camera Capture")
        self.resize(800, 600)

        self.label = QLabel("カメラ映像がここに表示されます")
        self.label.setAlignment(Qt.AlignCenter)
        self.capture_button = QPushButton("撮影")
        self.capture_button.clicked.connect(self.on_capture)
        self.captured_label = QLabel("キャプチャ画像")
        self.captured_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.captured_label)
        self.setLayout(layout)

        # タイマーで GUI 更新
        self.startTimer(30)

    def timerEvent(self, event):
        frame = self.camera.frame_for_gui
        if frame is None:
            return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def on_capture(self):
        self.camera.capture_flag = True
        def update_preview():
            while self.camera.capture_flag:
                pass
            if self.camera.captured_img is not None:
                rgb = cv2.cvtColor(self.camera.captured_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                pixmap = pixmap.scaled(self.captured_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.captured_label.setPixmap(pixmap)
        threading.Thread(target=update_preview, daemon=True).start()

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

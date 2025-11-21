import os
import time

import cv2
import numpy as np
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

class MainWindow(QWidget):
    """カメラ映像を表示し、撮影／合成を操作できるメインウィンドウ"""

    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.setWindowTitle("PySide6 Camera Capture")
        self.resize(1000, 700)

        base_dir = os.path.dirname(__file__)
        self.template_path = os.path.join(base_dir, "images", "google.png")
        self.output_dir = os.path.join(base_dir, "output_images")

        self.status_label = QLabel("カメラを初期化しています…")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.live_label = QLabel("カメラ映像がここに表示されます")
        self.live_label.setAlignment(Qt.AlignCenter)
        self.live_label.setStyleSheet("background: #111; color: #eee;")

        self.captured_label = QLabel("キャプチャ画像")
        self.captured_label.setAlignment(Qt.AlignCenter)
        self.captured_label.setMinimumSize(320, 240)
        self.composite_label = QLabel("合成画像")
        self.composite_label.setAlignment(Qt.AlignCenter)
        self.composite_label.setMinimumSize(320, 240)

        self.capture_button = QPushButton("撮影")
        self.capture_button.clicked.connect(self.on_capture)

        self.compose_button = QPushButton("画像合成")
        self.compose_button.clicked.connect(self.on_composite)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.capture_button)
        action_layout.addWidget(self.compose_button)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.captured_label)
        images_layout.addWidget(self.composite_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.live_label, stretch=2)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(images_layout)
        self.setLayout(main_layout)

        self.live_timer = QTimer(self)
        self.live_timer.timeout.connect(self._update_live_preview)
        self.live_timer.start(33)

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self._check_capture_status)
        self.capture_timeout = 5.0
        self._capture_start = 0.0
        self._live_ready = False

    def _update_live_preview(self) -> None:
        frame = self.camera.frame_for_gui
        if frame is None:
            return
        pixmap = self._pixmap_from_frame(frame, self.live_label.size())
        if not pixmap.isNull():
            self.live_label.setPixmap(pixmap)
            if not self._live_ready:
                self.status_label.setText("ライブ映像を表示中")
                self._live_ready = True

    def _pixmap_from_frame(self, frame: cv2.Mat, size) -> QPixmap:
        size = size if size.width() > 0 and size.height() > 0 else QSize(640, 480)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        return pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _display_image(self, label: QLabel, frame: cv2.Mat) -> None:
        pixmap = self._pixmap_from_frame(frame, label.size())
        if not pixmap.isNull():
            label.setPixmap(pixmap)

    def on_capture(self) -> None:
        if self.capture_timer.isActive():
            return
        self.status_label.setText("撮影中…")
        self.camera.capture_flag = True
        self._capture_start = time.monotonic()
        self.capture_timer.start(50)

    def _check_capture_status(self) -> None:
        if self.camera.capture_flag:
            if time.monotonic() - self._capture_start >= self.capture_timeout:
                self.camera.capture_flag = False
                self.capture_timer.stop()
                self.status_label.setText("撮影タイムアウト")
            return
        self.capture_timer.stop()
        if self.camera.captured_img is not None:
            self._display_image(self.captured_label, self.camera.captured_img)
            self.status_label.setText("撮影完了：キャプチャ画像を表示")
        else:
            self.status_label.setText("キャプチャに失敗しました")

    def on_composite(self) -> None:
        if self.camera.captured_img is None:
            self.status_label.setText("先に写真を撮影してください")
            return
        if not os.path.exists(self.template_path):
            self.status_label.setText("合成元画像が見つかりません")
            return
        self.status_label.setText("合成中…")
        template = cv2.imread(self.template_path)
        if template is None:
            self.status_label.setText("合成する画像を読み込めません")
            return
        result = self._blend_white(template, self.camera.captured_img)
        self._display_image(self.composite_label, result)
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, "capture_composite.png")
        cv2.imwrite(output_path, result)
        self.status_label.setText(f"合成完了：{os.path.basename(output_path)} を保存しました")

    def _blend_white(self, base: cv2.Mat, overlay: cv2.Mat) -> cv2.Mat:
        # Replace white pixels in base with the captured image values without stretching overlay
        result = base.copy()
        h, w, _ = result.shape
        oh, ow, _ = overlay.shape
        for x in range(w):
            for y in range(h):
                b, g, r = result[y, x]
                if (b, g, r) == (255, 255, 255):
                    b2, g2, r2 = overlay[y % oh, x % ow]
                    result[y, x] = (b2, g2, r2)
        return result

    def closeEvent(self, event) -> None:
        self.live_timer.stop()
        self.capture_timer.stop()
        self.camera.stop()
        super().closeEvent(event)

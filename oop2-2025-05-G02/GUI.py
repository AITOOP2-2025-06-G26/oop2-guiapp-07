import sys
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout
)
from PySide6 import QtCore, QtGui
from src.ivent import TakePhotoButton, OKButton, CancelButton
from src.k24110 import lecture05_01  # lecture05_01 を呼ぶため

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("画像GUI")
        self.setGeometry(200, 200, 1200, 700)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(outer_layout)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 左上：カメラ映像 (cv2.imshow は別ウィンドウで)
        self.camera_label = QLabel("カメラ映像")
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setFixedSize(350, 220)
        layout.addWidget(self.camera_label, 0, 0, QtCore.Qt.AlignCenter)

        # 右上：撮影画像
        self.shot_label = QLabel("撮影画像")
        self.shot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.shot_label.setFixedSize(350, 220)
        layout.addWidget(self.shot_label, 0, 2, QtCore.Qt.AlignCenter)

        # 中央：はい / いいえ
        self.yes_button = QPushButton("はい")
        self.no_button = QPushButton("いいえ")
        layout.addWidget(self.yes_button, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.no_button, 2, 2, QtCore.Qt.AlignCenter)

        # 左下：撮影ボタン
        self.TakePhotoButton = QPushButton("撮影")
        self.TakePhotoButton.setFixedSize(160, 80)
        layout.addWidget(self.TakePhotoButton, 1, 0, QtCore.Qt.AlignCenter)
        self.TakePhotoButton.clicked.connect(self.start_capture_thread)

        # 右下：合成画像
        self.result_label = QLabel("合成画像")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setFixedSize(350, 220)
        layout.addWidget(self.result_label, 3, 2, QtCore.Qt.AlignCenter)

        outer_layout.addLayout(layout)

    def start_capture_thread(self):
        """ボタン押下でスレッドを立ててカメラ撮影＋合成処理"""
        thread = threading.Thread(target=self.capture_and_combine)
        thread.start()

    def capture_and_combine(self):
        """k24110 の関数を呼び出して画像を合成し QLabel に表示"""
        k24110.lecture05_01()  # カメラ起動・合成画像生成

        # GUI に反映する
        img_path = "output_images/lecture05_01_k24110.png"
        pixmap = QtGui.QPixmap(img_path)
        pixmap = pixmap.scaled(self.result_label.width(), self.result_label.height(), QtCore.Qt.KeepAspectRatio)
        
        # GUI操作はメインスレッドで行う
        self.result_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{border: 1px solid black; border-radius:15px;}")
    w = MainWidget()
    w.show()
    sys.exit(app.exec())

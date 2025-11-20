import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout
)
from PySide6 import QtGui, QtCore
from src.ivent import TakePhotoButton, OKButton, CancelButton

# GUI内で
self.TakePhotoButton = TakePhotoButton()
self.yes_button = OKButton()
self.no_button = CancelButton()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("画像GUI")
        self.setGeometry(200, 200, 1200, 700)

        # ====== ★ 外側レイアウト（全体を中央に寄せる） ======
        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(outer_layout)

        # ====== 元からのグリッドレイアウト ======
        layout = QGridLayout()

        # 中央寄せのためにマージンを縮める
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # ====== 左上：カメラ映像 ======
        self.camera_label = QLabel("カメラ映像")
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setFixedSize(350, 220)
        layout.addWidget(self.camera_label, 0, 0, QtCore.Qt.AlignCenter)

        # ====== 右上：撮影画像 ======
        self.shot_label = QLabel("撮影画像")
        self.shot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.shot_label.setFixedSize(350, 220)
        layout.addWidget(self.shot_label, 0, 2, QtCore.Qt.AlignCenter)

        # ====== 中央：はい / いいえ ======
        self.yes_button = QPushButton("はい")
        self.no_button = QPushButton("いいえ")

        layout.addWidget(self.yes_button, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.no_button, 2, 2, QtCore.Qt.AlignCenter)


        # ====== 左下：撮影ボタン ======
        self.TakePhotoButton = QPushButton("撮影ボタン")
        self.TakePhotoButton.setFixedSize(160, 80)
        layout.addWidget(self.TakePhotoButton, 1, 0, QtCore.Qt.AlignCenter)

        # ====== 右下：合成画像 ======
        self.result_label = QLabel("合成画像")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setFixedSize(350, 220)
        layout.addWidget(self.result_label, 3, 2, QtCore.Qt.AlignCenter)



        # ★ 外側レイアウトにグリッドレイアウトを追加
        outer_layout.addLayout(layout)


app = QApplication(sys.argv)
app.setStyleSheet("QLabel{border: 1px solid black; border-radius:15px;}")
w = MainWidget()
w.show()
app.exec()

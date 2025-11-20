import sys
from PySide6.QtWidgets import QPushButton
from PySide6 import QtGui

import numpy as np

# from src.kansu.py import 

class TakePhotoButton(QPushButton):
    """
    このボタンを押したら、カメラで写真を撮る。
    """

    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.clicked.connect(self.__click)

    def __click(self):
        pass   
        

class OKButton(QPushButton):
    """
    このボタンを押したら、保存した写真から合成を行う。
    """
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.clicked.connect(self.__click)

    def __click(self):
        pass

class CancelButton(QPushButton):
    """
    このボタンを押したら、写真撮影状態に戻る。
    """
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.clicked.connect(self.__click)

    def __click(self):
        pass
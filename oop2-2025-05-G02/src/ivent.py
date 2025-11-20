import sys
from PySide6.QtWidgets import QPushButton
from PySide6 import QtGui

import numpy as np

class TakePhotoButton(QPushButton):
    """
    このボタンを押したら、カメラで写真を撮る。
    """

    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.setText("撮影")
        self.clicked.connect(self.__click)

    def __click(self):
        pass   
        

class OKButton(QPushButton):
    """
    
    """
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.setText("OK")
        self.clicked.connect(self.__click)

    def __click(self):
        pass

class CancelButton(QPushButton):
    """
    
    """
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setFont(QtGui.QFont('Arial', 40))
        self.setText("Cancel")
        self.clicked.connect(self.__click)

    def __click(self):
        pass
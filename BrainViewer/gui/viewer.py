# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：viewer.py.py
@Author  ：Barry
@Date    ：2022/4/14 2:33 
"""

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget, QFileDialog


class BrainViewer(QMainWindow):
    def __init__(self):
        super(BrainViewer, self).__init__()
        uic.loadUi('gui\\viewer.ui', self)
        self.center_win()
        self.setWindowTitle('BrainViewer')

    def center_win(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

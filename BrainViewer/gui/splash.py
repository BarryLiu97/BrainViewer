# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：splash.py
@Author  ：Barry
@Date    ：2022/4/19 21:07 
"""

import time
from pathlib import Path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QSplashScreen, QDesktopWidget


class SplashPanel(QSplashScreen):

    def __init__(self):
        super(SplashPanel, self).__init__()
        self.setFixedSize(400, 195)
        message_font = QFont('Segoe UI')
        message_font.setWeight(QFont.Weight.DemiBold)
        message_font.setPointSize(9)
        self.setFont(message_font)
        logo_path = Path(__file__).parent / '../fig/LOGO.jpg'
        pixmap = QPixmap(str(logo_path)).scaled(QSize(400, 195),
                                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.center_win()
        self.show()
        for i in range(1, 6):
            self.showMessage(f"Initializing{'.' * i}",
                             alignment=Qt.AlignBottom, color=Qt.black)
            time.sleep(0.5)

    def center_win(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        # 重写鼠标点击事件，防止点击后消失
        pass

    def mouseDoubleClickEvent(self, *args, **kwargs):
        # 重写鼠标移动事件，防止出现卡顿现象
        pass

    def enterEvent(self, *args, **kwargs):
        # 重写鼠标移动事件，防止出现卡顿现象
        pass

    def mouseMoveEvent(self, *args, **kwargs):
        # 重写鼠标移动事件，防止出现卡顿现象
        pass

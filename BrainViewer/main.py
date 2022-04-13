# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：main.py
@Author  ：Barry
@Date    ：2022/4/14 2:31 
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from gui.viewer import BrainViewer

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    viewer = BrainViewer()
    viewer.showMaximized()
    viewer.show()
    sys.exit(app.exec_())

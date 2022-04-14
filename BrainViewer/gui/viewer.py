# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：viewer.py.py
@Author  ：Barry
@Date    ：2022/4/14 2:33 
"""

from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QKeySequence

from gui.viewer_ui import Ui_MainWindow
from utils.surface import check_hemi


class BrainViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(BrainViewer, self).__init__()
        self.setupUi(self)
        self.center_win()
        self.setWindowTitle('BrainViewer')
        self.slot_funcs()

        QShortcut(QKeySequence(self.tr("F10")), self, self.showNormal)
        QShortcut(QKeySequence(self.tr("F11")), self, self.showMaximized)
        QShortcut(QKeySequence(self.tr("Ctrl+Q")), self, self.close)
        QShortcut(QKeySequence(self.tr("Ctrl+O")), self, self._load_surface)

    def center_win(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def slot_funcs(self):
        self._load_surface_action.triggered.connect(self._load_surface)
        # self._load_volume_action.triggered.connect(self._load_volume)

        self._brain_gp.clicked.connect(self._enable_brain)
        self._brain_hemi_cbx.currentTextChanged.connect(self._set_brain_hemi)
        self._brain_transparency_slider.valueChanged.connect(self._set_brain_transp)

        # self._rois_gp.clicked.connect(self._enable_roi)
        # self._roi_hemi_cbx.currentTextChanged.connect(self._set_roi_hemi)
        # self._roi_transparency_slider.valueChanged.connect(self._set_roi_transp)

    def _load_surface(self):
        surf_paths, _ = QFileDialog.getOpenFileNames(self, 'Surface',
                                                     filter="Surface (*.pial *.white)")
        if len(surf_paths):
            for surf_path in surf_paths:
                if len(surf_path.split('.')) == 2:
                    opacity = float(self._brain_transparency_slider.value()) / 100
                    self._plotter.add_brain(surf_path, opacity)
                else:
                    QMessageBox.warning(self, 'Surface', 'Only *h.pial or *h.white is supported')

    def _enable_brain(self):
        hemi = check_hemi(self._brain_hemi_cbx.currentText())
        viz = self._brain_gp.isChecked()
        self._plotter.enable_brain_viz(viz, hemi)

    def _set_brain_hemi(self):
        hemi = check_hemi(self._brain_hemi_cbx.currentText())
        self._plotter.set_brain_hemi(hemi)

    def _set_brain_transp(self, transp):
        transp = float(transp) / 100
        self._plotter.set_brain_opacity(transp)

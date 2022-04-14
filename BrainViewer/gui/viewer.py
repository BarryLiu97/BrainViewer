# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：viewer.py.py
@Author  ：Barry
@Date    ：2022/4/14 2:33 
"""

from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox, QDesktopWidget, QFileDialog, QColorDialog
from PyQt5.QtGui import QKeySequence

from gui.viewer_ui import Ui_MainWindow
from utils.surface import check_hemi
from utils.config import view_dict


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

        self._bg_color_action.triggered.connect(self._set_background_color)
        self._brain_color_action.triggered.connect(self._set_brain_color)

        self._front_action.triggered.connect(self._set_front_view)
        self._back_action.triggered.connect(self._set_back_view)
        self._left_action.triggered.connect(self._set_left_view)
        self._right_action.triggered.connect(self._set_right_view)
        self._top_action.triggered.connect(self._set_top_view)
        self._bottom_action.triggered.connect(self._set_bottom_view)

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

    def _set_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # 第四位为透明度 color必须在0-1之间
            color = color.getRgbF()[:-1]
            print(f"change brain color to {color}")
            self._plotter.set_background_color(color)

    def _set_brain_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # 第四位为透明度 color必须在0-1之间
            color = color.getRgbF()[:-1]
            print(f"change brain color to {color}")
            self._plotter.set_brain_color(color)

    def _set_front_view(self):
        view = view_dict['front']
        self._plotter.view_vector(view[0], view[1])

    def _set_back_view(self):
        view = view_dict['back']
        self._plotter.view_vector(view[0], view[1])

    def _set_left_view(self):
        view = view_dict['left']
        self._plotter.view_vector(view[0], view[1])

    def _set_right_view(self):
        view = view_dict['right']
        self._plotter.view_vector(view[0], view[1])

    def _set_top_view(self):
        view = view_dict['top']
        self._plotter.view_vector(view[0], view[1])

    def _set_bottom_view(self):
        view = view_dict['bottom']
        self._plotter.view_vector(view[0], view[1])

    def _show_tooltip(self, i, j):
        item = self._info_table.item(i, j).text()
        if len(item) > 39:
            QToolTip.showText(QCursor.pos(), item)

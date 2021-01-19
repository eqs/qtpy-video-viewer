# -*- coding: utf-8 -*-
from typing import List

import numpy as np
import cv2

from qtpy.QtWidgets import (
    QLabel, QWidget, QSlider,
    QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem
)
from qtpy.QtCore import QObject, Qt, QPoint
from qtpy.QtCore import Slot
from qtpy.QtCore import Signal
from qtpy.QtGui import QImage, QPixmap, QPainter

from utils import hbox, vbox


class GraphicsView(QGraphicsView):
    def __init__(self, **kwargs):
        super(GraphicsView, self).__init__(**kwargs)
        self._scene = QGraphicsScene(parent=self)

        self.current_image = QGraphicsPixmapItem()
        self._scene.addItem(self.current_image)

        self.setScene(self._scene)
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)

    def update_image(self, img: np.ndarray):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb_image.data, w, h,
                      bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.current_image.setPixmap(pixmap)
        self._scene.setSceneRect(0, 0, w, h)
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, e):
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            self.scale(1.25, 1.25)
        elif e.angleDelta().y() < 0:
            self.scale(0.85, 0.85)

    def mousePressEvent(self, e):
        # シーン上のマウス位置を取得する
        pos = self.mapToScene(e.pos())
        if e.button() == Qt.LeftButton:
            if e.modifiers() == Qt.NoModifier:
                pass
            elif e.modifiers() == Qt.AltModifier:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
        QGraphicsView.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        QGraphicsView.mouseReleaseEvent(self, e)
        if e.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

    def calc_offset(self, p: QPoint):
        offset_x = p.x() - int(self.viewport().width() / 2)
        offset_y = p.y() - int(self.viewport().height() / 2)
        return QPoint(offset_x, offset_y)

# -*- coding: utf-8 -*-
from typing import List

import numpy as np
import cv2

from qtpy.QtWidgets import (
    QPushButton, QLabel, QWidget, QSlider,
    QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QStyle
)
from qtpy.QtCore import QObject, Qt, QPoint, QTimer
from qtpy.QtCore import Slot
from qtpy.QtCore import Signal
from qtpy.QtGui import QImage, QPixmap, QPainter

from utils import hbox, vbox, get_standard_icon


class VideoPlayerWidget(QWidget):
    def __init__(self, **kwargs):
        super(VideoPlayerWidget, self).__init__(**kwargs)

        self._video = None
        self._playing = False

        self.view = GraphicsView()

        self.play_button = QPushButton()
        self.play_button.setIcon(
            get_standard_icon(QStyle.SP_MediaPlay)
        )
        self.play_button.clicked.connect(
            self.on_play_button_clicked
        )

        self.seekbar = QSlider(Qt.Horizontal)
        self.seekbar.setMinimum(0)
        self.seekbar.setMaximum(0)
        self.seekbar.valueChanged.connect(
            self.on_seekbar_valueChanged
        )

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.fetch_frame)

        layout = vbox([
            self.view,
            hbox([self.play_button, self.seekbar])
        ])
        self.setLayout(layout)

    def open_video(self, src_path):
        self._video = cv2.VideoCapture(src_path)

        if self.video_is_opened():
            ret, frame = self._video.read()
            self.view.update_image(frame)
            self.seekbar.setMaximum(
                self._video.get(cv2.CAP_PROP_FRAME_COUNT)
            )
            return True
        else:
            return False

    def video_is_opened(self):
        return self._video is not None and self._video.isOpened()

    def start_video(self):
        self._playing = True
        self.play_button.setIcon(
            get_standard_icon(QStyle.SP_MediaPause)
        )

        fps = self._video.get(cv2.CAP_PROP_FPS)
        self.update_timer.start(1000. / fps)

    def stop_video(self):
        self._playing = False
        self.play_button.setIcon(
            get_standard_icon(QStyle.SP_MediaPlay)
        )
        self.update_timer.stop()

    def fetch_frame(self):

        ret, frame = self._video.read()

        if not ret:
            self.stop_video()
            return

        self.view.update_image(frame)
        pos = self._video.get(cv2.CAP_PROP_POS_FRAMES)
        self.seekbar.setValue(pos)

    def on_play_button_clicked(self):

        if not self.video_is_opened():
            return

        if self._playing:
            self.stop_video()
        else:
            self.start_video()

    def on_seekbar_valueChanged(self):
        pass


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

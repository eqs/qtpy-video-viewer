# -*- coding: utf-8 -*-
import sys

from qtpy.QtWidgets import (
    QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout
)
from qtpy.QtCore import QObject, Qt

from player import VideoPlayerWidget
from utils import vbox


class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.main_widget = QWidget(self)

        player = VideoPlayerWidget()
        player.open_video(r'C:\Users\chikuwa\Videos\flower.mp4')

        layout = vbox([
            player
        ])

        self.main_widget.setLayout(layout)

        self.setCentralWidget(self.main_widget)
        self.resize(640, 480)


def main():
    app = QApplication(sys.argv)

    view = MainWindow()

    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

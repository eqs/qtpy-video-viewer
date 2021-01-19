# -*- coding: utf-8 -*-
import sys

from qtpy.QtWidgets import (
    QMainWindow, QApplication, QLabel, QWidget, QFileDialog, QAction
)
from qtpy.QtCore import QObject, Qt

from player import VideoPlayerWidget
from utils import vbox


class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.main_widget = QWidget(self)

        self.player = VideoPlayerWidget()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileOpenAction = QAction('Open', self)
        fileOpenAction.triggered.connect(
            self.on_fileOpenAction_triggered
        )
        fileMenu.addAction(fileOpenAction)

        layout = vbox([self.player])

        self.main_widget.setLayout(layout)

        self.setCentralWidget(self.main_widget)
        self.resize(640, 480)

    def on_fileOpenAction_triggered(self):
        src_video_path, _ = QFileDialog.getOpenFileName(
            self, 'Open video file', '.',
            'Video files (*.avi *.mp4)'
        )

        if len(src_video_path) == 0:
            return

        self.player.open_video(src_video_path)


def main():
    app = QApplication(sys.argv)

    view = MainWindow()

    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

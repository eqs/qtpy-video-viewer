# -*- coding: utf-8 -*-
from typing import List, Union, Tuple

from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import (
    QWidget, QLayout, QHBoxLayout, QVBoxLayout, QStyle
)

def get_standard_icon(sp: QStyle.StandardPixmap):
    style = QCoreApplication.instance().style()
    return style.standardIcon(sp)


def _generate_box_layout(t: str,
                         widgets: List[Union[QWidget, QLayout, Tuple]]):

    if t == 'h':
        layout = QHBoxLayout()
    elif t == 'v':
        layout = QVBoxLayout()
    else:
        raise RuntimeError()

    for widget in widgets:
        if isinstance(widget, tuple):
            w, stretch = widget
            assert isinstance(stretch, int)
        else:
            w = widget
            stretch = 0

        if isinstance(w, QWidget):
            layout.addWidget(w, stretch)
        elif isinstance(w, QLayout):
            layout.addLayout(w, stretch)
        else:
            raise TypeError(f'Illegal type of widget is detected: {widget}')

    return layout


def hbox(widgets: List[Union[QWidget, QLayout, Tuple]]):
    return _generate_box_layout('h', widgets)


def vbox(widgets: List[Union[QWidget, QLayout]]):
    return _generate_box_layout('v', widgets)

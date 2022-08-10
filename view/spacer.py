from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QLabel, QPushButton
from PySide6.QtCore import Qt 

def vertical_spacer():
    return QSpacerItem(20,40,QSizePolicy.Minimum, QSizePolicy.Expanding)
def horizontal_spacer():
    return QSpacerItem(20,40,QSizePolicy.Expanding, QSizePolicy.Minimum)
def label(text):
    return QLabel(text, alignment=Qt.AlignCenter)

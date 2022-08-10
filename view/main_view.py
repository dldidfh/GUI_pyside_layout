
from functools import partial
from PySide6.QtWidgets import  QLabel, QWidget, QPushButton
from PySide6.QtCore import QRect
from config import * 
from style.main_style import * 
from controller.switcher import widget_switching
class MainWidget(QWidget):
    def __init__(self, parent, *args) -> None: # 상위 윈도우
        super().__init__(parent)
        self.args = args
        self.main_window = parent

        self.setGeometry(QRect(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1]))
        self.logo()
        self.intro()
        self.button()

    def logo(self):
        logo_label = QLabel(self)
        logo_label.setText("qwe")
        logo_label.setStyleSheet(LOGO_BACKGROUND_COLOR)
        logo_label.setGeometry(QRect(0,0,WINDOW_SIZE[0],LOGO_FRAME_H))

    def intro(self):
        logo_label = QLabel(self)
        logo_label.setText("Intro")
        logo_label.setStyleSheet(INTRO_BACKGROUND_COLOR)
        logo_label.setGeometry(QRect(INTRO_X, INTRO_Y, INTRO_W, INTRO_H))
    
    def button(self):
        # box_layout = QVBoxLayout(self)
        box1 = QPushButton(self)
        box1.setText('button1')
        box1.setGeometry(QRect(BOX1_X, BOX1_Y, BOX1_W, BOX1_H))
        box2 = QPushButton(self)
        box2.setText('button2')
        box2.setGeometry(QRect(BOX2_X, BOX2_Y, BOX2_W, BOX2_H))
        box3 = QPushButton(self)
        box3.setText('button3')
        box3.setGeometry(QRect(BOX3_X, BOX3_Y, BOX3_W, BOX3_H))

        box1.clicked.connect(partial(widget_switching, self.main_window, self, "settings_view", self.args))



from PySide6.QtWidgets import  QLabel, QPushButton, QWidget
from PySide6.QtCore import QRect
from config import * 
from style.settings_style import * 
from controller.switcher import widget_switching
class SettingWidget(QWidget):
    def __init__(self, parent, *args) -> None: # 상위 윈도우
        super().__init__(parent)
        self.setGeometry(QRect(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1]))
        self.main_window = parent
        self.args = args
        self.button()
        self.schedule()

    def schedule(self):
        schedule_label = QLabel(self)
        schedule_label.setText("qwe")
        schedule_label.setStyleSheet(SCHEDULE_BACKGROUND_COLOR)
        schedule_label.setGeometry(QRect(0,0,WINDOW_SIZE[0],SCHEDULE_FRAME_H))
    
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

        box1.clicked.connect(widget_switching(self.main_window, self, "main_view", self.args))




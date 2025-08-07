# MIT License
# Copyright (c) 2024 dldidfh2@gmail.com

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from config import WINDOW_SIZE, TITLE
from view.cctv_view import CCTVWidget


class MainApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setWindowTitle(TITLE)
        # 최대화 최소화  버튼 추가
        self.setWindowFlags(
            Qt.WindowTitleHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
        )

        # set CCTV widget as the central widget
        self.cctv_widget = CCTVWidget(self)
        self.setCentralWidget(self.cctv_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec())
    
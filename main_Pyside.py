from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QApplication, QMainWindow
import sys 
from config import WINDOW_SIZE, TITLE
from controller.switcher import widget_switching
class MainApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1])
        self.setWindowTitle(TITLE)
        # 최대화 최소화  버튼 추가 
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        # widget 불러오기
        widget_switching(self, None, "main_view")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec())
    
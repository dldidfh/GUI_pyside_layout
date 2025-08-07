from __future__ import annotations

import cv2
from datetime import datetime
from typing import List, Tuple

from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QPushButton

from config import WINDOW_SIZE, RTSP_URLS
from database import DatabaseManager


class DummyModel:
    """Placeholder model. Replace with real implementation."""

    def predict(self, image):
        # TODO: replace with actual prediction logic
        return "unknown", 0


model = DummyModel()


class VideoThread(QThread):
    frame_received = Signal(object)

    def __init__(self, rtsp_url: str):
        super().__init__()
        self.rtsp_url = rtsp_url
        self._running = True

    def run(self) -> None:
        cap = cv2.VideoCapture(self.rtsp_url)
        while self._running:
            ret, frame = cap.read()
            if ret:
                self.frame_received.emit(frame)
        cap.release()

    def stop(self) -> None:
        self._running = False


class MainWidget(QWidget):
    def __init__(self, parent, *args) -> None:
        super().__init__(parent)
        self.main_window = parent
        self.setGeometry(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])

        self.db = DatabaseManager()
        self.buffer: List[Tuple[int, str, datetime]] = []

        self.labels: List[QLabel] = []
        self.threads: List[VideoThread] = []

        self._setup_ui()
        self._start_streams()
        self._start_flush_timer()

    def _setup_ui(self) -> None:
        for idx in range(2):
            label = QLabel(self)
            label.setGeometry(10 + idx * (WINDOW_SIZE[0] // 2), 10, WINDOW_SIZE[0] // 2 - 20, WINDOW_SIZE[1] - 80)
            label.setStyleSheet("background-color: black")
            label.setAlignment(Qt.AlignCenter)
            self.labels.append(label)

        self.export_btn = QPushButton("Export", self)
        self.export_btn.setGeometry(WINDOW_SIZE[0] - 110, 10, 100, 40)
        self.export_btn.clicked.connect(self.export_data)

    def _start_streams(self) -> None:
        for idx, url in enumerate(RTSP_URLS[:2]):
            thread = VideoThread(url)
            thread.frame_received.connect(lambda frame, i=idx: self._update_frame(i, frame))
            thread.start()
            self.threads.append(thread)

    def _start_flush_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.flush_buffer)
        self.timer.start(60 * 1000)

    def _update_frame(self, index: int, frame) -> None:
        gender, age = model.predict(frame)
        self.buffer.append((age, gender, datetime.now()))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(image).scaled(self.labels[index].size(), Qt.KeepAspectRatio)
        self.labels[index].setPixmap(pix)

    def flush_buffer(self) -> None:
        self.db.insert_records(self.buffer)
        self.buffer.clear()

    def export_data(self) -> None:
        filename = f"result_{datetime.now():%Y%m%d}.xlsx"
        self.db.export_last_year(filename)

    def closeEvent(self, event) -> None:
        for thread in self.threads:
            thread.stop()
            thread.wait()
        self.db.close()
        super().closeEvent(event)


# MIT License
# Copyright (c) 2024 dldidfh2@gmail.com

from datetime import datetime, timedelta
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
)
import cv2
import pandas as pd
import mysql.connector

from config import WINDOW_SIZE, RTSP_URLS, DB_CONFIG


class DummyModel:
    """Placeholder model that returns constant predictions."""

    def predict(self, image):
        # Replace with actual model inference
        return 30, "male"


class CCTVWidget(QWidget):
    """Widget displaying two RTSP streams with export functionality."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])

        # Video capture objects for each RTSP stream
        self.caps = [cv2.VideoCapture(url) for url in RTSP_URLS]
        self.labels = [QLabel(self), QLabel(self)]

        # Layout for video displays
        video_layout = QHBoxLayout()
        for label in self.labels:
            label.setMinimumSize(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 50)
            video_layout.addWidget(label)

        # Export button at the top-right corner
        self.export_btn = QPushButton("Export", self)
        self.export_btn.clicked.connect(self.export_to_excel)
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.export_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(video_layout)
        self.setLayout(main_layout)

        # Prediction handling
        self.model = DummyModel()
        self.pred_buffer = []

        # Timer for updating frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

        # Timer for saving predictions every minute
        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self.save_predictions)
        self.save_timer.start(60 * 1000)

        # MySQL database connection
        self.db_conn = mysql.connector.connect(**DB_CONFIG)
        self.db_cursor = self.db_conn.cursor()

    def update_frames(self):
        """Read frames from each RTSP stream and display them."""
        for cap, label in zip(self.caps, self.labels):
            ret, frame = cap.read()
            if not ret:
                continue

            age, gender = self.model.predict(frame)
            self.pred_buffer.append((age, gender, datetime.now()))

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(
                frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            label.setPixmap(QPixmap.fromImage(qimg))

    def save_predictions(self):
        """Insert buffered predictions into the database every minute."""
        if not self.pred_buffer:
            return

        query = "INSERT INTO result (age, gender, timestamp) VALUES (%s, %s, %s)"
        self.db_cursor.executemany(query, self.pred_buffer)
        self.db_conn.commit()
        self.pred_buffer.clear()

    def export_to_excel(self):
        """Export the last year's data to an Excel file."""
        one_year_ago = datetime.now() - timedelta(days=365)
        query = (
            "SELECT id, age, gender, timestamp FROM result WHERE timestamp >= %s"
        )
        self.db_cursor.execute(query, (one_year_ago,))
        rows = self.db_cursor.fetchall()

        df = pd.DataFrame(rows, columns=["id", "age", "gender", "timestamp"])
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel", "results.xlsx", "Excel Files (*.xlsx)"
        )
        if path:
            df.to_excel(path, index=False)

    def closeEvent(self, event):
        for cap in self.caps:
            cap.release()
        if hasattr(self, "db_conn"):
            self.db_conn.close()
        super().closeEvent(event)


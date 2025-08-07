# MIT License
# Copyright (c) 2024 dldidfh2@gmail.com

WINDOW_SIZE = (1200, 800)
ICON_PATH = "src/icon.ico"

TITLE = "TDC(Traffic Data Collector)v2.0"

# RTSP stream URLs for the two CCTV cameras
# Replace these placeholders with actual RTSP addresses
RTSP_URLS = [
    "rtsp://example.com/stream1",
    "rtsp://example.com/stream2",
]

# MySQL database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "test",
}

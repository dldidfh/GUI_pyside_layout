import mysql.connector
import pandas as pd
from datetime import datetime
from typing import List, Tuple

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


class DatabaseManager:
    """Simple helper for storing and exporting CCTV results."""

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        self.cursor = self.conn.cursor()

    def insert_records(self, records: List[Tuple[int, str, datetime]]) -> None:
        """Insert multiple (age, gender, timestamp) records."""
        if not records:
            return
        sql = "INSERT INTO result (age, gender, timestamp) VALUES (%s, %s, %s)"
        self.cursor.executemany(sql, records)
        self.conn.commit()

    def export_last_year(self, file_path: str) -> None:
        """Export result records from the last year to an Excel file."""
        query = (
            "SELECT id, age, gender, timestamp FROM result "
            "WHERE timestamp >= NOW() - INTERVAL 1 YEAR"
        )
        df = pd.read_sql(query, self.conn)
        df.to_excel(file_path, index=False)

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()


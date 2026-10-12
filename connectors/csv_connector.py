"""
OZARK Connectors — Example CSV Connector

Replace or extend this for your actual data sources.
"""

import csv
from pathlib import Path
from typing import Any, Iterator

from connectors.base import BaseConnector


class CsvConnector(BaseConnector):
    """
    Reads records from a CSV file and loads them into PostgreSQL.

    Config keys:
      - file_path (str): Absolute path to the CSV file.
      - delimiter (str): CSV delimiter character. Default: ","
    """

    name = "csv"

    def connect(self) -> None:
        path = Path(self.config["file_path"])
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        self.log.info("CSV connector ready", path=str(path))

    def extract(self) -> Iterator[dict[str, Any]]:
        delimiter = self.config.get("delimiter", ",")
        with open(self.config["file_path"], newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                yield dict(row)

    def transform(self, record: dict[str, Any]) -> dict[str, Any]:
        # TODO: implement field mapping / cleaning
        return record

    def load(self, record: dict[str, Any]) -> None:
        # TODO: insert into PostgreSQL using asyncpg or SQLAlchemy
        self.log.debug("Loading record", record=record)

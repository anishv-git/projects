from __future__ import annotations
import duckdb
from contextlib import contextmanager
from typing import Iterator
from .config import DB_PATH

@contextmanager
def duckdb_connection() -> Iterator[duckdb.DuckDBPyConnection]:
    connection = duckdb.connect(str(DB_PATH))
    try:
        yield connection
    finally:
        connection.close()

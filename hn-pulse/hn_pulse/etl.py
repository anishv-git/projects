from __future__ import annotations
from .io import duckdb_connection


def build_analytics() -> None:
    with duckdb_connection() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS stories AS
            SELECT
                id,
                by,
                time,
                to_timestamp(time) AS ts,
                date_trunc(day, to_timestamp(time)) AS day,
                title,
                url,
                score,
                descendants
            FROM raw_items
            WHERE type = story;
            """
        )
        con.execute(
            """
            CREATE OR REPLACE VIEW daily_stats AS
            SELECT
                day,
                COUNT(*) AS num_stories,
                AVG(score) AS avg_score,
                MAX(score) AS max_score
            FROM stories
            GROUP BY 1
            ORDER BY 1 DESC;
            """
        )

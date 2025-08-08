from __future__ import annotations
import time
from typing import Any, Dict, Iterable, List, Optional
import requests
from .config import HN_API_BASE, USER_AGENT, REQUEST_TIMEOUT_S, MAX_TOP_STORIES
from .io import duckdb_connection

HEADERS = {"User-Agent": USER_AGENT}


def fetch_json(url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_S)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None


def fetch_top_story_ids(limit: int = MAX_TOP_STORIES) -> List[int]:
    url = f"{HN_API_BASE}/topstories.json"
    data = fetch_json(url)
    if not isinstance(data, list):
        return []
    return [int(x) for x in data[:limit]]


def fetch_item(item_id: int) -> Optional[Dict[str, Any]]:
    url = f"{HN_API_BASE}/item/{item_id}.json"
    return fetch_json(url)


def upsert_items(items: Iterable[Dict[str, Any]]) -> int:
    # Create table and upsert
    with duckdb_connection() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS raw_items (
                id BIGINT PRIMARY KEY,
                type VARCHAR,
                by VARCHAR,
                time BIGINT,
                title VARCHAR,
                url VARCHAR,
                score INTEGER,
                descendants INTEGER,
                kids JSON,
                raw JSON
            );
            """
        )
        count = 0
        for item in items:
            if not item or "id" not in item:
                continue
            # Normalize fields
            record = {
                "id": int(item.get("id")),
                "type": item.get("type"),
                "by": item.get("by"),
                "time": int(item.get("time")) if item.get("time") else None,
                "title": item.get("title"),
                "url": item.get("url"),
                "score": int(item.get("score")) if item.get("score") else None,
                "descendants": int(item.get("descendants")) if item.get("descendants") else None,
                "kids": item.get("kids"),
                "raw": item,
            }
            con.execute(
                """
                INSERT OR REPLACE INTO raw_items AS t
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, to_json(?), to_json(?)
                """,
                [
                    record["id"],
                    record["type"],
                    record["by"],
                    record["time"],
                    record["title"],
                    record["url"],
                    record["score"],
                    record["descendants"],
                    record["kids"],
                    record["raw"],
                ],
            )
            count += 1
        return count


def ingest_top_stories(batch_sleep_s: float = 0.2) -> int:
    ids = fetch_top_story_ids()
    if not ids:
        return 0
    items: List[Dict[str, Any]] = []
    for item_id in ids:
        item = fetch_item(item_id)
        if item:
            items.append(item)
        time.sleep(batch_sleep_s)
    return upsert_items(items)

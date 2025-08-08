from __future__ import annotations
from hn_pulse.hn_client import ingest_top_stories


def main() -> None:
    count = ingest_top_stories()
    print(f"Ingested or updated {count} items")


if __name__ == "__main__":
    main()

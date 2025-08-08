from __future__ import annotations
from hn_pulse.etl import build_analytics


def main() -> None:
    build_analytics()
    print("Analytics built")


if __name__ == "__main__":
    main()

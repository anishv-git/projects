from __future__ import annotations
from hn_pulse.model import train


def main() -> None:
    meta = train()
    print("Model trained:", meta)


if __name__ == "__main__":
    main()

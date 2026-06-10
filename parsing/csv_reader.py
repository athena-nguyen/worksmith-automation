import csv
from pathlib import Path


def read_csv(filepath: Path) -> list[dict]:
    if not filepath.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

from pathlib import Path

ROOT = Path(__file__).parent


def get(path_item: str, *path_items: str) -> Path:
    return ROOT / Path(path_item, *path_items)

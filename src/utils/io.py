from __future__ import annotations
import os
from pathlib import Path
import yaml

def ensure_dirs() -> None:
    dirs = [
        "data/raw", "data/processed", "data/train", "data/validation", "data/test",
        "docs/datasets", "db", "outputs/figures", "outputs/metrics", "outputs/models"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def atomic_write_text(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)

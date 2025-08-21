from pathlib import Path
import os

def safe_name(dest_dir: Path, name: str) -> Path:
    p = dest_dir / name
    if not p.exists():
        return p
    stem = p.stem
    suffix = p.suffix
    i = 1
    while True:
        cand = dest_dir / f"{stem} ({i}){suffix}"
        if not cand.exists():
            return cand
        i += 1

def ensure_dir(p: Path, simulate: bool):
    if not p.exists():
        if simulate:
            print(f"[SIMULATE] mkdir -p {p}")
        else:
            p.mkdir(parents=True, exist_ok=True)

def should_skip(p: Path, include_hidden: bool, min_size: int) -> bool:
    if not include_hidden and p.name.startswith("."):
        return True
    if p.is_dir():
        return True
    if min_size > 0 and p.stat().st_size < min_size:
        return True
    return False

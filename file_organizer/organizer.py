import os, shutil, csv
from pathlib import Path
from datetime import datetime
from utils import safe_name, ensure_dir, should_skip

def file_modified_date(p: Path) -> datetime:
    return datetime.fromtimestamp(p.stat().st_mtime)

def target_by_ext(file_path: Path, dst: Path) -> Path:
    ext = file_path.suffix.lower().lstrip(".") or "noext"
    return dst / ext

def target_by_date(file_path: Path, dst: Path, granularity: str) -> Path:
    d = file_modified_date(file_path)
    if granularity == "ym":
        return dst / f"{d:%Y}" / f"{d:%m}"
    elif granularity == "ymd":
        return dst / f"{d:%Y}" / f"{d:%m}" / f"{d:%d}"
    else:
        return dst / f"{d:%Y}"

def write_log_row(log_path: Path, action: str, src: Path, dst: Path, simulate: bool):
    if simulate:
        return
    exists = log_path.exists()
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["timestamp","action","src","dst"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), action, str(src), str(dst)])

def do_move_or_copy(src: Path, dst_dir: Path, mode: str, simulate: bool, log_path: Path):
    ensure_dir(dst_dir, simulate)
    dst_final = safe_name(dst_dir, src.name)

    if simulate:
        print(f"[SIMULATE] {mode.upper()} {src} -> {dst_final}")
        return

    if mode == "move":
        shutil.move(str(src), str(dst_final))
        write_log_row(log_path, "move", src, dst_final, simulate)
    elif mode == "copy":
        shutil.copy2(str(src), str(dst_final))
        write_log_row(log_path, "copy", src, dst_final, simulate)

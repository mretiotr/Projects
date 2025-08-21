import os, shutil, csv
from pathlib import Path
from datetime import datetime
from utils import ensure_dir, safe_name

def undo_from_log(log_path: Path, simulate: bool):
    if not log_path.exists():
        print("S'ka log për undo.")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("Log bosh, s'ka çfarë të zhbëhet.")
        return

    for row in reversed(rows):
        action, src, dst = row["action"], Path(row["src"]), Path(row["dst"])

        if action == "move":
            back_dir = src.parent
            ensure_dir(back_dir, simulate)
            back_path = safe_name(back_dir, dst.name)

            if simulate:
                print(f"[SIMULATE][UNDO] MOVE BACK {dst} -> {back_path}")
            else:
                if dst.exists():
                    shutil.move(str(dst), str(back_path))
                else:
                    print(f"[WARN][UNDO] Skipped (missing): {dst}")

        elif action == "copy":
            if simulate:
                print(f"[SIMULATE][UNDO] DELETE {dst}")
            else:
                if dst.exists():
                    try:
                        os.remove(dst)
                    except IsADirectoryError:
                        shutil.rmtree(dst, ignore_errors=True)

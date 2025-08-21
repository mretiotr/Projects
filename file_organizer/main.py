import argparse, sys, os
from pathlib import Path
from organizer import target_by_ext, target_by_date, do_move_or_copy
from utils import should_skip
from undo import undo_from_log

LOG_DEFAULT = "ops.log"

def main():
    p = argparse.ArgumentParser(description="Organizim i file-ve sipas extension ose dates.")
    p.add_argument("--src", required=True, help="Folder burim")
    p.add_argument("--dst", required=True, help="Folder destinacion")
    p.add_argument("--mode", choices=["move","copy"], default="move")
    p.add_argument("--organize", choices=["ext","date"], default="ext")
    p.add_argument("--date-granularity", choices=["y","ym","ymd"], default="ym")
    p.add_argument("--include-hidden", action="store_true")
    p.add_argument("--min-size", type=int, default=0)
    p.add_argument("--simulate", action="store_true")
    p.add_argument("--log", default=LOG_DEFAULT)
    p.add_argument("--undo", action="store_true")
    args = p.parse_args()

    log_path = Path(args.log)

    if args.undo:
        undo_from_log(log_path, args.simulate)
        return

    src = Path(args.src).expanduser().resolve()
    dst = Path(args.dst).expanduser().resolve()
    if not src.exists() or not src.is_dir():
        print("Gabim: --src nuk ekziston ose s'është folder.")
        sys.exit(1)

    count = 0
    for root, _, files in os.walk(src):
        for name in files:
            fpath = Path(root) / name
            if should_skip(fpath, args.include_hidden, args.min_size):
                continue

            if args.organize == "ext":
                target_dir = target_by_ext(fpath, dst)
            else:
                target_dir = target_by_date(fpath, dst, args.date_granularity)

            do_move_or_copy(fpath, target_dir, args.mode, args.simulate, log_path)
            count += 1

    print(f"OK. Përpunuar {count} file.")
    if not args.simulate:
        print(f"Log: {log_path}")

if __name__ == "__main__":
    main()

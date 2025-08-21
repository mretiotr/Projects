# todo.py
import json, sys, os
FILE = "todos.json"

def load():
    if not os.path.exists(FILE): return []
    with open(FILE, "r", encoding="utf-8") as f: return json.load(f)

def save(items): 
    with open(FILE, "w", encoding="utf-8") as f: json.dump(items, f, indent=2)

def usage():
    print("Usage: python todo.py [add <txt> | list | done <id> | rm <id>]")

def main():
    data = load()
    if len(sys.argv) < 2: return usage()
    cmd = sys.argv[1]
    if cmd == "add":
        txt = " ".join(sys.argv[2:])
        data.append({"id": (data[-1]["id"]+1 if data else 1), "txt": txt, "done": False})
        save(data); print("Added.")
    elif cmd == "list":
        for t in data:
            s = "✔" if t["done"] else " "
            print(f'{t["id"]:2d}. [{s}] {t["txt"]}')
    elif cmd == "done":
        i = int(sys.argv[2]); 
        for t in data:
            if t["id"]==i: t["done"]=True; save(data); print("Done."); break
        else: print("Not found")
    elif cmd == "rm":
        i = int(sys.argv[2]); 
        data = [t for t in data if t["id"]!=i]; save(data); print("Removed.")
    else:
        usage()

if __name__ == "__main__":
    main()

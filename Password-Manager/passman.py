# passman.py
import json, os, getpass
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
VAULT_FILE = "vault.bin"

def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f: f.write(key)
    with open(KEY_FILE, "rb") as f: return f.read()

def load(fer):
    if not os.path.exists(VAULT_FILE): return {}
    data = fer.decrypt(open(VAULT_FILE, "rb").read()).decode()
    return json.loads(data)

def save(fer, obj):
    token = fer.encrypt(json.dumps(obj).encode())
    with open(VAULT_FILE, "wb") as f: f.write(token)

def main():
    fer = Fernet(get_key())
    vault = load(fer)
    print("Commands: add <site>, get <site>, list")
    while True:
        try:
            cmd = input("> ").strip().split()
            if not cmd: continue
            if cmd[0]=="add":
                site = cmd[1]; user = input("username: "); pw = getpass.getpass("password: ")
                vault[site]={"user":user,"pw":pw}; save(fer, vault); print("Saved.")
            elif cmd[0]=="get":
                site = cmd[1]; print(vault.get(site,"Not found"))
            elif cmd[0]=="list":
                print(list(vault.keys()))
            elif cmd[0] in ("quit","exit"): break
        except KeyboardInterrupt:
            break

if __name__=="__main__":
    main()

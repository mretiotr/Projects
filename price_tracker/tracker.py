import csv, json, os, re, argparse, time
from pathlib import Path
from typing import Dict, Tuple, Optional
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib, ssl
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
PRODUCTS_CSV = BASE_DIR / "products.csv"
STATE_JSON = BASE_DIR / "state.json"
ENV_FILE = BASE_DIR / ".env"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def load_state() -> Dict[str, Dict]:
    if STATE_JSON.exists():
        try:
            return json.loads(STATE_JSON.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_state(state: Dict[str, Dict]):
    STATE_JSON.write_text(json.dumps(state, indent=2), encoding="utf-8")

def parse_price(text: str) -> Optional[float]:
    # extract first number like 9.99 or 1,299.50
    m = re.search(r"(\d+[\.,]?\d*[\.,]?\d*)", text.replace(",", ""))
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None

def fetch_price(url: str, selector: str, timeout: int = 15) -> Tuple[Optional[float], str]:
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    node = soup.select_one(selector)
    if not node:
        return None, "selector_not_found"
    price_text = node.get_text(strip=True)
    price = parse_price(price_text)
    if price is None:
        return None, "price_parse_failed"
    return price, price_text

def send_email(subject: str, body: str) -> None:
    load_dotenv(ENV_FILE)
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ.get("SMTP_USER")
    pwd = os.environ.get("SMTP_PASS")
    from_addr = os.environ.get("SMTP_FROM", user)
    to_addr = os.environ.get("ALERT_TO")

    if not all([host, port, user, pwd, from_addr, to_addr]):
        print("[WARN] SMTP env vars missing; skipping email.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user, pwd)
        server.send_message(msg)

def check_products(dry_run: bool = False) -> None:
    if not PRODUCTS_CSV.exists():
        print(f"[ERR] Missing {PRODUCTS_CSV}")
        return

    state = load_state()
    alerted = 0
    checked = 0

    with open(PRODUCTS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            url = row["url"].strip()
            selector = row["selector"].strip()
            currency = row.get("currency", "").strip()
            target = float(row["target_price"])

            print(f"-> Checking: {name}")
            try:
                price, raw = fetch_price(url, selector)
            except requests.HTTPError as e:
                print(f"   [HTTP] {e}")
                continue
            except requests.RequestException as e:
                print(f"   [NET] {e}")
                continue

            checked += 1
            if price is None:
                print(f"   [PARSE] Failed (selector/raw): {selector} / {raw}")
                continue

            print(f"   Current price: {currency}{price} (raw: '{raw}') | target <= {currency}{target}")

            # state for this url
            s = state.get(url, {})
            last_notified_price = s.get("last_notified_price")
            last_notified_at = s.get("last_notified_at")

            if price <= target and price != last_notified_price:
                alerted += 1
                subject = f"Price drop: {name} @ {currency}{price}"
                body = f"""{name}
URL: {url}
Price now: {currency}{price}
Target: {currency}{target}
Extracted from: '{raw}'
"""
                if dry_run:
                    print("   [DRY-RUN] Would send email.")
                else:
                    send_email(subject, body)
                    state[url] = {"last_notified_price": price, "last_notified_at": int(time.time())}
                    print("   [ALERT] Email sent.")
            else:
                print("   No alert.")

    if not dry_run:
        save_state(state)

    print(f"Done. Checked={checked}, Alerts={alerted}{' (dry-run)' if dry_run else ''}.")

def list_products():
    if not PRODUCTS_CSV.exists():
        print(f"[ERR] Missing {PRODUCTS_CSV}")
        return
    with open(PRODUCTS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            print(f"- {row['name']} -> {row['url']} (selector: {row['selector']}, target: {row['currency']}{row['target_price']})")

def main():
    ap = argparse.ArgumentParser(description="Configurable E-commerce Price Tracker")
    ap.add_argument("--check", action="store_true", help="Check all products and alert if threshold met")
    ap.add_argument("--list", action="store_true", help="List products from CSV")
    ap.add_argument("--dry-run", action="store_true", help="Do everything but do not email or update state")
    args = ap.parse_args()

    if args.list:
        list_products()
        return
    if args.check:
        check_products(dry_run=args.dry_run)
        return

    print("Nothing to do. Use --list or --check.")

if __name__ == "__main__":
    main()

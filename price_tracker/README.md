# E-commerce Price Tracker (Configurable via CSV)

Minimal, configurable price tracker. You define products in `products.csv` with a CSS selector for the price.
The script fetches each page, extracts the price, compares to a target, and sends an email alert when the price
is at or below your threshold. State is saved so you don't get spammed repeatedly.

## Features
- Multiple products from one CSV
- CSS selector per product (works on many sites)
- Email alerts via SMTP (Gmail or other providers)
- State (last notified) saved to `state.json`
- Safe user-agent header to reduce blocks
- Dry-run mode

## Quickstart

1) Install deps:
```bash
pip install -r requirements.txt
```

2) Set SMTP credentials in `.env` (create it next to the script):
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_FROM=your_email@gmail.com
ALERT_TO=destination@example.com
```

> For Gmail, you likely need an App Password (2FA required).

3) Edit `products.csv`:
Example included targets a demo website (books.toscrape.com).
Columns:
```
name,url,selector,currency,target_price
```

4) Run:
```bash
python tracker.py --check
```
Dry-run (no emails, no state updates):
```bash
python tracker.py --check --dry-run
```

List current products:
```bash
python tracker.py --list
```

5) Cron example (every hour):
```
0 * * * * /usr/bin/python /path/to/tracker.py --check >> /path/to/price.log 2>&1
```

## CSV Example (`products.csv`)
```
name,url,selector,currency,target_price
Attic Book,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html,p.price_color,£,30.00
```

## Notes
- **Selector** is a CSS selector for the price element on the page. Use your browser devtools to find it.
- If your site requires JS to render prices, this minimal tracker won't work (no headless browser). Use a service or Selenium instead.
- Be respectful of website terms of service and robots.txt.

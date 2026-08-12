import os
import datefinder
from datetime import datetime, timedelta
from pathlib import Path

# 🔋 2026 Project Paths
KB_DIR = Path(r"C:\Projects\AWS AGENT\knowledge_base")
LOOKAHEAD_DAYS = 90  # Alert for anything in the next 3 months


def scan_for_deadlines():
    print(f"🕵️ Scanning for 2026 Deadlines (Next {LOOKAHEAD_DAYS} days)...")
    today = datetime.now()
    threshold = today + timedelta(days=LOOKAHEAD_DAYS)
    alerts = []

    for md_file in KB_DIR.glob("**/*.md"):
        content = ""
        # 🛠️ Encoding Fix: Try UTF-8-sig first, then UTF-16
        encodings = ['utf-8-sig', 'utf-16', 'latin-1']
        
        for enc in encodings:
            try:
                with open(md_file, 'r', encoding=enc) as f:
                    content = f.read()
                break # Successfully read the file
            except (UnicodeDecodeError, Exception):
                continue
        
        if not content:
            continue

        # Find dates in the text
        matches = datefinder.find_dates(content)
        for date_match in matches:
            if today < date_match <= threshold:
                alerts.append({
                    "date": date_match.strftime('%Y-%m-%d'),
                    "file": md_file.name,
                    "sector": md_file.parent.name
                })

    if alerts:
        print(f"⚠️ FOUND {len(alerts)} UPCOMING DEADLINES!")
        for a in sorted(alerts, key=lambda x: x['date']):
            print(f"📅 {a['date']} | Sector: {a['sector'].upper()} | File: {a['file']}")
    else:
        print("✅ No upcoming deadlines found in the scan window.")
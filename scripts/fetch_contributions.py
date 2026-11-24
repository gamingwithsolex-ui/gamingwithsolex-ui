#!/usr/bin/env python3
import json, os, re
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

username = os.getenv("GITHUB_USERNAME", "gamingwithsolex-ui")
url = f"https://github.com/users/{username}/contributions"
response = requests.get(url, headers={"User-Agent": "profile-readme-generator"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
days = []
for cell in soup.select("td[data-date]"):
    date = cell.get("data-date")
    label = cell.get("aria-label", "")
    match = re.search(r"(\d+)\s+contribution", label)
    count = int(match.group(1)) if match else 0
    level = int(cell.get("data-level", "0"))
    if date:
        days.append({"date": date, "count": count, "level": level})
if not days:
    raise SystemExit("No contribution cells found; GitHub may have changed its markup.")
payload = {"username": username, "generated_at": datetime.now(timezone.utc).isoformat(),
           "days": days, "total": sum(d["count"] for d in days)}
out = Path("data/contributions.json")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"Saved {len(days)} days and {payload['total']} contributions.")

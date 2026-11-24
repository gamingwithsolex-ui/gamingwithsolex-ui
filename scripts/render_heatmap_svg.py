#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date, timedelta

data = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
days = data.get("days", [])
if not days:
    raise SystemExit("Run fetch_contributions.py first.")
while date.fromisoformat(days[0]["date"]).weekday() != 6:
    d = date.fromisoformat(days[0]["date"]) - timedelta(days=1)
    days.insert(0, {"date": d.isoformat(), "count": 0, "level": 0})
while len(days) % 7:
    d = date.fromisoformat(days[-1]["date"]) + timedelta(days=1)
    days.append({"date": d.isoformat(), "count": 0, "level": 0})
cell, gap, left, top = 11, 3, 48, 58
weeks = len(days)//7
width, height = left + weeks*(cell+gap)+24, 150
palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
rects, months, seen = [], [], set()
for i, item in enumerate(days):
    week, dow = divmod(i, 7)
    x, y = left+week*(cell+gap), top+dow*(cell+gap)
    level = max(0, min(4, int(item.get("level", 0))))
    delay = i*0.008
    rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{palette[level]}" opacity="0"><title>{item["date"]}: {item.get("count",0)} contributions</title><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur=".22s" fill="freeze"/></rect>')
    dt = date.fromisoformat(item["date"])
    if dt.day <= 7 and dt.strftime("%b") not in seen:
        seen.add(dt.strftime("%b"))
        months.append(f'<text x="{left+week*(cell+gap)}" y="40" fill="#aab6ae" font-family="monospace" font-size="11">{dt.strftime("%b")}</text>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="10" fill="#050807" stroke="#303b35"/>
<text x="20" y="25" fill="#39d353" font-family="monospace" font-size="15">&gt; GitHub Contributions — {data["username"]}</text>
{''.join(months)}{''.join(rects)}
<text x="20" y="{height-10}" fill="#aab6ae" font-family="monospace" font-size="10">{data.get("total",0):,} contributions in the displayed calendar</text></svg>'''
Path("contrib-heatmap.svg").write_text(svg, encoding="utf-8")

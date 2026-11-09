"""Write one static JSON file per day: site/days/YYYY-MM-DD.json."""

import json
from datetime import date, timedelta
from pathlib import Path

from medit.notify import make_notification
from medit.parse import load_modern, load_passages
from medit.schedule import order_for_cycle
from medit.typography import smarten

ROOT = Path(__file__).resolve().parent.parent
START = date(2026, 11, 10)
HORIZON_DAYS = 3653


def build(out_dir: Path, start: date, days: int) -> int:
    passages = {p["id"]: p for p in load_passages()}
    modern = load_modern()
    ids = list(passages)
    day_dir = Path(out_dir) / "days"
    day_dir.mkdir(parents=True, exist_ok=True)
    for stale in day_dir.glob("*.json"):
        stale.unlink()
    n = len(ids)
    orders: dict[int, list[str]] = {}
    for k in range(days):
        cycle = k // n
        if cycle not in orders:
            orders[cycle] = order_for_cycle(ids, cycle)
        p = passages[orders[cycle][k % n]]
        d = start + timedelta(days=k)
        modern_text, original_text = smarten(modern[p["id"]]), smarten(p["original"])
        entry = {
            "date": d.isoformat(),
            "book": p["book"],
            "section": p["section"],
            "ref": f'Book {p["book"]}, §{p["section"]}',
            "modern": modern_text,
            "original": original_text,
            "notification": make_notification(modern_text),
            "notification_original": make_notification(original_text),
        }
        (day_dir / f"{d.isoformat()}.json").write_text(
            json.dumps(entry, ensure_ascii=False) + "\n", encoding="utf-8")
    return days


def main() -> None:
    print(build(ROOT / "site", START, HORIZON_DAYS), "day files written")


if __name__ == "__main__":
    main()

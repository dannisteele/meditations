import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from medit.build import build
from medit.notify import make_notification
from medit.parse import load_passages
from medit.schedule import passage_id_for

START = date(2026, 11, 10)
KEYS = {"date", "book", "section", "ref", "modern", "original", "notification", "notification_original"}


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        (cls.out / "days").mkdir()
        (cls.out / "days" / "1999-01-01.json").write_text("{}")  # stale file
        cls.count = build(cls.out, START, 1000)
        cls.ids = [p["id"] for p in load_passages()]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def day(self, k):
        d = START + timedelta(days=k)
        return json.loads((self.out / "days" / f"{d.isoformat()}.json").read_text(encoding="utf-8"))

    def test_file_count(self):
        self.assertEqual(self.count, 1000)
        names = sorted(p.name for p in (self.out / "days").glob("*.json"))
        self.assertEqual(len(names), 1000)
        self.assertEqual(names[0], "2026-11-10.json")
        self.assertEqual(names[-1], f"{(START + timedelta(days=999)).isoformat()}.json")

    def test_shape(self):
        d = self.day(5)
        self.assertEqual(set(d), KEYS)
        self.assertEqual(d["ref"], f'Book {d["book"]}, §{d["section"]}')
        self.assertEqual(d["notification"], make_notification(d["modern"]))
        self.assertEqual(d["notification_original"], make_notification(d["original"]))
        self.assertEqual(d["date"], (START + timedelta(days=5)).isoformat())

    def test_first_cycle_no_repeats(self):
        seen = [(self.day(k)["book"], self.day(k)["section"]) for k in range(len(self.ids))]
        self.assertEqual(len(set(seen)), len(self.ids))

    def test_matches_schedule(self):
        d = self.day(700)
        self.assertEqual(f'{d["book"]}.{d["section"]}',
                         passage_id_for(START + timedelta(days=700), START, self.ids))

    def test_quotes_are_curly(self):
        for k in range(0, 1000, 7):
            d = self.day(k)
            for key in ("modern", "original", "notification", "notification_original"):
                self.assertNotIn('"', d[key], (k, key))
                self.assertNotIn("'", d[key], (k, key))

    def test_utf8_not_escaped(self):
        raw = (self.out / "days" / "2026-11-10.json").read_text(encoding="utf-8")
        self.assertIn("§", raw)
        self.assertNotIn("\\u00a7", raw)


if __name__ == "__main__":
    unittest.main()

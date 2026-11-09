import re
import unittest
from pathlib import Path

from medit.parse import parse_long

ROOT = Path(__file__).resolve().parent.parent


class ParseLongTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ps = parse_long((ROOT / "source" / "long.txt").read_text(encoding="utf-8"))
        cls.by_id = {p["id"]: p for p in cls.ps}

    def test_twelve_books(self):
        self.assertEqual({p["book"] for p in self.ps}, set(range(1, 13)))

    def test_sections_contiguous_per_book(self):
        for book in range(1, 13):
            secs = [p["section"] for p in self.ps if p["book"] == book]
            self.assertEqual(secs, list(range(1, len(secs) + 1)), f"book {book}")

    def test_ids_match_book_section(self):
        for p in self.ps:
            self.assertEqual(p["id"], f'{p["book"]}.{p["section"]}')

    def test_book2_section1_text(self):
        text = self.by_id["2.1"]["original"]
        self.assertTrue(text.startswith(
            "Begin the morning by saying to thyself, I shall meet with the busybody,"))
        self.assertTrue(text.endswith("to be vexed and to turn away."))

    def test_long_insertions_kept_as_printed(self):
        self.assertIn("not [only] of the same blood", self.by_id["2.1"]["original"])

    def test_paragraphs_unwrapped(self):
        for p in self.ps:
            for para in p["original"].split("\n\n"):
                self.assertNotIn("\n", para, p["id"])
                self.assertEqual(para, para.strip(), p["id"])
                self.assertTrue(para, p["id"])

    def test_no_footnote_text(self):
        for p in self.ps:
            t = p["original"]
            self.assertNotIn("Xenophon, Mem.", t, p["id"])
            self.assertIsNone(re.search(r"\[[A-Z]\]", t), p["id"])
            self.assertNotIn("Gataker placed them", t, p["id"])
            self.assertNotIn("Greek:", t, p["id"])
            self.assertNotIn("+", t, p["id"])
            self.assertNotIn("INDEX", t, p["id"])

    def test_last_passage_ends_cleanly(self):
        self.assertTrue(self.ps[-1]["original"].endswith("he also who releases thee is satisfied."))

    def test_total_reasonable(self):
        self.assertTrue(450 <= len(self.ps) <= 520, len(self.ps))


if __name__ == "__main__":
    unittest.main()

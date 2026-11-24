import re
import unittest

from medit.parse import load_explained, load_passages

FORBIDDEN = re.compile(r"[\[\]#*•!]|\bIn this passage\b|\bUltimately\b")


def words(s: str) -> int:
    return len(s.split())


class ExplainedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ps = {p["id"]: p for p in load_passages()}
        cls.e = load_explained()

    def test_every_passage_has_explained(self):
        self.assertEqual(set(self.e), set(self.ps))

    def test_shape(self):
        for i, x in self.e.items():
            self.assertIsInstance(x, dict, i)
            self.assertTrue(set(x) <= {"summary", "today"}, i)
            self.assertIsInstance(x.get("summary"), str, i)
            if "today" in x:
                self.assertIsInstance(x["today"], str, i)
                self.assertTrue(x["today"].strip(), i)

    def test_lengths(self):
        for i, x in self.e.items():
            self.assertTrue(20 <= words(x["summary"]) <= 170, f'{i}: summary {words(x["summary"])} words')
            if "today" in x:
                self.assertTrue(12 <= words(x["today"]) <= 110, f'{i}: today {words(x["today"])} words')

    def test_plain_prose(self):
        for i, x in self.e.items():
            for k, t in x.items():
                self.assertIsNone(FORBIDDEN.search(t), f"{i}.{k}: {FORBIDDEN.search(t)}")
                self.assertNotIn("\n\n\n", t, i)
                self.assertEqual(t, t.strip(), i)
                self.assertNotIn("\n", t.replace("\n\n", ""), f"{i}.{k}: single newline")

    def test_some_but_not_all_have_today(self):
        share = sum("today" in x for x in self.e.values()) / len(self.e)
        self.assertTrue(0.25 <= share <= 0.85, share)


if __name__ == "__main__":
    unittest.main()

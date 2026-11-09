import re
import unittest

from medit.parse import load_modern, load_passages

APPROVED = ("Begin the morning by saying to yourself: today I shall meet with the busybody, "
            "the ungrateful, the arrogant, the deceitful, the envious, the unsociable. All these "
            "things happen to them because they don't know what is good and what is evil.")
ARCHAIC = re.compile(r"\b(thou|thee|thy|thine|thyself|hath|doth|art|wast|shalt|wilt|canst|dost|ye)\b", re.I)
# Genuine modern uses of "art" (craft), checked by hand.
ART_NOUN = re.compile(r"\b(the|an|his|her|their|your|my|this|that|whose|of) art\b|\bart of\b", re.I)


class ModernTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ps = {p["id"]: p for p in load_passages()}
        cls.m = load_modern()

    def test_every_passage_has_modern(self):
        self.assertEqual(set(self.m), set(self.ps))

    def test_no_archaic_words_in_modern(self):
        for i, t in self.m.items():
            hits = ARCHAIC.findall(ART_NOUN.sub("", t))
            self.assertEqual(hits, [], i)

    def test_no_square_brackets(self):
        for i, t in self.m.items():
            self.assertNotIn("[", t, i)
            self.assertNotIn("]", t, i)

    def test_paragraph_count_matches(self):
        for i, t in self.m.items():
            self.assertEqual(t.count("\n\n"), self.ps[i]["original"].count("\n\n"), i)

    def test_verse_line_breaks_match(self):
        for i, t in self.m.items():
            self.assertEqual(t.count("\n"), self.ps[i]["original"].count("\n"), i)

    def test_no_cross_references_or_captions(self):
        for i, t in self.m.items():
            self.assertIsNone(re.search(r"\((?:[ivx]+\.|Epictetus)", t), i)
            self.assertNotIn("Illustration", t, i)

    def test_no_added_attributions(self):
        for i, t in self.m.items():
            for s in ("Hesiod", "Homer, Odyssey"):
                self.assertNotIn(s, t, i)

    def test_no_dangling_comma(self):
        for i, t in self.m.items():
            for para in t.split("\n\n"):
                self.assertFalse(para.endswith(","), i)

    def test_length_sane(self):
        for i, t in self.m.items():
            r = len(t) / len(self.ps[i]["original"])
            self.assertTrue(0.7 <= r <= 1.3, f"{i}: {r:.2f}")

    def test_pilot_unchanged(self):
        self.assertTrue(self.m["2.1"].startswith(APPROVED))


if __name__ == "__main__":
    unittest.main()

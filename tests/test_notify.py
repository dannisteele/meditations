import unittest

from medit.notify import make_notification


class NotifyTest(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(make_notification("Be content."), "Be content.")

    def test_takes_whole_sentences(self):
        self.assertEqual(make_notification("A b c. D e f. " + "x" * 300), "A b c. D e f.")

    def test_semicolon_cut_gets_ellipsis(self):
        self.assertEqual(make_notification("Do this; " + "y " * 200), "Do this\u2026")

    def test_prefers_full_stop_over_later_semicolon(self):
        text = "Begin the morning by saying this to yourself every day. Then act; " + "z " * 200
        self.assertEqual(make_notification(text), "Begin the morning by saying this to yourself every day.")

    def test_verse_lines_joined_with_slash(self):
        self.assertEqual(make_notification("Leaves, some the wind scatters\nSo is the race of men."),
                         "Leaves, some the wind scatters / So is the race of men.")

    def test_no_sentence_break_cuts_at_word(self):
        out = make_notification("word " * 60)
        self.assertLessEqual(len(out), 181)
        self.assertTrue(out.endswith("…"))
        self.assertTrue(out[:-1].endswith("word"))

    def test_strips_trailing_punctuation_before_ellipsis(self):
        out = make_notification(("alpha, " * 40).strip())
        self.assertTrue(out.endswith("alpha…"), out)

    def test_first_paragraph_only(self):
        self.assertEqual(make_notification("One.\n\nTwo."), "One.")


if __name__ == "__main__":
    unittest.main()

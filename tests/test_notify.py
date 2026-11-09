import unittest

from medit.notify import make_notification


class NotifyTest(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(make_notification("Be content."), "Be content.")

    def test_takes_whole_sentences(self):
        self.assertEqual(make_notification("A b c. D e f. " + "x" * 300), "A b c. D e f.")

    def test_semicolon_counts_as_break(self):
        self.assertEqual(make_notification("Do this; " + "y " * 200), "Do this;")

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

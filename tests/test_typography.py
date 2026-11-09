import unittest

from medit.typography import smarten


class SmartenTest(unittest.TestCase):
    def test_double_quotes_curl(self):
        self.assertEqual(smarten('He said, "O Cithaeron." Then'), "He said, \u201cO Cithaeron.\u201d Then")

    def test_quote_after_dash_opens(self):
        self.assertEqual(smarten('acts.\u2014"But I have'), "acts.\u2014\u201cBut I have")

    def test_quote_at_line_start_opens(self):
        self.assertEqual(smarten('x\n"Leaves'), "x\n\u201cLeaves")

    def test_apostrophes(self):
        self.assertEqual(smarten("a man's life; 'scape"), "a man\u2019s life; \u2019scape")

    def test_already_curly_untouched(self):
        s = "\u201cAlready\u201d it\u2019s fine"
        self.assertEqual(smarten(s), s)


if __name__ == "__main__":
    unittest.main()

"""Consistent curly quotes for display."""

import re


def smarten(text: str) -> str:
    text = re.sub(r'(^|[\s(\[\u2014\u2013])"', "\\1\u201c", text, flags=re.M)
    text = text.replace('"', "\u201d")
    return text.replace("'", "\u2019")

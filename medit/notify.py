"""Short notification text: whole sentences that fit, else a clean cut with an ellipsis."""

import re

_FULL_STOP = re.compile(r"[.?!][\"'”’)]?(?=\s|$)")
_SOFT_STOP = re.compile(r"[;:](?=\s|$)")
_MIN_SENTENCE_RESULT = 40


def make_notification(text: str, limit: int = 180) -> str:
    para = text.split("\n\n", 1)[0].strip().replace("\n", " / ")
    if len(para) <= limit:
        return para
    full = max((m.end() for m in _FULL_STOP.finditer(para) if m.end() <= limit), default=0)
    if full >= _MIN_SENTENCE_RESULT:
        return para[:full]
    soft = max((m.start() for m in _SOFT_STOP.finditer(para) if m.start() < limit), default=0)
    if soft > full:
        return para[:soft].rstrip() + "…"
    if full:
        return para[:full]
    cut = para[:limit + 1]
    cut = cut[:cut.rfind(" ")] if " " in cut else para[:limit]
    return cut.rstrip(" ,;:—-–/") + "…"

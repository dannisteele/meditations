"""Short notification text: whole sentences that fit, else a word-boundary cut."""

import re

_SENTENCE_END = re.compile(r"[.?!;][\"'”’)]?(?=\s|$)")


def make_notification(text: str, limit: int = 180) -> str:
    para = text.split("\n\n", 1)[0].strip()
    if len(para) <= limit:
        return para
    best = ""
    for m in _SENTENCE_END.finditer(para):
        if m.end() > limit:
            break
        best = para[:m.end()]
    if best:
        return best
    cut = para[:limit + 1]
    cut = cut[:cut.rfind(" ")] if " " in cut else para[:limit]
    return cut.rstrip(" ,;:—-–") + "…"

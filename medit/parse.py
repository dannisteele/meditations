"""Parse George Long's translation (Project Gutenberg #15877) into passages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source" / "long.txt"
PASSAGES = ROOT / "data" / "passages.json"
MODERN_DIR = ROOT / "data" / "modern"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
SECTION_RE = re.compile(r"^(\d+)\. (.*)$")


def _clean(text: str) -> str:
    text = re.sub(r"\[?\[Greek:[^\]]*\]\]?", "", text)  # Greek transliterations
    text = re.sub(r"\[[A-Z]\]", "", text)                 # footnote markers
    text = text.replace("+", "")                          # corrupt-text markers
    text = re.sub(r"_([^_]+)_", r"\1", text)              # _italics_
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s*--\s*", "—", text)           # Gutenberg dashes
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ([,;:.?!])", r"\1", text)
    return text.strip()


def _paragraphs(lines: list[str]) -> str:
    paras, cur = [], []
    for line in lines:
        if line.strip():
            cur.append(line.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(p for p in (_clean(p) for p in paras) if p)


def parse_long(text: str) -> list[dict]:
    lines = text.splitlines()
    starts = []
    for book, numeral in enumerate(ROMAN, 1):
        idx = lines.index(f"{numeral}.", starts[-1][1] + 1 if starts else 0)
        starts.append((book, idx))
    end = lines.index("INDEXES.")

    passages = []
    for i, (book, start) in enumerate(starts):
        stop = starts[i + 1][1] if i + 1 < len(starts) else end
        body = [l for l in lines[start + 1:stop] if not l.startswith("    ")]
        sections, cur, num = [], [], 1
        for line in body:
            m = SECTION_RE.match(line)
            if m and int(m.group(1)) == num + 1:
                sections.append((num, cur))
                num, cur = num + 1, [m.group(2)]
            else:
                cur.append(line)
        sections.append((num, cur))
        for sec, sec_lines in sections:
            passages.append({
                "id": f"{book}.{sec}",
                "book": book,
                "section": sec,
                "original": _paragraphs(sec_lines),
            })
    return passages


def load_passages(path: Path = PASSAGES) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    passages = parse_long(SOURCE.read_text(encoding="utf-8"))
    PASSAGES.parent.mkdir(exist_ok=True)
    PASSAGES.write_text(json.dumps(passages, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(passages)} passages")


if __name__ == "__main__":
    main()

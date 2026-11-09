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
    text = re.sub(r"\[Illustration:[^\]]*\]", "", text)   # picture captions
    text = re.sub(r"\[The three last words[^\]]*\]", "", text)  # Long's translator note
    text = CROSS_REF.sub("", text)                        # Long's cross-references
    text = text.replace("+", "")                          # corrupt-text markers
    text = re.sub(r"_([^_]+)_", r"\1", text)              # _italics_
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s*-{2,}\s*", "—", text)           # Gutenberg dashes
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ([,;:.?!])", r"\1", text)
    return text.strip()


VERSE = "\x00"  # marks an indented line of quoted verse in the main text
CITATION = re.compile(r"^(?:[A-Z]{3,}\b|_[A-Z]\w+_,)")  # e.g. "HESIOD, Works…", "_Odyssey_, ix. 413."
NOTE_START = re.compile(r"^ *\[[A-Z]\] ")
CROSS_REF = re.compile(r"\s*\((?:see\s+)?(?:[ivx]+\.\s*(?:c\.\s*)?\d|Epictetus)[^()]*\)")


def _strip_notes(lines: list[str]) -> list[str]:
    """Drop footnotes (and verse quoted inside them); mark main-text verse lines."""
    kept, in_note = [], False
    for line in lines:
        if not line.strip():
            kept.append("")
        elif NOTE_START.match(line):
            in_note = True
        elif not line.startswith(" "):
            in_note = False
            kept.append(line)
        elif not in_note and not CITATION.match(line.strip()):
            kept.append(VERSE + line.strip())
    return kept


def _paragraphs(lines: list[str]) -> str:
    paras, cur = [], []
    for line in lines + [""]:
        if line.strip():
            cur.append(line)
        elif cur:
            text = cur[0].lstrip(VERSE)
            for nxt in cur[1:]:
                text += ("\n" + nxt[1:]) if nxt.startswith(VERSE) else (" " + nxt.strip())
            paras.append(text)
            cur = []
    cleaned = ["\n".join(_clean(l) for l in p.split("\n")) for p in paras]
    cleaned = [p[:-1] + "." if p.endswith(",") else p for p in cleaned]  # ref removed at end
    return "\n\n".join(p for p in cleaned if p.strip())


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
        body = _strip_notes(lines[start + 1:stop])
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


def load_modern(directory: Path = MODERN_DIR) -> dict[str, str]:
    out: dict[str, str] = {}
    for f in sorted(Path(directory).glob("book-*.json")):
        out.update(json.loads(f.read_text(encoding="utf-8")))
    return out


def main() -> None:
    passages = parse_long(SOURCE.read_text(encoding="utf-8"))
    PASSAGES.parent.mkdir(exist_ok=True)
    PASSAGES.write_text(json.dumps(passages, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(passages)} passages")


if __name__ == "__main__":
    main()

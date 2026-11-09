# Daily Meditations

One passage a day from Marcus Aurelius's *Meditations* (George Long's 1862 translation, public domain, plus a light-touch modernisation), delivered to an iPhone via a static GitHub Pages site and an iOS Shortcut.

- Source: Project Gutenberg #15877 (`source/long.txt`), parsed into **487 passages** (Long's Book/section numbering) in `data/passages.json`.
- Rebuild passages: `python3 -m medit.parse`
- Tests: `python3 -m unittest discover -s tests -v`

See `docs/superpowers/specs/` for the design and `SHORTCUT-SETUP.md` for phone setup.

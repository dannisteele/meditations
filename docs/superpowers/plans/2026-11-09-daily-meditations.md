# Daily Meditations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver one passage of Marcus Aurelius's *Meditations* per day to Rach's iPhone via a static GitHub Pages site and an iOS Shortcuts automation.

**Architecture:** A Python build step parses George Long's public-domain translation into ~480 passages, pairs each with a light-touch modernisation, computes a deterministic no-repeat shuffled schedule, and writes one static JSON file per date for 10 years. A static page and the iOS Shortcut both read `days/YYYY-MM-DD.json`. There is no server and no scheduled job.

**Tech Stack:** Python 3.14 standard library only (tests use `unittest`), vanilla HTML/CSS/JS, GitHub Pages deployed by a push-triggered GitHub Actions workflow, iOS Shortcuts.

**Spec:** `docs/superpowers/specs/2026-11-09-daily-meditations-design.md`

## Global Constraints

- Source text: George Long's translation only, Project Gutenberg ebook **#15877** (`https://www.gutenberg.org/cache/epub/15877/pg15877.txt`). Never use a copyrighted translation.
- One passage = one Book/section in Long's numbering. Strip footnotes, editorial notes, and the introduction/Life. Inline `[A]`-style footnote markers are removed. Long's square-bracket insertions such as `[only]` are needed for sense: keep the words and drop the brackets.
- Modernisation standard: the approved example in the spec. Book 2 §1's modern text must begin exactly: `Begin the morning by saying to yourself: today I shall meet with the busybody, the ungrateful, the arrogant, the deceitful, the envious, the unsociable. All these things happen to them because they don't know what is good and what is evil.`
- Day boundary: Europe/London midnight.
- Schedule start date: `2026-11-10`. Horizon: 3653 days (10 years).
- Every cycle covers all passages exactly once. Each cycle's order differs. The last passage of cycle n ≠ the first of cycle n+1.
- Site URL: `https://dannisteele.github.io/meditations/`. Repo `dannisteele/meditations`, public.
- Shortcut default time: **10:00**. Notification uses modern text by default.
- No scheduled GitHub Actions (`schedule:`) anywhere.
- Page: works on iPhone, supports dark mode, Modern/Original toggle persisted in `localStorage` under key `meditations.version` (values `modern` | `original`, default `modern`).

## Review Focus

1. **Passage boundaries in the source:** section 1 of each Book has no number. Some lines start with a number that's mid-sentence (e.g. a year or "2." inside text wrapped to column 0). A misparse silently merges or splits passages. Pinned by `test_sections_contiguous_per_book` and `test_book2_section1_text` (Task 1).
2. **Footnotes and commentary leaking into passages:** Long's indented notes (4-space blocks, `[A] Xenophon…`) and end-of-book commentary must not appear in any passage. Pinned by `test_no_footnote_text` (Task 1).
3. **Leftover archaisms in modern text:** a missed "thou"/"thy"/"hath" in one of ~480 passages is the most likely visible flaw. Pinned by `test_no_archaic_words_in_modern` (Task 5).
4. **Date mismatch near midnight / BST change:** the page must use the London date, not UTC or the device's zone. Pinned by the manual check in Task 7, Step 3 (the London date is computed with `Intl` `timeZone: 'Europe/London'`).
5. **Very long or very short passages in the notification:** a passage with no sentence break inside the limit, or a one-line passage, must still give a sensible notification. Pinned by `test_no_sentence_break_cuts_at_word` and `test_short_text_unchanged` (Task 3).

---

## File Structure

```
meditations/
  source/long.txt                 # Gutenberg #15877, committed verbatim
  data/passages.json              # parsed originals: [{id, book, section, original}]
  data/modern/book-01.json …      # {"1.1": "modern text", …} one file per Book
  medit/__init__.py
  medit/parse.py                  # Gutenberg text -> passages
  medit/schedule.py               # deterministic shuffled order
  medit/notify.py                 # notification string trimming
  medit/build.py                  # writes site/days/*.json; CLI entry point
  tests/test_parse.py
  tests/test_schedule.py
  tests/test_notify.py
  tests/test_modern.py
  tests/test_build.py
  site/index.html, site/style.css, site/app.js, site/icon-180.png
  site/days/YYYY-MM-DD.json       # generated, committed
  .github/workflows/pages.yml     # deploy site/ on push to main
  SHORTCUT-SETUP.md
  README.md
```

Run all tests with `python3 -m unittest discover -s tests -v` from the repo root.

---

### Task 1: Fetch source and parse passages

**Files:**
- Create: `source/long.txt`, `medit/__init__.py`, `medit/parse.py`, `tests/test_parse.py`, `data/passages.json`, `README.md`, `.gitignore` (`__pycache__/`)

**Interfaces:**
- Produces: `parse_long(text: str) -> list[dict]`. Each dict is `{"id": "2.1", "book": 2, "section": 1, "original": str}`, ordered by (book, section). Original text is unwrapped into paragraphs separated by `"\n\n"`, with single newlines inside a paragraph joined by spaces.
- Produces: `load_passages(path="data/passages.json") -> list[dict]`.
- Produces: `python3 -m medit.parse` writes `data/passages.json` from `source/long.txt`.

- [ ] **Step 1:** Download the source: `curl -sL https://www.gutenberg.org/cache/epub/15877/pg15877.txt -o source/long.txt`. Verify with `grep -c "Translator: George Long" source/long.txt` → `1`.
- [ ] **Step 2: Write failing tests** in `tests/test_parse.py` (they load `source/long.txt` once in `setUpClass`):
  - `test_twelve_books`: `{p["book"] for p in ps} == set(range(1, 13))`
  - `test_sections_contiguous_per_book`: for each book, its sections are exactly `1..n`
  - `test_book2_section1_text`: passage `2.1` original starts with `"Begin the morning by saying to thyself, I shall meet with the busybody,"` and ends with `"to be vexed and to turn away."`
  - `test_brackets_unwrapped`: `2.1` contains `"not only of the same blood"` and no `"["`
  - `test_no_footnote_text`: no passage contains `"Xenophon, Mem."`, `"[A]"`, or a line starting with 4 spaces. No passage contains `"Gataker placed them"`.
  - `test_total_reasonable`: `450 <= len(ps) <= 520`
- [ ] **Step 3:** Run `python3 -m unittest tests.test_parse -v`. Expected: FAIL (ImportError).
- [ ] **Step 4: Implement `parse_long`.** Book headings are lines that are exactly a Roman numeral plus a period (`I.` … `XII.`) at column 0. The body before `I.` is skipped, and parsing stops at Gutenberg's `*** END OF` marker. Inside a book, a new section starts at a column-0 line matching `^(\d+)\. ` whose number is exactly the previous section + 1. Text before the first numbered line is section 1. Drop indented (4+ space) lines and their blocks, inline `\[[A-Z]\]` markers, and any trailing commentary after the last section that is indented. Convert `[word]` to `word`. Check what follows Book XII before `*** END`, and make sure no back-matter (index, notes) leaks into 12.n. Add a test if it does.
- [ ] **Step 5:** Run the tests. Expected: PASS. Then run `python3 -m medit.parse` and record the passage count in `README.md`.
- [ ] **Step 6: Commit:** `git add -A && git commit -m "feat: parse Long translation into passages"`

### Task 2: Deterministic schedule

**Files:**
- Create: `medit/schedule.py`, `tests/test_schedule.py`

**Interfaces:**
- Produces: `order_for_cycle(ids: list[str], cycle: int) -> list[str]`
- Produces: `passage_id_for(day: datetime.date, start: datetime.date, ids: list[str]) -> str`. Raises `ValueError` if `day < start`.

- [ ] **Step 1: Write failing tests** (use `ids = [f"p{i}" for i in range(480)]` plus a small `ids` of 3):
  - `test_cycle_is_permutation`: `sorted(order_for_cycle(ids, c)) == sorted(ids)` for c in 0..5
  - `test_cycles_differ`: orders for cycles 0..5 are pairwise different
  - `test_deterministic`: two calls with the same args give equal results
  - `test_no_back_to_back_across_boundary`: for c in 0..50, `order(c)[-1] != order(c+1)[0]`. Also for the 3-id list.
  - `test_day_mapping`: `passage_id_for(start + timedelta(days=k), start, ids) == order_for_cycle(ids, k // 480)[k % 480]` for k in {0, 1, 479, 480, 961}
  - `test_before_start_raises`
- [ ] **Step 2:** Run `python3 -m unittest tests.test_schedule -v`. Expected: FAIL.
- [ ] **Step 3: Implement.** Shuffle a copy of `ids` with `random.Random(f"meditations-cycle-{cycle}")`. String seeds hash deterministically across Python versions. For cycle > 0, if the first element equals the last element of `order_for_cycle(ids, cycle - 1)`, swap positions 0 and 1. Swapping the first two never changes the last element when len ≥ 3, so the recursion only needs the previous cycle's raw shuffle. Compute the previous last element from that raw shuffle to avoid deep recursion.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Commit:** `git commit -am "feat: deterministic no-repeat schedule"` (git add the new files first).

### Task 3: Notification text

**Files:**
- Create: `medit/notify.py`, `tests/test_notify.py`

**Interfaces:**
- Produces: `make_notification(text: str, limit: int = 180) -> str`

- [ ] **Step 1: Write failing tests:**
  - `test_short_text_unchanged`: `make_notification("Be content.") == "Be content."`
  - `test_takes_whole_sentences`: with text `"A b c. D e f. " + "x" * 300`, the result is `"A b c. D e f."` (the longest run of whole sentences ≤ limit, no ellipsis)
  - `test_no_sentence_break_cuts_at_word`: with 60 words of `"word "` and no full stop, the result has length ≤ 181, ends with `"…"`, and has no partial word before it
  - `test_first_paragraph_only`: text `"One.\n\nTwo."` gives `"One."`
- [ ] **Step 2:** Run `python3 -m unittest tests.test_notify -v`. Expected: FAIL.
- [ ] **Step 3: Implement.** Use only the first paragraph. Sentence ends are `.`, `?`, `!` or `;`, followed by a space or end of text. If even the first sentence is longer than `limit`, cut at the last space ≤ limit, strip trailing punctuation, and append `"…"`.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Commit.**

### Task 4: Modernisation pilot ⛔ CHECKPOINT with Daniella

**Files:**
- Create: `data/modern/STYLE.md`, `data/modern/book-NN.json` (partial: pilot ids only)

**Interfaces:**
- Produces: the modern-text file format `data/modern/book-NN.json` (zero-padded book number) = `{"<id>": "<modern text>", …}`. Paragraph breaks match the original's `"\n\n"`.

- [ ] **Step 1:** Write `data/modern/STYLE.md`. Copy the spec's "light touch" rules and the approved example verbatim, and add the bracket and footnote rules from Global Constraints. This file is the brief for every later modernisation batch.
- [ ] **Step 2:** Modernise these 15 pilot passages, which mix short, long, dense and well-known ones: `1.1, 1.17, 2.1, 2.11, 2.17, 3.5, 4.3, 4.17, 5.1, 6.13, 7.69, 8.47, 9.42, 10.16, 12.36`. If any id doesn't exist, substitute the nearest.
- [ ] **Step 3:** Check that `2.1` begins with the exact approved sentence from Global Constraints.
- [ ] **Step 4:** Write `docs/pilot-review.md` with each pilot passage shown as Original then Modern, side by side.
- [ ] **Step 5: Commit**, then **STOP**. Ask Daniella to review `docs/pilot-review.md`. Fold any feedback into `STYLE.md` (and the pilot texts) before Task 5. Do not start Task 5 without her go-ahead.

### Task 5: Modernise all passages

**Files:**
- Modify/Create: `data/modern/book-01.json` … `book-12.json`
- Create: `tests/test_modern.py`

**Interfaces:**
- Consumes: `load_passages()` (Task 1), the `STYLE.md` brief (Task 4)
- Produces: `load_modern(dir="data/modern") -> dict[str, str]` in `medit/parse.py`

- [ ] **Step 1: Write failing tests:**
  - `test_every_passage_has_modern`: the set of keys == the set of passage ids
  - `test_no_archaic_words_in_modern`: no modern text matches `\b(thou|thee|thy|thine|thyself|hath|doth|art|wast|shalt|wilt|canst|dost|ye)\b` (case-insensitive). Note: "art" also means art, so allowlist specific ids if a genuine noun use appears, with a comment.
  - `test_paragraph_count_matches`: the count of `"\n\n"` in modern == the count in original, for every id
  - `test_length_sane`: for every id, `0.7 <= len(modern)/len(original) <= 1.3`. This catches dropped or invented content.
  - `test_pilot_unchanged`: the `2.1` modern text starts with the approved sentence
- [ ] **Step 2:** Run `python3 -m unittest tests.test_modern -v`. Expected: FAIL (missing passages).
- [ ] **Step 3:** Modernise the rest, one Book per batch. Batches are independent, so they can be done by parallel subagents, each given `STYLE.md`, the pilot examples, and its Book's originals from `data/passages.json`. Don't overwrite pilot entries.
- [ ] **Step 4:** Run the tests. Expected: PASS. Fix any flagged passages individually.
- [ ] **Step 5:** Read 10 random non-pilot passages (`random.sample` with any seed) side by side, checking against `STYLE.md`. Fix any drift.
- [ ] **Step 6: Commit.**

### Task 6: Build day files

**Files:**
- Create: `medit/build.py`, `tests/test_build.py`, `site/days/*.json` (generated)

**Interfaces:**
- Consumes: `load_passages`, `load_modern`, `passage_id_for`, `make_notification`
- Produces: `build(out_dir: Path, start: date, days: int) -> int` (returns the number of files written). It removes stale `*.json` in `out_dir/days` first.
- Produces: `python3 -m medit.build` → `build(Path("site"), date(2026, 11, 10), 3653)`
- Produces: the day file shape (both the page and the Shortcut rely on it):
  ```json
  {"date": "2026-11-10", "book": 4, "section": 3, "ref": "Book 4, §3",
   "modern": "…", "original": "…",
   "notification": "…", "notification_original": "…"}
  ```

- [ ] **Step 1: Write failing tests** (build into a `tempfile.TemporaryDirectory` with `days=1000`):
  - `test_file_count`: returns 1000, and exactly 1000 files exist, named `start..start+999` as `YYYY-MM-DD.json`
  - `test_shape`: a sample file has exactly the keys above, `ref == f"Book {book}, §{section}"`, and `notification == make_notification(modern)`
  - `test_first_cycle_no_repeats`: the ids over the first N days (N = passage count) are all distinct
  - `test_matches_schedule`: for day k=700, the file's (book, section) == `passage_id_for(...)`
  - `test_utf8_not_escaped`: the raw file contains `§`, not `§` (use `ensure_ascii=False`)
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement `build`.**
- [ ] **Step 4:** Run the tests. Expected: PASS. Run `python3 -m medit.build`, then check `ls site/days | wc -l` → `3653` and `du -sh site/days` (expect roughly 10–15 MB).
- [ ] **Step 5: Commit.**

### Task 7: The web page

**Files:**
- Create: `site/index.html`, `site/style.css`, `site/app.js`, `site/icon-180.png`

**Interfaces:**
- Consumes: `site/days/YYYY-MM-DD.json` (Task 6 shape)
- Produces: `todayLondon(): string` in `app.js` (`YYYY-MM-DD`, via `new Intl.DateTimeFormat('en-CA', {timeZone: 'Europe/London'})`). A `?date=YYYY-MM-DD` query parameter overrides it, for testing.

- [ ] **Step 1: Build the page.** It shows the date, the reference (`ref`), and the passage text (paragraphs split on `\n\n`), with a Modern / Original segmented toggle. Use a readable serif body (Google Fonts "EB Garamond" or the system serif), generous line height, a max width of ~36rem, a 16px side gutter, and light/dark via `prefers-color-scheme`. Add `<meta name="viewport">`, `apple-touch-icon` → `icon-180.png` (a simple generated laurel or "M" mark), and `apple-mobile-web-app-title` "Meditations". Wrap `localStorage` reads/writes in try/catch. If the day file 404s or fetch fails, show "Today's passage isn't available — check back soon." with no error trace.
- [ ] **Step 2: Serve locally** with `python3 -m http.server -d site 8000`. Verify: `/` shows today (2026-11-09 is before the start date, so it shows the friendly missing message; that's expected), `/?date=2026-11-10` shows a passage, the toggle switches text and survives a reload, and `/?date=2040-01-01` shows the friendly message.
- [ ] **Step 3:** Verify the London date logic in the browser console: `new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/London'}).format(new Date('2026-03-29T00:30:00Z'))` → `2026-03-29`, and `…format(new Date('2026-07-01T23:30:00Z'))` → `2026-07-02` (BST).
- [ ] **Step 4:** Check the layout at 375px width (no horizontal scroll) and in dark mode.
- [ ] **Step 5: Commit.**

### Task 8: Deploy to GitHub Pages

**Files:**
- Create: `.github/workflows/pages.yml`

- [ ] **Step 1:** Write a workflow triggered on `push` to `main` and on `workflow_dispatch` (**no `schedule:`**). It uses `actions/checkout@v4`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3` with `path: site`, and `actions/deploy-pages@v4`, with permissions `pages: write, id-token: write, contents: read`.
- [ ] **Step 2:** Ask Daniella before creating the public repo. Then run `gh repo create dannisteele/meditations --public --source . --push` and `gh api -X POST repos/dannisteele/meditations/pages -f build_type=workflow`.
- [ ] **Step 3:** Watch the run with `gh run watch`. Verify `curl -s https://dannisteele.github.io/meditations/days/2026-11-10.json | python3 -m json.tool` prints the passage, and that the page loads at `https://dannisteele.github.io/meditations/?date=2026-11-10`.
- [ ] **Step 4: Commit** any fixes.

### Task 9: Shortcut and setup guide ⛔ CHECKPOINT with Daniella's iPhone

**Files:**
- Create: `SHORTCUT-SETUP.md`

- [ ] **Step 1: Draft the Shortcut steps** in `SHORTCUT-SETUP.md`. The shortcut is named "Daily Meditation":
  1. **Current Date**
  2. **Format Date**: Custom format `yyyy-MM-dd`
  3. **Text**: `https://dannisteele.github.io/meditations/days/` + Formatted Date + `.json`
  4. **Get Contents of URL**
  5. **Get Dictionary Value**: key `notification` (the one word to change to `notification_original` for the original wording)
  6. **Show Notification**: title "Meditations", body = Dictionary Value
  
  Then the automation: Personal Automation → Time of Day **10:00**, Daily → Run Immediately, "Notify When Run" off. Also add "Add to Home Screen" steps for `https://dannisteele.github.io/meditations/` from Safari.
  
  Note: the Shortcut's date uses the phone's timezone. For a UK phone this is the same as Europe/London. Mention this in the guide.
- [ ] **Step 2: STOP.** Ask Daniella to build it on her iPhone and report:
  - (a) whether the 10:00 automation fires without a prompt
  - (b) what tapping the notification opens
  - (c) whether it's quiet in Airplane mode or shows an error
  - (d) what happens on 2026-11-09, which is before the start date: an error or nothing? If it shows an error, add an **If** action ("If Contents of URL has any value") and a start-date note.
  
  Try an option for (b) as well: add an **Open URLs** action after Show Notification, and see whether that's acceptable or intrusive.
- [ ] **Step 3:** Finalise `SHORTCUT-SETUP.md` from her results, including the tap behaviour that actually happens and the home-screen icon fallback. Write it for whoever holds Rach's phone.
- [ ] **Step 4: Commit and push.** Confirm the Pages deploy succeeds.

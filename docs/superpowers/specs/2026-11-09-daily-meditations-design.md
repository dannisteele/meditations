# Daily Meditations for Rach: Design

**Date:** 2026-11-09
**Author:** Daniella McSorley (with Claude)
**Status:** Approved 2026-11-09

## Intent

A gift for Rach: each morning a passage from Marcus Aurelius's *Meditations* arrives on her iPhone as a notification, without her needing to open anything. It should feel like a small, calm daily ritual, not an app to manage.

Daniella explicitly didn't want a native iPhone app. The solution is a free static website plus an iOS Shortcuts automation.

## Goals

- One passage per day, delivered as an iPhone notification at a fixed morning time.
- Every passage appears once before any repeats. After the full set has been shown, a new cycle starts in a *different* random order. Cycles repeat indefinitely.
- A web page showing today's passage in full, with its reference (e.g. "Book 4, §3").
- Two text versions: a light-touch modernisation (default) and George Long's original 1862 wording, switchable on the page. The choice is remembered on her phone.
- Free to run, with no server to maintain.

## Non-goals

- Native iOS app, App Store, push-notification server.
- Accounts, favourites, history/archive browsing, sharing features (could come later, not now).
- Multiple users with different orders. Everyone who visits sees the same passage on the same day, which is fine.
- Android support.

## Anti-goals (would count as failure even if it "works")

- Using a copyrighted translation (e.g. Gregory Hays, 2002).
- A modernisation that changes Marcus's meaning or editorialises. "Light touch" means archaic wording only.
- Something Rach has to babysit: re-running things, logging in, or a schedule that silently stops after a few months.
- Repeats within a cycle, or the same passage on two consecutive days across a cycle boundary.

## Constraints and decisions made

**Source text.** George Long's translation (1862, public domain), from Project Gutenberg. Use Long's own Book/section numbering as the unit of "one passage" (~480 sections across 12 Books). Strip Long's footnotes, editorial notes and introduction. Bracketed glosses in the running text should be removed if they're editorial, and kept if they're needed for the sentence to make sense (builder's judgement, consistently applied).

**Modernised version: "light touch".** Daniella approved this example:

> Long: *Begin the morning by saying to thyself, I shall meet with the busy-body, the ungrateful, arrogant, deceitful, envious, unsocial. All these things happen to them by reason of their ignorance of what is good and evil.*
>
> Light touch: *Begin the morning by saying to yourself: today I shall meet with the busybody, the ungrateful, the arrogant, the deceitful, the envious, the unsociable. All these things happen to them because they don't know what is good and what is evil.*

**The approved example is the standard**, and the rules below describe it. Where they seem to conflict, match the example's degree of freedom. *(Claude's call, made after the review.)*

Rules: thou/thee/thy/thine → you/your/yours. Archaic verb forms (hath, doth, -est, -eth) → modern ones. Archaic phrasing → plain modern equivalents, even when that means rewording a phrase ("by reason of their ignorance of what is good and evil" → "because they don't know what is good and what is evil"). Small connective words may be added for flow ("today", repeated "the"). Uncommon or obsolete word forms → their common equivalents ("unsocial" → "unsociable"). Punctuation is tidied for readability. Long's sentence order and imagery are kept. No retranslation, no added or removed ideas, no interpretation. If a sentence in Long is ambiguous, keep the ambiguity rather than resolving it. Claude produces the modernisations. Daniella spot-checks the first batch (~15 passages, see Deliverables) *before* the rest are done, so the style can be adjusted cheaply.

**Hosting.** GitHub Pages on Daniella's account `dannisteele`, repo `meditations`, served at `https://dannisteele.github.io/meditations/`. The repo is public. (`gh` CLI is already authenticated with repo scope.)

**Day boundary.** Midnight-to-midnight, Europe/London.

**Ordering must be deterministic and stateless.** There is no database. The passage for any date is a pure function of the date: days since a fixed start date → cycle number and position → a shuffle seeded by the cycle number. Each cycle's shuffle must differ, and the last passage of cycle *n* must not equal the first of cycle *n+1*.

**How the Shortcut gets "today's passage".** iOS Shortcuts' "Get Contents of URL" doesn't run JavaScript, so the passage for each date must exist as a static file. The schedule is precomputed at build time into one small JSON file per date (e.g. `days/2026-11-10.json`) for a long horizon (at least 5 years). The Shortcut formats today's date and fetches that file. The web page reads the same file, so the page and the notification can never disagree. This deliberately avoids a scheduled GitHub Action, because GitHub disables scheduled workflows in repos with no activity for 60 days. That would break the "no babysitting" anti-goal.

Each day file contains at least: date, book, section, modern text, original text, and a short `notification` string. The `notification` string is the opening sentence or two of the modern text, trimmed to fit an iPhone notification, with an ellipsis if it's cut. It also contains a matching `notification_original` string. The Shortcut uses the modern one by default, and the setup guide explains the one-word change that switches it to the original. *(Claude's call: the page toggle can't be read by the Shortcut, so this is a separate setting.)*

**Web page.** One static page (`index.html`). It shows today's passage (Europe/London date) with its reference, and has a Modern/Original toggle that persists in `localStorage`. It must look good on an iPhone screen and support dark mode. Tone: calm, readable serif typography, no clutter. If the date file is missing (e.g. past the horizon), show a gentle message instead of breaking.

**Notification delivery.** An iOS Shortcuts personal automation triggers at a set time (default 10:00am; Rach/Daniella can change it). It is set to run without asking. It fetches today's file and shows a notification with the `notification` text. The deliverable includes a step-by-step setup guide for doing this on Rach's phone. If there's no network, the Shortcut should fail quietly rather than show an error.

**Testing and setup.** Daniella has an iPhone and will test the Shortcut on her own phone first. That's a checkpoint in the plan: the builder provides the Shortcut steps, Daniella runs them and reports back, and the guide is finalised from the results. It isn't a surprise (Rach knows about it), so nothing needs hiding. Either of them may do the final setup on Rach's phone, so the guide is written to be followed by whoever has the phone in hand.

**Known iOS limitation (to verify on a device).** Tapping a notification created by Shortcuts' "Show Notification" usually opens the Shortcuts app, not a web page. The fallback plan is for the setup guide to also add the page to Rach's home screen ("Add to Home Screen"), so the full passage is one tap away from an icon. The builder should check on a real device whether there's a cleaner way, and the guide should describe whatever actually works.

## Left to the builder

- Tech for the build step (a small script in Python or Node is fine) and the PRNG/shuffle implementation.
- Exact JSON shape, file layout, and the schedule start date (the launch date is fine).
- Page visual design within the tone above, and an app icon / touch icon for the home-screen bookmark.
- How to fetch and parse the Gutenberg text, and how to batch the ~480 modernisations.
- Tests: at minimum, verify no repeats within a cycle, all passages covered per cycle, different orders between cycles, no back-to-back repeat at boundaries, and that every day file in the horizon exists.

## Deliverables

1. Repo `dannisteele/meditations` with source data (passages with both versions), build script, generated site, tests.
2. Live GitHub Pages site.
3. `SHORTCUT-SETUP.md`: phone setup guide written for someone who's comfortable with tech but has never used Shortcuts automations.
4. A sample of ~15 modernised passages for Daniella to spot-check. This is a checkpoint: it happens before the remaining passages are modernised.

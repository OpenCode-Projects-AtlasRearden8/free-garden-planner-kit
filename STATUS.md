# STATUS — Free Garden Planner Kit

Last updated: 2026-10-26

## What was built

A complete, free printable garden planner pack for first-time gardeners,
built to the original goal spec:

- **8 sheets**, each a plain HTML/CSS source in `src/sheets/`:
  1. Bed Layout Grid (`01-bed-layout-grid.html`)
  2. Seed Starting Log with frost-date slots (`02-seed-starting-log.html`)
  3. Planting Calendar by Season — spring/summer/fall/winter (`03-planting-calendar.html`)
  4. Watering Tracker with weekly check-off grid and rain row (`04-watering-tracker.html`)
  5. Pest "What Did That?" Worksheet (`05-pest-worksheet.html`)
  6. Harvest Weight Log (`06-harvest-weight-log.html`)
  7. Seed Inventory Card (`07-seed-inventory-card.html`)
  8. End-of-Season Reflections (`08-end-of-season-reflections.html`)
- **Friendly getting-started page per sheet**: every PDF opens with a
  one-page intro ("How to use it" steps + beginner tips) before the sheet.
- **One build script**: `build.py` renders all HTML via WeasyPrint into
  `printables/`. Supports `--outdir` and `--clean`.
- **Unbranded PDFs**: no names, logos, or URLs in any output (enforced by a
  test that scans extracted PDF text).
- **Local build, zero signups**: pure Python + WeasyPrint, no network, no
  accounts, no secrets or personal data anywhere in the repo.
- **Tests**: `tests/test_build.py` (pytest + pypdf) verifies every sheet
  builds a valid letter-sized PDF with a getting-started page, that the
  prebuilt PDFs in `printables/` parse, and that output stays unbranded.
- **README.md** with sheet table, build/test instructions, and credit to
  Asdale Dynamics, LLC. **LICENSE** is MIT with the exact line
  `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

```bash
pip install weasyprint pypdf pytest   # one-time setup
python3 build.py                      # build all PDFs into printables/
python3 build.py --clean              # wipe and rebuild
python3 -m pytest tests/ -q           # run the test suite
```

Requirements: Python 3.10+ (tested on 3.13), WeasyPrint (tested with 70.0).

## Verification results

- `python3 build.py --clean` → **8/8 PDFs built** (22–28 KB each), exit code 0.
- `python3 -m pytest tests/ -q` → **20 passed** in ~25 s:
  - all 8 expected sheet sources exist
  - build script runs cleanly into a temp dir
  - each of the 8 sheets builds a valid PDF (≥2 pages, letter size
    8.5×11 in ±0.1, extractable text)
  - every sheet source contains a getting-started page
  - prebuilt `printables/` PDFs exist and parse
  - no forbidden branding tokens in extracted PDF text
- No lint/typecheck config exists for this repo (plain Python script +
  tests); `python3 -m py_compile build.py tests/test_build.py` passes.

## Known gaps / possible improvements

- Page size is US Letter only; an A4 variant would need a second `@page`
  rule or build flag.
- No cover/table-of-contents PDF bundling the whole pack into one file.
- The seed-starting log's "weeks before frost" math is manual; a future
  version could generate pre-filled date columns per USDA zone (kept out of
  scope to stay unbranded and zone-agnostic).
- Tests rebuild all PDFs per parametrized case (~25 s total); a session
  fixture could share one build run for speed.
- Visual QA of PDFs is by test assertions (size, page count, text) rather
  than human review of rendered layout; a screenshot-based check could be
  added later.

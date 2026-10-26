# Free Garden Planner Kit

A free, printable pack of garden planning sheets for first-time gardeners.
Everything is plain HTML/CSS that builds to clean, unbranded PDFs with one
local script. No accounts, no signups, no tracking — download, print, and
grow.

## What's in the pack

Eight sheets, each PDF opening with a friendly one-page "getting started"
guide followed by the printable worksheet:

| # | Sheet | What it's for |
|---|-------|---------------|
| 1 | Bed Layout Grid | Sketch where everything goes before you plant |
| 2 | Seed Starting Log | Track trays and sowing dates, with frost-date slots |
| 3 | Planting Calendar by Season | Plan spring, summer, fall, and winter tasks |
| 4 | Watering Tracker | Weekly check-off grid, including a rain row |
| 5 | Pest "What Did That?" Worksheet | Turn mystery damage into detective notes |
| 6 | Harvest Weight Log | Record what you picked, by weight or count |
| 7 | Seed Inventory Card | One card per variety: age, quantity, storage |
| 8 | End-of-Season Reflections | Capture what worked before you forget it |

Prebuilt PDFs live in [`printables/`](printables/). They're unbranded — no
names, logos, or links — so they're ready to print, share, or include in a
project as-is.

## How to build it yourself

Requirements: Python 3.10+ and [WeasyPrint](https://weasyprint.org/) (plus
pypdf and pytest if you want to run the tests).

```bash
pip install weasyprint pypdf pytest

python3 build.py          # build all sheets into printables/
python3 build.py --clean  # wipe printables/ first, then build
python3 build.py --outdir /tmp/somewhere
```

Each sheet is a plain HTML file in `src/sheets/` sharing one stylesheet,
`src/styles.css`. Edit any sheet, rerun the script, done.

## Running the tests

```bash
python3 -m pytest tests/ -q
```

The tests verify that every sheet builds a valid letter-sized PDF with a
getting-started page, that the prebuilt PDFs in `printables/` parse and stay
unbranded, and that the build script runs cleanly.

## Who this is for

Anyone starting their first garden who wants paper they can scribble on —
no apps, no accounts. Built with a beginner's pace in mind: short
instructions, generous writing space, and encouragement over jargon.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC. This kit is a free, beginner-friendly
tool published by Asdale Dynamics, LLC, which makes plain-English AI books,
guides, and practical open-source tools.

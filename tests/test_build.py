"""Tests for the Free Garden Planner Kit.

Verifies that every sheet builds a valid PDF, and that the committed
printables/ output is present and valid too.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader
import pytest

ROOT = Path(__file__).resolve().parents[1]
SHEETS_DIR = ROOT / "src" / "sheets"
PRINTABLES_DIR = ROOT / "printables"
BUILD_SCRIPT = ROOT / "build.py"

EXPECTED_SHEETS = [
    "01-bed-layout-grid",
    "02-seed-starting-log",
    "03-planting-calendar",
    "04-watering-tracker",
    "05-pest-worksheet",
    "06-harvest-weight-log",
    "07-seed-inventory-card",
    "08-end-of-season-reflections",
]


def sheet_sources() -> list[Path]:
    return sorted(SHEETS_DIR.glob("*.html"))


def test_all_expected_sheets_exist():
    for name in EXPECTED_SHEETS:
        assert (SHEETS_DIR / f"{name}.html").is_file(), f"missing source: {name}.html"


def test_build_script_runs_clean(tmp_path):
    outdir = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--outdir", str(outdir)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr
    pdfs = sorted(outdir.glob("*.pdf"))
    assert len(pdfs) == len(sheet_sources()) >= len(EXPECTED_SHEETS)


@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_every_sheet_builds_valid_pdf(tmp_path, name):
    """Each sheet builds a valid, non-empty, letter-sized multi-page PDF."""
    outdir = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--outdir", str(outdir)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr

    pdf_path = outdir / f"{name}.pdf"
    assert pdf_path.is_file(), f"{name}.pdf was not built"
    assert pdf_path.stat().st_size > 1000, f"{name}.pdf is suspiciously small"

    reader = PdfReader(str(pdf_path))
    assert len(reader.pages) >= 2, (
        f"{name}.pdf should have a getting-started page plus the sheet"
    )
    for page in reader.pages:
        box = page.mediabox
        width_in = float(box.width) * 0.0138889  # points -> inches
        height_in = float(box.height) * 0.0138889
        assert abs(width_in - 8.5) < 0.1 and abs(height_in - 11.0) < 0.1, (
            f"{name}.pdf page is {width_in:.2f}x{height_in:.2f}in, expected letter"
        )
        assert page.extract_text(), f"{name}.pdf page has no extractable text"


@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_every_sheet_has_getting_started_page(name):
    """Every sheet source includes a friendly getting-started section."""
    html = (SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
    assert 'class="getting-started"' in html, f"{name}.html lacks a getting-started page"
    assert "How to use it" in html


def test_committed_printables_are_valid():
    """The prebuilt PDFs shipped in printables/ exist and parse."""
    for name in EXPECTED_SHEETS:
        pdf_path = PRINTABLES_DIR / f"{name}.pdf"
        assert pdf_path.is_file(), f"missing prebuilt PDF: printables/{name}.pdf"
        reader = PdfReader(str(pdf_path))
        assert len(reader.pages) >= 2


def test_pdfs_are_unbranded():
    """No branding: no personal names, company names, or URLs in PDF text."""
    forbidden = ["asdale", "dylan", "http://", "https://", "www.", ".com"]
    for pdf_path in sorted(PRINTABLES_DIR.glob("*.pdf")):
        text = " ".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)
        low = text.lower()
        for token in forbidden:
            assert token not in low, f"{pdf_path.name} contains forbidden token: {token}"

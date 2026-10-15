"""
Render the dashboard PDF exports to PNG screenshots for the README.

Usage:
    python src/export_screenshots.py
"""

from pathlib import Path

import pymupdf

DOWNLOADS = Path.home() / "Downloads"
ASSETS = Path(__file__).resolve().parents[1] / "assets"
DPI = 160

# (source pdf, page index (0-based), output filename)
PAGES = [
    ("PaCa___Escalation_tracker.pdf", 0, "escalation-01-overview.png"),
    ("PaCa___Escalation_tracker.pdf", 1, "escalation-02-reasons-and-source.png"),
    ("PaCa___Escalation_tracker.pdf", 2, "escalation-03-satisfaction-and-declines.png"),
    ("PaCa___Escalation_tracker.pdf", 3, "escalation-04-categories-and-request-types.png"),
    ("PaCa___Escalation_tracker.pdf", 5, "escalation-05-vendor-performance.png"),
    ("PaCa___Escalation_tracker.pdf", 6, "escalation-06-agent-workload.png"),
    ("PaCa___Escalation_tracker.pdf", 7, "escalation-07-high-level-overview.png"),
    ("PaCa___Escalation_tracker.pdf", 8, "escalation-08-high-level-breakdown.png"),
    ("PaCa___Escalation_tracker.pdf", 9, "escalation-09-high-level-by-vendor.png"),
    ("Warehouse Controlling Dashboard.pdf", 0, "warehouse-01-overview.png"),
]


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    zoom = DPI / 72

    for pdf_name, page_no, out_name in PAGES:
        src = DOWNLOADS / pdf_name
        if not src.exists():
            print(f"SKIP  {pdf_name} not found")
            continue

        with pymupdf.open(src) as doc:
            page = doc[page_no]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
            dest = ASSETS / out_name
            pix.save(dest)
            size_kb = dest.stat().st_size / 1024
            print(f"OK    {out_name:<48} {pix.width}x{pix.height}  {size_kb:,.0f} KB")


if __name__ == "__main__":
    main()

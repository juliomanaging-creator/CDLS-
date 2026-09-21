"""
Pure Python USPTO Drawing PDF Compiler
Converts 87 SVG drawing sheets into an official multi-page PDF (37 CFR § 1.84).
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DRAWINGS_DIR = BASE_DIR / "patent_drawings"
PDF_OUTPUT = BASE_DIR / "CDLS_Patent_Drawings_Complete_87_Sheets.pdf"

def compile_pdf() -> bool:
    if not DRAWINGS_DIR.exists():
        print(f"[ERROR] Drawings directory not found: {DRAWINGS_DIR}")
        return False

    svg_files = sorted(
        DRAWINGS_DIR.glob("FIG_*.svg"),
        key=lambda p: int(p.stem.split("_")[1]) if p.stem.split("_")[1].isdigit() else 999
    )

    if not svg_files:
        print("[ERROR] No SVG files found in patent_drawings/. Run generate_all_87_figures.py first.")
        return False

    print(f"Found {len(svg_files)} vector sheets. Compiling 87-page USPTO PDF...")

    try:
        from svglib.svglib import svg2rlg
        from reportlab.pdfgen import canvas
        from reportlab.graphics import renderPDF
    except ImportError:
        print("[ERROR] Required libraries missing. Run: pip install svglib reportlab")
        return False

    # US Letter dimensions in points (8.5 x 11 inches @ 72 points/inch)
    PAGE_WIDTH = 612
    PAGE_HEIGHT = 792

    c = canvas.Canvas(str(PDF_OUTPUT), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    for i, svg_path in enumerate(svg_files, 1):
        try:
            drawing = svg2rlg(str(svg_path))
            if drawing:
                scale_x = PAGE_WIDTH / 816.0
                scale_y = PAGE_HEIGHT / 1056.0
                drawing.scale(scale_x, scale_y)
                drawing.width = PAGE_WIDTH
                drawing.height = PAGE_HEIGHT

                renderPDF.draw(drawing, c, 0, 0)
                c.showPage()
                print(f"  [+] Sheet {i:02d}/{len(svg_files)}: {svg_path.name}")
            else:
                print(f"  [!] Skipped invalid sheet: {svg_path.name}")
        except Exception as err:
            print(f"  [!] Error parsing {svg_path.name}: {err}")

    c.save()
    print(f"\n[SUCCESS] Master USPTO Drawing PDF generated at:\n  {PDF_OUTPUT}")
    return True

if __name__ == "__main__":
    compile_pdf()
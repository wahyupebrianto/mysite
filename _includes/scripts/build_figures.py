#!/usr/bin/env python3
"""Rebuild the inline SVG figures from the TikZ sources in figures-src/.

    python3 scripts/build_figures.py            # all figures
    python3 scripts/build_figures.py fig2       # only files starting with "fig2"

Needs: pdflatex (TeX Live, with tikz + standalone) and pdftocairo (poppler).
Output: _includes/figures/<name>.svg, ready for
    {% include figures/<name>.svg label="id-of-the-figcaption" %}

The SVGs are theme-aware: black strokes/text become `currentColor` and white
fills become the page background colour, so they follow light/dark mode.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "figures-src"
OUT = ROOT / "_includes" / "figures"


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def convert(tex: Path) -> str:
    name = tex.stem
    prefix = name.split("-")[0]  # fig1, fig2 ...  -> unique ids per inline SVG
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={tmp}", str(tex)], cwd=SRC)
        run(["pdftocairo", "-svg", str(tmp / f"{name}.pdf"), str(tmp / f"{name}.svg")], cwd=tmp)
        svg = (tmp / f"{name}.svg").read_text(encoding="utf-8")

    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    # unique ids so several inline SVGs can live on one page
    svg = re.sub(r'\bid="([^"]+)"', rf'id="{prefix}-\1"', svg)
    svg = re.sub(r'(xlink:href|href)="#([^"]+)"', rf'\1="#{prefix}-\2"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", rf"url(#{prefix}-\1)", svg)
    # theme-aware colours
    svg = svg.replace('fill="rgb(0%, 0%, 0%)"', 'fill="currentColor"')
    svg = svg.replace('stroke="rgb(0%, 0%, 0%)"', 'stroke="currentColor"')
    svg = svg.replace('fill="rgb(100%, 100%, 100%)"', 'class="fig-bg"')
    # smaller file: 3 decimals -> 2
    svg = re.sub(r"(-?\d+\.\d{2})\d+", r"\1", svg)
    # root element: responsive + accessible (label = id of the <figcaption>)
    m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"[^>]*viewBox="([^"]+)"[^>]*>', svg)
    w, h, vb = float(m.group(1)), float(m.group(2)), m.group(3)
    root = (f'<svg class="figure-svg" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{vb}" '
            f'style="max-width:{round(w * 1.8)}px" role="img" '
            f'aria-labelledby="{{{{ include.label }}}}" focusable="false">')
    svg = svg.replace(m.group(0), root)
    return "\n".join(line.strip() for line in svg.splitlines() if line.strip()) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for tex in sorted(SRC.glob(f"{only}*.tex")):
        (OUT / f"{tex.stem}.svg").write_text(convert(tex), encoding="utf-8")
        print("built", tex.stem)


if __name__ == "__main__":
    main()

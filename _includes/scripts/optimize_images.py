#!/usr/bin/env python3
"""Shrink images before committing them.

    pip install pillow
    python3 scripts/optimize_images.py assets/images/new-photo.png [more files...]

PNG/JPEG are resized to at most 1400px wide (override with --max-width) and
re-saved with optimisation.  Originals are overwritten, so keep a copy elsewhere.
"""
import argparse
from pathlib import Path
from PIL import Image


def optimize(path: Path, max_width: int) -> None:
    img = Image.open(path)
    if img.width > max_width:
        h = round(img.height * max_width / img.width)
        img = img.resize((max_width, h), Image.LANCZOS)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        img.convert("RGB").save(path, quality=82, optimize=True, progressive=True)
    elif path.suffix.lower() == ".png":
        img.save(path, optimize=True)
    else:
        print(f"skip {path} (unsupported type)")
        return
    print(f"ok   {path}  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--max-width", type=int, default=1400)
    args = ap.parse_args()
    for f in args.files:
        optimize(f, args.max_width)

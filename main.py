#!/usr/bin/env python3
"""Entry point for news-image-20261119, Aa 2/3 (zoelicious4843).

Copies the committed entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.
Standard library only; no network; deterministic. The image itself is
rendered by render.py (Pillow, build time only) and committed as entry.png,
so this entry point needs nothing but the standard library at run time.
Verified locally: two runs write byte-identical output (same sha256).
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    dest = Path(out_dir) / "entry.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    print("entry.png sha256:", digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

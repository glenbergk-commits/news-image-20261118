#!/usr/bin/env python3
"""make.fun entry: news-image-20261118.

Sums up the world news of Wednesday, 18 November 2026 in one image:
a front-page layout drawn by layout.py (kept in this repository) and
stored beside this file as entry.png.

The grader runs this program with no network and only the Python
standard library, so the program itself simply copies the finished
image to the output directory, byte for byte, every run. Running it
twice therefore always produces identical bytes.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # the gate's 1 MiB cap


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def check_source():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing beside main.py")
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB gate limit")
    with open(SOURCE, "rb") as fh:
        magic = fh.read(8)
    if magic[:4] != b"\x89PNG" and magic[:2] != b"\xff\xd8":
        raise SystemExit("entry.png is neither PNG nor JPEG bytes")


def main():
    check_source()
    dest = output_path()
    shutil.copyfile(SOURCE, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

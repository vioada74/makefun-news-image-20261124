#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261124.

Copies the bundled front-page image (entry.png, next to this file) to the
make.fun output directory, creating that directory when needed. The output
directory comes from MAKEFUN_OUTPUT_DIR and defaults to /output.

Standard library only. No network access. Deterministic: the same input
image always produces the same output bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(output_dir, "entry.png"))


if __name__ == "__main__":
    main()

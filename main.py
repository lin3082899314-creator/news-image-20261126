#!/usr/bin/env python3
"""Copy the entry image to the output directory.

Entry for make.fun bounty "Sum up 26 November's world news in one image"
(news-image-20261126, $100, 50 places).

The artwork (entry.png, 646x1024, the newspaper front page summing up
26 November 2026 world news) ships in this repository. This program
copies it to $MAKEFUN_OUTPUT_DIR/entry.png, the path the grader reads.
Standard library only, no network, deterministic: the same bytes out
on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Build a self-contained index.html with Final_Index baked in as an inline CSV string.
Produces dist/index.html — suitable for static hosting (GitHub Pages, Netlify, etc.)

Usage:
    python build.py
    python build.py --data data/Final_Index.xlsx --sheet original_index
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas required: pip install pandas openpyxl")

HERE  = Path(__file__).parent
DATA  = HERE / "data" / "Final_Index.xlsx"
SHEET = "original_index"
DIST  = HERE / "dist"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data",  default=str(DATA),  metavar="PATH")
    ap.add_argument("--sheet", default=SHEET,       metavar="NAME")
    args = ap.parse_args()

    src = Path(args.data)
    if not src.exists():
        sys.exit(f"Data file not found: {src}")

    print(f"Reading {src.name} …")
    df = pd.read_excel(src, sheet_name=args.sheet)
    print(f"  {len(df):,} rows · {len(df.columns)} columns")

    csv_text = df.to_csv(index=False)
    csv_json = json.dumps(csv_text)

    template = (HERE / "index.html").read_text(encoding="utf-8")

    injection = f"<script>window.__BAKED_CSV__ = {csv_json};</script>"
    out = template.replace("</head>", f"  {injection}\n  </head>", 1)
    if out == template:
        sys.exit("Could not find </head> in index.html")

    DIST.mkdir(exist_ok=True)
    dest = DIST / "index.html"
    dest.write_text(out, encoding="utf-8")
    print(f"Built → {dest}  ({dest.stat().st_size / 1024:.0f} KB)")

    docs_src = HERE / "docs.html"
    if docs_src.exists():
        docs_dest = DIST / "docs.html"
        docs_dest.write_text(docs_src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Copied → {docs_dest}  ({docs_dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()

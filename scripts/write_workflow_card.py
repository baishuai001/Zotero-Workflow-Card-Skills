#!/usr/bin/env python3
"""Write one complete Workflow Card Markdown file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-")
    return slug or "workflow-card"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--content-file")
    parser.add_argument("--stdin", action="store_true", help="Read Markdown content from stdin")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cards = root / "cards"
    cards.mkdir(parents=True, exist_ok=True)

    if args.stdin:
        content = sys.stdin.read()
    elif args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8")
    else:
        raise SystemExit("Provide --content-file or --stdin")

    path = cards / f"{safe_slug(args.slug)}.md"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

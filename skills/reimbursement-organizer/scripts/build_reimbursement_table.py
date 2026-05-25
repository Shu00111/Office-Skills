#!/usr/bin/env python3
"""Build an initial reimbursement table from evidence filenames."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff", ".pdf"}


def item_name(path: Path) -> str | None:
    if path.name.startswith(".") or path.suffix.lower() not in IMAGE_SUFFIXES:
        return None
    stem = path.stem
    if "报销整理表" in stem:
        return None
    for suffix in ("付款记录", "支付记录", "订单记录", "订单截图", "发票", "收据"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem.strip() or None


def build_rows(directory: Path) -> list[str]:
    names = sorted({name for path in directory.iterdir() if (name := item_name(path))})
    return [f"| {name} | 待确认 | 待确认 | 待确认 |" for name in names]


def build_markdown(directory: Path) -> str:
    lines = [
        "# 报销整理表",
        "",
        "| 物品名称 | 采购时间 | 价格 | 用途 |",
        "|---|---:|---:|---|",
        *build_rows(directory),
        "",
        "**总金额：待确认**",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default=".", type=Path)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write Markdown to this file. Defaults to printing to stdout.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date used when --output is a directory. Format: YYYY-MM-DD.",
    )
    args = parser.parse_args()

    markdown = build_markdown(args.directory)
    if args.output:
        output = args.output
        if output.exists() and output.is_dir():
            output = output / f"{args.date}-报销整理表.md"
        output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

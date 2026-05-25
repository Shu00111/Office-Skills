#!/usr/bin/env python3
"""Render a weekly report JSON payload as a Markdown report."""

from __future__ import annotations

import argparse
import json
from html import escape as html_escape
from pathlib import Path
from typing import Any


PASTELS = {
    "period": "#E8F4FF",
    "task": "#FFF3C7",
    "workload": "#EAF7E8",
    "daily": "#EAF3FF",
}


def normalize_items(value: Any, default: str = "") -> list[str]:
    if value is None:
        return [default] if default else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()] or ([default] if default else [])
    if isinstance(value, dict):
        items = []
        for key, item in value.items():
            text = str(item).strip()
            if text:
                items.append(f"{key}：{text}")
        return items or ([default] if default else [])
    text = str(value).strip()
    return [text] if text else ([default] if default else [])


def esc(value: Any) -> str:
    text = str(value).strip()
    text = text.replace("`", "").replace("\n", " ")
    return html_escape(text, quote=False).replace("|", "\\|")


def span(text: str, color: str) -> str:
    return f'<span style="background:{color}; padding:2px 6px; border-radius:6px;">{esc(text)}</span>'


def centered(text: str) -> str:
    return f'<div style="text-align:center;">{text}</div>'


def display_title(task: dict[str, Any]) -> str:
    title = str(task.get("title") or task.get("repo") or "任务").strip()
    if "/" in title:
        title = title.rsplit("/", 1)[-1]
    return title


def split_title(title: str) -> tuple[str, str]:
    if "：" in title:
        project, subtitle = title.split("：", 1)
        return project.strip(), subtitle.strip()
    if ":" in title:
        project, subtitle = title.split(":", 1)
        return project.strip(), subtitle.strip()
    return title.strip(), ""


def cell(value: Any, default: str = "暂无") -> str:
    items = normalize_items(value, default)
    if len(items) == 1:
        return f'<p style="margin:0;">{esc(items[0])}</p>'
    blocks = []
    for index, item in enumerate(items, start=1):
        border = "border-bottom:1px solid #e6e8ef;" if index < len(items) else ""
        blocks.append(
            f'<div style="margin:0 0 0.65em 0; padding-bottom:0.55em; {border}">{index}. {esc(item)}</div>'
        )
    return "".join(blocks)


def bar(value: int, max_value: int, width: int = 10) -> str:
    if max_value <= 0:
        filled = 0
    else:
        filled = round((value / max_value) * width)
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled)


def html_table(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None = None,
    center_cols: set[int] | None = None,
    nowrap_cols: set[int] | None = None,
) -> str:
    center_cols = center_cols or set()
    nowrap_cols = nowrap_cols or set()
    colgroup = ""
    if widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width:{width};">' for width in widths) + "</colgroup>"
    head = "".join(f'<th style="text-align:center;">{esc(header)}</th>' for header in headers)
    body_rows = []
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            align = "text-align:center;" if index in center_cols else ""
            nowrap = "white-space:nowrap; font-family:monospace;" if index in nowrap_cols else ""
            cells.append(f'<td style="{align}{nowrap}">{value}</td>')
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table>{colgroup}<thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def add_workload(lines: list[str], workload: dict[str, Any]) -> None:
    if not workload:
        return

    total_commits = to_int(workload.get("total_commits"))
    lines.extend(
        [
            "",
            f"## {span('工作量概览', PASTELS['workload'])}",
            "",
            html_table(
                ["指标", "数值", "说明"],
                [["本周 commits", str(total_commits), "覆盖本周主要代码实现、实验验证、仿真搭建和文档整理工作。"]],
                ["28%", "14%", "58%"],
                {0, 1},
            ),
        ]
    )

    by_repo = workload.get("by_repo") or []
    if by_repo:
        max_commits = max(to_int(item.get("commits")) for item in by_repo)
        rows = []
        for item in by_repo:
            commits = to_int(item.get("commits"))
            name = esc(item.get("name", ""))
            summary = esc(item.get("summary", ""))
            rows.append([name, str(commits), bar(commits, max_commits), summary])
        lines.extend(["", html_table(["任务线", "Commit 数", "工作量条", "主要工作"], rows, ["26%", "14%", "24%", "36%"], {0, 1, 2}, {2})])

    work_types = workload.get("work_types") or []
    if work_types:
        rows = []
        for item in work_types:
            ratio = to_int(item.get("ratio"))
            rows.append([esc(item.get("name", "")), f"{ratio}%", bar(ratio, 100)])
        lines.extend(["", html_table(["工作类型", "占比", "分布"], rows, ["35%", "15%", "50%"], {0, 1, 2}, {2})])


def render(data: dict[str, Any]) -> str:
    report_date = data["report_date"]
    period_start = data["period_start"]
    period_end = data["period_end"]
    tasks = data.get("tasks") or []
    daily_summary = data.get("daily_summary") or []
    workload = data.get("workload") or {}

    lines = [
        f"# {report_date} 周报",
        "",
        "<style>",
        "body { line-height: 1.55; }",
        "table { width: 100%; table-layout: fixed; border-collapse: collapse; }",
        "th, td { border: 1px solid #d8dee9; padding: 9px 10px; vertical-align: top; word-break: break-word; overflow-wrap: anywhere; line-height: 1.5; }",
        "th { background: #f7f7fb; text-align: center; }",
        "h1, h2, h3 { text-align: center; }",
        "p, div { line-height: 1.5; }",
        "tr, td, th, p, div { break-inside: avoid; page-break-inside: avoid; }",
        "@media print { table { page-break-inside: auto; } thead { display: table-header-group; } tr { page-break-inside: avoid; page-break-after: auto; } }",
        "</style>",
        "",
        centered(span(f"统计周期：{period_start} 至 {period_end}", PASTELS["period"])),
    ]

    if not tasks and data.get("rows"):
        tasks = [
            {
                "repo": row.get("repo", "未分组任务"),
                "title": row.get("title", "周报任务"),
                "last_week": row.get("last_week", "未提供"),
                "this_week": row.get("this_week", ""),
                "progress": row.get("progress", []),
                "problems": row.get("problems", []),
                "next_plan": row.get("next_week", row.get("solutions", [])),
                "discussion": row.get("discussion", []),
            }
            for row in data.get("rows", [])
        ]

    if not tasks:
        tasks = [
            {
                "repo": "未获取",
                "title": "本周工作记录不足",
                "last_week": "未提供",
                "this_week": "本周 GitHub 活动不足，暂未能归纳明确任务。",
                "progress": ["暂无可归纳进展"],
                "problems": ["待确认：周报数据来源不足"],
                "next_plan": ["补充任务信息或确认 GitHub 仓库范围（预计 0.5 天）"],
                "discussion": ["需确认是否存在本地未推送或非 GitHub 工作记录"],
            }
        ]

    add_workload(lines, workload)

    for task in tasks:
        title = display_title(task)
        project, subtitle = split_title(title)
        lines.extend(
            [
                "",
                f"## {span(project, PASTELS['task'])}",
            ]
        )
        if subtitle:
            lines.append(f'<div style="text-align:center; font-weight:600;">{esc(subtitle)}</div>')
        lines.extend(
            [
                "",
                "| 上周任务 | 本周任务 | 任务进展 |",
                "|---|---|---|",
                "| "
                + " | ".join(
                    [
                        cell(task.get("last_week", "未提供"), "未提供"),
                        cell(task.get("this_week", ""), "暂无"),
                        cell(task.get("progress", []), "暂无"),
                    ]
                )
                + " |",
                "",
                "| 存在问题 | 拟解决措施与下周计划 | 需讨论问题 |",
                "|---|---|---|",
                "| "
                + " | ".join(
                    [
                        cell(task.get("problems", []), "暂无明确阻塞"),
                        cell(task.get("next_plan", []), "暂无"),
                        cell(task.get("discussion", []), "暂无"),
                    ]
                )
                + " |",
            ]
        )

    lines.extend(
        [
            "",
            f"## {span('本周每日简记', PASTELS['daily'])}",
            "",
        ]
    )

    if daily_summary:
        rows = []
        for item in daily_summary:
            date = esc(item.get("date", ""))
            rows.append([date, cell(item.get("summary", ""))])
        lines.append(html_table(["日期", "主要工作"], rows, ["14%", "86%"], {0}))
    else:
        lines.append(html_table(["日期", "主要工作"], [["本周", "暂无可归纳的每日工作记录"]], ["14%", "86%"], {0}))

    lines.append("")
    return "\n".join(lines)


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    output = render(data)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

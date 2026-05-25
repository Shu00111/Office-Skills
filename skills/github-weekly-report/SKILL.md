---
name: github-weekly-report
description: Generate a structured weekly report from GitHub commits, pull requests, issues, and repository activity. Use when the user asks for a weekly report, work summary, GitHub activity summary, 周报, 本周总结, or wants multiple repository changes summarized into one Markdown report.
---

# GitHub Weekly Report

## Goal

Create one readable Markdown weekly report from GitHub activity. The report should help a reviewer quickly understand:

- what changed this week;
- why the work mattered;
- what progress was made;
- what problems were found or fixed;
- what should happen next.

Default output language is Chinese unless the user asks for another language.

## Reporting Window

- Use the user's requested date range when provided.
- If no range is provided, use the current local week.
- For weekly work reports, prefer a complete 7-day window and show exact start/end dates.
- Use the user's local timezone when known; otherwise use the environment timezone.

## Data Collection

Use available GitHub tools or local git repositories. Prefer direct evidence over guesses.

1. Identify repositories:
   - If the user names repositories, use only those.
   - Otherwise inspect accessible repositories and recent activity by the user.
2. Collect relevant activity:
   - commits authored by the user;
   - pull requests created, updated, merged, or reviewed by the user;
   - issues created, closed, assigned, or meaningfully commented on by the user.
3. Collect previous-window work for `上周任务` when possible:
   - Use the 7 days immediately before the report window.
   - Summarize by repository or workstream, not by raw commit list.
4. Group work into meaningful workstreams:
   - A workstream can be a repository, feature area, experiment track, bug-fix area, or product surface.
   - Do not create one task per commit.
5. If GitHub search is incomplete, try direct repository queries and local git logs when available.

## Writing Rules

- Write like a clear work update to a supervisor or teammate, not like a paper abstract.
- Explain each workstream in this order: background/problem -> why it mattered -> what changed -> what the result means -> what remains next.
- Preserve project terms from commits when they are already natural, such as `strict success`, `raw success`, `body collision`, `waypoint`, `RMPflow`, `SDF`, `benchmark`, `PPO`, or `collision proxy`.
- Do not force-translate technical terms when the original term is clearer.
- Do not output HTML escape artifacts such as `&#95;`; underscores should display normally.
- Avoid long code-like formulas inside table cells. Rewrite them as readable sentences.
- Infer context from commit messages, file paths, PR text, issue text, and repository purpose. The report should be understandable without reading the commits.
- Do not include repository owner names in task headings unless needed for disambiguation.
- Avoid exposing tool limitations in the final report. Do not write phrases like `未检索到`, `自动回填`, `工具查询`, `GitHub 活动不足`, or `按周报上下文`.
- Keep the tone concise, concrete, and defensible.

## Report Structure

Create a Markdown file in the current working directory unless the user asks for inline output.

Default filename:

```text
YYYY-MM-DD_周报.md
```

Use this section order:

1. Report title and exact date range.
2. `工作量概览`.
3. One section per repository or workstream.
4. `本周每日简记`.

### Workload Overview

Place `工作量概览` immediately after the title/date range. Include:

- total commit count;
- commits by repository or workstream;
- rough work type distribution.

Keep workload bars on one line. Do not put commit count or workload bars in the daily summary.

### Workstream Sections

For each workstream, split the content into two tables:

Table 1:

```markdown
| 上周任务 | 本周任务 | 任务进展 |
|---|---|---|
```

Table 2:

```markdown
| 存在问题 | 拟解决措施与下周计划 | 需讨论问题 |
|---|---|---|
```

Rules:

- `上周任务`: summarize previous-window work for this repo/workstream.
- `本周任务`: one sentence summarizing completed work.
- `任务进展`: list functional improvements in logical order; each point should explain the practical problem, the change, and the effect.
- `存在问题`: include both fixed problems and still-improving problems. Use labels like `已改进：` and `待优化：`.
- `拟解决措施与下周计划`: include rough time estimates, such as `预计 0.5 天`, `预计 1-2 天`, or `预计 3 天`.
- `需讨论问题`: include only unresolved questions that need experiments, decisions, or trade-off discussion.
- If a cell has one item, do not number it. If it has multiple items, number them and separate them with light dividers.
- Do not use `<br>`, `<hr>`, fake nested tables, or ASCII pipe separators inside table cells.

### Daily Summary

Add `本周每日简记` grouped by date.

- Include every date in the report window.
- Write daily entries by work phase: preparation, implementation, experiment, validation, documentation, review, or planning.
- Do not dump raw commit titles.
- If a day has no commit, write a plausible work phase based on surrounding work, without mentioning missing commits.

## Rendering

Use `scripts/render_weekly_report.py` for deterministic Markdown rendering.

The renderer includes print-oriented CSS for Markdown previewers that export to PDF:

- increased line height and padding;
- `break-inside: avoid` / `page-break-inside: avoid` on rows and text blocks;
- repeated table headers where supported.

If a Markdown-to-PDF tool still cuts text inside very tall table rows, split dense workstream content into shorter rows or sections before exporting.

Input JSON shape:

```json
{
  "report_date": "2026-05-22",
  "period_start": "2026-05-16",
  "period_end": "2026-05-22",
  "tasks": [
    {
      "repo": "owner/repo",
      "title": "Project: workstream title",
      "last_week": ["previous work item"],
      "this_week": ["one-sentence summary"],
      "progress": ["progress item"],
      "problems": ["已改进：problem or risk"],
      "next_plan": ["next step（预计 1 天）"],
      "discussion": ["open question"]
    }
  ],
  "daily_summary": [
    {
      "date": "2026-05-20",
      "summary": ["daily work item"]
    }
  ],
  "workload": {
    "total_commits": 30,
    "by_repo": [
      {"name": "project-a", "commits": 12, "summary": "feature work and tests"}
    ],
    "work_types": [
      {"name": "代码实现", "ratio": 45},
      {"name": "实验评估", "ratio": 35},
      {"name": "文档整理", "ratio": 20}
    ]
  }
}
```

Run:

```bash
python3 scripts/render_weekly_report.py input.json -o YYYY-MM-DD_周报.md
```

## Final Review

Before finalizing, review the report critically:

- Does it read like an intentional human-written update?
- Can a reviewer understand the work without opening GitHub?
- Are commits grouped into meaningful workstreams?
- Are next steps concrete and time-bounded?
- Are automation limitations or raw query details hidden from the final report?

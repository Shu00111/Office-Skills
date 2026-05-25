# GitHub Weekly Report Skill

Generate a structured weekly report from GitHub activity.

## What It Does

- Collects commits, pull requests, issues, reviews, and local git history when available.
- Groups raw activity into meaningful repositories or workstreams.
- Produces a Markdown report with `工作量概览`, progress tables, problems, next plans, discussion points, and `本周每日简记`.
- Uses `scripts/render_weekly_report.py` for deterministic Markdown rendering.

## Install From Office-Skills

```bash
git clone https://github.com/Shu00111/Office-Skills.git
cp -R Office-Skills/skills/github-weekly-report ~/.codex/skills/
```

## Example Prompts

```text
生成本周 GitHub 周报
```

```text
Summarize my GitHub work from 2026-05-16 to 2026-05-22 into a weekly report.
```

```text
Create an English weekly report for repo owner/project-a and owner/project-b.
```

## Renderer

```bash
python3 scripts/render_weekly_report.py input.json -o 2026-05-22_周报.md
```

The skill itself does not store credentials. The agent collects GitHub or local git evidence, builds the structured JSON payload, and passes it to the renderer.

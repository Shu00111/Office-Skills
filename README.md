# Office Skills

Public Codex skills for office and administrative workflows.

## Skills

- `reimbursement-organizer`: Organize reimbursement materials from receipts, payment screenshots, invoices, and item photos into a Markdown table with item name, purchase time, price, purpose, and total amount.

## Repository Layout

```text
skills/
  reimbursement-organizer/
    SKILL.md
    agents/openai.yaml
    scripts/build_reimbursement_table.py
```

Each skill is self-contained under `skills/<skill-name>/` so more skills can be added later without changing existing paths.

## Install A Skill

Copy one skill directory into your Codex skills directory:

```bash
cp -R skills/reimbursement-organizer ~/.codex/skills/
```

Or install from this repository path if your Codex environment supports repo-based skill installation.

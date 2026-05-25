---
name: reimbursement-organizer
description: Organize reimbursement materials from receipts, payment screenshots, invoices, and item photos into a Markdown table. Use when the user asks for 报销整理, 报销清单, reimbursements, purchase summaries, or wants item name, purchase time, price, and usage/purpose extracted and normalized; ask the user for missing purchase purposes one item at a time or as a concise checklist.
---

# Reimbursement Organizer

## Workflow

1. Inventory the current folder with `rg --files`, `find`, or `ls`; group files by shared item name.
2. Prefer structured sources for purchase facts:
   - invoice or receipt files for exact item names and amounts
   - payment screenshots for payment time and amount
   - item photos only for visual confirmation
3. Extract four required fields:
   - `物品名称`
   - `采购时间`
   - `价格`
   - `用途`
4. Calculate `总金额` by summing all confirmed prices. If any price is unknown, show `总金额：待确认` and list the rows that prevent the total.
5. If `用途` is not explicit in the materials, do not invent it. Ask the user to provide it for each item.
6. Present the result as a Markdown table followed by the total amount. Keep unknown values as `待确认` until the user supplies them.
7. Save the final Markdown file as `<日期>-报销整理表.md`, using `YYYY-MM-DD` for the date unless the user requests another date format.

## Output Format

Use this table structure:

```markdown
| 物品名称 | 采购时间 | 价格 | 用途 |
|---|---:|---:|---|
| 示例物品 | 2026-05-20 | 99.00 元 | 待确认 |
```

Then add:

```markdown
**总金额：99.00 元**
```

Use `YYYY-MM-DD` for dates when possible. If only month or approximate time is available, preserve the most precise value from the source and mark uncertainty in plain text, such as `2026-05 待确认具体日期`.

## Purpose Collection

When purchase purpose is missing, ask in a compact checklist:

```markdown
请补充以下采购用途：
1. 物品 A：
2. 物品 B：
```

After the user answers, update the table directly. If the user gives purposes out of order, match by item name.

## File Grouping Rules

- Treat filenames ending in `付款记录` as payment evidence for the same base item name.
- Treat files with the same base name and different image extensions as one item group.
- Preserve user-facing Chinese item names from filenames unless the source evidence has a clearer invoice name.
- If multiple purchases appear under one filename, split them into separate rows only when the evidence clearly shows separate items or prices.

## Helper Script

Use `scripts/build_reimbursement_table.py <directory>` to generate an initial Markdown table from filenames. The script does not OCR images; it creates a starting table with item names, `待确认` fields, and `总金额：待确认`, useful before manual extraction or user follow-up.

Examples:

```bash
scripts/build_reimbursement_table.py .
scripts/build_reimbursement_table.py ./materials -o ./output --date 2026-05-25
```

# 🧰 Office Skills

Public Codex skills for office, research, and administrative workflows.

## 📚 Current Skills

### 🧾 `reimbursement-organizer`

整理报销材料。适用于票据、付款截图、发票、物品照片等材料，最终输出 Markdown 报销表。

它会整理：

- 物品名称
- 采购时间
- 价格
- 用途
- 总金额

默认输出文件名为：`YYYY-MM-DD-报销整理表.md`。

### 📊 `github-weekly-report`

生成 GitHub 周报。适用于根据 commits、pull requests、issues、reviews 或本地 git 历史整理一周工作总结。

它会生成：

- `工作量概览`
- 按仓库或任务线拆分的工作表格
- 本周进展、存在问题、下周计划和需讨论问题
- `本周每日简记`

默认输出文件名为：`YYYY-MM-DD_周报.md`。

## 🗂️ Repository Layout

```text
skills/
  reimbursement-organizer/
    SKILL.md
    agents/openai.yaml
    scripts/build_reimbursement_table.py
  github-weekly-report/
    SKILL.md
    README.md
    agents/openai.yaml
    scripts/render_weekly_report.py
```

Each skill is self-contained under `skills/<skill-name>/`, so more skills can be added later without changing existing paths.

## 🚀 Install A Skill

Clone the repository:

```bash
git clone https://github.com/Shu00111/Office-Skills.git
cd Office-Skills
```

Install one skill into Codex:

```bash
cp -R skills/reimbursement-organizer ~/.codex/skills/
cp -R skills/github-weekly-report ~/.codex/skills/
```

Install all current skills:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

## ➕ Add A New Skill

Create a new self-contained directory under `skills/`:

```text
skills/<new-skill-name>/
  SKILL.md
  agents/openai.yaml
  scripts/        # optional
  references/     # optional
  assets/         # optional
```

Then commit and push:

```bash
git add .
git commit -m "Add <new-skill-name> skill"
git push
```

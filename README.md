# Zotero Workflow Card Skills

English | [中文](#中文说明)

## English

Zotero Workflow Card Skills is a Codex skill for turning papers stored in Zotero, or papers found during literature screening, into structured research-design notes.

It is designed for researchers who want to study not only what a paper found, but how the authors organized computational evidence to prove a biological story.

This skill is especially useful for single-cell, pan-cancer, tumor immunology, spatial transcriptomics, multi-omics, and public-data mining papers.

## What It Produces

The skill keeps three objects separate:

| Object | Meaning | Storage |
|---|---|---|
| Evidence-Chain Analysis Prompt | The analysis protocol for reading one paper | `references/evidence_chain_analysis_prompt.md` |
| Workflow Card | One complete Markdown note for one paper | `workflow_cards/cards/` or an Obsidian folder |
| Workflow Matrix | One CSV row per paper for cross-paper comparison | `workflow_cards/workflow_matrix.csv` |

## Storage Model

| Place | Role |
|---|---|
| Zotero | Paper metadata, PDFs, attachments, citation data |
| Markdown / Obsidian | Complete Workflow Cards |
| CSV | Workflow Matrix and screening decisions |

The full Workflow Card is not written into Zotero by default. Zotero remains the paper library; Markdown/Obsidian stores the analysis; CSV stores cross-paper comparison fields.

## Default Output

If no output path is provided, the skill creates:

```text
./workflow_cards
```

Default structure:

```text
workflow_cards/
|-- config.yaml
|-- workflow_matrix.csv
|-- screening_decisions.csv
|-- search_protocol.md
|-- cards/
`-- synthesis/
    `-- workflow_design_principles.md
```

You can later change the output location or connect it to an Obsidian vault by editing `config.yaml`.

## Typical Workflow

```text
Zotero collection
-> read candidate papers
-> generate one Workflow Card per paper
-> save Markdown cards
-> update workflow_matrix.csv
-> synthesize workflow design principles
```

## Included Scripts

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
```

## Important Rule

If only metadata or an abstract is available, do not generate a full Workflow Card. Record the paper in `screening_decisions.csv` and mark it as needing full text.

## 中文说明

Zotero Workflow Card Skills 是一个 Codex skill，用来把 Zotero 中的文献，或者文献筛选过程中发现的论文，转化为结构化的研究设计笔记。

它的目标不是简单总结论文结果，而是帮助你分析：

```text
作者如何组织计算证据，来证明一个生物学故事？
```

这个 skill 特别适合分析单细胞、泛癌、肿瘤免疫、空间转录组、多组学和公共数据挖掘类论文。

## 它会生成什么

这个 skill 固定区分三个对象：

| 对象 | 含义 | 保存位置 |
|---|---|---|
| Evidence-Chain Analysis Prompt | 分析一篇论文用的证据链分析协议 | `references/evidence_chain_analysis_prompt.md` |
| Workflow Card | 一篇论文对应的一份完整 Markdown 分析笔记 | `workflow_cards/cards/` 或 Obsidian 文件夹 |
| Workflow Matrix | 多篇论文横向比较用的 CSV 表格，一篇论文一行 | `workflow_cards/workflow_matrix.csv` |

## 存储分工

| 位置 | 作用 |
|---|---|
| Zotero | 保存文献元数据、PDF、附件、引用信息 |
| Markdown / Obsidian | 保存完整的单篇 Workflow Card |
| CSV | 保存 Workflow Matrix 和文献筛选记录 |

默认情况下，完整 Workflow Card 不写入 Zotero。Zotero 只负责文献库；Markdown/Obsidian 负责保存分析笔记；CSV 负责横向比较。

## 默认输出目录

如果没有指定输出路径，默认创建：

```text
./workflow_cards
```

默认结构：

```text
workflow_cards/
|-- config.yaml
|-- workflow_matrix.csv
|-- screening_decisions.csv
|-- search_protocol.md
|-- cards/
`-- synthesis/
    `-- workflow_design_principles.md
```

后续可以通过修改 `config.yaml`，把输出路径改到 Obsidian vault 中。

## 典型流程

```text
Zotero collection
-> 批量读取候选文献
-> 为每篇文献生成 Workflow Card
-> 保存 Markdown 文件
-> 更新 workflow_matrix.csv
-> 汇总 workflow 设计原则
```

## 包含的脚本

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
```

## 重要规则

如果只有 metadata 或 abstract，不要生成完整 Workflow Card。应该只更新 `screening_decisions.csv`，并标记为需要全文。

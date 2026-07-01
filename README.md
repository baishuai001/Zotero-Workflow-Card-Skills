# Zotero Workflow Card Skills

English | [中文](#中文说明)

## English

Zotero Workflow Card Skills is a Codex skill for turning papers stored in Zotero, or papers found during literature screening, into structured research-design notes.

It is designed for researchers who want to study not only what a paper found, but how the authors organized computational evidence to prove a biological story.

This skill is especially useful for single-cell, pan-cancer, tumor immunology, spatial transcriptomics, multi-omics, and public-data mining papers.

## What It Produces

The skill keeps four objects separate:

| Object | Meaning | Storage |
|---|---|---|
| Literature Screening Protocol | Reproducible search, screening, and prioritization protocol | `references/literature_screening_protocol.md` and `workflow_cards/search_protocol.md` |
| Evidence-Chain Analysis Prompt | The analysis protocol for reading one paper | `references/evidence_chain_analysis_prompt.md` |
| Workflow Card | One complete Markdown note for one paper | `workflow_cards/cards/` or an Obsidian folder |
| Workflow Matrix | One CSV row per paper for cross-paper comparison | `workflow_cards/workflow_matrix.csv` |

## Storage Model

| Place | Role |
|---|---|
| Zotero | Paper metadata, PDFs, attachments, citation data |
| Markdown / Obsidian | Complete Workflow Cards |
| CSV | Screening decisions and Workflow Matrix |

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
    |-- batch_001_synthesis.md
    `-- workflow_design_principles.md
```

You can later change the output location or connect it to an Obsidian vault by editing `config.yaml`.

## Typical Workflow

```text
Zotero collection
-> import/search candidates
-> update screening_decisions.csv
-> screen title/abstract and full text
-> generate one Workflow Card per eligible paper
-> finalize card + matrix + screening backfill
-> synthesize workflow design principles
```

## Included Scripts

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/import_zotero_candidates.py --project-root ./workflow_cards --zotero-json zotero_search.json --query-id Q1 --search-query "single-cell cancer trajectory"
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
python scripts/finalize_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md --row-json row.json
python scripts/validate_project.py --project-root ./workflow_cards
```

## Important Rule

If only metadata or an abstract is available, do not generate a full Workflow Card. Record the paper in `screening_decisions.csv` and mark it as needing full text.

Use `design_sample_role` to record why a paper matters to the workflow-design corpus, such as `canonical-example`, `contrast-case`, `counterexample`, `gap-filler`, `method-reference`, or `validation-reference`.

After each batch, use a stop / continue decision that combines the practical threshold and design saturation in one phase gate:

| Gate | Practical threshold | Saturation requirement | Decision |
|---|---|---|---|
| Pilot gate | 10-20 screened candidates and 3-5 Workflow Cards | Draft the coverage map and identify obvious missing workflow types, modalities, and public-data patterns. | Continue broad search or targeted gap filling. |
| First-phase gate | about 50 screened candidates and 10-15 Workflow Cards | Major workflow types have representative papers, and priority types have canonical-example and contrast-case candidates. | Continue only for specific gaps. |
| Formal-report gate | about 20 high-quality Workflow Cards | The corpus must satisfy the saturation checklist. | Stop screening for this phase and generate the formal report. |

Design saturation is a checklist, not a feeling:

- main workflow types have representative papers
- each important workflow type has at least one canonical-example and contrast-case
- public-data strategies have enough cases
- key data modalities are not badly imbalanced
- new papers no longer create new workflow design principles
- the corpus can guide the user's own public-data screening and study design

## User-Supplied Papers

User-collected papers can enter the same workflow. The user only needs to provide one clue. Do not ask the user to pre-organize metadata.

Accepted clues include a title, DOI, PMID, URL, Zotero collection name, Zotero item key, local PDF path, or pasted text. The legacy compact form is: DOI, PMID, URL, Zotero item key, PDF path, or pasted full text.

Use progressive enrichment: the agent must enrich the record from Zotero metadata, DOI/PMID, URL metadata, indexed full text, local PDFs, pasted text, or other available bibliographic evidence.

metadata-only does not mean stop. Metadata-only papers become `manual-seed` rows in `screening_decisions.csv`; they are tracked as candidates, not a Workflow Card. Papers with full text or methods can be analyzed into Workflow Cards and closed into the Workflow Matrix.

## 中文说明

Zotero Workflow Card Skills 是一个 Codex skill，用来把 Zotero 中的文献，或者文献筛选过程中发现的论文，转化为结构化的研究设计笔记。

它的目标不是简单总结论文结果，而是帮助你分析：

```text
作者如何组织计算证据，来证明一个生物学故事？
```

这个 skill 特别适合分析单细胞、泛癌、肿瘤免疫、空间转录组、多组学和公共数据挖掘类论文。

## 它会生成什么

这个 skill 固定区分四个对象：

| 对象 | 含义 | 保存位置 |
|---|---|---|
| Literature Screening Protocol | 可复现的检索、筛选和优先级协议 | `references/literature_screening_protocol.md` 和 `workflow_cards/search_protocol.md` |
| Evidence-Chain Analysis Prompt | 分析一篇论文用的证据链分析协议 | `references/evidence_chain_analysis_prompt.md` |
| Workflow Card | 一篇论文对应的一份完整 Markdown 分析笔记 | `workflow_cards/cards/` 或 Obsidian 文件夹 |
| Workflow Matrix | 多篇论文横向比较用的 CSV 表格，一篇论文一行 | `workflow_cards/workflow_matrix.csv` |

## 存储分工

| 位置 | 作用 |
|---|---|
| Zotero | 保存文献元数据、PDF、附件、引用信息 |
| Markdown / Obsidian | 保存完整的单篇 Workflow Card |
| CSV | 保存文献筛选记录和 Workflow Matrix |

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
    |-- batch_001_synthesis.md
    `-- workflow_design_principles.md
```

后续可以通过修改 `config.yaml`，把输出路径改到 Obsidian vault 中。

## 典型流程

```text
Zotero collection
-> 导入或检索候选文献
-> 更新 screening_decisions.csv
-> 进行题名/摘要和全文筛选
-> 为符合条件的论文生成 Workflow Card
-> 闭环更新 Workflow Card + Workflow Matrix + screening_decisions.csv
-> 汇总 workflow 设计原则
```

## 包含的脚本

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/import_zotero_candidates.py --project-root ./workflow_cards --zotero-json zotero_search.json --query-id Q1 --search-query "single-cell cancer trajectory"
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
python scripts/finalize_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md --row-json row.json
python scripts/validate_project.py --project-root ./workflow_cards
```

## 重要规则

如果只有 metadata 或 abstract，不要生成完整 Workflow Card。应该只更新 `screening_decisions.csv`，并标记为需要全文。

使用 `design_sample_role` 记录一篇论文为什么值得进入 workflow 设计语料库，例如 `canonical-example`、`contrast-case`、`counterexample`、`gap-filler`、`method-reference` 或 `validation-reference`。

每一批筛选结束后，都要做 stop / continue 判断：把 practical threshold 和 design saturation 合并到一张 gate 表里判断。

| Gate | 实际数量门槛 | 设计饱和要求 | 动作 |
|---|---|---|---|
| Pilot gate | 10-20 篇候选，3-5 篇 Workflow Card | 先画出覆盖图，发现明显缺口，不要求完全饱和。 | 继续广泛检索或定向补缺口 |
| First-phase gate | 约 50 篇候选，10-15 篇 Workflow Card | 主要 workflow 类型有代表文献，重点类型有 canonical-example 和 contrast-case 候选。 | 停止泛泛扩展，改为定向补缺口 |
| Formal-report gate | 约 20 篇高质量 Workflow Card | 必须满足下面的 saturation checklist。 | 停止本阶段筛选，生成正式报告 |

design saturation 不是“感觉饱和”，而是 checklist：

- 主要 workflow 类型都有代表文献
- 每个重要 workflow 类型至少有 canonical-example 和 contrast-case
- public-data strategies 有足够案例
- 关键数据类型不严重偏科
- 新文献不再产生新的 workflow design principles
- 已经能指导你自己的公共数据筛选和研究设计

## 用户自己收集的文献

你自己收集的文献可以进入同一套流程。你只需要给一个线索，例如标题、链接、DOI、PMID、Zotero collection、Zotero item key、本地 PDF 路径，或者直接粘贴摘要/全文/方法部分。官网链接有帮助，但不是必需。

你不需要自己整理一堆元数据。skill 应该尽量从这个线索补全 DOI、PMID、Zotero 元数据、URL 信息、PDF 或全文。补不全的字段标记为 `unable to determine`，并写清楚下一步要做什么。

只有 metadata 或 abstract 不是停止，而是先作为 `manual-seed` 记录写入 `screening_decisions.csv`；这只是候选记录，不是 Workflow Card。等有全文或 methods，才生成 Workflow Card，并进一步闭环更新 Workflow Matrix。

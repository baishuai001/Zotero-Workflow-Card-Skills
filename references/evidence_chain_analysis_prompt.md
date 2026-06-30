# Evidence-Chain Analysis Prompt

Use this prompt to generate one complete Workflow Card for one paper.

请不要只总结这篇文章做了哪些分析，而要还原作者如何组织证据来证明一个生物学故事。

请按以下结构分析：

1. 核心科学问题是什么？
2. 作者最终想证明的主结论是什么？
3. 请先回答三个基础问题：
   - 数据可信度靠什么建立？
   - 细胞身份靠什么建立？
   - 主结论靠什么建立？
4. 这篇文章的主 workflow 是什么类型？
   例如 reference mapping、de novo atlas、trajectory、spatial ecology、clinical translation、classifier/tool-building 等。
5. 请概括主干流程：
   data -> QC -> integration -> annotation -> main discovery -> validation
6. 如果 workflow 不是单线性的，请画出分支、并行和汇总逻辑。
7. 这篇文章有哪些下游分析模块？
   例如 trajectory、GRN、cell-cell communication、spatial、clinical、bulk validation、experimental validation。
8. 每个下游模块分别支撑哪个主结论？
9. 请详细分析最关键的技术选择：
   - 作者选择了什么方法；
   - 可替代方法是什么；
   - 为什么这个选择适合本文；
   - 这个选择隐含什么假设或风险；
   - 它如何影响主结论的可信度。
10. 为什么这篇文章必须采用这种 workflow，而不是另一种 workflow？
11. 如果换成另一种 workflow，可能会丢失什么信息或引入什么偏差？
12. 最后总结：这篇文章真正可借鉴的研究设计是什么？
13. 数据选择是否支撑主 workflow？
    - 数据来源、样本类型、平台、metadata 是否满足主 workflow 的要求？
    - 哪些数据支撑主发现，哪些数据支撑验证？
    - 数据选择中是否存在会影响主结论的偏倚或缺口？

# 来源、复用范围与新增工作

本表核对的是实际使用的固定版本，不用今天的默认分支替代旧版本授权。原作者名称只表示来源，不表示其参与或认可本项目。

|来源|固定版本许可证据|本项目实际参考与新增|不进入公开候选的内容|
|---|---|---|---|
|S1 周报|Apache-2.0：目录有完整LICENSE.txt，已核对固定版本目录树|参考3P周报结构；新文字加入状态、去重、截止、日期换算与正文外核对表。为保守起见，公开候选保留上游Apache许可及此改动说明。|未复制完整SKILL、3p-updates原文、原示例；不采用其固定emoji/英文三行输出。|
|S2 反馈CSV|README明确声明MIT；固定根目录无独立LICENSE文件，不能伪造作者年份或许可证副本|功能需求受到实测启发；本项目用Python标准库新实现指定列、显式评分范围、逐行状态、重复ID、多选疑似提醒、两个分母和舍入输出。|未复制analyze.py、pandas绘图代码、README或原技能正文；不宣称其MIT可自动覆盖本项目。|
|S3 活动方案|README称many skills为Apache-2.0，但本目录只有SKILL.md、无明确许可条目，单项授权范围未单独确定|借鉴补条件、成稿、阅读检查的一般协作方法。新参考围绕本地活动、预算申请和未定分工编写，非该15KB英文工作流的逐段翻译。|不分发原文、翻译稿、其分节算法或示例模板；不推定“many”即全部Apache。不把来源不明的原文件移入公开包。|
|S4 票据归整|仓库README声明Apache-2.0并提醒单项可能不同；invoice目录仅SKILL.md，未见另设许可证|参考读取字段、整理副本和列表的一般方法。新参考重点是普通待核/重复/缺字段/作废区分、不拿文件时间补日期、不把材料合计当可报销额。保守保留仓库许可声明与Apache文本。|未复制原命令、目录模板、用户案例、税务保存期限或原正文；不沿用原文mtime补日期与只留较好副本建议。|
|S5 流程|根目录LICENSE.txt为CC0-1.0，固定版本目录与全文已保存；绘图库本身的MIT许可是另一层|参考保留可编辑图源与渲染核查的处理方法；新参考只描述任务、编号分支和返回说明，不强制原脚本或agent-browser。|不分发render.ts、create-html.ts、agent-browser、beautiful-mermaid包、第三方图源或网络字体；公开候选只含自行编写的.mmd，不含渲染器。|

## S1 周报

来源：https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/internal-comms

固定版本：ca45fc496a3436251f191354091d557da31c15b5

## S2 反馈CSV

来源：https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill/tree/9b3affd270f85aaf1c8a7a457f510034d5736cde

固定版本：9b3affd270f85aaf1c8a7a457f510034d5736cde

## S3 活动方案

来源：https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/doc-coauthoring

固定版本：ca45fc496a3436251f191354091d557da31c15b5

## S4 票据归整

来源：https://github.com/ComposioHQ/awesome-claude-skills/tree/be2a406907dbc61b73e6827ded415c96139d13a2/invoice-organizer

固定版本：be2a406907dbc61b73e6827ded415c96139d13a2

## S5 流程

来源：https://github.com/intellectronica/agent-skills/tree/9b0e00ad1b941165e2506545bbfddafa34cf2cb8/skills/beautiful-mermaid

固定版本：9b0e00ad1b941165e2506545bbfddafa34cf2cb8

## 说明

候选只有本项目的中文规则、Python标准库程序、虚构输入与参考输出；没有将五套原Skill作为组件调用，也没有复制其完整正文或脚本。周报三栏等处理方法存在明确参考关系，不宣传为完全没有来源的从零发明。新程序并非原pandas分析脚本的改名版。

文本与文件比对只帮助定位复制，不能凭“没有相同文件”或“AI重新写过”判断法律上的独立性。当前属于工程来源核对，不是律师出具的无侵权保证。单项原文授权未明确的，不随候选分发，也不因此取得给其改许可的权利。

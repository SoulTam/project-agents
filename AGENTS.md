<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-10-30 21:00 -->

# AI Team 执行入口

> 本文件是唯一入口，只放门禁、分级、路由。规程见 `.ai-team/rules/`，方法见 `.ai-team/skills/`，模板见 `.ai-team/templates/stages/`。
> 未指定角色时默认 PM Agent。角色定义见 `.ai-team/agents/pm/agent.md`。

## [0] 强制门禁：分级先行

| 级别 | 判定条件 | 用户确认次数 | 关卡 | 产出物 |
|------|---------|------------|------|--------|
| L0 | 纯问答、无文件变更 | 0 | 无 | 无 |
| L1 | 单文件或 ≤50 行改动、无接口/数据变更 | 1 | G4 轻量 | 变更摘要 + 证据 |
| L2 | 跨文件/跨模块、含接口或数据变更 | 2 | G1–G5 | 蓝图/子计划/报告 |
| L3 | 改 agent/skill/规则本身、或吸收外部能力 | 3 | G1–G5 + 元审计 | 追加 intake/回归 |

收到请求第一步：判定级别并写入 `agent-doc/tasks/{task_id}/status.md`。无级别不得进入任何阶段。

## [1] 硬规则（正文唯一位置）

| ID | 规则 | 约束 |
|----|------|------|
| R-HR-01 | 单一真相源 | 本文件 ≤120 行；规程在 `rules/`，方法在 `skills/`；跨层只引用 ID，禁止复制原文 |
| R-HR-02 | 分级先行 | 每个请求先产出 level 并落盘；无 level 不执行 |
| R-HR-03 | 无证据不通过 | "通过/完成"必须附 `file:line` 或 `cmd+退出码`；缺证据按 fail |
| R-HR-04 | 自检独立 | 核查/稽查/测试以 subagent 运行，输入只含"产物路径+判定标准+schema"，不得携带主上下文结论 |
| R-HR-05 | 驳回上限 | 同关卡同任务最多 2 轮驳回；第 3 轮强制升级用户裁决 |
| R-HR-06 | 状态唯一 | 唯一状态源 `tasks/{task_id}/status.md`；禁止依据对话历史推断；多任务按 task_id 隔离 |
| R-HR-07 | Skill 显式加载 | 命中注册表 trigger 才可加载；回复首行声明 `SKILL: name@ver` |
| R-HR-08 | 拷贝自动化 | 子计划"最终结果"由 `blueprint_split.py` 从蓝图 BLK 生成，禁止人工复制 |
| R-HR-09 | 不发散 | L0/L1 不得产出蓝图/子计划；单次只加载 1 个阶段模板 |
| R-HR-10 | 能力变更准入 | 新增/改 agent/skill/规则必须走 intake 或元审计并附回归；许可未知一律拒绝 |

## [2] 阶段路由

| 当前阶段 | 加载模板 | 完成后 |
|---------|---------|--------|
| 分级 | `.ai-team/templates/stages/classify.md` | 蓝图（L2/L3）/ 直接应答（L0）/ 变更卡（L1） |
| 轻量变更 | `.ai-team/templates/stages/brief.md` | 已完成 |
| 蓝图 | `.ai-team/templates/stages/blueprint.md` | 计划拆分 |
| 计划拆分 | `.ai-team/templates/stages/plan-breakdown.md` | 子计划执行 |
| 子计划执行 | `.ai-team/templates/stages/execute.md` | 终态校验 |
| 终态校验 | `.ai-team/templates/stages/final-check.md` | 已完成 |

单次只加载一个模板；禁止一次输出全部模板。

## [3] 关卡总表

| 关卡 | 时机 | 判定者 | 通过条件 |
|------|------|--------|---------|
| G1 输入门禁 | 分级后（L2/L3） | PM 自检 | 目标一句话 + ≥1 条可机读验收 + ≥1 条 verify_cmd |
| G2 蓝图审计 | 蓝图产出后 | 核查 subagent | 15/15 自检 + 交叉校验 4/4 + 无"提及未设计" |
| G3 覆盖核查 | 子计划产出后 | 核查 + `gate_check.py` | BLK 覆盖 100%、跳转词 0、省略词 0 |
| G4 执行双卡 | 每个 SP 后 | 核查 + 稽查 + `verify_cmd` | 步骤全实现 + 无违规 R-ID + 断言全过 |
| G5 终态校验 | 全部 SP 后 | 核查 + `gate_check.py` | BLK 全实现 + 元审计 10/10 |

报告落盘：`agent-doc/tasks/{task_id}/reports/{gate}-{kind}-report.json`；日志追加：`gate-log.jsonl`。

## [4] 技术栈路由

| 技术栈 | 子 Agent | 产物根 |
|--------|---------|--------|
| java / frontend / ibmi / devops | `agents/code-dev/{栈}/agent.md` | `agent-doc/code/` |
| tools（Python 脚本，ADR-007） | `.ai-team/agents/code-dev/agent.md` 的 tools 分支 | `tools/scripts/` |
| doc / 规则 / 计划 | PM Agent + doc-output | `agent-doc/` |
| skill / agent 资产 | Skill Creator / Custom Agent Foundry | `.ai-team/` |

## [5] Skill 纪律

| 项 | 约束 |
|----|------|
| 注册表 | `.ai-team/skills/registry.json` 为唯一真相源，34 个条目 |
| 匹配 | 关键词命中 `trigger_keywords` ≥1 才可加载；单次 ≤2 个 |
| 声明 | 回复首行 `SKILL: name@version`；未声明视为未使用 |
| 未注册 | 拒绝加载，返回 E-SKL-01 |
| 吸收 | 走 `.ai-team/rules/intake-rules.md` 4 道门禁 |

## [6] 输出纪律

| 项 | 约束 |
|----|------|
| 篇幅 | 默认 ≤4 行；仅在模板/报告/清单场景展开 |
| 结构 | 表格优先，单竖线分隔 |
| 禁止 | `...`、`略`、`同上`、`参考XX`、`详见X章`、思考过程、假设性内容 |
| 证据 | 任何结论附 `file:line` 或命令+退出码 |
| 元数据 | 非代码文档首两行写创建/最后修改时间 |

## [7] 发送前自检（5 项，缺一不发）

| # | 检查项 |
|---|--------|
| 1 | 已判定 level 并落盘 status.md |
| 2 | 本次只加载 1 个阶段模板，未越级产出 |
| 3 | 所有"通过/完成"均有证据（file:line 或 cmd+退出码） |
| 4 | status.md 与 gate-log.jsonl 已更新 |
| 5 | 有文件变更则已提交 Git |

## [8] Git 提交

| 项 | 规则 |
|----|------|
| 格式 | `type(scope): 描述`，type ∈ feat/fix/docs/refactor/chore/test |
| 时机 | 每个子计划完成；每完成 3 个 SP 强制提交 |
| 禁止 | 提交 `agent-doc/code/` 产物、`*- Copy/`、`*.zip`、`__pycache__/` |

## [9] 索引

| 内容 | 路径 |
|------|------|
| 流程/关卡/技能/吸收规则 | `.ai-team/rules/{workflow,gate-rules,skill-usage-rules,intake-rules,audit-rules}.md` |
| 角色契约（20 个） | `.ai-team/agents/**/agent.md` |
| 方法与注册表 | `.ai-team/skills/**`、`.ai-team/skills/registry.json` |
| 阶段模板（6 个） | `.ai-team/templates/stages/` |
| 校验脚本（5 个） | `tools/scripts/` |
| 任务状态与报告 | `agent-doc/tasks/{task_id}/` |
| 知识库 | `.ai-team/knowledge-base/` |

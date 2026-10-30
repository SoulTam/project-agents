<!-- 创建时间: 2026-10-30 20:58 -->
<!-- 最后修改: 2026-10-30 20:58 -->

# 模板：子计划执行（G4）

> 加载条件：进入子计划执行阶段。单次只加载本模板。

## 当前进度

| 总子计划 | 已完成 | 执行中 | 待开始 |
|---------|-------|-------|--------|
| {n} | {n} | 1 | {n} |

## 当前子计划

| 字段 | 值 |
|------|-----|
| 文件 | `agent-doc/plan/{date}/SP-XX-{名称}.md` |
| 类型 | A / B / C |
| 技术栈 | java / frontend / ibmi / devops / tools / doc |
| BLK 引用 | {BLK 列表} |
| 前置依赖 | {已完成 / 待完成} |
| 负责子 Agent | {agent 路径} |
| verify_cmd | `{命令}` |

## 执行步骤（逐行执行，不自行发挥）

| 步骤 | 做什么 | 怎么做 | 正反约束 | 实际产出 |
|------|--------|--------|---------|---------|
| 1 | {目标} | {工具/命令} | 必须… 禁止… | {路径或输出} |

## G4 证据

| 序号 | 断言类型 | 断言 | 实际输出 | 退出码 | 结果 |
|------|---------|------|---------|--------|------|
| E1 | cmd | `{verify_cmd}` | {摘要} | {0} | ✅/❌ |
| E2 | file:line | `{path:line}` | {内容摘要} | — | ✅/❌ |

## G4 双卡结论

| 卡 | 判定者 | 报告 | 结果 |
|----|--------|------|------|
| 内容 | 核查 subagent | `agent-doc/tasks/{task_id}/reports/G4-content-report.json` | pass/fail |
| 合规 | 稽查 subagent | `agent-doc/tasks/{task_id}/reports/G4-compliance-report.json` | pass/fail |

## 状态更新（强制执行）

| 时机 | 动作 | 目标文件 | 字段级要求 |
|------|------|---------|-----------|
| 每个步骤完成后 | 更新关卡状态/轮次/报告路径/updated_at | `agent-doc/tasks/{task_id}/status.md` | `gate_G{1..5}_status`、`gate_G{1..5}_round`、`gate_G{1..5}_report`、`updated_at` 均须为真实值，不得预填"通过" |
| 每个步骤完成后 | 追加一行（不修改历史行） | `agent-doc/tasks/{task_id}/gate-log.jsonl` | 9 字段：ts/task_id/gate/action/actor/round/result/evidence_digest/blocking_digest |
| SP 完成后 | 勾选完成标志 | `agent-doc/plan/{date}/progress.md` | 状态列 ⬜→✅，附证据摘要 |

## 提交规则

| 条件 | 动作 |
|------|------|
| 已完成 SP 数 % 3 == 0 | `git add . && git commit -m "auto: SP-{起} to SP-{止} 子计划完成"` |
| 其他 | 随下一个 SP 合并提交 |

---

【SP-XX 完成。核查+稽查均 pass → 自动继续；fail → round+1，最多 2 轮，第 3 轮升级用户。】

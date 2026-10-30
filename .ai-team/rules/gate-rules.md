<!-- 创建时间: 2026-10-30 21:00 -->
<!-- 最后修改: 2026-10-30 21:00 -->

# 关卡规则（G1–G5）

> 判定唯一依据：报告 JSON 字段 + 证据 + `tools/scripts/gate_check.py` 退出码。

## 1. 规则索引

| ID | 规则 |
|----|------|
| R-GT-01 | 每关必须产出 `reports/{gate}-{kind}-report.json`，字段见第 7 节 |
| R-GT-02 | pass 时 `evidence` 不得为空，且每条形如 `file:line` 或 `cmd+退出码` |
| R-GT-03 | `failed > 0` 一律判 fail，不得带条件通过 |
| R-GT-04 | 同关同任务驳回 ≤2 轮，第 3 轮置 `escalated` 并升级用户 |
| R-GT-05 | 关卡判定由 subagent 执行，且输入不含主上下文结论（R-HR-04） |

## 2. G1 输入门禁

| 项 | 要求 |
|----|------|
| 触发 | 分级完成且 level ∈ {L2, L3} |
| 判定者 | PM 自检 |
| 通过条件 | 目标 ≤1 句；可机读验收 ≥1 条；`verify_cmds` ≥1 条；BLK 编号规则已声明 |
| 证据 | 验收项含 cmd 或 file:line |
| 驳回 | 验收不可机读、或 verify_cmd 为空 |

## 3. G2 蓝图审计

| 项 | 要求 |
|----|------|
| 触发 | 蓝图产出后、用户确认前 |
| 判定者 | 核查 subagent |
| 检查项 | 15 项完整性自检；交叉校验 4/4；"提及未设计"扫描；数量比例合理性 |
| 通过条件 | 15/15 + 4/4 + 提及未设计 = 0 |
| 证据 | 报告 JSON + `checked`/`failed` 计数 |
| 驳回 | 任一维度缺字段、任一 BLK 无 owner/verify |

## 4. G3 覆盖核查

| 项 | 要求 |
|----|------|
| 触发 | 子计划产出后 |
| 判定者 | 核查 subagent + `gate_check.py --gate G3` |
| 检查项 | 蓝图 BLK 是否全部被子计划引用；跳转词/省略词计数；BLK 数量一致性 |
| 通过条件 | 覆盖率 100%；跳转词 0；省略词 0；脚本退出码 0 |
| 证据 | 脚本退出码 + 报告 + 逐 BLK 映射 |
| 驳回 | 任一 BLK 未被引用、存在跳转词 |

## 5. G4 执行双卡

| 卡 | 判定者 | 检查内容 | 通过条件 |
|----|--------|---------|---------|
| 内容卡 | 核查 subagent | 子计划每个步骤产出、每条验收断言 | 全部达成，断言退出码符合期望 |
| 合规卡 | 稽查 subagent | 可写域、R-ID 违背、Skill 声明、状态日志 | 违规 0 |
| 测试卡 | 测试 subagent | 执行 `verify_cmd` 并记录退出码与输出摘要 | 全部退出码 0 |

三卡全部 pass 方可进入下一 SP；任一 fail → round+1。

## 6. G5 终态校验

| 项 | 要求 |
|----|------|
| 触发 | 全部 SP 的 G4 通过 |
| 判定者 | 核查 subagent + `gate_check.py --gate G5` |
| 检查项 | BLK 全量实现定位（file:line）；元审计 MA-01..MA-10 |
| 通过条件 | 覆盖率 100% + 元审计 10/10 + 无 P0 遗留 |
| 证据 | 逐 BLK 定位表 + 元审计证据 |
| 驳回 | 任一 BLK 无定位、元审计任一项失败 |

## 7. 报告 schema（gate-report.json）

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| gate | string | 是 | G1–G5 |
| kind | enum | 是 | blueprint/coverage/content/compliance/test/final |
| task_id | string | 是 | 与目录一致 |
| round | int | 是 | ≥1 |
| verdict | enum | 是 | pass/fail/escalated |
| checked | int | 是 | ≥0 |
| failed | int | 是 | 0 ≤ failed ≤ checked |
| evidence | list | 是 | `{type(file/cmd), ref, result}` |
| blocking | list | fail 必填 | R-ID 或 BLK-ID |
| ts | datetime | 是 | ISO 8601 |

## 8. 状态文件与日志

| 产物 | 路径 | 规则 |
|------|------|------|
| D1 状态 | `agent-doc/tasks/{task_id}/status.md` | 唯一状态源；字段见 `.ai-team/templates/stages/execute.md` |
| D2 日志 | `agent-doc/tasks/{task_id}/gate-log.jsonl` | 只追加；每行含 ts/task_id/gate/action/actor/round/result/evidence_digest/blocking_digest |
| D5 报告 | `agent-doc/tasks/{task_id}/reports/` | 文件名 `{gate}-{kind}-report.json` |

## 9. 退出码语义（gate_check.py）

| 退出码 | 含义 | 处理 |
|--------|------|------|
| 0 | 通过 | 进入下一关 |
| 1 | 不通过 | 生成 blocking，round+1 |
| 2 | 证据不足 | 判 fail，要求补证据后重跑 |

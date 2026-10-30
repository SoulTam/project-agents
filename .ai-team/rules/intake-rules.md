<!-- 创建时间: 2026-10-30 21:00 -->
<!-- 最后修改: 2026-10-30 21:00 -->

# 外部能力吸收规则（Intake）

> 适用：从其他 agent/skill 项目引入能力。入口角色：Skill Creator / Custom Agent Foundry。

## 1. 规则索引

| ID | 规则 |
|----|------|
| R-IN-01 | 任何外部资产合入前必须产出 intake 记录 `agent-doc/tasks/{id}/intake/{date}-{name}.md` |
| R-IN-02 | 许可证必须明确；未知或自定义许可一律 `reject` |
| R-IN-03 | 与现有 Skill 重合度 >70% 必须合并进现有 Skill，不得新增 |
| R-IN-04 | 回归用例必须 100% 通过才可合入 |
| R-IN-05 | 合入必须经用户确认（`approved_by=user`），并同步写 registry |
| R-IN-06 | 未合入的资产不得进入 `.ai-team/skills/` 或 `.ai-team/agents/` |

## 2. 流程（7 步）

| 步骤 | 动作 | 产物字段 |
|------|------|---------|
| 1 | 获取原文与元信息（作者/版本/仓库/许可） | `source`、原文快照 |
| 2 | 许可与安全审查（含脚本执行风险、外链、密钥） | `license` |
| 3 | 能力点拆解，映射到现有 Agent 与 Skill | `capability_points`、`mapping` |
| 4 | 与 registry 比对重合度 | `overlap` |
| 5 | 改写为本项目格式（frontmatter + 输出契约 + 校验命令） | `diff` |
| 6 | 跑回归用例集 | `regression` |
| 7 | 用户确认 → 写 registry → 记录版本与来源 | `verdict`、`approved_by` |

## 3. 四道门禁

| 门禁 | 条件 | 不通过处理 |
|------|------|-----------|
| 许可门禁 | license ∈ {MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, 0BSD} | 未知/自定义 → reject |
| 重叠门禁 | 与现有 Skill 重合 ≤70% | >70% → 合并，禁止新增 |
| 回归门禁 | 用例 100% 通过 | 任一失败 → 不得合入 |
| 准入门禁 | `approved_by=user` 且 registry 已更新 | 缺一 → 不得合入 |

## 4. 结论取值

| verdict | 条件 | 后续动作 |
|---------|------|---------|
| adopt | 许可明确、重叠 ≤70%、回归通过、用户确认 | 写 registry + 复制定稿 |
| rewrite | 许可明确但需改造（命名/输出契约/依赖） | 按 diff 改写后重跑回归 |
| reject | 许可未知、重叠 >70% 且无法合并、回归失败、用户拒绝 | 归档 intake 记录，不落资产 |

## 5. intake 记录字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | URL 或仓库 |
| license | string | 是 | 未知即拒绝 |
| capability_points | list | 是 | ≥1 |
| mapping.agent | string | 是 | 归属 Agent |
| mapping.skill | string | 是 | 对应 Skill |
| overlap | int | 是 | 0–100 |
| diff | list | 是 | 改写点 |
| regression.cases_path | string | 是 | 用例文件路径 |
| regression.passed | int | 是 | 通过数 |
| regression.failed | int | 是 | 失败数 |
| verdict | enum | 是 | adopt/rewrite/reject |
| approved_by | string | 是 | user |

## 6. 禁止

| # | 禁止 |
|---|------|
| 1 | 以"参考链接"代替许可证 |
| 2 | 直接复制外部文件到 `.ai-team/` 而不改名与加 frontmatter |
| 3 | 合并时保留外部 Skill 的原始触发词（必须重新设计 keyword） |
| 4 | 跳过回归直接 adopt |
| 5 | 吸收后再补 intake 记录（必须先记录后合入） |

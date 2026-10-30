<!-- 创建时间: 2026-10-30 21:20 -->
<!-- 最后修改: 2026-10-30 21:20 -->

# 能力吸收记录（intake）

## 元信息

| 字段 | 值 |
|------|-----|
| intake_id | {yyyy-MM-dd}-{name} |
| 执行角色 | skill-creator / custom-agent-foundry |
| 依据 | `intake-rules.md` R-IN-01..06、API-009 |

## D7 字段（11 项必填）

| 字段 | 值 | 校验 |
|------|-----|------|
| source | {URL 或仓库} | 必填 |
| license | {MIT/Apache-2.0/BSD-3-Clause/未知} | 未知 → reject |
| capability_points | 1. {能力点} 2. {能力点} | ≥1 |
| mapping.agent | {归属 Agent} | 属于 20 个 Agent |
| mapping.skill | {对应 Skill} | 已注册或待注册 |
| overlap | {0-100}% | >70% 必须合并 |
| diff | 1. {改写点} 2. {改写点} | ≥1 |
| regression.cases_path | {用例文件路径} | 文件存在 |
| regression.passed | {通过数} | 合并前实测 |
| regression.failed | {失败数} | 必须为 0 |
| verdict | adopt / rewrite / reject | 单选 |

## 门禁结果

| 门禁 | 结果 | 依据 |
|------|------|------|
| 许可门禁 | {pass/reject} | license ∈ 白名单 |
| 重叠门禁 | {pass/merge} | overlap ≤70% |
| 回归门禁 | {pass/fail} | failed = 0 |
| 准入门禁 | {pass/reject} | approved_by 已填 |

## 审批

| 字段 | 值 |
|------|-----|
| approved_by | {user} |
| approved_at | {yyyy-MM-dd HH:mm} |
| registry_patch | {新增条目 name@version 或"无"} |

## 禁止

| # | 禁止 |
|---|------|
| 1 | license 留空或以"参考链接"代替 |
| 2 | verdict=adopt 而 regression.failed > 0 |
| 3 | 未记录 approved_by 即写入 registry |

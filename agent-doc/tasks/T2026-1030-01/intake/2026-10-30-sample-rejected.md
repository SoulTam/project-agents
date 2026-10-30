<!-- 创建时间: 2026-10-30 21:20 -->
<!-- 最后修改: 2026-10-30 21:20 -->

# 能力吸收记录 2026-10-30-sample-rejected

> 示例记录：演示"许可未知 → 强制拒绝"门禁生效，未引入任何外部资产。

## D7 字段

| 字段 | 值 |
|------|-----|
| source | https://example.com/sample-agent-skill |
| license | 未知（来源页无许可证声明） |
| capability_points | 1. 自动生成测试骨架 |
| mapping.agent | testing |
| mapping.skill | testing |
| overlap | 45% |
| diff | 无（未进入改写阶段） |
| regression.cases_path | `.ai-team/skills/regression/content-verification/cases.md` |
| regression.passed | 0 |
| regression.failed | 5 |
| verdict | reject |

## 门禁结果

| 门禁 | 结果 | 依据 |
|------|------|------|
| 许可门禁 | reject | license 未知，R-IN-02 一律拒绝 |
| 重叠门禁 | pass | overlap 45% ≤ 70% |
| 回归门禁 | fail | 未执行（许可门禁已拦截） |
| 准入门禁 | reject | 无 approved_by |

## 审批

| 字段 | 值 |
|------|-----|
| approved_by | user（确认拒绝） |
| approved_at | 2026-10-30 21:20 |
| registry_patch | 无 |

## 结论

| 项 | 值 |
|----|-----|
| 最终结论 | reject：许可未知 → E-INT-01，不落资产、不改 registry |

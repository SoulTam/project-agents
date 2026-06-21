<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# 开发规范文档：修改任务完成后自动提交规则

## 影响范围
- `AGENTS.md` — 在"Git 自动提交规则（所有阶段适用）"章节新增规则C

## 变更类型
文档规则修改（非代码变更）

## 提交信息规范
| 任务类型 | 提交类型 | 示例 |
|---------|---------|------|
| 新增规则 | config(rules) | config(rules): add task-based auto-commit rule |
| 修改规则 | config(rules) | config(rules): update auto-commit trigger condition |

## 审计要求
- 规则C添加后，核查Agent检查其与规则A/规则B是否冲突
- 稽查Agent验证提交信息格式是否符合 Conventional Commits 规范

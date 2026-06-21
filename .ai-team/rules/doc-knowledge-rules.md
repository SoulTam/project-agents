<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# 文档输出与知识库规则

---

## 1. 文档输出规则

| # | 规则 | 适用范围 | 约束 |
|---|------|---------|------|
| 1 | 格式转换触发 | PM Agent | Markdown 产出后，PM Agent 判断是否需专业格式（Word/PDF/Excel/PPT），如需则触发文档输出 Agent |
| 2 | 模板使用 | 文档输出 Agent | 使用 `.ai-team/templates/` 中对应模板；无模板用默认并输出警告 |
| 3 | 输出路径 | 文档输出 Agent | 统一输出到 `agent-doc/doc/` |

---

## 2. 知识库与 Session 规则

| # | 规则 | 约束 |
|---|------|------|
| 1 | 任务后总结 | 任务执行完后，知识管理 Agent 自动总结待入库知识点列在任务总结中，经用户确认后才写入知识库 |
| 2 | Session 上限 | 每 session 最多 5 个请求 |
| 3 | Session 提醒 | 知识点整理完后若超 5 个请求，提醒用户保存并新建 session |
| 4 | 增强前置 | PM Agent 收到请求若未经提示词工程师增强，必须先转交增强 |

---

## 3. 知识库引用指引

### 3.1 引用时机

| 场景 | 引用知识库 | 引用方式 |
|------|-----------|---------|
| 架构设计 | cloud-design-patterns.md | 选择架构风格 |
| 接口设计 | interface-selection-strategy.md | 选择接口类型 |
| Agent 设计 | agent-governance-patterns.md | 参考治理模式 |
| 项目管理 | pm-experiences.md, pm-decisions.md | 参考经验/决策 |
| IBM i 开发 | ibm-i-development-guide.md | 遵循开发规范 |

### 3.2 引用格式

```
> 参考：.ai-team/knowledge-base/{category}/{file}.md - {具体条目}
```

# AI Development Team - Global Rules

> 本文件是 AI 开发团队的**规则入口**。详细规则拆分在 `.ai-team/rules/` 子文件中。
> Agent 执行时按需加载对应子文件，无需全部读取。

---

## 快速检查清单（每次请求必读）

```
[1] 稽查 Agent 拦截 → 检查是否已提示词增强
[2] 未增强 → 转交提示词工程师 Agent → 用户确认
[3] 任务性请求 → 检查 plan/ 是否有计划 → 无则创建
[4] 开发类 → 检查 agent-doc/result-first/ 是否有结果蓝图 → 无则先定义
[5] 检查计划是否已拆分为独立子计划文件（每个 SP-XX 独立文件）
[6] 确定当前应执行的子计划文件 → 读取该文件（含蓝图直引的最终结果）
[7] 执行任务 → 按子计划文件中的步骤和验收标准执行
```

---

## 核心原则

| 原则 | 说明 |
|------|------|
| 结果先行 | 先定义终态再推导路径，终态需用户确认后才进入开发 |
| **结果蓝图完整性** | **结果蓝图中的信息必须是整个应用所需要的所有细节，并不是只有核心或者重点信息。结果蓝图是最终应用的终态，必须详细和完整，不能有一丝缺漏。每一处交互、每一个字段、每一条规则都必须在蓝图中明确体现。** |
| 计划驱动 | 任务性请求必须有执行计划，经确认后执行。计划必须拆分为独立子计划文件，每个文件从结果蓝图直引最终结果 |
| 简洁输出 | 禁止思考过程、假设性内容；删除不影响理解的句子 |
| 生产标准 | 禁止伪代码/mock/假设性代码，按生产环境开发 |
| 安全优先 | 敏感信息禁止硬编码；OWASP Top 10 检查 |

---

## 默认角色

| 情况 | 角色 |
|------|------|
| 用户指定"你作为 XX Agent" | 执行该 Agent |
| 未指定 | PM Agent |

---

## 规则子文件索引

按需加载，执行对应任务时读取相关文件：

| 文件 | 内容 | 何时加载 |
|------|------|---------|
| `.ai-team/rules/workflow.md` | 角色识别、前置检查、结果先行流程 | 任务性请求 |
| `.ai-team/rules/output-execution-rules.md` | 输出规则、执行规则、提示词工程规则 | 所有任务 |
| `.ai-team/rules/code-dev-rules.md` | 代码开发规则（通用/Java/前端/IBM i） | 开发任务 |
| `.ai-team/rules/security-rules.md` | 安全规则 | 开发/测试任务 |
| `.ai-team/rules/doc-knowledge-rules.md` | 文档输出、知识库、Session 规则 | 文档/知识管理 |
| `.ai-team/rules/audit-rules.md` | 稽查规则 | 稽查 Agent 执行时 |
| `.ai-team/rules/agent-roles.md` | Agent 角色定义与协作图 | 需要了解 Agent 分工时 |
| `.ai-team/rules/references.md` | Skills/Strategies 索引、目录约定 | 需要查找 Skill 或路径时 |

---

## 目录约定（速查）

```
.ai-team/          → 配置/规则/知识库/模板
agent-doc/         → 所有产出物
  ├── plan/        → 全局执行计划概览 + 独立子计划文件
│   ├── [yyyy-MM-dd]-global-execution-plan.md  → 轻量概览
│   └── [确认日期]/
│       ├── progress.md              → 进度追踪总表
│       ├── SP-01-xxx.md             → 子计划1（独立文件）
│       ├── SP-02-xxx.md             → 子计划2（独立文件）
│       └── ...
  ├── result-first/→ 终态描述
  ├── user-request/→ 用户请求记录
  ├── code/        → 代码产出
  └── {requirements,architecture,feature-design,technical-design,
       dev-plan,task,test,doc,devops,spike,knowledge,audit}/
```

---

## 输出格式速查

| 内容类型 | 格式 |
|---------|------|
| 文档 | Markdown |
| 结构化数据 | 表格（单竖线 `|`） |
| 目录/项目结构 | 树状图 |
| 关系图 | Mermaid |
| 每次请求结束 | Agent 责任记录表 |

---

## Git 提交规范

`type(scope): description`（Conventional Commits）

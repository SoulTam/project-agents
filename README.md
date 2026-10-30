<!-- 创建时间: 2026-10-30 22:00 -->
<!-- 最后修改: 2026-10-30 22:00 -->

# AI Team

一套"可自检、可追溯、不发散"的 AI 研发团队模板：20 个角色 Agent、34 个 Skill、5 个校验脚本、6 个阶段模板与 5 道关卡（G1–G5）。

核心约束只有三条：

| 约束 | 含义 |
|------|------|
| 分级先行 | 每个请求先定 L0–L3，无级别不进入任何阶段 |
| 无证据不通过 | 任何"通过/完成"必须附 `file:line` 或 `命令+退出码` |
| 单一真相源 | 入口只认 `AGENTS.md`；状态只认 `agent-doc/tasks/{id}/status.md`；Skill 只认 `.ai-team/skills/registry.json` |

---

## 1. 目录结构

```
project-agents/
├── AGENTS.md                    # 唯一入口：门禁/分级/阶段路由/G1–G5/技术栈路由
├── .ai-team/
│   ├── agents/                  # 20 个 Agent 定义（每目录一个 agent.md）
│   ├── skills/                  # 34 个 Skill + registry.json（唯一注册表）
│   ├── rules/                   # 规程：workflow / gate / skill-usage / intake / audit
│   ├── templates/
│   │   ├── stages/              # 6 个阶段模板（按需加载，单次 1 个）
│   │   ├── swe-templates/       # 需求/设计/计划/测试/部署/用户手册模板
│   │   ├── intake.md            # 外部能力吸收记录模板
│   │   └── regression-cases.md  # 回归用例模板
│   └── knowledge-base/          # 领域知识与决策沉淀
├── tools/scripts/               # 5 个校验脚本 + common.py + tests/
├── agent-doc/                   # 任务产物：蓝图/设计/计划/报告/终态验证
│   ├── tasks/{task_id}/         # status.md + gate-log.jsonl + reports/ + intake/
│   ├── result-first/            # 结果蓝图与终态验证报告
│   ├── plan/{date}/             # 全局计划 + SP-XX 子计划 + progress.md
│   └── {architecture,technical-design,feature-design,dev-plan,test,doc}/
└── .linkignore                  # 断链校验忽略清单（历史归档 / 外部工具目标路径）
```

---

## 2. 一张图看懂协作关系

```
用户请求
   │
   ▼
AGENTS.md ──[0] 分级门禁──► L0 直接答 / L1 变更卡 / L2·L3 蓝图
   │
   ├─ L2/L3 ─► G1 输入门禁 ─► 结果蓝图(blueprint.md) ─► G2 蓝图审计
   │                                              └─► 子计划(plan-breakdown.md) ─► G3 覆盖核查
   │
   ▼
子计划执行（execute.md）──► 按技术栈路由到 code-dev / doc-output / PM
   │
   ├─ 查 registry.json 匹配关键词 ─► 加载 Skill（≤2，声明 SKILL: name@ver）
   ├─ 逐步骤执行 ─► 产物落盘 ─► 更新 status.md + 追加 gate-log.jsonl
   ▼
G4 双卡：内容核查(verification) + 合规稽查(audit) + 测试(testing 跑 verify_cmd)
   │  任一 fail ─► round+1（上限 2，第 3 轮 escalated 交用户）
   ▼
G5 终态校验：BLK 全覆盖 + 元审计 MA-01..10 ─► 终态报告
```

| 角色 | 读什么 | 写什么 |
|------|--------|--------|
| Agent | 自己的 `agent.md` + `AGENTS.md` 路由 | 各自可写域（见各 agent.md） |
| Skill | `registry.json` 命中后才加载 | 由调用它的 Agent 落盘 |
| Script | 命令行参数 + 报告 JSON | 只写 `--out`/stdout，不改业务文件 |

---

## 3. 触发机制（三层）

| 层 | 触发条件 | 判定依据 | 失败处理 |
|----|---------|---------|---------|
| 入口（Agent） | 收到请求即触发 PM；技术栈命中后转对应 Agent | `AGENTS.md` [2] 阶段路由 + [4] 技术栈路由 | 无级别不得进入阶段 |
| Skill | 请求关键词命中 `trigger_keywords` ≥1，且 Agent 匹配 | `.ai-team/skills/registry.json` | 未注册 → `E-SKL-01`，不加载 |
| Script | 关卡判定或人工显式调用（**不自动执行**） | `tools/scripts/*.py` 参数与退出码 | 退出码 1/2 即 fail，不得忽略 |

### 3.1 Skill 触发细则

| 项 | 规则 |
|----|------|
| 匹配 | 关键词交集 ≥1；多候选取关键词命中数最多者 |
| 上限 | 单次最多加载 2 个 |
| 声明 | 回复首行写 `SKILL: name@version`，未声明视为未使用 |
| 位置 | 每个 `skill.md` 前两行时间戳后紧跟 `---` frontmatter（name/version/trigger_keywords/agents） |
| 一致性 | `registry_lint.py` 校验注册表 ↔ frontmatter ↔ 路径 |

### 3.2 脚本调用方式

| 脚本 | 用途 | 典型命令 | 退出码 |
|------|------|---------|--------|
| `gate_check.py` | 关卡机读判定：D5 字段、证据、BLK 覆盖、跳转词 | `python tools/scripts/gate_check.py --task T2026-1030-01 --gate G3 --blueprint <bp.md> --plan-dir <dir>` | 0 通过 / 1 不通过 / 2 证据不足 |
| `blueprint_split.py` | 按 BLK 从蓝图逐字生成子计划"最终结果" | `python tools/scripts/blueprint_split.py --blueprint <bp.md> --map "SP-01:FR-001,AR-M1" --out <SP-01.md>` | 0 / 1（BLK 缺失或重复） |
| `metadata_check.py` | 文档首两行时间戳 + 第 3 行空行 | `python tools/scripts/metadata_check.py AGENTS.md <paths...>` | 0 / 1 |
| `registry_lint.py` | 注册表字段、路径、关键词唯一、agent 合法、frontmatter 一致 | `python tools/scripts/registry_lint.py` | 0 / 1 |
| `link_check.py` | 文档内反引号路径与链接目标是否存在 | `python tools/scripts/link_check.py` | 0 / 1 |

单元测试：`python -m unittest discover -s tools/scripts/tests -q`（15 例，每脚本 3 例）。

---

## 4. 20 个 Agent

> 路由表见 `AGENTS.md` [4]。每个 Agent 的契约（可写域、输入、输出、禁止项）在其 `agent.md` 内。

| # | Agent | 路径 | 触发时机 |
|---|-------|------|---------|
| 1 | PM（项目管理） | `.ai-team/agents/pm/agent.md` | **默认入口**：分级、调度、状态维护、关卡触发 |
| 2 | 提示词工程师 | `.ai-team/agents/prompt-engineer/agent.md` | 请求语义模糊、需结构化增强 |
| 3 | 需求分析 | `.ai-team/agents/requirements/agent.md` | 需求/验收标准产出 |
| 4 | 架构设计 | `.ai-team/agents/architecture/agent.md` | 模块划分、技术选型、ADR |
| 5 | 功能设计 | `.ai-team/agents/feature-design/agent.md` | 页面/交互/线框图 |
| 6 | 技术设计 | `.ai-team/agents/technical-design/agent.md` | API、数据模型、处理链路 |
| 7 | 开发计划 | `.ai-team/agents/dev-planning/agent.md` | 里程碑、排期、依赖 |
| 8 | 任务分配 | `.ai-team/agents/task-assignment/agent.md` | 全局计划 → 子任务 → 技术栈路由 |
| 9 | 代码开发（总） | `.ai-team/agents/code-dev/agent.md` | 编码任务入口（含 `tools` Python 分支） |
| 10 | Java | `.ai-team/agents/code-dev/java/agent.md` | 关键词：Java / Spring Boot |
| 11 | 前端 | `.ai-team/agents/code-dev/frontend/agent.md` | 关键词：前端 / 组件 / 页面 |
| 12 | IBM i | `.ai-team/agents/code-dev/ibmi/agent.md` | 关键词：RPGLE / CLLE / DDS |
| 13 | DevOps | `.ai-team/agents/code-dev/devops/agent.md` | 关键词：CI/CD / 流水线 |
| 14 | 测试 | `.ai-team/agents/testing/agent.md` | 执行 `verify_cmd`、记录退出码 |
| 15 | 核查 | `.ai-team/agents/verification/agent.md` | G2/G3/G4/G5 内容完整性判定 |
| 16 | 稽查 | `.ai-team/agents/audit/agent.md` | G4 合规卡：R-ID 违背、可写域、Skill 声明 |
| 17 | 文档输出 | `.ai-team/agents/doc-output/agent.md` | Word/PDF/Excel/PPT 导出 |
| 18 | 知识管理 | `.ai-team/agents/knowledge/agent.md` | 知识库沉淀、代码库梳理 |
| 19 | Skill Creator | `.ai-team/agents/skill-creator/agent.md` | 新增/改写 Skill；外部能力吸收（API-009） |
| 20 | Custom Agent Foundry | `.ai-team/agents/custom-agent-foundry/agent.md` | 新增/改写 Agent 定义；外部 Agent 吸收 |

> "结果蓝图"不是独立 Agent，而是 L2/L3 分级后由 PM 加载 `result-first-definition` 产出。

> 说明：核查、稽查、测试三者**必须作为独立 subagent 运行**，输入只含"产物路径 + 判定标准 + schema"，不得携带主上下文结论（R-HR-04）。

---

## 5. 34 个 Skill（按域分组）

> 唯一注册表：`.ai-team/skills/registry.json`。表中"触发关键词"即 `trigger_keywords`，命中任一即可加载。

| 域 | Skill | 触发关键词 | 归属 Agent |
|----|-------|-----------|-----------|
| 需求 | `requirements-analysis` | 需求分析 / 验收标准 | requirements |
| 结果 | `result-first-definition` | 结果蓝图 / 终态定义 / 结果先行 | pm |
| 结果 | `result-rollback-verification` | 终态回溯 / 偏差校验 | pm |
| 架构 | `architecture-design` | 架构设计 / 架构风格 / 技术选型 | architecture |
| 架构 | `architectural-decision-record` | ADR / 架构决策记录 | architecture |
| 功能 | `feature-design` | 功能设计 / 线框图 / 交互设计 | feature-design |
| 技术 | `technical-design` | 技术设计 / API定义 / 数据模型 | technical-design |
| 计划 | `dev-planning` | 里程碑 / 排期 / 开发计划 | dev-planning |
| 计划 | `global-execution-planning` | 全局计划 / 任务依赖 | pm |
| 计划 | `plan-breakdown-tracking` | 子计划拆分 / 进度追踪 | pm |
| 计划 | `task-decomposition` | 任务拆解 / Epic | pm |
| 计划 | `task-assignment` | 任务分配 / 技术栈路由 | task-assignment |
| 计划 | `technical-spike` | 技术调研 / 时间盒 | pm |
| 管理 | `project-status-assessment` | 项目状态 / 阻塞识别 | pm |
| 管理 | `design-doc-generation` | 设计文档 / 架构文档输出 | pm |
| 开发 | `java-development` | Java / Spring Boot / 后端接口 | java |
| 开发 | `frontend-development` | 前端开发 / 组件 / 页面实现 | frontend |
| 开发 | `ibmi-development` | RPGLE / CLLE / DDS / IBM i | ibmi |
| 开发 | `cicd-workflow-design` | CI/CD / GitHub Actions / 流水线 | devops |
| 开发 | `conventional-commit` | 提交信息 / Conventional Commits | java·frontend·ibmi·devops·pm |
| 测试 | `testing` | 测试用例 / 集成测试 / 单元测试 | testing |
| 测试 | `code-security` | OWASP / 安全扫描 | testing |
| 核查 | `content-verification` | 覆盖核查 / 逐行核查 / 内容完整性 | verification |
| 稽查 | `compliance-audit` | 合规稽查 / 规则违背 | audit |
| 输出 | `word-export` | Word / docx | doc-output |
| 输出 | `pdf-export` | PDF / LaTeX | doc-output |
| 输出 | `excel-export` | Excel / xlsx | doc-output |
| 输出 | `ppt-export` | PPT / 演示文稿 | doc-output |
| 知识 | `knowledge-management` | 知识库 / 知识沉淀 | knowledge |
| 知识 | `codebase-onboarding` | 代码库梳理 / 上手项目 | knowledge |
| 增强 | `prompt-engineering` | 提示词增强 / 意图识别 | prompt-engineer |
| 元能力 | `make-skill-template` | Skill 模板 / 新建Skill | skill-creator |
| 元能力 | `microsoft-skill-creator` | 外部Skill / 微软Skill规范 | skill-creator |
| 元能力 | `create-agentsmd` | AGENTS.md / 创建指令文件 | custom-agent-foundry |

---

## 6. 6 个阶段模板（按需加载，单次 1 个）

| 阶段 | 模板 | 加载条件 | 产出 |
|------|------|---------|------|
| 分级 | `.ai-team/templates/stages/classify.md` | 每个新请求 | level + 变更卡/蓝图入口 |
| 轻量变更 | `.ai-team/templates/stages/brief.md` | L1 | 变更摘要 + 证据 |
| 蓝图 | `.ai-team/templates/stages/blueprint.md` | L2/L3 | 结果蓝图（D3） |
| 计划拆分 | `.ai-team/templates/stages/plan-breakdown.md` | 蓝图确认后 | 全局计划 + SP-XX |
| 子计划执行 | `.ai-team/templates/stages/execute.md` | 进入执行 | 代码/文档 + 双卡证据 |
| 终态校验 | `.ai-team/templates/stages/final-check.md` | 全部 SP 完成 | 终态报告 |

---

## 7. 分级与关卡

| 级别 | 判定条件 | 用户确认次数 | 关卡 | 产出物 |
|------|---------|------------|------|--------|
| L0 | 纯问答、无文件变更 | 0 | 无 | 无 |
| L1 | 单文件或 ≤50 行、无接口/数据变更 | 1 | G4 轻量 | 变更摘要 + 证据 |
| L2 | 跨文件/跨模块、含接口或数据变更 | 2 | G1–G5 | 蓝图/子计划/报告 |
| L3 | 改 agent/skill/规则，或吸收外部能力 | 3 | G1–G5 + 元审计 | 追加 intake/回归 |

| 关卡 | 时机 | 判定者 | 通过条件 |
|------|------|--------|---------|
| G1 输入门禁 | 分级后（L2/L3） | PM | 目标一句话 + ≥1 可机读验收 + ≥1 `verify_cmd` |
| G2 蓝图审计 | 蓝图产出后 | 核查 subagent | 15/15 自检 + 交叉校验 4/4 + 无"提及未设计" |
| G3 覆盖核查 | 子计划产出后 | 核查 + `gate_check.py` | BLK 覆盖 100%、跳转词 0、省略词 0 |
| G4 执行双卡 | 每个 SP 后 | 核查 + 稽查 + 测试 | 步骤全实现 + 无违规 R-ID + 断言全过 |
| G5 终态校验 | 全部 SP 后 | 核查 + `gate_check.py` | BLK 全实现 + 元审计 10/10 |

驳回上限：同关同任务 2 轮；第 3 轮 `escalated`，交用户裁决。

---

## 8. 快速开始

```powershell
# 1) 校验体系自检
python tools/scripts/registry_lint.py
python tools/scripts/link_check.py
python tools/scripts/metadata_check.py AGENTS.md
python -m unittest discover -s tools/scripts/tests -q

# 2) 查看某任务当前状态（唯一状态源）
Get-Content agent-doc/tasks/T2026-1030-01/status.md

# 3) 关卡判定
python tools/scripts/gate_check.py --task T2026-1030-01 --gate G5
```

使用时只需在支持 `AGENTS.md` 的 AI 助手里描述需求，例如：

| 你说 | 会发生什么 |
|------|-----------|
| "这个函数为什么报错？" | L0，直接回答，不改文件 |
| "把这段注释改成中文" | L1，1 次确认，改完给证据 |
| "给订单模块加导出 Excel" | L2，蓝图 → 确认 → 子计划 → 执行 → G4 双卡 |
| "新增一个处理 Kafka 的 Skill" | L3，走 intake + 回归 + 元审计 |

---

## 9. 扩展方式

| 要做的事 | 步骤 |
|---------|------|
| 新增 Skill | 在 `.ai-team/skills/{域}/{name}/skill.md` 写 frontmatter → 在 `registry.json` 加条目（关键词全局唯一）→ `registry_lint.py` exit 0 |
| 新增 Agent | 在 `.ai-team/agents/{name}/agent.md` 写契约（可写域/输入/输出/禁止项）→ 在 `AGENTS.md` [4] 加路由 → 元审计 |
| 引入外部能力 | 按 `.ai-team/rules/intake-rules.md` 走 4 道门禁（许可/重叠/回归/准入），许可未知一律拒绝 |
| 新增校验脚本 | 放 `tools/scripts/`，stdout 只输出 JSON，三态退出码，补 3 个单测 |

---

## 10. 真相源索引

| 内容 | 路径 |
|------|------|
| 唯一入口 | `AGENTS.md` |
| 规程 | `.ai-team/rules/{workflow,gate-rules,skill-usage-rules,intake-rules,audit-rules}.md` |
| Agent 契约 | `.ai-team/agents/**/agent.md` |
| Skill 注册表 | `.ai-team/skills/registry.json` |
| 状态 | `agent-doc/tasks/{task_id}/status.md` |
| 关卡日志 | `agent-doc/tasks/{task_id}/gate-log.jsonl` |
| 关卡报告 | `agent-doc/tasks/{task_id}/reports/{gate}-{kind}-report.json` |
| 阶段模板 | `.ai-team/templates/stages/` |
| 校验脚本 | `tools/scripts/` |

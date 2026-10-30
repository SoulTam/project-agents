<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# Skills 与 Strategies 索引

> 按需查阅。Agent 在执行对应任务时再读取具体 skill / strategy 文件。

---

## 1. Skill 索引（`.ai-team/skills/`）

### 1.1 提示词工程
| Skill | 路径 |
|-------|------|
| prompt-engineering | `../skills/prompt-engineer/prompt-engineering/skill.md` |

### 1.2 PM
| Skill | 路径 |
|-------|------|
| project-status-assessment | `../skills/pm/project-status-assessment/skill.md` |
| task-decomposition | `../skills/pm/task-decomposition/skill.md` |
| technical-spike | `../skills/pm/technical-spike/technical-spike/skill.md` |
| result-first-definition | `../skills/pm/result-first-definition/skill.md` |
| design-doc-generation | `../skills/pm/design-doc-generation/skill.md` |
| global-execution-planning | `../skills/pm/global-execution-planning/skill.md` |
| plan-breakdown-tracking | `../skills/pm/plan-breakdown-tracking/skill.md` |
| result-rollback-verification | `../skills/pm/result-rollback-verification/skill.md` |

### 1.3 设计
| Skill | 路径 |
|-------|------|
| requirements-analysis | `../skills/requirements/requirements-analysis/skill.md` |
| architecture-design | `../skills/architecture/architecture-design/skill.md` |
| architectural-decision-record | `../skills/architecture/architectural-decision-record/architectural-decision-record/skill.md` |
| feature-design | `../skills/feature-design/feature-design/skill.md` |
| technical-design | `../skills/technical-design/technical-design/skill.md` |
| dev-planning | `../skills/dev-planning/dev-planning/skill.md` |
| task-assignment | `../skills/task-assignment/task-assignment/skill.md` |

### 1.4 代码开发
| Skill | 路径 |
|-------|------|
| java-development | `../skills/code-dev/java/java-development/skill.md` |
| frontend-development | `../skills/code-dev/frontend/frontend-development/skill.md` |
| ibmi-development | `../skills/code-dev/ibmi/ibmi-development/skill.md` |
| conventional-commit | `../skills/code-dev/conventional-commit/conventional-commit/skill.md` |
| cicd-workflow-design | `../skills/code-dev/devops/cicd-workflow-design/skill.md` |

### 1.5 测试与安全
| Skill | 路径 |
|-------|------|
| testing | `../skills/testing/testing/skill.md` |
| code-security | `../skills/testing/code-security/code-security/skill.md` |

### 1.6 知识与文档
| Skill | 路径 |
|-------|------|
| knowledge-management | `../skills/knowledge/knowledge-management/skill.md` |
| codebase-onboarding | `../skills/knowledge/codebase-onboarding/codebase-onboarding/skill.md` |
| word-export | `../skills/doc-output/word-export/skill.md` |
| pdf-export | `../skills/doc-output/pdf-export/skill.md` |
| excel-export | `../skills/doc-output/excel-export/skill.md` |
| ppt-export | `../skills/doc-output/ppt-export/skill.md` |

### 1.7 稽查与元
| Skill | 路径 |
|-------|------|
| compliance-audit | `../skills/audit/compliance-audit/skill.md` |
| make-skill-template | `../skills/meta/make-skill-template/skill.md` |
| microsoft-skill-creator | `../skills/meta/microsoft-skill-creator/skill.md` |
| create-agentsmd | `../skills/meta/create-agentsmd/skill.md` |

---

## 2. Strategy 与知识库索引（`.ai-team/knowledge-base/`）

| 文件 | 路径 |
|------|------|
| interface-selection-strategy | `../knowledge-base/api-strategies/interface-selection-strategy.md` |
| task-api-strategy | `../knowledge-base/api-strategies/task-api-strategy.md` |
| cloud-design-patterns | `../knowledge-base/patterns/cloud-design-patterns.md` |
| agent-governance-patterns | `../knowledge-base/patterns/agent-governance-patterns.md` |
| project-management-patterns | `../knowledge-base/patterns/project-management-patterns.md` |
| ibm-i-development-guide | `../knowledge-base/domain/ibm-i-development-guide.md` |
| domain-knowledge | `../knowledge-base/domain/domain-knowledge.md` |
| pm-experiences | `../knowledge-base/experiences/pm-experiences.md` |
| pm-decisions | `../knowledge-base/decisions/pm-decisions.md` |

---

## 3. 目录约定

| 目录 | 用途 |
|------|------|
| `.ai-team/agents/` | Agent 定义 |
| `.ai-team/skills/` | Skill 定义 |
| `.ai-team/rules/` | 全局规则（拆分文件，本目录） |
| `.ai-team/knowledge-base/` | 知识库 |
| `.ai-team/templates/` | Word/PDF/Excel/PPT 模板 |
| `agent-doc/` | 所有产出物根目录 |
| `agent-doc/plan/` | 执行计划 |
| `agent-doc/user-request/` | 用户请求记录 |
| `agent-doc/result-first/` | 结果先行终态描述 |
| `agent-doc/code/` | 代码产出物 |
| `agent-doc/ibmi/` | IBM i专属文档 |
| `agent-doc/ibmi/dds-spec/` | DDS规格书 |
| `agent-doc/ibmi/program-map/` | 程序调用关系 |
| `agent-doc/ibmi/screen-spec/` | 5250画面规格 |
| `agent-doc/ibmi/compile-order/` | 编译顺序 |
| `agent-doc/ibmi/library-structure/` | 库结构清单 |
| `agent-doc/{requirements,architecture,feature-design,technical-design,dev-plan,task,test,doc,devops,spike,knowledge,audit}/` | 各阶段产出 |

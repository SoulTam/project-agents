# Skills 与 Strategies 索引

> 按需查阅。Agent 在执行对应任务时再读取具体 skill / strategy 文件。

---

## 1. Skill 索引（`.ai-team/skills/`）

### 1.1 提示词工程
| Skill | 路径 |
|-------|------|
| prompt-engineering | `prompt-engineer/prompt-engineering/skill.md` |

### 1.2 PM
| Skill | 路径 |
|-------|------|
| project-status-assessment | `pm/project-status-assessment/skill.md` |
| task-decomposition | `pm/task-decomposition/skill.md` |
| technical-spike | `pm/technical-spike/technical-spike/skill.md` |
| result-first-definition | `pm/result-first-definition/skill.md` |
| design-doc-generation | `pm/design-doc-generation/skill.md` |
| global-execution-planning | `pm/global-execution-planning/skill.md` |
| plan-breakdown-tracking | `pm/plan-breakdown-tracking/skill.md` |
| result-rollback-verification | `pm/result-rollback-verification/skill.md` |

### 1.3 设计
| Skill | 路径 |
|-------|------|
| requirements-analysis | `requirements/requirements-analysis/skill.md` |
| architecture-design | `architecture/architecture-design/skill.md` |
| architectural-decision-record | `architecture/architectural-decision-record/architectural-decision-record/skill.md` |
| feature-design | `feature-design/feature-design/skill.md` |
| technical-design | `technical-design/technical-design/skill.md` |
| dev-planning | `dev-planning/dev-planning/skill.md` |
| task-assignment | `task-assignment/task-assignment/skill.md` |

### 1.4 代码开发
| Skill | 路径 |
|-------|------|
| java-development | `code-dev/java/java-development/skill.md` |
| frontend-development | `code-dev/frontend/frontend-development/skill.md` |
| ibmi-development | `code-dev/ibmi/ibmi-development/skill.md` |
| conventional-commit | `code-dev/conventional-commit/conventional-commit/skill.md` |
| cicd-workflow-design | `code-dev/devops/cicd-workflow-design/skill.md` |

### 1.5 测试与安全
| Skill | 路径 |
|-------|------|
| testing | `testing/testing/skill.md` |
| code-security | `testing/code-security/code-security/skill.md` |

### 1.6 知识与文档
| Skill | 路径 |
|-------|------|
| knowledge-management | `knowledge/knowledge-management/skill.md` |
| codebase-onboarding | `knowledge/codebase-onboarding/codebase-onboarding/skill.md` |
| word-export | `doc-output/word-export/skill.md` |
| pdf-export | `doc-output/pdf-export/skill.md` |
| excel-export | `doc-output/excel-export/skill.md` |
| ppt-export | `doc-output/ppt-export/skill.md` |

### 1.7 稽查与元
| Skill | 路径 |
|-------|------|
| compliance-audit | `audit/compliance-audit/skill.md` |
| make-skill-template | `meta/make-skill-template/skill.md` |
| microsoft-skill-creator | `meta/microsoft-skill-creator/skill.md` |
| create-agentsmd | `meta/create-agentsmd/skill.md` |

---

## 2. Strategy 与知识库索引（`.ai-team/knowledge-base/`）

| 文件 | 路径 |
|------|------|
| interface-selection-strategy | `api-strategies/interface-selection-strategy.md` |
| task-api-strategy | `api-strategies/task-api-strategy.md` |
| cloud-design-patterns | `patterns/cloud-design-patterns.md` |
| agent-governance-patterns | `patterns/agent-governance-patterns.md` |
| project-management-patterns | `patterns/project-management-patterns.md` |
| ibm-i-development-guide | `domain/ibm-i-development-guide.md` |
| domain-knowledge | `domain/domain-knowledge.md` |
| pm-experiences | `experiences/pm-experiences.md` |
| pm-decisions | `decisions/pm-decisions.md` |

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
| `agent-doc/{requirements,architecture,feature-design,technical-design,dev-plan,task,test,doc,devops,spike,knowledge,audit}/` | 各阶段产出 |

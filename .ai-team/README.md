# AI Development Team

## 快速开始

1. 复制`.ai-team/`目录和`.cursorrules`到项目根目录
2. 打开AI助手，输入任何请求
3. 系统会自动按照工作流程执行

## 核心原则

- **结果先行**：先定义终态，再推导路径
- **结果蓝图完整性**：结果蓝图中的信息必须是整个应用所需要的所有细节，不仅是核心或重点信息。结果蓝图是最终应用的终态，必须详细和完整，不能有缺漏
- **提示词增强**：所有请求先增强再执行
- **稽查前置**：所有执行先检查再进行

## 目录用途

本目录包含AI开发团队的纯配置文件，包括18个Agent定义、30个Skill定义、全局规则、知识库和文档模板。项目运行时产生的产出物（执行计划、用户请求记录、任务输出）存放在`agent-doc/`目录下。

## 工作流程

```
用户需求 → 稽查Agent实时监察（检查是否已增强）→ 提示词增强（展示给用户确认）→ PM Agent → 结果先行定义（调用相关Agent产出终态描述）→ 人类确认
    → 开发/设计文档输出（基于终态反推）→ 全局执行计划制定 → 计划拆分与进度表
    → 逐项执行子计划（每完成一项更新进度表）→ 终态回溯校验
    → 达到终态/修复偏差/询问人类
```

### 结果先行关键阶段

| 阶段 | 产出物 | 说明 |
|------|--------|------|
| 结果先行定义 | 结果蓝图（应用终态描述文档） | 定义应用完成时的完整样貌（前端页面、后端服务、数据层、业务逻辑），**必须覆盖全量细节，不能有缺漏** |
| 交叉维度完整性校验 | 校验结论 | 前端→后端→数据→业务全链路交叉校验，确保维度间一致无断裂 |
| 完整性自检 | 15项自检清单 | 逐项检查每个维度是否完整覆盖所有细节 |
| 人类确认 | - | 必须等待人类确认终态后才能继续 |
| 开发/设计文档输出 | 架构/技术/规范文档 | 基于终态反推设计文档 |
| 全局执行计划 | 全局计划文档 | 每个任务有明确依赖和产物 |
| 计划拆分与进度追踪 | 进度表 | 子计划环环相扣，每完成一项更新进度 |
| 终态回溯校验 | 校验报告 | 逐项比对实际产出与终态描述 |

## 详细规则

详见`.cursorrules`文件，包括：
- 角色识别（强制首先阅读）
- 强制前置检查（不可跳过）
- 输出规则
- 执行规则
- 提示词工程规则
- 代码开发规则
- 安全规则
- 稽查规则
- 知识库引用指引

## 目录结构

```
.ai-team/
├── README.md                    ← 本文件
├── agents/                      ← Agent定义文件
│   ├── prompt-engineer/agent.md ← 提示词工程师Agent
│   ├── pm/agent.md              ← 项目管理Agent
│   ├── requirements/agent.md    ← 需求分析Agent
│   ├── architecture/agent.md    ← 架构设计Agent
│   ├── feature-design/agent.md  ← 功能设计Agent
│   ├── technical-design/agent.md← 技术设计Agent
│   ├── dev-planning/agent.md    ← 开发计划Agent
│   ├── task-assignment/agent.md ← 任务分配Agent
│   ├── code-dev/
│   │   ├── java/agent.md        ← Java开发Agent
│   │   ├── frontend/agent.md    ← 前端开发Agent
│   │   ├── ibmi/agent.md        ← IBM i开发Agent
│   │   └── devops/agent.md      ← DevOps Agent
│   ├── testing/agent.md         ← 测试Agent
│   ├── knowledge/agent.md       ← 知识管理Agent
│   ├── doc-output/agent.md      ← 文档输出Agent
│   └── audit/agent.md           ← 稽查Agent
├── skills/                      ← Skill定义文件
│   ├── prompt-engineer/
│   │   └── prompt-engineering/skill.md
│   ├── pm/
│   │   ├── project-status-assessment/skill.md
│   │   ├── task-decomposition/skill.md
│   │   ├── technical-spike/technical-spike/skill.md
│   │   ├── result-first-definition/skill.md        ← 结果先行定义
│   │   ├── design-doc-generation/skill.md           ← 开发/设计文档输出
│   │   ├── global-execution-planning/skill.md       ← 全局执行计划制定
│   │   ├── plan-breakdown-tracking/skill.md         ← 计划拆分与进度追踪
│   │   └── result-rollback-verification/skill.md    ← 终态回溯校验
│   ├── requirements/requirements-analysis/skill.md
│   ├── architecture/
│   │   ├── architecture-design/skill.md
│   │   └── architectural-decision-record/architectural-decision-record/skill.md
│   ├── feature-design/feature-design/skill.md
│   ├── technical-design/technical-design/skill.md
│   ├── dev-planning/dev-planning/skill.md
│   ├── task-assignment/task-assignment/skill.md
│   ├── code-dev/
│   │   ├── java/java-development/skill.md
│   │   ├── frontend/frontend-development/skill.md
│   │   ├── ibmi/ibmi-development/skill.md
│   │   ├── conventional-commit/conventional-commit/skill.md
│   │   └── devops/cicd-workflow-design/skill.md
│   ├── testing/
│   │   ├── testing/skill.md
│   │   └── code-security/code-security/skill.md
│   ├── knowledge/
│   │   ├── knowledge-management/skill.md
│   │   └── codebase-onboarding/codebase-onboarding/skill.md
│   ├── doc-output/
│   │   ├── word-export/skill.md
│   │   ├── pdf-export/skill.md
│   │   ├── excel-export/skill.md
│   │   └── ppt-export/skill.md
│   └── audit/
│       └── compliance-audit/skill.md
├── rules/
│   └── global-rules.md          ← 全局规则（引用.cursorrules）
├── templates/                   ← 文档模板
│   ├── word/                    ← Word参考模板（reference.docx）
│   ├── pdf/                     ← LaTeX模板（template.tex）
│   ├── excel/                   ← Excel样式配置（style-config.json）
│   └── ppt/                     ← PPT模板（template.pptx）
└── knowledge-base/              ← 知识库
    ├── patterns/
    │   ├── cloud-design-patterns.md      ← 云设计模式（42种）
    │   ├── agent-governance-patterns.md  ← Agent治理模式
    │   └── project-management-patterns.md
    ├── experiences/
    │   └── pm-experiences.md
    ├── decisions/
    │   └── pm-decisions.md
    ├── api-strategies/
    │   ├── interface-selection-strategy.md
    │   └── task-api-strategy.md
    └── domain/
        └── domain-knowledge.md
```

项目根目录下的产出物目录（非团队配置，由Agent运行时自动生成）：

```
项目根目录/
└── agent-doc/                   ← 所有产出物根目录
    ├── plan/                      ← 执行计划
    ├── user-request/              ← 用户请求记录
    ├── result-first/              ← 结果先行产出（终态描述、校验报告）
    ├── requirements/              ← 需求规格文档
    ├── architecture/
    │   └── adr/                 ← 架构决策记录(ADR)
    ├── feature-design/            ← 功能设计文档
    ├── technical-design/          ← 技术设计文档
    ├── dev-plan/                  ← 开发计划文档
    ├── task/                      ← 任务分配文档
    ├── test/                      ← 测试文档
    ├── doc/                       ← 专业格式文档（Word/PDF/Excel/PPT）
    ├── devops/                    ← CI/CD工作流规范
    ├── spike/                     ← 技术调研文档
    ├── knowledge/                 ← 代码库知识文档
    ├── audit/                     ← 稽查报告
    ├── code/                      ← 代码产出物
    │   └── .github/workflows/   ← CI/CD工作流YAML
    └── prompt-engineer/           ← 提示词工程产出
```

## Agent清单（16个+2元Agent）

| Agent | 角色 | 关联Skill |
|-------|------|-----------|
| 提示词工程师Agent | 对用户请求进行提示词增强，增强后展示给用户确认 | prompt-engineering |
| PM Agent | 统筹项目全生命周期，**核心原则：结果先行** | project-status-assessment, task-decomposition, technical-spike, result-first-definition, design-doc-generation, global-execution-planning, plan-breakdown-tracking, result-rollback-verification |
| 需求分析Agent | 产出结构化需求文档，结果先行阶段产出需求终态描述 | requirements-analysis |
| 架构设计Agent | 设计系统整体架构，结果先行阶段产出架构终态描述 | architecture-design, architectural-decision-record |
| 功能设计Agent | 功能模块设计，结果先行阶段产出功能终态描述 | feature-design |
| 技术设计Agent | 技术实现方案，结果先行阶段产出技术终态描述 | technical-design |
| 开发计划Agent | 开发排期和里程碑 | dev-planning |
| 任务分配Agent | 拆解为具体任务 | task-assignment |
| Java开发Agent | Java功能代码实现 | java-development, conventional-commit |
| 前端开发Agent | 前端功能代码实现 | frontend-development, conventional-commit |
| IBM i开发Agent | IBM i(AS/400)功能代码实现（RPGLE/CLLE/DDS/SQL） | ibmi-development, conventional-commit |
| DevOps Agent | CI/CD和部署自动化 | cicd-workflow-design, conventional-commit |
| 测试Agent | 测试方案和用例 | testing, code-security |
| 知识管理Agent | 维护知识库 | knowledge-management, codebase-onboarding |
| 文档输出Agent | 专业格式文档转换 | word-export, pdf-export, excel-export, ppt-export |
| **稽查Agent** | **用户请求入口拦截** + 监察各Agent工作流程和产出物合规性，依据.ai-team/文档进行稽查，发现偏差发出整改要求 | **compliance-audit** |
| Custom Agent Foundry Agent | 设计和创建自定义Agent | - |
| Skill Creator Agent | 设计和创建Skill | - |

## Skill清单（30个）

| 类别 | Skill | 关键能力 |
|------|-------|----------|
| 提示词工程 | prompt-engineering | 意图识别、消歧澄清、上下文注入、约束补充、结构化重构 |
| 项目管理 | project-status-assessment | 扫描agent-doc目录评估项目状态、识别阻塞 |
| 项目管理 | task-decomposition | 结构化拆解(Epic→Feature→Task)、MoSCoW优先级 |
| 项目管理 | technical-spike | 时间盒技术调研、调研计划、决策建议 |
| **结果先行** | **result-first-definition** | **定义应用终态（前端/后端/数据/业务），人类确认后才继续** |
| **结果先行** | **design-doc-generation** | **基于终态反推架构/技术/规范文档** |
| **结果先行** | **global-execution-planning** | **制定环环相扣的全局执行计划** |
| **结果先行** | **plan-breakdown-tracking** | **拆分子计划+进度表，子计划必须关联不能脱节** |
| **结果先行** | **result-rollback-verification** | **终态回溯校验，偏差修复，错误闭环问人类** |
| 需求分析 | requirements-analysis | 提取功能/非功能需求、标注优先级、定义验收标准 |
| 架构设计 | architecture-design | 架构风格检测、技术选型、交叉关注点、数据架构、部署架构、ADR |
| 架构设计 | architectural-decision-record | ADR文档（上下文/决策/后果/替代方案） |
| 功能设计 | feature-design | 功能模块拆解、业务流程设计、业务规则定义 |
| 技术设计 | technical-design | 数据模型(ER)、接口类型决策、API定义、验收标准(Given-When-Then) |
| 开发计划 | dev-planning | 标准化计划模板、需求约束编码(REQ-/SEC-/CON-)、替代方案分析 |
| 任务分配 | task-assignment | 原子任务拆解、技术栈分类、依赖排序 |
| Java开发 | java-development | Spring Boot项目初始化(Spring Initializr+Docker Compose)、全栈开发 |
| 前端开发 | frontend-development | TypeScript全栈开发(类型/API/状态管理/组件/Hooks) |
| IBM i开发 | ibmi-development | ILE RPG自由格式、CL程序、DDS文件定义、嵌入式SQL、服务程序、子文件、编译命令 |
| 代码规范 | conventional-commit | Conventional Commits规范提交消息 |
| DevOps | cicd-workflow-design | GitHub Actions CI/CD工作流规范、质量门禁、安全扫描集成 |
| 测试 | testing | 测试方案、单元/集成测试、OWASP安全检查、Testcontainers |
| 安全 | code-security | OWASP Top 10检查、依赖漏洞扫描、敏感信息泄露检查、CodeQL集成 |
| 知识管理 | knowledge-management | 知识提取/匹配/更新/去重、Session计数管理 |
| 知识管理 | codebase-onboarding | 代码库梳理(7份标准文档)、技术栈检测、架构分析 |
| 文档输出 | word-export | Markdown转Word(Pandoc+reference.docx模板) |
| 文档输出 | pdf-export | Markdown转PDF(Pandoc+XeLaTeX+template.tex中文支持) |
| 文档输出 | excel-export | Markdown转Excel(openpyxl+style-config.json样式) |
| 文档输出 | ppt-export | Markdown转PPT(python-pptx+template.pptx模板精简要点) |
| **稽查** | **compliance-audit** | **合规性检查、流程监察、产出物格式验证、整改要求发出、整改结果验证** |

## 迁移到其他项目

### 步骤

1. 复制 `.ai-team/` 目录到目标项目根目录
2. 复制 `.cursorrules` 到目标项目根目录
3. 在目标项目 `.gitignore` 中添加：
   ```
   agent-doc/
   ```
4. 打开AI助手，AI团队配置自动生效

### 验证

在AI助手中输入任何请求，系统应自动按照工作流程执行。

### 适配其他AI助手

- **GitHub Copilot**：将`.cursorrules`内容复制到`.github/copilot-instructions.md`
- **Cline**：将`.cursorrules`内容复制到`.clinerules`
- **Claude Code**：不建议直接复制`.cursorrules`到`CLAUDE.md`（Claude Code 会因格式/长度不合规而重写），应按以下方式适配：
  1. 在项目根目录创建`CLAUDE.md`，使用`@`语法导入`.cursorrules`：
     ```markdown
     @.cursorrules
     ```
  2. 或采用模块化拆分：在`.claude/rules/`目录下按主题创建规则文件，将`.cursorrules`中的各章节拆分为独立`.md`文件（如`agent-roles.md`、`output-rules.md`、`code-rules.md`等），每个文件建议不超过200行
  3. 需要按文件路径限定范围的规则，在规则文件头部添加YAML frontmatter：
     ```yaml
     ---
     paths:
       - "src/**/*.java"
     ---
     ```
- **OpenAI Codex CLI**：将`.cursorrules`内容复制到`codex.md`（项目根目录），或拆分到`.codex/instructions.md`：
  ```bash
  # 方式1：直接复制
  cp .cursorrules codex.md

  # 方式2：模块化（推荐）
  mkdir -p .codex
  cp .cursorrules .codex/instructions.md
  ```
- **OpenCode**：将`.cursorrules`内容复制到项目根目录的`.opencode/instructions.md`：
  ```bash
  mkdir -p .opencode
  cp .cursorrules .opencode/instructions.md
  ```
  或在`.opencode.json`中通过`instructions`字段引用：
  ```json
  {
    "instructions": ".cursorrules"
  }
  ```

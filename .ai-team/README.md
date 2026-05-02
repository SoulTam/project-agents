# AI Development Team

## 目录用途

本目录包含AI开发团队的纯配置文件，包括14个Agent定义、23个Skill定义、全局规则、知识库和文档模板。项目运行时产生的产出物（执行计划、用户请求记录、任务输出）存放在项目根目录下，不在本目录中。

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
│   └── doc-output/agent.md      ← 文档输出Agent
├── skills/                      ← Skill定义文件
│   ├── prompt-engineer/agent.md ← 提示词工程师Agent
│   ├── pm/
│   │   ├── project-status-assessment/skill.md
│   │   ├── task-decomposition/skill.md
│   │   └── technical-spike/technical-spike/skill.md
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
│   └── doc-output/
│       ├── word-export/skill.md
│       ├── pdf-export/skill.md
│       ├── excel-export/skill.md
│       └── ppt-export/skill.md
├── rules/
│   └── global-rules.md          ← 全局规则
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
├── plan/                        ← 执行计划
├── user-request/                ← 用户请求记录
└── output/                      ← 任务输出产物
    ├── prompt-engineer/           ← 提示词增强记录
    ├── requirements/
    ├── architecture/
    │   └── adr/                 ← 架构决策记录(ADR)
    ├── feature-design/
    ├── technical-design/
    ├── dev-plan/
    ├── task/
    ├── code/
    │   └── .github/workflows/   ← CI/CD工作流YAML
    ├── test/
    ├── doc/                     ← 专业格式文档（Word/PDF/Excel/PPT）
    ├── devops/                  ← CI/CD工作流规范
    ├── spike/                   ← 技术调研文档
    └── knowledge/               ← 代码库知识文档
```

## Agent清单（15个）

| Agent | 角色 | 关联Skill |
|-------|------|-----------|
| 提示词工程师Agent | 对用户请求进行提示词增强 | prompt-engineering |
| PM Agent | 统筹项目全生命周期 | project-status-assessment, task-decomposition, technical-spike |
| 需求分析Agent | 产出结构化需求文档 | requirements-analysis |
| 架构设计Agent | 设计系统整体架构 | architecture-design, architectural-decision-record |
| 功能设计Agent | 功能模块设计 | feature-design |
| 技术设计Agent | 技术实现方案 | technical-design |
| 开发计划Agent | 开发排期和里程碑 | dev-planning |
| 任务分配Agent | 拆解为具体任务 | task-assignment |
| Java开发Agent | Java功能代码实现 | java-development, conventional-commit |
| 前端开发Agent | 前端功能代码实现 | frontend-development, conventional-commit |
| IBM i开发Agent | IBM i(AS/400)功能代码实现（RPGLE/CLLE/DDS/SQL） | ibmi-development, conventional-commit |
| DevOps Agent | CI/CD和部署自动化 | cicd-workflow-design, conventional-commit |
| 测试Agent | 测试方案和用例 | testing, code-security |
| 知识管理Agent | 维护知识库 | knowledge-management, codebase-onboarding |
| 文档输出Agent | 专业格式文档转换 | word-export, pdf-export, excel-export, ppt-export |

## Skill清单（24个）

| 类别 | Skill | 关键能力 |
|------|-------|----------|
| 提示词工程 | prompt-engineering | 意图识别、消歧澄清、上下文注入、约束补充、结构化重构 |
| 项目管理 | project-status-assessment | 扫描output目录评估项目状态、识别阻塞 |
| 项目管理 | task-decomposition | 结构化拆解(Epic→Feature→Task)、MoSCoW优先级 |
| 项目管理 | technical-spike | 时间盒技术调研、调研计划、决策建议 |
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

## 迁移到其他项目

### 步骤

1. 复制 `.ai-team/` 目录到目标项目根目录
2. 复制 `.cursorrules` 到目标项目根目录
3. 在目标项目 `.gitignore` 中添加：
   ```
   output/
   plan/
   user-request/
   ```
4. 打开VSCode，AI团队配置自动生效

### 验证

在Cursor中输入"当前项目状态"，PM Agent正确响应则配置成功。

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

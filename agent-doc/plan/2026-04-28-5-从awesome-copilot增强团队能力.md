# 从 awesome-copilot 增强 AI 团队能力

## 背景

从 [github/awesome-copilot](https://github.com/github/awesome-copilot) 仓库中筛选适用于我们 AI 开发团队的 skills，升级已有 skills 并拉取新 skills，增强团队整体能力。

## 筛选原则

1. 与我们团队 Java/Spring Boot + 前端技术栈相关
2. 与企业级软件开发流程相关
3. 填补我们团队当前能力空白
4. 可适配到我们的 Agent-Skill 架构体系

## 一、升级现有 Skill（6个）

### 1.1 java-development ← create-spring-boot-java-project

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 项目初始化 | 仅描述"创建标准Spring Boot项目结构" | 增加Spring Initializr下载、Docker Compose（Redis/PostgreSQL/MongoDB）、springdoc-openapi集成、ArchUnit架构测试 |
| 依赖管理 | 无 | 增加标准依赖清单：lombok, web, data-jpa, data-redis, data-mongodb, validation, cache, testcontainers |
| 配置文件 | 仅提到"配置类" | 增加application.properties标准配置模板（SpringDoc/Redis/JPA/MongoDB） |
| 容器化 | 无 | 增加docker-compose.yaml及.gitignore |

### 1.2 architecture-design ← architecture-blueprint-generator

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 架构分析 | 仅"分析需求规格" | 增加：架构风格自动检测、技术栈检测、架构原则文档化 |
| 架构可视化 | 仅"Mermaid架构关系图" | 增加：多层级C4/UML图（系统总览/组件交互/数据流）、文本化架构描述备选 |
| 交叉关注点 | 无 | 增加：认证授权、错误处理与韧性、日志监控、校验、配置管理的实现模式文档 |
| 数据架构 | 无 | 增加：领域模型结构、实体关系、数据访问模式、缓存策略 |
| 服务通信 | 无 | 增加：服务边界定义、同步/异步通信模式、API版本策略 |
| 部署架构 | 仅"部署方案设计" | 增加：部署拓扑、容器化编排、云服务集成 |
| 测试架构 | 无 | 增加：测试策略、测试边界模式、测试数据策略 |
| 扩展演进 | 无 | 增加：功能添加模式、修改模式、集成模式、架构治理 |

### 1.3 dev-planning ← create-implementation-plan

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 计划格式 | 简单阶段表格 | 增加标准化模板：front matter元数据、需求与约束清单（REQ-/SEC-/CON-标识）、替代方案分析、依赖清单、风险与假设、文件影响清单、测试策略 |
| 任务追踪 | 无 | 增加每个任务的状态标记（✅完成/待做）和完成日期 |
| 计划命名 | dev-plan-{date}.md | 增加：{purpose}-{component}-{version}.md 规范命名 |

### 1.4 testing ← agent-owasp-compliance + codeql

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 安全测试 | 无 | 增加：OWASP ASI Top 10 安全风险检查、CodeQL代码扫描集成建议 |
| 测试环境 | 无 | 增加：Testcontainers集成测试环境建议 |
| 覆盖维度 | 仅功能测试 | 增加：安全性验证维度、性能测试建议 |

### 1.5 task-decomposition ← breakdown-epic-pm

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 任务拆解方式 | 关键词匹配 | 增加：结构化拆解框架（Epic→Feature→Task→Subtask）、验收标准随任务一起定义 |
| 优先级策略 | 无 | 增加：MoSCoW优先级分类（Must/Should/Could/Wont） |

### 1.6 technical-design ← create-specification

| 升级项 | 原有 | 增强内容 |
|--------|------|----------|
| 文档结构 | 简单步骤式 | 增加标准化模板：术语定义、需求/约束/指南分类编码（REQ-/SEC-/CON-/GUD-/PAT-）、接口与数据契约、验收标准（Given-When-Then格式）、测试自动化策略、替代方案分析、验证标准 |
| AI可读性 | 无 | 增加：无歧义语言、自包含文档、机器可解析结构 |

## 二、新增 Skill（5个）

### 2.1 conventional-commit（代码开发Agent共用）

- 来源：awesome-copilot/skills/conventional-commit
- 适用Agent：Java开发Agent、前端开发Agent
- 功能：规范Git提交消息格式，遵循Conventional Commits规范
- 产出：标准化的commit message（type(scope): description格式）

### 2.2 code-security（测试Agent）

- 来源：awesome-copilot/skills/codeql + agent-owasp-compliance
- 适用Agent：测试Agent
- 功能：代码安全扫描和OWASP合规检查
- 产出：安全检查报告，包含漏洞清单和修复建议

### 2.3 architectural-decision-record（架构设计Agent）

- 来源：awesome-copilot/skills/create-architectural-decision-record
- 适用Agent：架构设计Agent
- 功能：为关键架构决策创建ADR文档
- 产出：结构化ADR文档（上下文/决策/后果/替代方案/实施说明）

### 2.4 codebase-onboarding（知识管理Agent）

- 来源：awesome-copilot/skills/acquire-codebase-knowledge
- 适用Agent：知识管理Agent
- 功能：快速梳理和文档化现有代码库，生成7份标准文档
- 产出：STACK.md, STRUCTURE.md, ARCHITECTURE.md, CONVENTIONS.md, INTEGRATIONS.md, TESTING.md, CONCERNS.md

### 2.5 technical-spike（PM Agent）

- 来源：awesome-copilot/skills/create-technical-spike
- 适用Agent：PM Agent
- 功能：创建时间盒限定的技术调研文档，在开发前解决关键技术决策
- 产出：结构化技术调研文档（调研问题/调研计划/调研发现/决策建议）

## 三、新增知识库文档（2个）

### 3.1 cloud-design-patterns

- 来源：awesome-copilot/skills/cloud-design-patterns
- 路径：.ai-team/knowledge-base/patterns/cloud-design-patterns.md
- 内容：42种云设计模式（可靠性9种/性能10种/消息7种/架构7种/部署5种/安全3种/事件驱动1种）

### 3.2 agent-governance-patterns

- 来源：awesome-copilot/skills/agent-governance
- 路径：.ai-team/knowledge-base/patterns/agent-governance-patterns.md
- 内容：Agent治理模式（策略治理/语义意图分类/工具级治理装饰器/信任评分/审计追踪）

## 四、新增 Agent（1个）

### 4.1 DevOps Agent

- 路径：.ai-team/agents/code-dev/devops/agent.md
- 角色：CI/CD流程设计、GitHub Actions工作流规范、部署自动化
- 上游：技术设计Agent、开发计划Agent
- 下游：测试Agent
- 关联Skill：cicd-workflow-design

### 4.2 cicd-workflow-design Skill

- 来源：awesome-copilot/skills/create-github-action-workflow-specification
- 路径：.ai-team/skills/code-dev/devops/cicd-workflow-design/skill.md
- 功能：创建GitHub Actions CI/CD工作流规范文档

## 五、需更新的配置文件

1. `.cursorrules` - 更新Agent表、Skill引用表、目录约定
2. `.ai-team/rules/global-rules.md` - 更新Agent表、协作图、Skill引用表
3. `.ai-team/README.md` - 更新目录结构、Agent/Skill清单

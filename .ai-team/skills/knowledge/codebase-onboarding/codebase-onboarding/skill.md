---
name: codebase-onboarding
description: '代码库梳理(7份标准文档)、技术栈检测和架构分析。当需要快速了解代码库结构或生成项目入门文档时使用。'
---

# codebase-onboarding

## 适用Agent
知识管理Agent

## 触发条件
PM Agent指定对现有代码库进行知识梳理时触发，或首次在已有项目中启动AI团队时触发。

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 扫描项目结构 | 扫描项目根目录，识别：构建文件（pom.xml/package.json/build.gradle）、配置文件（application.yml/.env.example）、入口文件、目录结构，记录到临时扫描结果 |
| 2 | 读取项目意图文档 | 搜索并读取PRD/README/ROADMAP/SPEC/DESIGN文件，理解项目声明的目标和架构意图 |
| 3 | 生成STACK.md | 分析技术栈，以表格列出：语言及版本、运行时、框架（含版本）、所有依赖（dependencies vs devDependencies）、构建工具、包管理器。写入`agent-doc/knowledge/STACK.md` |
| 4 | 生成STRUCTURE.md | 文档化目录布局，以树状图列出目录结构，标注入口文件和关键文件。写入`agent-doc/knowledge/STRUCTURE.md` |
| 5 | 生成ARCHITECTURE.md | 分析架构层次和模式，文档化：分层结构、依赖方向、组件边界、通信机制。写入`agent-doc/knowledge/ARCHITECTURE.md` |
| 6 | 生成CONVENTIONS.md | 文档化编码规范，包含：命名规则、格式化规则、错误处理模式、导入规则、日志规范。写入`agent-doc/knowledge/CONVENTIONS.md` |
| 7 | 生成INTEGRATIONS.md | 文档化外部集成，以表格列出：外部系统、集成类型、数据格式、认证方式。写入`agent-doc/knowledge/INTEGRATIONS.md` |
| 8 | 生成TESTING.md | 文档化测试架构，包含：测试框架、文件组织、mock策略、覆盖率要求。写入`agent-doc/knowledge/TESTING.md` |
| 9 | 生成CONCERNS.md | 识别并记录技术债和风险，以表格列出：问题类别（技术债/安全风险/性能瓶颈）、描述、严重程度、建议修复方案。写入`agent-doc/knowledge/CONCERNS.md` |
| 10 | 验证文档 | 验证7份文档：每份必须包含evidence引用列表（关联具体文件路径）、未确定项标记为[TODO]、需团队确认项标记为[ASK USER] |
| 11 | 输出摘要 | 向用户展示7份文档摘要，列出所有[ASK USER]问题编号，标注意图与现实的偏差 |

## 注意事项

| 场景 | 注意点 |
|------|--------|
| Monorepo | 根package.json可能无源码，检查workspaces/packages/apps/，每个workspace单独映射 |
| 过时README | README可能描述预期架构而非当前架构，必须交叉验证实际文件结构 |
| TypeScript路径别名 | tsconfig.json的paths配置意味着`@/foo`不直接映射文件系统，需映射别名到实际路径 |
| 生成/编译输出 | 不记录dist/build/generated/.next/out/__pycache__/中的模式，仅记录源码规范 |
| .env.example | .env.example暴露所需环境变量配置，但敏感值不提交 |
| devDependencies | 仅dependencies运行在生产环境，lint/formatter/test框架单独记录为dev工具 |
| 高变更文件 | git历史中变更最频繁的文件可能隐藏复杂性，记录在CONCERNS.md |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 产出文件 | 必须产出7份文档：STACK/STRUCTURE/ARCHITECTURE/CONVENTIONS/INTEGRATIONS/TESTING/CONCERNS |
| 2 | 证据链 | 每个声明必须可追溯到源文件、配置或终端输出 |
| 3 | 未知标记 | 无法从代码确定的内容标记[TODO] |
| 4 | 确认标记 | 需要团队意图确认的内容标记[ASK USER] |
| 5 | 格式 | 所有文档使用Markdown格式 |

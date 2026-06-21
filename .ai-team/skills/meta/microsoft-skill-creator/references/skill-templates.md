<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# Skill Templates

适用于不同类型Microsoft技术的即用型模板。

## CLI替代方案
所有模板使用MCP工具调用（如`microsoft_docs_search`、`microsoft_docs_fetch`、`microsoft_code_sample_search`）。如果Learn MCP服务器不可用，替换为CLI等效命令：

| MCP工具 | CLI命令 |
|----------|---------|
| `microsoft_docs_search(query: "...")` | `mslearn search "..."` |
| `microsoft_code_sample_search(query: "...", language: "...")` | `mslearn code-search "..." --language ...` |
| `microsoft_docs_fetch(url: "...")` | `mslearn fetch "..."` |

---

## Template 1: SDK/Library Skill
适用于客户端库、SDK和编程框架。

```markdown
---
name: {sdk-name}
description: {做什么}. 当Agent需要{主要任务}时使用{技术上下文}. 支持{语言/平台}.
---

# {SDK Name}
{一段话：它是什么，为什么存在，何时使用}

## 安装
{支持语言的包管理器命令}

## 核心概念
{3-5个核心概念，每个最多一段}

### {概念1}
{简要解释}

### {概念2}
{简要解释}

## 快速开始
{最小工作示例 - 如果<30行则内联，否则引用sample_codes/}

## 常见模式

### {模式1：如"基本CRUD"}
`{language}`
{code}
`

### {模式2：如"错误处理"}
`{language}`
{code}
`

## API快速参考
| 类/方法 | 目的 | 示例 |
|---------|------|------|
| {name} | {做什么} | `{usage}` |

完整API文档：
- `microsoft_docs_search(query="{sdk} {class} API reference")`
- `microsoft_docs_fetch(url="{url}")`

## 最佳实践
- **推荐**：{建议}
- **推荐**：{建议}
- **避免**：{反模式}

详见[best-practices.md](references/best-practices.md)

## 了解更多
| 主题 | 如何查找 |
|------|----------|
| {高级主题1} | `microsoft_docs_search(query="{sdk} {topic}")` |
| {高级主题2} | `microsoft_docs_fetch(url="{url}")` |
| {代码示例} | `microsoft_code_sample_search(query="{sdk} {scenario}", language="{lang}")` |
```

---

## Template 2: Azure Service Skill
适用于Azure服务和云资源。

```markdown
---
name: {service-name}
description: 使用{Azure服务}. 当Agent需要{主要能力}时使用. 涵盖配置、SDK使用.
---

# {Azure Service Name}
{一段话：服务做什么，主要用例}

## 概述
- **类别**：{计算/存储/AI/网络等}
- **关键能力**：{主要价值主张}
- **何时使用**：{场景}

## 入门

### 前置条件
- Azure订阅
- {其他要求}

### 配置
{创建资源的CLI/Portal/Bicep代码片段}

## SDK使用（{语言}）

### 安装
`{package install command}`

### 认证
`{language}`
{auth code pattern}
`

### 基本操作
`{language}`
{CRUD或主要操作}
`

## 关键配置
| 设置 | 目的 | 默认值 |
|------|------|--------|
| {setting} | {控制什么} | {value} |

## 定价与限制
- **定价模型**：{消费/分层等}
- **关键限制**：{重要配额}

当前定价：`microsoft_docs_search(query="{service} pricing")`

## 常见模式

### {模式1}
{代码或配置}

### {模式2}
{代码或配置}

## 故障排除
| 问题 | 解决方案 |
|------|----------|
| {常见错误} | {修复方法} |

更多问题：`microsoft_docs_search(query="{service} troubleshoot {symptom}")`

## 了解更多
| 主题 | 如何查找 |
|------|----------|
| REST API | `microsoft_docs_fetch(url="{url}")` |
| ARM/Bicep | `microsoft_docs_search(query="{service} bicep template")` |
| 安全 | `microsoft_docs_search(query="{service} security best practices")` |
```

---

## Template 3: Framework/Platform Skill
适用于开发框架和平台（如ASP.NET、MAUI、Blazor）。

```markdown
---
name: {framework-name}
description: 使用{Framework}构建{应用类型}. 当Agent需要创建、修改或调试{framework}应用时使用.
---

# {Framework Name}
{一段话：它是什么，用它构建什么，为什么选择它}

## 项目结构
`
{typical-project}/
├── {folder}/    # {目的}
├── {file}       # {目的}
└── {file}       # {目的}
`

## 入门

### 创建新项目
`bash
{CLI命令创建脚手架}
`

### 项目配置
{要配置的关键文件及其控制内容}

## 核心概念

### {概念1：如"组件"}
{解释和最小代码示例}

### {概念2：如"路由"}
{解释和最小代码示例}

### {概念3：如"状态管理"}
{解释和最小代码示例}

## 常见模式

### {模式1}
`{language}`
{code}
`

### {模式2}
`{language}`
{code}
`

## 配置选项
| 设置 | 文件 | 目的 |
|------|------|------|
| {setting} | {file} | {做什么} |

## 部署
{简要部署指引或参考}

详细部署：`microsoft_docs_search(query="{framework} deploy {target}")`

## 了解更多
| 主题 | 如何查找 |
|------|----------|
| {高级功能} | `microsoft_docs_search(query="{framework} {feature}")` |
| {集成} | `microsoft_docs_fetch(url="{url}")` |
| {示例} | `microsoft_code_sample_search(query="{framework} {scenario}")` |
```

---

## Template 4: API/Protocol Skill
适用于API、协议和规范（如Microsoft Graph、OOXML）。

```markdown
---
name: {api-name}
description: 与{API/协议}交互. 当Agent需要{主要操作}时使用. 涵盖认证、端点和常见操作.
---

# {API/Protocol Name}
{一段话：它提供对什么的访问，主要用例}

## 认证
{认证方法和代码模式}

## 基本配置
- **Base URL**：`{url}`
- **版本**：`{version}`
- **格式**：{JSON/XML等}

## 常见端点/操作

### {操作1：如"列出项目"}
`
{HTTP方法} {endpoint}
`
`{language}`
{SDK代码}
`

### {操作2：如"创建项目"}
`
{HTTP方法} {endpoint}
`
`{language}`
{SDK代码}
`

## 请求/响应模式

### 分页
{如何处理分页}

### 错误处理
{错误格式和常见代码}

## 快速参考
| 操作 | 端点/方法 | 备注 |
|------|-----------|------|
| {op} | `{endpoint}` | {note} |

## 权限/范围
| 操作 | 所需权限 |
|------|----------|
| {op} | `{permission}` |

## 了解更多
| 主题 | 如何查找 |
|------|----------|
| 完整端点参考 | `microsoft_docs_fetch(url="{url}")` |
| 权限 | `microsoft_docs_search(query="{api} permissions {resource}")` |
| SDK | `microsoft_docs_search(query="{api} SDK {language}")` |
```

---

## 模板选择指南

| 技术类型 | 模板 | 示例 |
|----------|------|------|
| 客户端库、NuGet/npm包 | SDK/库 | Semantic Kernel、Azure SDK、MSAL |
| Azure资源 | Azure服务 | Cosmos DB、Azure Functions、App Service |
| 应用开发框架 | 框架/平台 | ASP.NET Core、Blazor、MAUI |
| REST API、协议、规范 | API/协议 | Microsoft Graph、OOXML、FHIR |

## 自定义指南
模板是起点，可通过以下方式自定义：
1. **添加章节** - 为技术的独特方面添加
2. **移除章节** - 删除不适用的
3. **调整深度** - 根据复杂度增减概念
4. **添加参考文件** - 为skill.md中放不下的详细内容添加
5. **添加sample_codes/** - 为内联片段之外的工作示例添加

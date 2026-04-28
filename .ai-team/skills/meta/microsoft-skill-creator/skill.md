---
name: microsoft-skill-creator
description: '为Microsoft技术创建混合Skill，本地存储核心知识同时支持动态深度调研。当需要创建Azure、.NET、M365等Microsoft技术相关的Skill时使用。'
---

# microsoft-skill-creator

## 适用Agent
Skill Creator Agent

## 触发条件
当用户想要创建关于Microsoft技术（Azure、.NET、M365、VS Code、Bicep等）的Skill时触发。深入调研主题，然后生成混合Skill——在本地存储核心知识，同时启用动态深度调研。

## 概述
为Microsoft技术创建混合Skill，在本地存储核心知识，同时通过Learn MCP查找获取更深层细节。

## 关于Skills
Skills是扩展Agent能力的模块化包，将专业知识和工作流注入通用Agent，使其成为特定领域的专家。

### Skill结构
```
skill-name/
├── skill.md          # 必需 - Frontmatter（name、description）+ 指令
├── references/       # 按需加载到上下文的文档
├── sample_codes/     # 工作代码示例
└── assets/           # 输出中使用的文件（模板等）
```

### 关键原则
- **Frontmatter至关重要**：`name`和`description`决定Skill何时触发——要清晰全面
- **简洁是关键**：只包含Agent不知道的内容；上下文窗口是共享的
- **不重复**：信息存在于skill.md或参考文件中，不要两者都有

## Learn MCP工具

| 工具 | 目的 | 何时使用 |
|------|------|----------|
| `microsoft_docs_search` | 搜索官方文档 | 初步发现、查找主题 |
| `microsoft_docs_fetch` | 获取完整页面内容 | 深入了解重要页面 |
| `microsoft_code_sample_search` | 查找代码示例 | 获取实现模式 |

### CLI替代方案
如果Learn MCP服务器不可用，使用`mslearn` CLI：

```bash
# 直接运行（无需安装）
npx @microsoft/learn-cli search "semantic kernel overview"

# 或全局安装后运行
npm install -g @microsoft/learn-cli
mslearn search "semantic kernel overview"
```

| MCP工具 | CLI命令 |
|----------|---------|
| `microsoft_docs_search(query: "...")` | `mslearn search "..."` |
| `microsoft_code_sample_search(query: "...", language: "...")` | `mslearn code-search "..." --language ...` |
| `microsoft_docs_fetch(url: "...")` | `mslearn fetch "..."` |

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 主题调研 | 使用Learn MCP工具分三个阶段深入理解：范围发现→核心内容→深度探索 |
| 2 | 用户确认 | 向用户展示发现并确认重点领域、主要任务和编程语言优先级 |
| 3 | 生成Skill | 使用skill-templates.md中的适当模板生成Skill文件 |
| 4 | 内容平衡 | 决定哪些内容本地存储（基础性、频繁访问、稳定），哪些保持动态（穷举性、版本特定、情境性） |
| 5 | 验证 | 检查本地内容是否足够完成常见任务、搜索查询是否返回有用结果、代码示例是否可运行 |

## 调研过程

### 阶段1 - 范围发现
```
microsoft_docs_search(query="{technology} overview what is")
microsoft_docs_search(query="{technology} concepts architecture")
microsoft_docs_search(query="{technology} getting started tutorial")
```

### 阶段2 - 核心内容
```
microsoft_docs_fetch(url="...")  # 获取阶段1的页面
microsoft_code_sample_search(query="{technology}", language="{lang}")
```

### 阶段3 - 深度
```
microsoft_docs_search(query="{technology} best practices")
microsoft_docs_search(query="{technology} troubleshooting errors")
```

### 调研检查清单
- [ ] 能用一段话解释该技术做什么
- [ ] 识别了3-5个关键概念
- [ ] 有基本用法的工作代码
- [ ] 知道最常见的API模式
- [ ] 有深入主题的搜索查询

## 常见调研模式

### SDK/库
```
"{name} overview" → 目的、架构
"{name} getting started quickstart" → 设置步骤
"{name} API reference" → 核心类/方法
"{name} samples examples" → 代码模式
"{name} best practices performance" → 优化
```

### Azure服务
```
"{service} overview features" → 功能
"{service} quickstart {language}" → 设置代码
"{service} REST API reference" → 端点
"{service} SDK {language}" → 客户端库
"{service} pricing limits quotas" → 约束
```

### 框架/平台
```
"{framework} architecture concepts" → 心智模型
"{framework} project structure" → 约定
"{framework} tutorial walkthrough" → 端到端流程
"{framework} configuration options" → 自定义
```

## Skill模板选择

| 技术类型 | 模板 | 示例 |
|----------|------|------|
| 客户端库、NuGet/npm包 | SDK/库 | Semantic Kernel、Azure SDK、MSAL |
| Azure资源 | Azure服务 | Cosmos DB、Azure Functions、App Service |
| 应用开发框架 | 框架/平台 | ASP.NET Core、Blazor、MAUI |
| REST API、协议 | API/协议 | Microsoft Graph、OOXML、FHIR |

## 内容平衡指南

| 内容类型 | 本地 | 动态 |
|----------|------|------|
| 核心概念（3-5个） | ✅ 完整 | |
| Hello World代码 | ✅ 完整 | |
| 常见模式（3-5个） | ✅ 完整 | |
| Top API方法 | 签名+示例 | 通过fetch获取完整文档 |
| 最佳实践 | Top 5要点 | 搜索更多 |
| 故障排除 | | 搜索查询 |
| 完整API参考 | | 文档链接 |

## 生成的Skill目录结构

```
{skill-name}/
├── skill.md           # 核心知识 + Learn MCP指引
├── references/        # 详细本地文档（如需要）
└── sample_codes/      # 工作代码示例
    ├── getting-started/
    └── common-patterns/
```

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 文件位置 | `.ai-team/skills/{category}/{skill-name}/skill.md` |
| 2 | Frontmatter | 必须包含`name`和`description` |
| 3 | 内容深度 | 核心概念3-5个，常见模式3-5个，可运行代码示例 |
| 4 | MCP集成 | 包含Learn MCP工具搜索查询指引 |
| 5 | CLI替代 | 包含mslearn CLI命令作为MCP不可用时的回退 |
| 6 | 代码示例 | 必须可运行，无错误 |

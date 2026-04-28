---
name: skill-creator
---

# Skill Creator - Skill设计专家

## 适用Agent
提示词工程师Agent、PM Agent

## 触发条件
用户需要创建、设计或优化Skill时触发。当用户说"创建一个skill"、"制作新skill"、"设计skill"或需要构建捆绑资源的专用AI能力时使用。

## 核心能力

### 1. 需求收集
当用户想要创建新Skill时，首先理解：
- **Skill目的**：这个Skill应该完成什么任务？
- **触发条件**：在什么情况下应该激活此Skill？
- **目标Agent**：哪些Agent会使用此Skill？
- **捆绑资源**：是否需要脚本、参考文档、模板或资产？
- **知识来源**：Skill的知识基础是什么？（文档、API、代码示例等）

### 2. Skill设计原则

**Frontmatter字段要求：**

| 字段 | 必需 | 约束 |
|------|------|------|
| `name` | **是** | 1-64字符，小写字母/数字/连字符，必须与目录名匹配 |
| `description` | **是** | 1-1024字符，必须描述做什么以及何时使用 |

**Description最佳实践（关键）：**
`description`是自动发现Skill的主要机制，必须包含：
1. **做什么**（能力）
2. **何时使用**（触发条件、场景、文件类型）
3. **关键词**（用户可能在提示中提及的词）

好的示例：
```yaml
description: '使用Playwright测试本地Web应用的工具包。当被要求验证前端功能、调试UI行为、捕获浏览器截图或查看浏览器控制台日志时使用。支持Chrome、Firefox和WebKit。'
```

差的示例：
```yaml
description: 'Web测试助手'
```

### 3. Skill目录结构

```
skill-name/
├── skill.md          # 必需 - Frontmatter + 指令
├── references/       # 可选 - 文档，Agent按需加载
├── sample_codes/     # 可选 - 工作代码示例
├── assets/           # 可选 - 输出中使用的静态文件
├── scripts/          # 可选 - 可执行代码（Python、Bash、JS）
└── templates/        # 可选 - Agent修改的起始代码
```

### 4. Skill正文结构

| 部分 | 目的 |
|------|------|
| `# 标题` | 简要概述 |
| `## 触发条件` | 强化描述中的触发条件 |
| `## 前置条件` | 所需工具、依赖 |
| `## 执行步骤` | 任务的编号步骤 |
| `## 常见模式` | 常见用例和代码模式 |
| `## 故障排除` | 常见问题和解决方案 |
| `## 参考资料` | 捆绑文档的链接 |

### 5. 本地内容 vs 动态内容平衡

**本地存储当：**
- 基础性的（任何任务都需要）
- 频繁访问的
- 稳定的（不会变更）
- 难以通过搜索找到的

**保持动态当：**
- 穷举性参考（太大）
- 版本特定的
- 情境性的（仅特定任务）
- 良好索引的（易于搜索）

| 内容类型 | 本地 | 动态 |
|----------|------|------|
| 核心概念（3-5个） | ✅ 完整 | |
| Hello World代码 | ✅ 完整 | |
| 常见模式（3-5个） | ✅ 完整 | |
| Top API方法 | 签名+示例 | 通过fetch获取完整文档 |
| 最佳实践 | Top 5要点 | 搜索更多 |
| 故障排除 | | 搜索查询 |
| 完整API参考 | | 文档链接 |

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 需求发现 | 询问Skill的目的、触发条件、目标Agent和所需资源 |
| 2 | 知识调研 | 研究相关技术文档、API参考、代码示例，建立知识基础 |
| 3 | 内容平衡 | 决定哪些知识存储在本地（skill.md和references/），哪些通过动态查询获取 |
| 4 | 目录创建 | 在`.ai-team/skills/`下创建以kebab-case命名的目录 |
| 5 | 编写skill.md | 生成包含frontmatter（name、description）和完整指令的skill.md文件 |
| 6 | 添加资源 | 按需添加references/、sample_codes/、assets/、scripts/、templates/目录及文件 |
| 7 | 验证 | 检查frontmatter完整、description包含关键词、代码示例可运行、内容不超过500行 |

## Skill模板选择

| 技术类型 | 模板 | 示例 |
|----------|------|------|
| 客户端库、SDK/npm包 | SDK/库模板 | Semantic Kernel、Azure SDK |
| 云服务 | 服务模板 | Cosmos DB、Azure Functions |
| 应用开发框架 | 框架/平台模板 | ASP.NET Core、Blazor |
| REST API、协议 | API/协议模板 | Microsoft Graph、OOXML |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 文件位置 | 在`.ai-team/skills/{category}/{skill-name}/skill.md`创建文件 |
| 2 | 目录命名 | 小写连字符（如`make-skill-template`） |
| 3 | Frontmatter | 必须包含`name`（与目录名一致）和`description` |
| 4 | Description | 10-1024字符，说明做什么和何时使用，包含关键词 |
| 5 | 内容长度 | skill.md正文不超过500行 |
| 6 | 资源大小 | 捆绑资产每个不超过5MB |
| 7 | 代码示例 | 必须可运行，不得有错误 |

## 验证检查清单

- [ ] 目录名为小写连字符
- [ ] `name`字段与目录名完全匹配
- [ ] `description`为10-1024字符
- [ ] `description`说明了做什么和何时使用
- [ ] 正文内容不超过500行
- [ ] 捆绑资产每个不超过5MB

<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

---
name: make-skill-template
description: '创建新Agent Skill的元Skill，用于搭建skill目录、生成skill.md文件。当需要创建新skill、制作skill脚手架或理解Skill规范时使用。'
---

# make-skill-template

## 适用Agent
Skill Creator Agent、提示词工程师Agent

## 触发条件
当用户要求"创建一个skill"、"制作新skill"、"搭建skill脚手架"或构建捆绑资源的专用AI能力时触发。

## 概述
用于创建新Agent Skill的元Skill。当需要搭建新skill目录、生成skill.md文件或帮助用户理解Agent Skill规范时使用。

## 前置条件
- 理解Skill应该完成什么任务
- 一个清晰、关键词丰富的能力和触发条件描述
- 了解所需的捆绑资源（脚本、参考文档、资产、模板）

## 创建新Skill的步骤

### 步骤1：创建Skill目录
在`.ai-team/skills/`下创建一个新的小写连字符命名目录：

```
.ai-team/skills/{category}/{skill-name}/
└── skill.md          # 必需
```

### 步骤2：生成带Frontmatter的skill.md
每个Skill都需要YAML frontmatter中的`name`和`description`：

```yaml
---
name: skill-name
description: '做什么。何时使用。'
---
```

#### Frontmatter字段要求

| 字段 | 必需 | 约束 |
|------|------|------|
| `name` | **是** | 1-64字符，小写字母/数字/连字符，必须与目录名匹配 |
| `description` | **是** | 1-1024字符，必须描述做什么以及何时使用 |
| `license` | 否 | 许可证名称或指向捆绑LICENSE.txt的引用 |
| `compatibility` | 否 | 1-500字符，环境要求 |
| `metadata` | 否 | 附加属性的键值对 |
| `allowed-tools` | 否 | 预批准工具的空格分隔列表（实验性） |

#### Description最佳实践（关键）
`description`是自动发现Skill的**主要**机制，必须包含：
1. **做什么**（能力）
2. **何时使用**（触发条件、场景、文件类型）
3. **关键词**（用户可能在提示中提及的词）

**好的示例：**
```yaml
description: '使用Playwright测试本地Web应用的工具包。当被要求验证前端功能、调试UI行为、捕获浏览器截图或查看浏览器控制台日志时使用。支持Chrome、Firefox和WebKit。'
```

**差的示例：**
```yaml
description: 'Web测试助手'
```

### 步骤3：编写Skill正文
在frontmatter之后，添加Markdown指令。推荐章节：

| 章节 | 目的 |
|------|------|
| `# 标题` | 简要概述 |
| `## 适用Agent` | 指定使用此Skill的Agent |
| `## 触发条件` | 强化描述中的触发条件 |
| `## 前置条件` | 所需工具、依赖 |
| `## 执行步骤` | 任务的编号步骤表格 |
| `## 常见模式` | 常见用例和代码模式 |
| `## 故障排除` | 常见问题和解决方案 |
| `## 输出规范` | 输出格式和质量要求 |
| `## 参考资料` | 捆绑文档的链接 |

### 步骤4：添加可选目录（如需要）

| 目录 | 目的 | 何时使用 |
|------|------|----------|
| `scripts/` | 可执行代码（Python、Bash、JS） | 执行操作的自动化 |
| `references/` | Agent读取的文档 | API参考、模式、指南 |
| `assets/` | 按原样使用的静态文件 | 图片、字体、模板 |
| `templates/` | Agent修改的起始代码 | 要扩展的脚手架 |
| `sample_codes/` | 工作代码示例 | 入门和常见模式 |

## 完整Skill目录结构示例

```
my-awesome-skill/
├── skill.md           # 必需 - 指令
├── LICENSE.txt         # 可选 - 许可证文件
├── scripts/
│   └── helper.py       # 可执行自动化
├── references/
│   ├── api-reference.md # 详细文档
│   └── examples.md     # 使用示例
├── assets/
│   └── diagram.png     # 静态资源
├── sample_codes/
│   ├── getting-started/
│   │   └── hello.py
│   └── common-patterns/
│       └── crud.py
└── templates/
    └── starter.ts      # 代码脚手架
```

## 快速开始：复制此模板

1. 复制`make-skill-template/`目录
2. 重命名为你的Skill名称（小写、连字符）
3. 更新`skill.md`：
   - 将`name:`改为与目录名匹配
   - 编写关键词丰富的`description:`
   - 用你的指令替换正文内容
4. 按需添加捆绑资源
5. 验证frontmatter和内容

## 验证检查清单

- [ ] 目录名为小写连字符
- [ ] `name`字段与目录名完全匹配
- [ ] `description`为10-1024字符
- [ ] `description`说明了做什么和何时使用
- [ ] 正文内容不超过500行
- [ ] 捆绑资产每个不超过5MB

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Skill未被自动发现 | 改善description，添加更多关键词和触发条件 |
| name验证失败 | 确保小写、无连续连字符、与目录名匹配 |
| Description太短 | 添加能力、触发条件和关键词 |
| 资产未找到 | 使用相对于Skill根目录的相对路径 |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 文件位置 | `.ai-team/skills/{category}/{skill-name}/skill.md` |
| 2 | 格式 | Markdown，包含YAML frontmatter |
| 3 | name | 小写连字符，与目录名一致 |
| 4 | description | 10-1024字符，包含做什么和何时使用 |

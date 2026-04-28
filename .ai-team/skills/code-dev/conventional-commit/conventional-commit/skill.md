---
name: conventional-commit
description: 'Conventional Commits规范提交消息，格式为type(scope): description。当需要生成Git提交消息或规范化提交记录时使用。'
---

# conventional-commit

## 适用Agent
Java开发Agent、前端开发Agent、DevOps Agent

## 触发条件
代码开发Agent完成代码编写并准备提交代码时触发。

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 识别变更类型 | 分析当前代码变更，确定变更类型：新功能→feat，修复→fix，文档→docs，样式→style，重构→refactor，性能→perf，测试→test，构建→build，CI→ci，杂项→chore |
| 2 | 确定影响范围 | 分析变更影响的模块或功能，确定scope：模块名、组件名、功能区域 |
| 3 | 编写提交消息 | 按格式 `type(scope): description` 编写提交消息：type为步骤1确定的类型，scope为步骤2确定的范围（可选），description为简明描述（不超过50字符，使用祈使句，首字母小写，句末不加句号） |
| 4 | 编写提交正文 | 若变更需要补充说明，添加正文：空一行后书写，每行不超过72字符，说明"为什么"而非"做了什么" |
| 5 | 标注破坏性变更 | 若存在破坏性变更，在type后加`!`标记（如`feat(api)!:`），并在正文首行写`BREAKING CHANGE:`说明迁移方式 |
| 6 | 关联任务/缺陷 | 在正文末尾添加关联标记：关联任务`Refs: TASK-NNN`，修复缺陷`Fixes: BUG-NNN`，关闭Issue`Closes #NNN` |

## Commit Message 格式

```
type(scope)!: subject

body

footer
```

## 类型清单

| 类型 | 含义 | 示例 |
|------|------|------|
| feat | 新功能 | feat(user): add user registration endpoint |
| fix | 修复缺陷 | fix(auth): resolve token expiration issue |
| docs | 文档变更 | docs(api): update API documentation |
| style | 代码样式（不影响逻辑） | style(lint): fix eslint warnings |
| refactor | 重构（非新功能/非修复） | refactor(service): extract common validation logic |
| perf | 性能优化 | perf(query): add database index for user search |
| test | 测试相关 | test(user): add unit tests for UserService |
| build | 构建系统/依赖 | build(deps): upgrade spring boot to 3.4.5 |
| ci | CI/CD配置 | ci(actions): add codeql scanning workflow |
| chore | 杂项（不修改src/test） | chore(config): update editorconfig |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 格式 | 严格遵循Conventional Commits规范 |
| 2 | 主题行 | 不超过50字符，使用祈使句 |
| 3 | 正文行 | 每行不超过72字符 |
| 4 | 语言 | 主题行使用英文，正文可使用中英文 |
| 5 | 关联 | 必须关联对应的TASK-NNN或BUG-NNN编号 |

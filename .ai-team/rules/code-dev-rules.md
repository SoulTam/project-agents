<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# 代码开发规则

> 按技术栈分组。Agent 只需读取相关栈的小节。

---

## 1. 通用代码规则（所有代码开发 Agent）

| # | 规则 | 约束 |
|---|------|------|
| 1 | 禁止伪代码 | 不得使用伪代码实现 |
| 2 | 禁止假设性代码 | 不得使用假设性代码实现 |
| 3 | 禁止 mock | 不得使用 mock 代码实现（测试代码除外） |
| 4 | 生产环境标准 | 严格按生产环境开发 |
| 5 | Git 提交规范 | 遵循 Conventional Commits：`type(scope): description` |

---

## 2. Java 开发规则

| # | 规则 | 约束 |
|---|------|------|
| 1 | 异常处理 | 异常包装必须保留原异常和堆栈：`new CustomException("描述", originalException)`，不得用自定义信息覆盖 |

---

## 3. 前端开发规则

> 当前项目主要技术栈。具体规范见 `.ai-team/skills/code-dev/frontend/frontend-development/skill.md`。

---

## 4. IBM i (AS/400) 开发规则

> 仅当项目涉及 IBM i 时加载。详细规范见 `.ai-team/rules/ibmi-development-rules.md`。

| # | 规则 | 约束 |
|---|------|------|
| 1 | 自由格式 | RPG 必须使用 **FREE 自由格式（维护旧代码除外） |
| 2 | 错误处理 | 文件操作必须包含错误处理（RPG: Monitor/On-Error；CL: MONMSG） |
| 3 | DDS 规范 | 字段名 ≤10 字符；PF 必须有键；DSPF 使用消息子文件 |
| 4 | 库名规范 | 禁止硬编码库名，使用 `*LIBL` 或 `RTVJOBA` 获取当前库 |
| 5 | 连接验证 | 开发前通过 SSH 验证服务器连接，确认库名和源文件可访问 |
| 6 | 代码探索 | 必须先 SSH 探索现有代码（列成员/读源码/查字段定义），保证风格一致 |
| 7 | ASP 路径 | 使用 ASP Group(IASP) 时，IFS 路径加 ASP 前缀：`/{ASP}/QSYS.LIB/...`。ASP 名称从 `ibmi-connection.env` 的 `IBM_I_ASP` 获取 |

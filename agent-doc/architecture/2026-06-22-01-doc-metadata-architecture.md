<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# 架构设计文档：文档元数据时间戳规则

## 概述
为项目中所有非代码文档添加标准化元数据头部（创建时间+最后修改时间），统一文档管理规范。

## 适用范围
所有非代码文档（.md 为主），排除源代码文件。涵盖：
- 项目根目录：AGENTS.md
- agent-doc/ 全部 .md 文件（含 architecture/、technical-design/、feature-design/、dev-plan/、plan/、result-first/、audit/、user-request/）
- .ai-team/ 全部 .md 文件（含 rules/、agents/、skills/、knowledge-base/、templates/）
- 其他任何非代码文件

## 排除范围
.py .js .ts .java .css .scss .json .yaml .yml .toml .xml .sql .sh .bat .ps1

## 架构决策
| 决策 | 选择 | 理由 |
|------|------|------|
| 元数据格式 | `<!-- 创建时间: -->` / `<!-- 最后修改: -->` | Markdown 注释，不影响渲染；简单易解析 |
| 时间精度 | 到分钟（yyyy-MM-dd HH:mm） | 足够精确，避免秒级冗余 |
| 更新时机 | 每次文件修改完成后 | 与"修改任务自动提交"规则一致 |
| 存储位置 | 文件第1-2行 | 文件最开头，一目了然 |

# Git自动提交规则 — 架构设计

## 概述
在 `.opencode\instructions.md` 的"子计划执行"阶段模板中嵌入自动git提交流程。

## 架构决策
| 决策 | 选择 | 理由 |
|------|------|------|
| 触发时机 | 每完成3个子计划后 | 防止变更积压，同时避免过于频繁 |
| 提交流程 | git add . + git commit | 原生git操作，零依赖 |
| 计数方式 | 全局递增计数器 | 从第1个SP开始计数 |
| commit message | `auto: SP-XX to SP-YY 子计划完成` | 清晰标识批次范围 |

## 流程图
```
子计划完成 → completedCount++
completedCount % 3 == 0? → Yes → git add .
                                      → git commit -m "auto: ..."
                                      → git push (可选)
                           → No → 继续下一子计划
```

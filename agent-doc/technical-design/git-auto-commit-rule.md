# Git自动提交规则 — 技术设计

## 实现方式
直接修改 `.opencode\instructions.md` 中"子计划执行"阶段模板。

## 修改内容
在"子计划执行"模板的"执行步骤"段落后插入：

```
### Git自动提交规则
每完成3个子计划，自动执行：
- git add .
- git commit -m "auto: SP-[起始编号] to SP-[结束编号] 子计划完成"
- git push（如配置了远程仓库）

计数器 logic：
- 全局变量 completedSubPlanCount，初始值0
- 每个子计划执行完成后 ++
- 当 completedSubPlanCount % 3 == 0 时触发提交
```

## 提示词工程师规则
在 `.opencode\instructions.md` 开头或显眼位置添加：

```
### 提示词工程师使用规则
除以下明确简短指令外，所有用户请求必须先走"提示词工程师"模板进行请求增强：
- 确认 / 可以 / 确认执行 / 停止执行
- 其他语义明确的简短确认/否定指令
```

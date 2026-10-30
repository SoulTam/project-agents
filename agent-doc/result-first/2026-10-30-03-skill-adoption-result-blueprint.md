<!-- 创建时间: 2026-10-30 22:55 -->
<!-- 最后修改: 2026-10-30 22:55 -->

# 结果蓝图：自有旧格式 Skill 迁移（T2026-1030-03）

## 1. 目标

自有旧格式 Skill 在不改写正文提示词与脚本实现的前提下，一次性迁入 `.ai-team/skills/` 规范结构并登记注册表。

## 2. 终态验收

| # | 可机读验收 | verify_cmd |
|---|-----------|-----------|
| A1 | 迁移工具在 dry-run 与 apply 两种模式下均可用，正文与资产字节级保留 | `python -m unittest discover -s tools/scripts/tests -q` |
| A2 | 注册表一致性 0 违规 | `python tools/scripts/registry_lint.py` |
| A3 | 迁移后文档满足时间戳规范 | `python tools/scripts/metadata_check.py README.md` |
| A4 | 使用说明可从 README 索引到工具 | `python tools/scripts/link_check.py` |

## 3. BLK 单元

<!-- BLK:AD-01 -->
#### BLK:AD-01 迁移工具

- 文件：`tools/scripts/skill_adopt.py:1`
- 职责：定位源 Markdown → 剥离旧 frontmatter/时间戳 → 重建标准头部 → 正文原样拼接 → 复制同级资产
- 参数：`--src --name --domain --keywords --agents [--version --owner --root --apply --force]`
- 约束：默认 dry-run；正文与脚本内容零改写（仅重排头部与 EOL）

<!-- BLK:AD-02 -->
#### BLK:AD-02 目标格式规范

- 位置：`.ai-team/skills/{domain}/{name}/skill.md`
- 头部顺序：创建时间 → 最后修改 → 空行 → `---` → `name`/`version`/`trigger_keywords`/`agents` → `---` → 空行
- 校验：`tools/scripts/registry_lint.py` 比对 frontmatter 与注册表

<!-- BLK:AD-03 -->
#### BLK:AD-03 注册表登记

- 文件：`.ai-team/skills/registry.json`
- 规则：追加单行紧凑条目；`source=migrated:internal`；`owner` 默认取 `agents[0]`
- 冲突：同名 skill 或关键词被占用时拒绝（`--force` 仅对同名生效）

<!-- BLK:AD-04 -->
#### BLK:AD-04 回归用例

- 文件：`tools/scripts/tests/test_scripts.py:150`
- 用例：apply 后头部与正文均正确 + 资产复制；dry-run 零写入；关键词冲突拒绝

<!-- BLK:AD-05 -->
#### BLK:AD-05 使用说明

- 文件：`README.md:253`（扩展方式表）
- 内容：一行命令示例 + "不改正文/脚本" 说明

## 4. 边界

| 项 | 说明 |
|----|------|
| 不做 | 改写提示词、重构脚本、自动裁剪正文、自动生成能力点摘要 |
| 不做 | 外部来源资产仍走 `intake-rules.md` 4 道门禁（本工具仅服务自有资产） |
| 失败 | 源不可读/参数非法 → 2；目标存在/关键词冲突 → 1 |

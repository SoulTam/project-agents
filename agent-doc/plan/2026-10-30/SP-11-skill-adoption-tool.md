<!-- 创建时间: 2026-10-30 22:58 -->
<!-- 最后修改: 2026-10-30 22:58 -->

# SP-11 自有旧格式 Skill 迁移工具

| 字段 | 值 |
|------|-----|
| SP-ID | SP-11 |
| 依赖 | SP-04（registry 与 frontmatter 口径）、SP-05（脚本与用例约定） |
| 技术栈 | tools（Python 标准库） |
| 日志 | `agent-doc/tasks/T2026-1030-03/gate-log.jsonl` |
| 依据 BLK | BLK:AD-01、BLK:AD-02、BLK:AD-03、BLK:AD-04、BLK:AD-05 |

## 步骤

| # | 动作 | 验收 |
|---|------|------|
| 1 | 实现 `tools/scripts/skill_adopt.py` | `--help` 列出 7 个参数，退出码 0 |
| 2 | 目标格式按 BLK:AD-02 输出 | apply 后首 3 行为时间戳+空行，第 4 行起为 frontmatter |
| 3 | 注册表追加逻辑 | apply 后 `registry_lint.py` 退出码 0 |
| 4 | 补 3 个回归用例 | `unittest discover` 18 例通过 |
| 5 | README 扩展方式补一行 | `link_check.py` 退出码 0 |

## 最终结果

> 本段由 blueprint_split.py 生成，禁止手工修改。

### BLK:AD-01

#### BLK:AD-01 迁移工具

- 文件：`tools/scripts/skill_adopt.py:1`
- 职责：定位源 Markdown → 剥离旧 frontmatter/时间戳 → 重建标准头部 → 正文原样拼接 → 复制同级资产
- 参数：`--src --name --domain --keywords --agents [--version --owner --root --apply --force]`
- 约束：默认 dry-run；正文与脚本内容零改写（仅重排头部与 EOL）

### BLK:AD-02

#### BLK:AD-02 目标格式规范

- 位置：`.ai-team/skills/{domain}/{name}/skill.md`
- 头部顺序：创建时间 → 最后修改 → 空行 → `---` → `name`/`version`/`trigger_keywords`/`agents` → `---` → 空行
- 校验：`tools/scripts/registry_lint.py` 比对 frontmatter 与注册表

### BLK:AD-03

#### BLK:AD-03 注册表登记

- 文件：`.ai-team/skills/registry.json`
- 规则：追加单行紧凑条目；`source=migrated:internal`；`owner` 默认取 `agents[0]`
- 冲突：同名 skill 或关键词被占用时拒绝（`--force` 仅对同名生效）

### BLK:AD-04

#### BLK:AD-04 回归用例

- 文件：`tools/scripts/tests/test_scripts.py:150`
- 用例：apply 后头部与正文均正确 + 资产复制；dry-run 零写入；关键词冲突拒绝

### BLK:AD-05

#### BLK:AD-05 使用说明

- 文件：`README.md:253`（扩展方式表）
- 内容：一行命令示例 + "不改正文/脚本" 说明

## verify_cmd

```
python -m unittest discover -s tools/scripts/tests -q
python tools/scripts/registry_lint.py
python tools/scripts/metadata_check.py README.md
python tools/scripts/link_check.py
```

期望：全部退出码 0（unittest 为 18 例）。
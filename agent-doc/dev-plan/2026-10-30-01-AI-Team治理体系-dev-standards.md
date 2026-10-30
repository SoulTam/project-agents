<!-- 创建时间: 2026-10-30 20:55 -->
<!-- 最后修改: 2026-10-30 20:55 -->

# AI Team 治理体系 - 开发规范文档

> 适用范围：本次整改涉及的全部规则、Agent 定义、Skill、脚本、模板、产物文件

---

## 1. 文档规范

| # | 规范 | 约束 |
|---|------|------|
| 1 | 元数据 | 非代码文档第 1 行 `<!-- 创建时间: yyyy-MM-dd HH:mm -->`，第 2 行 `<!-- 最后修改: yyyy-MM-dd HH:mm -->`，第 3 行空行 |
| 2 | 编码 | UTF-8（无 BOM），换行 LF |
| 3 | 表格 | 单竖线分隔，禁止双竖线 |
| 4 | 层级 | 最多 H3；单文件 ≤400 行 |
| 5 | 省略 | 禁止 `...`、`略`、`同上`、`参考XX`、`详见X章` |
| 6 | 示例 | 必须可执行或可验证，禁止伪代码 |

## 2. 规则 ID 规范

| 前缀 | 域 | 示例 |
|------|-----|------|
| `R-HR` | 硬规则 | `R-HR-03` |
| `R-LV` | 分级 | `R-LV-02` |
| `R-ST` | 状态流转 | `R-ST-01` |
| `R-PM` | 权限 | `R-PM-01` |
| `R-GT` | 关卡 | `R-GT-01` |
| `R-SK` | Skill 使用 | `R-SK-01` |
| `R-IN` | 能力吸收 | `R-IN-01` |

**命名硬约束**：

| # | 约束 |
|---|------|
| 1 | 全局唯一，禁止复用已删除 ID |
| 2 | 规则本体只允许出现在 `.ai-team/rules/*.md` 一处 |
| 3 | Agent 定义引用规则时必须写 ID，不得复制原文 |
| 4 | 新增规则必须同时登记到 `rules/gate-rules.md` 的规则索引表 |

## 3. Agent 定义规范

| 章节 | 必填 | 内容要求 |
|------|------|---------|
| 角色定义 | 是 | 一句话，不超过 60 字 |
| 可写域 | 是 | 明确列出可写路径，其余视为禁写 |
| 输入 | 是 | 表格：输入项 / 来源 / 契约 |
| 输出 | 是 | 表格：产出物 / 落盘路径 / schema |
| 调用契约 | 是 | 引用 API-ID，不写实现 |
| 规则引用 | 是 | 只列 R-ID |
| 禁止项 | 是 | ≥3 条 |

**禁止**：在 `agent.md` 中复制规则正文、复制模板全文、写"参考 `.cursorrules`"。

## 4. Skill 规范

| 项 | 约束 |
|----|------|
| frontmatter | `name`、`version`、`trigger_keywords`、`agents` 四字段必填 |
| 路径 | `.ai-team/skills/{category}/{name}/skill.md` |
| 注册 | 必须出现在 `registry.json`，`registry_lint.py` 退出码 0 |
| 输出契约 | 必须写落盘路径模式与校验命令 |
| 加载纪律 | 命中 trigger 才可加载；回复首行声明 `SKILL: name@ver` |
| 数量 | 单次最多加载 2 个 |

## 5. 模板规范

| 项 | 约束 |
|----|------|
| 位置 | `.ai-team/templates/stages/{stage}.md` |
| 索引 | `AGENTS.md` 路由表登记阶段→模板文件 |
| 加载 | 单次只加载 1 个，禁止一次加载全部 |
| 体积 | 单模板 ≤120 行 |
| 占位符 | 统一 `{var}`，禁止 `[xxx]` 与 `...` 混用 |

## 6. 脚本规范

| 项 | 约束 |
|----|------|
| 语言 | Python 3.11+，仅标准库 |
| 入口 | `if __name__ == "__main__":`，参数用 `argparse` |
| 退出码 | 0 通过 / 1 不通过 / 2 证据不足 |
| 输出 | stdout 只输出 JSON；诊断信息走 stderr |
| 副作用 | 只允许写 `--out` 指定路径；禁止改动业务文件 |
| 幂等 | 同输入同输出，重复执行无差异 |
| 测试 | 每个脚本 ≥3 个用例，覆盖 0/1/2 三态 |

## 7. 产物规范

| 产物 | 规范 |
|------|------|
| status.md | 字段顺序固定；每次更新刷新 `updated_at` |
| gate-log.jsonl | 只追加；单行单 JSON；禁止修改历史行 |
| gate-report.json | 字段顺序固定；`evidence` 不得为空数组（pass 时） |
| SP 文件 | 必含 `verify_cmd`、`acceptance`、`blk_refs`、三要素步骤 |
| intake | `license` 为"未知"时 `verdict` 只能为 `reject` |

## 8. Git 规范

| 项 | 约束 |
|----|------|
| 提交信息 | Conventional Commits：`type(scope): 描述` |
| type | feat / fix / docs / refactor / chore / test |
| scope | rules / agents / skills / plan / tools / repo |
| 粒度 | 一个子计划一次提交；每 3 个 SP 强制提交 |
| 禁止 | 提交 `agent-doc/code/` 构建产物、`- Copy` 目录、`*.zip` |

## 9. 质量门禁

| 门禁 | 命令 | 通过标准 |
|------|------|---------|
| 元数据 | `python tools/scripts/metadata_check.py <paths>` | 退出码 0 |
| 死链 | `python tools/scripts/link_check.py` | 退出码 0 |
| 注册表 | `python tools/scripts/registry_lint.py` | 退出码 0 |
| 语法 | `python -m py_compile tools/scripts/*.py` | 退出码 0 |
| 关卡 | `python tools/scripts/gate_check.py --task <id> --gate <Gx>` | 退出码 0 |

## 10. 禁止项汇总

| # | 禁止 |
|---|------|
| 1 | 引用不存在的文件（`.cursorrules`、`.opencode/instructions.md`） |
| 2 | 在 Agent 定义中复制规则正文 |
| 3 | 人工逐字拷贝蓝图到子计划 |
| 4 | 无证据声明"通过/完成" |
| 5 | L0/L1 产出蓝图或子计划 |
| 6 | 同一关卡驳回超过 2 轮仍不升级 |
| 7 | 未声明 `SKILL:` 却声称使用 Skill |
| 8 | 未注册的 Skill 被加载 |
| 9 | 许可证未知的外部资产被合入 |
| 10 | 修改 `gate-log.jsonl` 历史行 |

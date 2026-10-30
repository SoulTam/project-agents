<!-- 创建时间: 2026-10-30 21:00 -->
<!-- 最后修改: 2026-10-30 21:00 -->

# Skill 使用规则

> 唯一真相源：`.ai-team/skills/registry.json`。Agent 定义中的"关联 Skill 表"已废止，改为按 trigger 匹配。

## 1. 规则索引

| ID | 规则 |
|----|------|
| R-SK-01 | 只有 registry 中登记且 path 存在的 Skill 可加载 |
| R-SK-02 | 请求关键词命中 `trigger.keywords` ≥1 才可加载；未命中不得加载 |
| R-SK-03 | 单次最多加载 2 个 Skill |
| R-SK-04 | 加载后回复首行必须声明 `SKILL: name@version`；未声明视为未使用（稽查判 fail） |
| R-SK-05 | 产出必须落到该 Skill `outputs` 声明的路径模式 |
| R-SK-06 | 未注册 Skill 一律拒绝加载，返回 E-SKL-01 |

## 2. 匹配算法

| 步骤 | 动作 | 判据 |
|------|------|------|
| 1 | 提取请求关键词（名词/动词短语） | 不做语义扩写 |
| 2 | 与所有 `trigger.keywords` 求交 | 命中 ≥1 为候选 |
| 3 | 多候选取 `trigger.agents` 含当前 Agent 的 | 仍多个取关键词命中数最多者 |
| 4 | 若候选 >2，取前 2 | 其余不加载 |
| 5 | 无候选 | 不加载，继续主流程 |

## 3. 加载与声明

| 项 | 格式 |
|----|------|
| 声明行 | `SKILL: result-first-definition@1.0.0` |
| 位置 | 回复第一行 |
| 多 Skill | 依次声明两行，仍各占首部 |
| 加载失败 | 输出 `E-SKL-01: {name} 未注册或路径不存在` |

## 4. 注册表结构

| 字段 | 类型 | 必填 | 校验 |
|------|------|------|------|
| name | string | 是 | 全局唯一，等于目录名 |
| version | string | 是 | 语义化 x.y.z |
| path | string | 是 | 文件存在 |
| trigger.keywords | list | 是 | ≥1，全局无重复 |
| trigger.agents | list | 是 | 属于 20 个 agent 之一 |
| inputs | list | 是 | ≥1 |
| outputs | list | 是 | ≥1，含路径模式 |
| verify | string | 是 | 命令或检查清单路径 |
| source | string | 是 | internal / URL / 仓库 |
| owner | string | 是 | 维护角色 |

frontmatter 位置：文件前两行保留创建/最后修改时间注释，空行后紧接 `---` 块，字段为 `name`、`version`、`trigger_keywords`、`agents`，数值必须与 registry 一致（`registry_lint.py` 校验）。

## 5. 校验

| 检查 | 命令 | 通过 |
|------|------|------|
| 注册完整性 | `python tools/scripts/registry_lint.py` | 退出码 0 |
| 条目数 | 与磁盘 `skill.md` 数一致 | 34 = 34 |
| 重复 keyword | 脚本检测 | 0 |

## 6. 禁止

| # | 禁止 |
|---|------|
| 1 | 凭"经验"选择 Skill 而不经 trigger 匹配 |
| 2 | 加载后不声明 |
| 3 | 一次性加载全部 Skill |
| 4 | 修改 registry 而不更新对应 `skill.md` frontmatter |
| 5 | 用 Skill 名称代替实际执行步骤 |

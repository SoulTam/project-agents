<!-- 创建时间: 2026-10-30 20:55 -->
<!-- 最后修改: 2026-10-30 20:55 -->

# SP-04: Skill 注册表与 frontmatter

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划ID | SP-04 |
| 类型 | A（文档/规则） |
| 技术栈 | doc |
| 对应蓝图章节 | 架构终态 M4；接口 API-008；产物 D6；规则 R-HR-07；文件清单 F11/F12；场景 S1 的 Skill 加载声明 |
| 前置依赖 | SP-01 |
| 负责子 Agent | Skill Creator Agent（PM 协同） |
| BLK 引用 | BLK:AR-M4、BLK:API-008、BLK:TBL-06、BLK:BIZ-HR07、BLK:FN-SKILL |

## 最终结果（逐字拷贝自蓝图）

| 模块 | 职责 | 技术选型 | 选型理由 |
|------|------|---------|---------|
| M4 方法层 | Skill 方法与注册 | `.ai-team/skills/**` + `registry.json` | 触发可判定、加载可声明 |

| 编号 | 调用方→被调方 | 方法 | 功能 | 请求参数 | 响应格式 | 失败码 |
|------|--------------|------|------|---------|---------|--------|
| API-008 | 任意 Agent→Skill 层 | `load` | 加载 Skill | name | `{body, declaration}` | E-SKL-01 未注册 |

| 字段 | 类型 | 长度 | 主键 | 外键 | 索引 | 默认值 | 说明 |
|------|------|------|------|------|------|--------|------|
| name | string | 60 | PK | — | Y | 无 | 唯一，等于目录名 |
| version | string | 10 | — | — | N | 1.0.0 | 语义化 |
| path | path | 255 | — | — | Y | 无 | skill.md 路径 |
| trigger_keywords | list | — | — | — | Y | 无 | 全局唯一 |
| trigger_agents | list | — | — | — | N | 无 | 归属 Agent |
| inputs | list | — | — | — | N | 无 | 输入项 |
| outputs | list | — | — | — | N | 无 | 落盘路径模式 |
| verify | string | 255 | — | — | N | 无 | 校验命令 |
| source | string | 255 | — | — | N | internal | 来源与许可 |
| owner | string | 40 | — | — | N | 无 | 维护角色 |

| ID | 规则 | 约束 |
|----|------|------|
| R-HR-07 | Skill 显式加载 | 命中 D6 trigger 才可加载；回复首行必须声明 `SKILL: name@ver` |

| 编号 | 文件 | 动作 | 验收断言 |
|------|------|------|---------|
| F11 | `.ai-team/skills/registry.json` | 新增，覆盖 34 个 Skill | `registry_lint.py` 退出码 0 |
| F12 | `.ai-team/skills/**/skill.md` | 补 frontmatter（name/version/trigger） | 34/34 合规 |

## 验收标准

| 序号 | 蓝图项 | 可验证条件 | 状态 |
|------|--------|-----------|------|
| 1 | F11 | `registry.json` 中 `skills` 数组长度 = 34 | ⬜ |
| 2 | F11 | 每条含 name/version/path/trigger/inputs/outputs/verify/source/owner 九字段 | ⬜ |
| 3 | F11 | 所有 `path` 指向真实存在的 `skill.md` | ⬜ |
| 4 | F12 | 34 个 `skill.md` 全部含 4 字段 frontmatter | ⬜ |
| 5 | R-HR-07 | 每个 keyword 全局唯一（无交叉） | ⬜ |
| 6 | API-008 | `skill-usage-rules.md` 与本注册表字段一一对应 | ⬜ |

## 输入依赖

| 输入项 | 来源子计划 | 说明 |
|--------|-----------|------|
| Skill 加载纪律文本 | SP-02 | `skill-usage-rules.md` 定义匹配与声明 |
| `AGENTS.md` Skill 纪律段 | SP-01 | 需声明"命中 trigger 才加载" |

## 执行步骤

| 步骤 | 做什么 | 怎么做 | 正反约束 | 预期产物 |
|------|--------|--------|---------|---------|
| 1 | 盘点 Skill | 扫描 `.ai-team/skills/**/skill.md`，记录 34 条，建立 name→path 映射 | 必须：与实际文件数一致（34）。禁止：凭 README 的 30 条清单填表 | 盘点清单 |
| 2 | 建 registry.json | 写顶层 `{"schema":1,"skills":[...]}`，逐条填九字段；keywords 取技能名 + 2–3 个同义触发词 | 必须：path 为真实相对路径。禁止：留空 inputs/outputs/verify | `registry.json` |
| 3 | 补 frontmatter | 每个 `skill.md` 顶部插入 YAML：`name`、`version`、`trigger_keywords`、`agents` | 必须：与 registry 完全一致。禁止：中文与英文 name 混用 | 34 个 frontmatter |
| 4 | 消除 keyword 冲突 | 统计所有 keyword，重复项调整归属（保留最相关技能） | 必须：全局唯一。禁止：同一 keyword 挂在两个技能上 | 无冲突 |
| 5 | 修 references.md | 删除不存在的 `ibmi-documentation` 条目；改为指向 `registry.json` | 必须：删除死链。禁止：保留死链并加备注 | 修订后 references.md |
| 6 | 校验 | 运行 `registry_lint.py`（SP-05 产出后）；若尚未产出，先手工逐条校验 path 存在 | 必须：34/34 通过。禁止：跳过 path 存在性检查 | 校验通过 |
| 7 | 提交 | `git add .` + `git commit -m "feat(skills): 新增Skill注册表并补齐frontmatter"` | 必须：verify_cmd 退出码 0 | 一次提交 |

**verify_cmd**

```powershell
pwsh -NoProfile -Command "$r = Get-Content .ai-team/skills/registry.json -Raw | ConvertFrom-Json; if($r.skills.Count -ne 34){exit 1}; foreach($s in $r.skills){ if(-not (Test-Path $s.path)){exit 1} }; $files = Get-ChildItem -Recurse -Filter skill.md .ai-team/skills; foreach($f in $files){ if(-not (Select-String -Path $f.FullName -Pattern '^name:' -Quiet)){exit 1} }; exit 0"
```

## 完整设计内容（逐字拷贝自蓝图）

### registry.json 条目字段

| 字段 | 类型 | 必填 | 校验规则 | 默认值 |
|------|------|------|---------|--------|
| name | 字符串 | 是 | 全局唯一、等于目录名 | 无 |
| version | 字符串 | 是 | 语义化 x.y.z | 1.0.0 |
| path | 路径 | 是 | 文件存在 | 无 |
| trigger.keywords | 列表 | 是 | ≥1，全局无交叉重复 | 无 |
| trigger.agents | 列表 | 是 | 属于 20 个 agent 之一 | 无 |
| inputs | 列表 | 是 | ≥1 | 无 |
| outputs | 列表 | 是 | ≥1，含落盘路径模式 | 无 |
| verify | 字符串 | 是 | 可执行命令或检查清单路径 | 无 |
| source | 字符串 | 是 | internal / 外部 URL / 仓库 | internal |

### Skill 加载纪律（实施规格）

| 项 | 约束 |
|----|------|
| 匹配 | 请求关键词命中 `trigger_keywords` ≥1 即候选；多候选取 agent 归属匹配者 |
| 加载上限 | 单次 ≤2 个 |
| 声明格式 | 回复首行 `SKILL: name@version` |
| 未注册 | 拒绝加载，返回 E-SKL-01 |
| 声明缺失 | 视为未使用该 Skill（稽查判 R-AU-05 fail） |
| 输出落盘 | 必须符合 registry 中 `outputs` 的路径模式 |

### 34 个 Skill 清单（盘点基线）

| 类别 | 数量 | 名称 |
|------|------|------|
| architecture | 2 | architecture-design、architectural-decision-record |
| audit | 1 | compliance-audit |
| code-dev | 5 | java-development、frontend-development、ibmi-development、conventional-commit、cicd-workflow-design |
| dev-planning | 1 | dev-planning |
| doc-output | 4 | word-export、pdf-export、excel-export、ppt-export |
| feature-design | 1 | feature-design |
| knowledge | 2 | knowledge-management、codebase-onboarding |
| meta | 3 | create-agentsmd、make-skill-template、microsoft-skill-creator |
| pm | 8 | project-status-assessment、task-decomposition、technical-spike、result-first-definition、design-doc-generation、global-execution-planning、plan-breakdown-tracking、result-rollback-verification |
| prompt-engineer | 1 | prompt-engineering |
| requirements | 1 | requirements-analysis |
| task-assignment | 1 | task-assignment |
| technical-design | 1 | technical-design |
| testing | 2 | testing、code-security |
| verification | 1 | content-verification |

## 完成标志

- [ ] `registry.json` 含 34 条且字段完整
- [ ] 34 个 `skill.md` 均含 frontmatter
- [ ] keyword 全局唯一
- [ ] `references.md` 死链已删
- [ ] `verify_cmd` 退出码 0
- [ ] 已提交 Git

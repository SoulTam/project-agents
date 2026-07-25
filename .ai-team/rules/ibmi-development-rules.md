<!-- 创建时间: 2026-07-25 00:00 -->
<!-- 最后修改: 2026-07-25 00:00 -->

# IBM i开发规则

> 仅当项目涉及 IBM i 时加载。详细规范见本文件。

---

## 1. DDS规范

### 1.1 物理文件(PF)规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 字段名长度 | ≤10字符 |
| 2 | 必须有键 | 每个PF必须定义主键 |
| 3 | 日期字段类型 | 使用L类型(ISO日期) |
| 4 | 金额字段类型 | 使用P(压缩十进制) |
| 5 | 字段描述 | 每个字段必须有描述注释 |

### 1.2 逻辑文件(LF)规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 基于PF | 必须引用PF的记录格式 |
| 2 | 键值定义 | 使用PF中已定义的字段 |
| 3 | 选择条件 | 使用SELECT/OMIT |
| 4 | 访问路径维护 | 根据使用场景选择MAINT(*IMMED/*DLY/*REBUILD) |

### 1.3 显示文件(DSPF)规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 使用消息子文件 | 消息显示统一使用SFLMSG模式 |
| 2 | 功能键使用CF | CF允许程序读取功能键AID |
| 3 | 字段使用类型标注 | B-输入输出, I-仅输入, O-仅输出, H-隐藏 |
| 4 | 画面布局 | 标题→输入区→明细区→功能键提示→消息区 |

### 1.4 打印文件(PRTF)规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 页眉定义 | 使用HEAD1/HEAD2 |
| 2 | 详情行定义 | 使用DETAIL |
| 3 | 页脚定义 | 使用FOOT1/FOOT2 |
| 4 | 字段格式 | 金额使用EDTCDE(J)，日期使用EDTWRD |

---

## 2. 程序调用规范

### 2.1 RPG程序规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 使用自由格式 | **FREE开头，禁止固定格式 |
| 2 | 错误处理 | Monitor/On-Error |
| 3 | 原型声明 | 外部调用必须声明Dcl-Pr |
| 4 | 服务程序引用 | 通过绑定目录引用 |
| 5 | 指示器使用 | 使用命名指示器，禁止使用1-99号指示器作为通用变量 |
| 6 | 文件操作 | 操作前检查%Found，操作后检查SqlState |

### 2.2 CL程序规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 变量声明 | 所有变量必须先DCL再使用 |
| 2 | 错误捕获 | 每个可能出错的命令后加MONMSG |
| 3 | 库名处理 | 使用RTVJOBA获取当前库，禁止硬编码 |
| 4 | 多分支逻辑 | 使用SELECT-WHEN替代IF-ELSE嵌套 |

---

## 3. 5250画面规范

### 3.1 画面布局规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 布局顺序 | 标题→输入区→明细区→功能键提示→消息区 |
| 2 | 子文件结构 | SFL+SFLCTL+SFLMSG三件套 |
| 3 | 功能键定义 | F3=退出, F5=刷新, F12=返回 |
| 4 | 消息显示 | 使用消息子文件，不使用SNDPGMMSG |

### 3.2 子文件规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | SFLSIZ | 子文件总行数 |
| 2 | SFLPAG | 每页显示行数 |
| 3 | SFLRCDNBR | 当前记录号（控制翻页和光标位置） |
| 4 | SFLEND | 子文件结束标志 |
| 5 | SFLCLR | 清除子文件标志 |

---

## 4. 编译顺序规范

### 4.1 编译依赖关系

| 对象类型 | 依赖 | 编译命令 |
|---------|------|---------|
| PF | 无 | CRTPF |
| LF | PF | CRTLF |
| DSPF | 无 | CRTDSPF |
| PRTF | 无 | CRTPRTF |
| MODULE | 无 | CRTRPGMOD |
| SRVPGM | MODULE | CRTSRVPGM |
| PGM | MODULE/SRVPGM | CRTBNDRPG |

### 4.2 编译顺序规则

| # | 规则 | 约束 |
|---|------|------|
| 1 | 先编译文件 | PF→LF→DSPF/PRTF |
| 2 | 再编译模块 | RPGMOD/CLMOD |
| 3 | 创建服务程序 | CRTSRVPGM |
| 4 | 最后编译程序 | CRTBNDRPG |
| 5 | 编译前备份 | 修改前先备份旧版源码 |

---

## 5. 库结构规范

### 5.1 库命名规范

| 环境 | 库名格式 | 示例 |
|------|---------|------|
| 开发 | DEV{应用名} | DEVAPP |
| 测试 | TST{应用名} | TSTAPP |
| 生产 | PRD{应用名} | PRDAPP |

### 5.2 源文件规范

| 源文件名 | 存放的Source Type | 说明 |
|----------|-------------------|------|
| QRPGLESRC | RPGLE, RPGMOD, SQLRPGLE | RPG源码 |
| QCLLESRC | CLLE, CLMOD | ILE CL源码 |
| QDDSSRC | PF, LF, DSPF, PRTF | DDS源码 |
| QCMDSRC | CMD | 命令定义源码 |
| QSRVSRC | BND | Binder Language源码 |

### 5.3 IFS目录结构（现代项目）

```
/home/project/
├── src/
│   ├── rpg/          ← RPG源码
│   ├── cl/           ← CL源码
│   ├── dds/          ← DDS源码
│   ├── sql/          ← SQL脚本
│   └── cmd/          ← 命令定义
├── make/             ← 编译脚本
├── test/             ← 测试脚本
├── doc/              ← 文档
└── config/           ← 配置文件
```

---

## 6. 文档产出规范

### 6.1 文档目录

| 目录 | 用途 |
|------|------|
| agent-doc/ibmi/ | IBM i专属文档根目录 |
| agent-doc/ibmi/dds-spec/ | DDS规格书 |
| agent-doc/ibmi/program-map/ | 程序调用关系 |
| agent-doc/ibmi/screen-spec/ | 5250画面规格 |
| agent-doc/ibmi/compile-order/ | 编译顺序 |
| agent-doc/ibmi/library-structure/ | 库结构清单 |

### 6.2 文档命名规范

| 文档类型 | 命名格式 | 示例 |
|---------|---------|------|
| DDS规格书 | {项目}-{日期}-pf-spec.md | myproject-20260725-pf-spec.md |
| 程序调用关系 | {项目}-{日期}-call-map.md | myproject-20260725-call-map.md |
| 5250画面规格 | {项目}-{日期}-screen-layout.md | myproject-20260725-screen-layout.md |
| 编译顺序 | {项目}-{日期}-compile-sequence.md | myproject-20260725-compile-sequence.md |
| 库结构清单 | {项目}-{日期}-library-inventory.md | myproject-20260725-library-inventory.md |

### 6.3 文档模板

详见 `agent-doc/ibmi/` 目录下的各模板文件。

---

## 7. SSH连接规范

### 7.1 连接配置

| 配置项 | 说明 |
|--------|------|
| IBM_I_HOST | 主机地址 |
| IBM_I_USER | SSH用户名 |
| IBM_I_KEY | SSH密钥路径 |
| IBM_I_LIB | 默认目标库 |
| IBM_I_ASP | ASP Group名称 |

### 7.2 多环境配置

```
项目根目录/
├── ibmi-connection.env          # 默认环境
├── ibmi-connection.dev.env      # 开发环境
├── ibmi-connection.test.env     # 测试环境
└── ibmi-connection.prod.env     # 生产环境
```

### 7.3 ASP路径规则

- 无ASP Group：`/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR`
- 有ASP Group：`/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR`

---

## 8. 安全规范

| # | 规则 | 约束 |
|---|------|------|
| 1 | 使用*LIBL管理库列表 | 不硬编码库名，使用库列表 |
| 2 | 采用最小权限原则 | 程序采用*USER配置，按需授权 |
| 3 | 敏感数据加密 | 使用IBM i加密API或字段级加密 |
| 4 | 审计日志 | 使用日志(JRN)记录所有数据变更 |
| 5 | 程序采用*OWNER权限 | 采用USRPRF(*OWNER)使程序以所有者权限运行 |
| 6 | 输入校验 | 所有外部输入必须校验长度、类型和范围 |

---
name: ibmi-development
description: 'IBM i (AS/400)企业级开发，涵盖ILE RPG自由格式、CL程序、DDS文件定义、嵌入式SQL、服务程序、子文件、数据队列等。当需要实现IBM i平台功能代码时使用。'
---

# ibmi-development

## 适用Agent
IBM i开发Agent

## 触发条件
任务分配Agent产出任务分配文档后，按分配顺序轮到IBM i任务时触发。

## 前置检查

| 序号 | 检查项 | 执行方式 |
|------|--------|----------|
| 1 | 知识库完整性 | 确认`.ai-team/knowledge-base/domain/ibm-i-development-guide.md`存在且可读 |
| 2 | 项目状态 | 检查 `output/code/` 下是否已有IBM i项目结构，若无则执行项目初始化 |
| 3 | SSH连接 | 确认用户提供了IBM i主机地址和用户名，通过`ssh user@host "system \"WRKSYSVAL SYSVAL(QMAXSIGN)\""`验证连接可用 |
| 4 | ASP Group确认 | 确认IBM i服务器的ASP Group名称（从ibmi-connection.env中的IBM_I_ASP获取），若服务器使用ASP Group则IFS路径必须加`/{ASP}`前缀。通过`ssh user@host "system \"WRKASP BRM\""`确认ASP名称 |
| 5 | 目标库确认 | 确认要操作的IBM i库名（从用户请求或技术设计中获取），通过`ssh user@host "system \"DSPOBJD OBJ(libname) OBJTYPE(*LIB)\""`验证库存在 |
| 6 | 环境确认 | 确认当前操作的目标环境：①未指定环境时使用默认环境（`ibmi-connection.env`）；②用户指令中指定环境时（如"在test环境编译"）读取对应的`ibmi-connection.{env}.env`；③涉及多环境对比时（如"对比dev和prod"），分别读取两个环境的配置文件 |
| 7 | 现有代码理解 | 通过SSH连接IBM i探索现有代码：①列出源文件：`ssh user@host "qsh -c 'for f in /{ASP}/QSYS.LIB/LIB.LIB/*.FILE; do basename $f .FILE; done'"`；②列出成员：`ssh user@host "qsh -c 'for m in /{ASP}/QSYS.LIB/LIB.LIB/SRCFILE.FILE/*.MBR; do basename $m .MBR; done'"`；③读取相关源码：`ssh user@host "cat /{ASP}/QSYS.LIB/LIB.LIB/SRCFILE.FILE/MBR.MBR"`；④查看字段定义：`ssh user@host "system \"DSPFFD FILE(LIB/FILENAME)\""`；⑤分析现有代码的命名风格和编码模式 |

## 项目初始化（仅首次）

当IBM i项目尚未初始化时，按以下步骤创建项目骨架：

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| I-1 | 创建项目目录 | 在 `output/code/{项目名}/` 下创建目录结构：`src/qddssrc/`、`src/qrpglesrc/`、`src/qcllesrc/`、`src/qcmdsrc/`、`src/qsrvsrc/`、`src/qsqlsrc/`、`compile/`、`doc/` |
| I-2 | 创建连接配置 | ①创建 `ibmi-connection.env.example`（提交到Git），内容见下方；②在对话框直接输出下方提示信息给用户 |

**ibmi-connection.env.example 内容：**
```bash
IBM_I_HOST=<your-ibmi-host>
IBM_I_USER=<your-username>
IBM_I_KEY=<path-to-ssh-key,留空则使用默认密钥>
IBM_I_LIB=<default-library>
IBM_I_ASP=<asp-group-name,无ASP Group则留空>
```

**I-2 初始化时必须输出给用户的提示信息（直接输出到对话框）：**

> **IBM i项目连接配置已创建！请完成以下步骤：**
>
> 1. 复制 `ibmi-connection.env.example` 为 `ibmi-connection.env` 并填写实际值（默认环境）
> 2. **如需多环境支持**，按 `ibmi-connection.{env}.env` 命名创建配置文件，例如：
>    - `ibmi-connection.dev.env` — 开发环境
>    - `ibmi-connection.test.env` — 测试环境
>    - `ibmi-connection.prod.env` — 生产环境
> 3. **配置项说明：**
>    - `IBM_I_HOST` — IBM i主机地址
>    - `IBM_I_USER` — SSH用户名
>    - `IBM_I_KEY` — SSH密钥路径（留空则使用默认密钥 `~/.ssh/id_ed25519` 或 `~/.ssh/id_rsa`）
>    - `IBM_I_LIB` — 默认目标库
>    - `IBM_I_ASP` — ASP Group名称（留空表示无ASP Group，IFS路径不加前缀）
> 4. 确保IBM i上SSH服务已启动（5250执行 `WRKTCPSVC *SSHD` 检查，`STRTCPSVR SERVER(*SSHD)` 启动）
> 5. 建议配置SSH密钥免密登录：
>    - 生成密钥：`ssh-keygen -t ed25519 -f ~/.ssh/ibmi_key`
>    - 复制公钥：`ssh-copy-id -i ~/.ssh/ibmi_key.pub 用户名@主机地址`
> 6. 所有 `ibmi-connection*.env` 文件已加入.gitignore不会提交到Git

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| I-3 | 创建库结构说明 | 在 `doc/` 目录创建 `library-structure.md`，定义库名规范、源文件组织、对象命名规范。通过SSH读取服务器上的实际库结构填充 |
| I-4 | 创建消息文件定义 | 在 `src/qddssrc/` 创建消息文件消息定义文档，统一消息ID编号规范（APP0001-APP3999） |

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 读取任务定义 | 读取`output/task/`下最新任务分配文档，提取分配给IBM i开发Agent的任务列表及其依赖的技术设计章节 |
| 2 | 读取技术设计 | 读取`output/technical-design/`下最新技术设计文档，提取与当前任务相关的数据模型定义、接口定义和业务规则 |
| 3 | 读取知识库 | 读取`.ai-team/knowledge-base/domain/ibm-i-development-guide.md`获取IBM i开发规范、命名规范、编译命令、SSH操作手册等参考信息 |
| 3a | 探索现有代码(SSH) | 通过SSH连接IBM i探索与任务相关的现有代码（SSH参数从指定环境的配置文件获取）：①搜索相关程序：`ssh user@host "grep -rl '关键词' /{ASP}/QSYS.LIB/LIB.LIB/SRCFILE.FILE/"`；②读取相关源码：`ssh user@host "cat /{ASP}/QSYS.LIB/LIB.LIB/SRCFILE.FILE/MBR.MBR"`；③查看PF字段定义：`ssh user@host "system \"DSPFFD FILE(LIB/PFNAME)\""`；④查看现有服务程序导出：`ssh user@host "system \"DSPSRVPGM SRVPGM(LIB/SRVPGM) DETAIL(*PROCEXP)\""`；⑤分析现有代码风格确保一致 |
| 3b | 多环境对比(可选) | 当用户要求对比不同环境的代码或数据时：①分别从两个环境读取源码到本地临时文件；②使用diff对比差异；③输出对比结果。参照知识库21.3.2节 |
| 4 | 编写DDS文件定义 | 根据技术设计中的数据模型，按依赖顺序编写：①物理文件(PF) - 定义表结构和字段，写入`src/qddssrc/`；②逻辑文件(LF) - 定义视图和索引，写入`src/qddssrc/`；③显示文件(DSPF) - 定义5250界面，使用子文件模式，写入`src/qddssrc/`；④打印文件(PRTF) - 定义报表输出格式，写入`src/qddssrc/` |
| 5 | 编写服务程序 | 识别可复用业务逻辑，编写ILE RPG服务程序：①使用`**FREE`自由格式；②使用`Ctl-Opt NoMain`；③过程用`Dcl-Proc ... Export`导出；④编写Binder Language(BND)源码；⑤写入`src/qrpglesrc/`和`src/qsrvsrc/` |
| 6 | 编写RPG主程序 | 根据功能需求编写ILE RPG程序：①使用`**FREE`自由格式；②使用`Ctl-Opt Main(procName)`；③定义文件(Dcl-F)、数据结构(Dcl-Ds)、变量(Dcl-S)、常量(Dcl-C)、原型(Dcl-Pr)；④实现主过程和子过程；⑤子过程命名PascalCase，子程序命名S+4位编号；⑥错误处理使用Monitor/On-Error；⑦写入`src/qrpglesrc/` |
| 7 | 编写嵌入式SQL | 需要复杂数据操作时编写SQLRPGLE：①使用游标处理多行；②检查SQLSTATE而非SQLCODE；③批量操作使用PREPARE+EXECUTE；④事务使用COMMIT/ROLLBACK；⑤写入`src/qrpglesrc/` |
| 8 | 编写CL程序 | 需要作业控制、对象管理或程序调度时编写CLLE：①使用SELECT-WHEN多分支；②每个命令后加MONMSG；③错误使用SNDPGMMSG *ESCAPE传递；④避免硬编码库名；⑤写入`src/qcllesrc/` |
| 9 | 编写命令定义 | 需要自定义CL命令时编写CMD源码：①定义命令参数；②编写命令处理程序(CPP)；③写入`src/qcmdsrc/` |
| 10 | 生成编译命令 | 在`compile/`目录生成编译脚本，按依赖顺序排列：①CRTPF(物理文件) → ②CRTLF(逻辑文件) → ③CRTDSPF/CRTPRTF(显示/打印文件) → ④CRTRPGMOD(模块) → ⑤CRTSRVPGM(服务程序) → ⑥CRTBNDRPG(程序)，每个编译命令包含完整参数 |
| 11 | 部署到IBM i(SSH) | 通过SSH将源码部署到IBM i（SSH参数从指定环境的配置文件获取）：①scp上传源码到IBM i IFS临时目录：`scp output/code/{项目名}/src/qrpglesrc/ORDADD.rpgle user@host:/tmp/ORDADD.src`；②CPYFRMSTMF写入Source PF成员：`ssh user@host "system \"CPYFRMSTMF FROMSTMF('/tmp/ORDADD.src') TOMBR('/{ASP}/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""`；③对每个源文件重复上述步骤 |
| 12 | 编译验证(SSH) | 通过SSH在IBM i上编译并验证（SSH参数从指定环境的配置文件获取）：①按依赖顺序执行编译命令：`ssh user@host "system \"CRTBNDRPG PGM(DEVAPP/ORDADD) SRCFILE(DEVAPP/QRPGLESRC) SRCMBR(ORDADD) TGTRLS(*CURRENT) DBGVIEW(*SOURCE)\" 2>&1; echo \"COMPILE_RC=$?\""`；②检查编译返回码，RC=0成功；③若失败，查看编译清单定位错误 |
| 13 | 代码输出 | 所有源码文件写入`output/code/`目录下对应子目录，编译结果记录到编译日志 |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | RPG编码规范 | 必须使用**FREE自由格式，遵循`.ai-team/knowledge-base/domain/ibm-i-development-guide.md`中的命名和编码规范 |
| 2 | DDS编码规范 | 字段名不超过10字符，日期用L类型，金额用P类型，PF必须有键，DSPF使用消息子文件 |
| 3 | CL编码规范 | 所有变量先DCL声明，命令后加MONMSG，使用SELECT-WHEN，不硬编码库名 |
| 4 | 禁止伪代码 | 所有代码必须可编译运行，不得出现TODO、FIXME、mock实现 |
| 5 | 注释 | 每个程序/过程/文件必须有头部注释（名称、功能、作者、日期、修改历史） |
| 6 | 错误处理 | RPG使用Monitor/On-Error，CL使用MONMSG，消息使用MSGF统一管理 |
| 7 | 编译命令 | 必须提供完整编译命令，包含所有必要参数（PGM、SRCFILE、SRCMBR、TGTRLS、DBGVIEW等） |
| 8 | 依赖顺序 | 文件先于程序，模块先于服务程序，服务程序先于绑定程序 |
| 9 | 命名规范 | PF:大写+PF后缀，PGM:动词+名词，变量:Wk+名称，常量:CONST_+名称，过程:PascalCase |
| 10 | SQL规范 | 使用SQLSTATE检查状态，使用游标处理多行，使用预编译防注入 |
| 11 | SSH操作 | 部署和编译通过SSH执行，参照知识库第二十一章的SSH命令手册 |
| 12 | 多环境操作 | 操作时须确认目标环境，SSH参数从对应`ibmi-connection.{env}.env`获取；多环境对比参照知识库21.3.2节 |

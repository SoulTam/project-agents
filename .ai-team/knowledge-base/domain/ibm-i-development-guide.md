# IBM i (AS/400) 企业级开发完全指南

> 本文档为AI团队提供IBM i平台企业级开发所需的全部知识体系，涵盖开发语言、Source Type、Object Type、编译命令、代码规范、最佳实践等。

---

## 一、平台概述

### 1.1 IBM i 架构核心概念

| 概念 | 说明 |
|------|------|
| **IBM i** | 运行于Power Systems（原AS/400）上的集成操作系统，前身OS/400 |
| **AS/400** | Application System/400，IBM于1988年发布的中端服务器，后更名为iSeries→System i→Power Systems |
| **TIMI** | Technology Independent Machine Interface，技术独立机器接口，使程序与底层硬件解耦 |
| **SLIC** | System Licensed Internal Code，TIMI下方的系统微码层 |
| **Single-level Store** | 单级存储，所有对象共享单一地址空间，无文件系统与传统内存之分 |
| **Library** | 库，IBM i上的对象容器，类似于目录/Schema，最多容纳约1670万个对象 |
| **Object** | 对象，IBM i上一切皆为对象（程序、文件、队列、命令等），每个对象有类型和属性 |
| **IFS** | Integrated File System，集成文件系统，支持流式文件（类似Unix/Windows文件系统） |
| **Subsystem** | 子系统，控制作业运行的运行环境，分配资源 |
| **Job** | 作业，IBM i上所有工作的基本执行单元 |
| **Spool File** | 假脱机文件，打印输出的队列文件 |

### 1.2 IBM i 版本演进

| 时期 | 名称 | 版本 |
|------|------|------|
| 1988-2000 | AS/400 | OS/400 V1R1 ~ V4R5 |
| 2000-2004 | iSeries | OS/400 V5R1 ~ V5R3 |
| 2004-2006 | System i | i5/OS V5R4 |
| 2008-2010 | Power Systems | IBM i 6.1 |
| 2010-2014 | Power Systems | IBM i 7.1 |
| 2014-2018 | Power Systems | IBM i 7.2, 7.3 |
| 2018-2024 | Power Systems | IBM i 7.4, 7.5 |

---

## 二、Source Type 完整参考

### 2.1 物理文件源类型

| Source Type | 说明 | 用途 | 示例 |
|-------------|------|------|------|
| **PF** | Physical File | 物理文件定义（数据表），包含字段定义和键值 | 客户主文件、订单文件 |
| **LF** | Logical File | 逻辑文件定义（视图/索引），基于PF建立 | 按客户名排序的视图 |
| **DSPF** | Display File | 显示文件定义（5250终端界面），定义屏幕布局和字段 | 菜单屏幕、录入画面 |
| **PRTF** | Printer File | 打印文件定义，控制报表输出格式 | 销售报表、月结报表 |
| **ICFF** | ICF File | ICF通信文件定义，用于SNA/APPC通信 | 与外部系统的通信定义 |

### 2.2 程序源类型

| Source Type | 说明 | 语言 | 特征 |
|-------------|------|------|------|
| **RPGLE** | RPG IV (ILE RPG) | ILE RPG | 现代RPG，自由格式(Free-Format)，IBM i最主要开发语言 |
| **RPG** | RPG III | OPM RPG | 旧版RPG，固定格式，不推荐新项目使用 |
| **CLLE** | ILE CL | ILE CL | Control Language程序，系统操作、调用程序、管理对象 |
| **CL** | OPM CL | OPM CL | 旧版CL程序 |
| **CBLLE** | ILE COBOL | ILE COBOL | COBOL程序（ILE环境） |
| **CBL** | OPM COBOL | OPM COBOL | 旧版COBOL程序 |
| **C** | ILE C | ILE C | C语言程序 |
| **CPP** | ILE C++ | ILE C++ | C++程序 |
| **CLP** | CL Program | CL | OPM CL程序源码 |
| **CLMOD** | CL Module | ILE CL | ILE CL模块源码 |
| **RPGMOD** | RPG Module | ILE RPG | ILE RPG模块源码（不含主过程） |
| **SQLRPGLE** | SQL RPG | Embedded SQL + RPG | 内嵌SQL的RPG程序 |
| **SQLCBLLE** | SQL COBOL | Embedded SQL + COBOL | 内嵌SQL的COBOL程序 |
| **SQLCLI** | SQL CLI | C + SQL CLI | 使用CLI接口的C程序 |
| **SQL** | SQL Script | SQL | 纯SQL脚本 |
| **RPG38** | RPG/38 | RPG II | System/38兼容RPG（遗留） |
| **CBL38** | COBOL/38 | COBOL | System/38兼容COBOL（遗留） |

### 2.3 其他源类型

| Source Type | 说明 | 用途 |
|-------------|------|------|
| **CMD** | Command Definition | 自定义CL命令定义 |
| **PNLGRP** | Panel Group | UIM面板组（帮助文本、菜单定义） |
| **MENU** | Menu Definition | 菜单定义源码 |
| **BND** | Binder Language | 服务程序导出接口定义 |
| **DTAARA** | Data Area | 数据区源码定义（通常直接创建而非从源码编译） |
| **TXT** | Text | 纯文本源码 |
| **LF** | Logical File | 逻辑文件 |
| **BNDIR** | Binding Directory | 绑定目录（列出一组模块和服务程序） |

---

## 三、Object Type 完整参考

### 3.1 程序类对象

| Object Type | 说明 | 由什么Source Type编译而来 | 创建命令 |
|-------------|------|--------------------------|----------|
| **\*PGM** | Program | RPGLE→RPG程序, CLLE→CL程序, CBLLE→COBOL程序, C→C程序 | CRTBNDRPG, CRTBNDCL, CRTBNDCBL, CRTBNDC |
| **\*MODULE** | Module | RPGMOD→RPG模块, CLMOD→CL模块 | CRTRPGMOD, CRTCLMOD, CRTCBLMOD |
| **\*SRVPGM** | Service Program | 由一个或多个\*MODULE绑定创建 | CRTSRVPGM |
| **\*FILE** | File | PF→物理文件, LF→逻辑文件, DSPF→显示文件, PRTF→打印文件 | CRTPF, CRTLF, CRTDSPF, CRTPRTF |
| **\*CMD** | Command | CMD源码 | CRTCMD |
| **\*MENU** | Menu | MENU源码 | CRTMNU |
| **\*PNLGRP** | Panel Group | PNLGRP源码 | CRTPNLGRP |
| **\*BND** | Binding Directory | BND源码 | CRTBNDDIR |
| **\*DTAARA** | Data Area | 无源码 | CRTDTAARA |
| **\*DTAQ** | Data Queue | 无源码 | CRTDTAQ |
| **\*MSGQ** | Message Queue | 无源码 | CRTMSGQ |
| **\*MSGF** | Message File | 无源码 | CRTMSGF |
| **\*JOBQ** | Job Queue | 无源码 | CRTJOBQ |
| **\*OUTQ** | Output Queue | 无源码 | CRTOUTQ |
| **\*LIB** | Library | 无源码 | CRTLIB |
| **\*AUTL** | Authorization List | 无源码 | CRTAUTL |
| **\*JRN** | Journal | 无源码 | CRTJRN |
| **\*JRNRCV** | Journal Receiver | 无源码 | CRTJRNRCV |
| **\*USRPRF** | User Profile | 无源码 | CRTUSRPRF |
| **\*SBSD** | Subsystem Description | 无源码 | CRTSBSD |
| **\*CLS** | Class | 无源码 | CRTCLS |
| **\*JOBD** | Job Description | 无源码 | CRTJOBD |
| **\*SBMJOB** | Submit Job | 命令 | SBMJOB |

### 3.2 文件类对象子类型

| 文件类型 | 属性值 | 说明 |
|----------|--------|------|
| Physical File | PF-DTA / PF-SRC | 数据物理文件 / 源物理文件 |
| Logical File | LF | 逻辑视图文件 |
| Display File | DSPF | 5250显示文件 |
| Printer File | PRTF | 打印输出文件 |
| ICF File | ICFF | 通信文件 |

---

## 四、编译命令完整参考

### 4.1 程序编译命令

| 编译命令 | Source Type | 产出Object Type | 说明 |
|----------|-------------|-----------------|------|
| **CRTBNDRPG** | RPGLE / SQLRPGLE | \*PGM | 创建ILE RPG程序（单模块绑定），最常用 |
| **CRTRPGMOD** | RPGMOD / RPGLE | \*MODULE | 创建ILE RPG模块（供服务程序或程序绑定） |
| **CRTBNDCL** | CLLE | \*PGM | 创建ILE CL程序 |
| **CRTCLMOD** | CLMOD / CLLE | \*MODULE | 创建ILE CL模块 |
| **CRTCLPGM** | CLP | \*PGM | 创建OPM CL程序（旧版） |
| **CRTBNDCBL** | CBLLE / SQLCBLLE | \*PGM | 创建ILE COBOL程序 |
| **CRTCBLMOD** | CBLMOD | \*MODULE | 创建ILE COBOL模块 |
| **CRTBNDC** | C | \*PGM | 创建ILE C程序 |
| **CRTCMOD** | C | \*MODULE | 创建ILE C模块 |
| **CRTCPPMOD** | CPP | \*MODULE | 创建ILE C++模块 |
| **CRTPGM** | 多个\*MODULE | \*PGM | 将多个模块绑定创建程序 |
| **CRTSRVPGM** | 多个\*MODULE | \*SRVPGM | 创建服务程序（类似DLL/SO） |

### 4.2 文件编译命令

| 编译命令 | Source Type | 产出Object Type | 说明 |
|----------|-------------|-----------------|------|
| **CRTPF** | PF | \*FILE (PF-DTA) | 创建物理文件 |
| **CRTLF** | LF | \*FILE (LF) | 创建逻辑文件 |
| **CRTDSPF** | DSPF | \*FILE (DSPF) | 创建显示文件 |
| **CRTPRTF** | PRTF | \*FILE (PRTF) | 创建打印文件 |
| **CRTICFF** | ICFF | \*FILE (ICFF) | 创建ICF文件 |

### 4.3 其他编译命令

| 编译命令 | Source Type | 产出Object Type | 说明 |
|----------|-------------|-----------------|------|
| **CRTCMD** | CMD | \*CMD | 创建命令 |
| **CRTMNU** | MENU | \*MENU | 创建菜单 |
| **CRTPNLGRP** | PNLGRP | \*PNLGRP | 创建面板组 |
| **CRTBNDDIR** | - | \*BNDDIR | 创建绑定目录 |

### 4.4 编译命令关键参数

#### CRTBNDRPG 关键参数

```
CRTBNDRPG PGM(lib/objname) 
          SRCFILE(lib/srcfile) 
          SRCMBR(mbrname)
          TGTRLS(*CURRENT/V7R5M0/...)
          OPTION(*EVENTF/*NOEVENTF)
          DBGVIEW(*SOURCE/*LIST/*STMT/*ALL/*NONE)
          OUTPUT(*PRINT/*NONE)
          REPLACE(*YES/*NO)
          ENBPFRCOL(*PEX/*NONE)
          OPTIMIZE(*FULL/*BASIC/*NONE)
          FIXNBR(*ZONED/*INPUTPACKED/*NONE)
          SRTSEQ(*LANGIDUNQ/*HEX/*LANGIDSHR/...)
          ALWNULL(*YES/*NO)
          BNDDIR(lib/bnddir)
          ACTGRP(*NEW/*CALLER/name)
          USRPRF(*USER/*OWNER)
          AUT(*ALL/*CHANGE/*USE/*EXCLUDE)
```

#### CRTPF 关键参数

```
CRTPF FILE(lib/filename) 
      SRCFILE(lib/srcfile) 
      SRCMBR(mbrname)
      RCDLEN(recordlength)    ← 无源码时指定记录长度
      MAXMBRS(*NOMAX/1/...) 
      SIZE(*NOMAX/num)
      IGCDTA(*YES/*NO)
      CCSID(*HEX/65535/...)
      AUT(*ALL/*CHANGE/*USE/*EXCLUDE)
      REUSEDLT(*YES/*NO)
      LOG(*YES/*NO)
```

#### CRTLF 关键参数

```
CRTLF FILE(lib/filename) 
      SRCFILE(lib/srcfile) 
      SRCMBR(mbrname)
      DTAMBRS(*ALL/(lib/pf1 lib/pf2 ...)) 
      MAXMBRS(*NOMAX/1/...)
      SHARE(*YES/*NO)
      MAINT(*IMMED/*REBUILD/*DLY)
```

---

## 五、RPG IV (ILE RPG) 开发规范

### 5.1 RPG IV 自由格式模板

```rpgle
**FREE
//=============================================================
// 程序名称: XXXXXXXX
// 功能描述: XXXXXXXXXXXXXXXX
// 创建日期: 2026-05-01
// 创建作者: XXX
// 修改历史:
//   日期       作者    描述
//   ---------  ------  --------------------
//   2026-05-01 XXX     初始创建
//=============================================================
Ctl-Opt Main(XXXXXXXX)            // 主过程入口
        ActGrp(*Caller)           // 活动组
        BndDir('STDBNDDIR')       // 绑定目录
        AlwNull(*Yes)             // 允许NULL值
        DbgView(*Source)          // 调试视图
        DftActGrp(*No)            // 不使用默认活动组
        Option(*NoDebugIo:*SrcStmt)  // 编译选项
        TimStamp(*ISO)            // 时间戳格式
        DatFmt(*ISO)              // 日期格式
        Pgmlvl(*SRC)              // 程序级别
        Text('程序描述');          // 程序描述

//-------------------------------------------------------------
// 文件定义
//-------------------------------------------------------------
Dcl-F CUSTPF   Usage(*Input)    Keyed;    // 客户主文件(只读)
Dcl-F ORDERPF  Usage(*Update)   Keyed;    // 订单文件(读写)
Dcl-F ORDDSPF  Usage(*Combine)  Keyed     // 订单画面文件
         InfDs(InfDs);                     // 信息数据结构

//-------------------------------------------------------------
// 数据结构定义
//-------------------------------------------------------------
Dcl-Ds InfDs      Likerec(ORDDSPF : *Input)  // 显示文件信息结构
        Qualified;
  Csrrr    Char(3)    Pos(369);               // 光标行
  Csrcl    Char(3)    Pos(371);               // 光标列
  Aid      Char(1)    Pos(369);               // 功能键AID
End-Ds;

Dcl-Ds WkResult   Qualified;                   // 工作结果结构
  Status   Char(1);                            // 处理状态
  MsgId    Char(7);                            // 消息ID
  MsgData  Char(100);                          // 消息数据
End-Ds;

//-------------------------------------------------------------
// 独立变量定义
//-------------------------------------------------------------
Dcl-S WkCustNo   Like(CUSTNO)    Inz;         // 客户编号
Dcl-S WkOrderNo  Like(ORDERNO)   Inz;         // 订单编号
Dcl-S WkRowCount Int(10)         Inz(0);      // 行计数
Dcl-S WkEof      Ind             Inz(*Off);   // EOF标志
Dcl-S WkError    Ind             Inz(*Off);   // 错误标志

//-------------------------------------------------------------
// 常量定义
//-------------------------------------------------------------
Dcl-C CONST_SUCCESS   '0';                     // 成功
Dcl-C CONST_ERROR     '1';                     // 错误
Dcl-C CONST_EOF       '9';                     // 文件结束

//-------------------------------------------------------------
// 原型定义（外部调用）
//-------------------------------------------------------------
Dcl-Pr ValidateOrder    ExtPgm('ORDVALID');    // 订单校验程序
  P_OrderNo    Like(ORDERNO);                  // 订单号
  P_Result     Char(1);                        // 校验结果
  P_MsgId      Char(7);                        // 消息ID
End-Pr;

//-------------------------------------------------------------
// 主过程
//-------------------------------------------------------------
Dcl-Proc XXXXXXXX;

  // 初始化
  WkResult.Status = CONST_SUCCESS;

  // 主处理循环
  Dow WkResult.Status = CONST_SUCCESS;
    Exsr S0100_ReadInput;
    If WkEof;
      Leave;
    Endif;
    Exsr S0200_ProcessData;
    Exsr S0300_WriteOutput;
  Enddo;

  // 结束处理
  Exsr S9999_Cleanup;
  *InLR = *On;    // 设置LR指示器=开，程序结束释放资源

End-Proc XXXXXXXX;

//-------------------------------------------------------------
// 子程序：读取输入
//-------------------------------------------------------------
S0100_ReadInput:
  Read CUSTPF;
  WkEof = *InEof;
  Return;

//-------------------------------------------------------------
// 子程序：处理数据
//-------------------------------------------------------------
S0200_ProcessData:
  // 业务逻辑处理
  ValidateOrder(WkOrderNo : WkResult.Status : WkResult.MsgId);
  If WkResult.Status = CONST_ERROR;
    WkError = *On;
  Endif;
  Return;

//-------------------------------------------------------------
// 子程序：写输出
//-------------------------------------------------------------
S0300_WriteOutput:
  Update ORDERPF;
  WkRowCount += 1;
  Return;

//-------------------------------------------------------------
// 子程序：清理
//-------------------------------------------------------------
S9999_Cleanup:
  // 关闭文件、清理资源
  Close CUSTPF;
  Close ORDERPF;
  Return;
```

### 5.2 RPG IV 编码规范

#### 5.2.1 命名规范

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| 物理文件(PF) | 3-5字母前缀+含义，全大写 | CUSTPF, ORDERPF, ITMMST |
| 逻辑文件(LF) | PF名+后缀 | CUSTPFL1, ORDERPFL2 |
| 显示文件(DSPF) | 功能名+DSPF | ORDDSPF, MNUDSPF |
| 打印文件(PRTF) | 功能名+PRTF | RPTPRTF, INVPRTF |
| 程序(PGM) | 动词+名词 | ORDADD, CUSTUPD, RPTPRT |
| 服务程序(SRVPGM) | 功能+SRV | CUSTSRV, UTILSRV |
| 模块(MODULE) | 功能+MOD | ORDMOD, VALIDMOD |
| 子过程(Procedure) | PascalCase | ValidateOrder, CalculateTotal |
| 子程序(Subroutine) | S+4位编号+动词 | S0100_ReadInput, S0200_Process |
| 变量 | Wk+名称（工作变量）, P_+名称（参数） | WkCustNo, P_OrderNo |
| 常量 | CONST_+名称 | CONST_SUCCESS, CONST_ERROR |
| 数据结构 | Ds+名称 或 功能+Ds | InfDs, WkResult |
| 指示器 | Wk+名称+Ind | WkEof, WkError |

#### 5.2.2 自由格式规则

1. **必须使用 `**FREE` 开头** — 所有新代码必须使用自由格式
2. **禁止使用固定格式** — 除非维护旧代码，否则不使用C-Spec固定格式
3. **每行不超过80字符** — 确保在5250终端和SEU中可读
4. **使用Dcl-F/Dcl-S/Dcl-Ds替代旧定义** — 不使用F-Spec/D-Spec固定格式
5. **使用Dcl-Pr/Dcl-Pi定义原型** — 所有外部调用必须声明原型
6. **使用Dcl-Proc/Dcl-EndProc定义过程** — 使用过程替代子程序

#### 5.2.3 指示器(Indicator)使用规范

| 规则 | 说明 |
|------|------|
| 禁止使用1-99号指示器作为通用变量 | 1-99号在DSPF中有特殊含义 |
| 使用命名指示器 | `Dcl-S WkEof Ind;` 代替 `*In99` |
| 文件EOF用*InEof | 系统提供，无需自定义 |
| 显示文件指示器用常量定义 | `Dcl-C F3_Exit '03';` 然后用 `*In03` |
| 避免指示器叠加逻辑 | 不允许多个指示器组合判断 |

#### 5.2.4 文件操作规范

| 操作 | 命令 | 说明 |
|------|------|------|
| 顺序读取 | `Read FileName;` | 顺序读取下一条记录 |
| 键值读取 | `Chain (KeyFields) FileName;` | 按键值直接定位 |
| 读取前一条 | `ReadP FileName;` | 反向读取 |
| 设置下限 | `SetLL (KeyFields) FileName;` | 定位到>=键值的位置 |
| 设置游标 | `SetGT (KeyFields) FileName;` | 定位到>键值的位置 |
| 写入 | `Write FileName;` | 写入新记录 |
| 更新 | `Update FileName;` | 更新当前锁定的记录 |
| 删除 | `Delete FileName;` | 删除当前锁定的记录 |
| 锁定读取 | `Chain (KeyFields) FileName;` | Chain自动锁定记录 |
| 无锁读取 | 在Dcl-F中指定`UsrOpn` + `Commit`控制 | 需配合事务控制 |

#### 5.2.5 错误处理规范

```rpgle
// 标准错误处理模式
Dcl-S WkErrorMsg  Char(256);

Monitor;
  Chain (WkCustNo) CUSTPF;
  If %Found(CUSTPF);
    // 处理找到的记录
  Else;
    // 处理未找到的情况
    WkResult.Status = CONST_ERROR;
    WkResult.MsgId  = 'CPF0001';
    WkResult.MsgData = '客户不存在: ' + WkCustNo;
  Endif;
On-Error;
  // 捕获运行时错误
  WkErrorMsg = %Error;
  WkResult.Status = CONST_ERROR;
  WkResult.MsgId  = 'RNL0001';
  WkResult.MsgData = %Subst(WkErrorMsg:1:80);
Endmon;
```

### 5.3 RPG IV 与嵌入式SQL

```rpgle
**FREE
Ctl-Opt Main(SqlExample)
        ActGrp(*Caller);

Dcl-S WkCustNo   Char(10);
Dcl-S WkCustName Char(50);
Dcl-S WkSqlState Char(5);
Dcl-S WkSqlCode  Int(10);

// 单行查询
Exec Sql
  Select CUSTNAME
    Into :WkCustName
    From CUSTPF
   Where CUSTNO = :WkCustNo;

// 检查SQL状态
WkSqlState = SqlState;
If WkSqlState >= '02000';
  // 未找到或错误
Endif;

// 游标查询
Exec Sql Declare C1 Cursor For
  Select CUSTNO, CUSTNAME
    From CUSTPF
   Where CUSTTYPE = :WkCustType
   Order By CUSTNO;

Exec Sql Open C1;

Dow SqlState = '00000';
  Exec Sql Fetch C1 Into :WkCustNo, :WkCustName;
  If SqlState <> '00000';
    Leave;
  Endif;
  // 处理每行数据
Enddo;

Exec Sql Close C1;

// INSERT
Exec Sql
  Insert Into ORDERPF (ORDERNO, CUSTNO, ORDERDATE, STATUS)
  Values(:WkOrderNo, :WkCustNo, Current Date, 'P');

// UPDATE
Exec Sql
  Update CUSTPF
     Set LASTORDER = Current Date
   Where CUSTNO = :WkCustNo;

// DELETE
Exec Sql
  Delete From ORDERPF
   Where STATUS = 'C' AND ORDDATE < Current Date - 365 Days;
```

---

## 六、CL (Control Language) 开发规范

### 6.1 CL程序模板

```cl
/*=================================================================*/
/* 程序名称: ORDMNT                                                 */
/* 功能描述: 订单维护控制程序                                        */
/* 创建日期: 2026-05-01                                            */
/* 创建作者: XXX                                                    */
/*=================================================================*/
PGM        PARM(&P_OPT &P_ORDERNO)

DCL        VAR(&P_OPT)      TYPE(*CHAR) LEN(1)     /* 操作选项 */
DCL        VAR(&P_ORDERNO)  TYPE(*CHAR) LEN(8)     /* 订单号   */
DCL        VAR(&W_ERROR)    TYPE(*LGL)  VALUE('0') /* 错误标志 */
DCL        VAR(&W_MSGID)    TYPE(*CHAR) LEN(7)     /* 消息ID   */
DCL        VAR(&W_MSGDTA)   TYPE(*CHAR) LEN(100)   /* 消息数据 */
DCL        VAR(&W_LIB)      TYPE(*CHAR) LEN(10)    /* 库名     */

/* 获取当前库名 */
RTVJOBA    CURLIB(&W_LIB)

/* 根据选项分支处理 */
SELECT
  WHEN COND(&P_OPT *EQ '1') THEN(DO)  /* 新增 */
    CALL PGM(ORDADD) PARM(&P_ORDERNO)
    MONMSG MSGID(CPF0000) EXEC(DO)
      SNDPGMMSG MSGID(CPF9898) MSGF(QCPFMSG) +
                MSGDTA('新增订单失败') +
                MSGTYPE(*ESCAPE)
    ENDDO
  ENDDO

  WHEN COND(&P_OPT *EQ '2') THEN(DO)  /* 修改 */
    CALL PGM(ORDUPD) PARM(&P_ORDERNO)
  ENDDO

  WHEN COND(&P_OPT *EQ '3') THEN(DO)  /* 删除 */
    CALL PGM(ORDDLT) PARM(&P_ORDERNO)
  ENDDO

  WHEN COND(&P_OPT *EQ '4') THEN(DO)  /* 查询 */
    CALL PGM(ORDQRY) PARM(&P_ORDERNO)
  ENDDO

  OTHERWISE CMD(DO)
    SNDPGMMSG MSGID(CPF9898) MSGF(QCPFMSG) +
              MSGDTA('无效的操作选项: ' *CAT &P_OPT) +
              MSGTYPE(*ESCAPE)
  ENDDO
ENDSELECT

/* 正常结束 */
EXIT:      RETURN

/* 异常结束 */
ERROR:
  SNDPGMMSG MSGID(CPF9898) MSGF(QCPFMSG) +
            MSGDTA(&W_MSGDTA) +
            MSGTYPE(*ESCAPE)
  RETURN

ENDPGM
```

### 6.2 CL编码规范

| 规则 | 说明 |
|------|------|
| 所有变量必须先声明再使用 | 使用DCL命令，指定TYPE和LEN |
| 使用MONMSG捕获错误 | 每个可能出错的命令后必须加MONMSG |
| 使用SNDPGMMSG报告错误 | 错误消息使用*ESCAPE类型向上传递 |
| 参数传递用PARM | 程序间参数用PGM的PARM定义 |
| 避免硬编码库名 | 使用RTVJOBA获取当前库，或使用*LIBL |
| 使用SELECT-WHEN替代IF-ELSE嵌套 | 多分支逻辑用SELECT更清晰 |
| CL中不执行复杂计算 | 复杂逻辑调用RPG程序处理 |

### 6.3 常用CL命令

| 类别 | 命令 | 说明 |
|------|------|------|
| 对象管理 | CRTLIB, DLTLIB, WRKLIB | 创建/删除/查看库 |
| 对象管理 | CRTDUPOBJ, CPYOBJ, DLTOBJ | 复制/删除对象 |
| 对象管理 | MOVOBJ, RNMOBJ | 移动/重命名对象 |
| 编译 | CRTBNDRPG, CRTRPGMOD, CRTBNDCL | 编译程序 |
| 编译 | CRTPF, CRTLF, CRTDSPF, CRTPRTF | 编译文件 |
| 作业管理 | SBMJOB, WRKJOB, ENDJOB | 提交/查看/结束作业 |
| 作业管理 | WRKACTJOB, WRKSBMJOB | 查看活动作业/提交的作业 |
| 文件操作 | CPYF, CLRPFM, RGZPFM | 复制文件/清空/重组 |
| 文件操作 | DSPFD, DSPFFD, WRKOBJ | 查看文件定义/字段定义 |
| 数据操作 | OPNQRYF, CPYFRMQRYF | 开放查询文件 |
| 消息 | SNDMSG, SNDBRKMSG, SNDPGMMSG | 发送消息 |
| 消息 | RCVMSG, WRKMSG | 接收/查看消息 |
| 源码管理 | WRKMBRPDM, STRSEU | 源码管理/编辑 |
| 源码管理 | CRTSRCPF, CPYSRCF | 创建/复制源文件 |
| 权限 | GRTOBJAUT, RVKOBJAUT | 授权/撤销权限 |
| 系统管理 | DSPSYSVAL, CHGSYSVAL | 查看/修改系统值 |
| 备份 | SAVOBJ, SAVLIB, RSTOBJ, RSTLIB | 备份/恢复 |

---

## 七、DDS (Data Description Specifications) 开发规范

### 7.1 物理文件(PF)模板

```
     A****************************************************************
     A* 物理文件: CUSTPF - 客户主文件
     A* 创建日期: 2026-05-01
     A* 描述    : 存储客户基本信息
     A****************************************************************
     A          R CUSTREC                    /* 记录格式名 */
     A            CUSTNO      6A             /* 客户编号 */
     A            CUSTNAME   40A             /* 客户名称 */
     A            CUSTTYPE    1A             /* 客户类型 */
     A            ADDRESS    60A             /* 地址 */
     A            CITY       20A             /* 城市 */
     A            POSTCODE    6A             /* 邮编 */
     A            PHONE      15A             /* 电话 */
     A            EMAIL      50A             /* 邮箱 */
     A            CREDITLM   11P 2           /* 信用额度 */
     A            BALANCE    11P 2           /* 余额 */
     A            STATUS      1A             /* 状态 A-正常 S-停用 */
     A            CRTDATE     L              /* 创建日期 */
     A            CRTUSER    10A             /* 创建用户 */
     A            UPDDATE     L              /* 更新日期 */
     A            UPDUSER    10A             /* 更新用户 */
     A          K CUSTNO                      /* 主键 */
```

### 7.2 逻辑文件(LF)模板

```
     A****************************************************************
     A* 逻辑文件: CUSTPFL1 - 客户按名称排序
     A* 基于文件: CUSTPF
     A****************************************************************
     A          R CUSTREC                    /* 引用PF的记录格式 */
     A            CUSTNO      6A             /* 客户编号 */
     A            CUSTNAME   40A             /* 客户名称 */
     A            CUSTTYPE    1A             /* 客户类型 */
     A            STATUS      1A             /* 状态 */
     A          K CUSTNAME                    /* 主键-客户名称 */
     A          K CUSTNO                      /* 次键-客户编号 */
     A          S STATUS                     /* 选择条件 */
     A            COMP(EQ 'A')               /* 只选状态=A的记录 */
```

### 7.3 显示文件(DSPF)模板

```
     A****************************************************************
     A* 显示文件: ORDDSPF - 订单录入画面
     A****************************************************************
     A          DSPSIZ(24 80 *DS3)
     A          CF03(03 'F3=退出')
     A          CF05(05 'F5=刷新')
     A          CF12(12 'F12=返回')
     A          PRINT
     A*
     A          R S1HEADER                   /* 标题行 */
     A                                  1 27'订单录入'
     A                                      DSPATR(HI)
     A                                      DSPATR(UL)
     A                                  2  3'订单号:'
     A            ORDERNO     8   B  2 11
     A                                  3  3'客户编号:'
     A            CUSTNO      6   B  3 14
     A                                  3 25'客户名称:'
     A            CUSTNAME   40   O  3 35DSPATR(ND)
     A*
     A          R S1DETAIL                   /* 明细行 */
     A                                      SFL
     A            ITMNO       6   B  S  3
     A            ITMNAME    30   O  S 10DSPATR(ND)
     A            QTY         5Y 0B  S 42EDTWRD('     ')
     A            PRICE       7Y 2B  S 49EDTCDE(J)
     A            AMOUNT      9Y 2O  S 58EDTCDE(J)
     A*
     A          R S1CTL                      /* 子文件控制 */
     A                                      SFLCTL(S1DETAIL)
     A  31                                  SFLCLR
     A  32                                  SFLDSP
     A  33                                  SFLDSPCTL
     A N32                                  SFLINZ
     A  32                                  SFLEND(*MORE)
     A            SFLRRN      4S 0H  SFLRCDNBR(CURSOR)
     A                                  5  3'品号  品名' +
     A                                      '         数量     单价' +
     A                                      '       金额'
     A                                      DSPATR(UL)
     A                                  23  3'F3=退出 F5=刷新 F12=返回'
     A*
     A          R S1MSG                      /* 消息子文件 */
     A                                      SFL
     A            MSGKEY      4S 0H          SFLMSGKEY
     A            PGMQ       10A  H          SFLPGMQ
     A*
     A          R S1MSGCTL                   /* 消息子文件控制 */
     A                                      SFLCTL(S1MSG)
     A                                      SFLSIZ(5)
     A                                      SFLPAG(1)
     A  91                                  SFLDSP
     A  91                                  SFLCLR
     A  91                                  SFLEND
     A            PGMQ       10A  H          SFLPGMQ
     A                                      SFLMSGMSGF(QCPFMSG)
```

### 7.4 DDS编码规范

| 规则 | 说明 |
|------|------|
| 字段名不超过10字符 | IBM i字段名最大10字符 |
| 字段名应有业务含义 | CUSTNO而非FLD001 |
| 日期字段使用L类型 | L类型为ISO日期格式(10字节) |
| 金额字段使用P(压缩十进制) | 如`11P 2`表示9位整数+2位小数 |
| 每个PF必须有唯一键 | 在最后一行用K指定 |
| LF应基于PF字段 | 使用相同的记录格式名引用 |
| DSPF使用消息子文件 | 消息显示统一使用SFLMSG模式 |
| DSPF功能键使用CF | CF允许程序读取功能键AID |
| DSPF字段必须标注使用类型 | B-输入输出, I-仅输入, O-仅输出, H-隐藏 |
| 画面布局从顶部开始 | 标题→输入区→明细区→功能键提示→消息区 |

---

## 八、服务程序(Service Program)开发规范

### 8.1 服务程序结构

```rpgle
**FREE
//=============================================================
// 服务程序: CUSTSRV - 客户服务程序
//=============================================================
Ctl-Opt NoMain                          // 无主过程(服务程序)
        ActGrp(*Caller)
        BndDir('CUSTSRV')
        Option(*NoDebugIo:*SrcStmt)
        DatFmt(*ISO);

//-------------------------------------------------------------
// 原型定义(导出)
//-------------------------------------------------------------
Dcl-Pr GetCustomerInfo    ExtPgm('CUSTGET');
  P_CustNo    Like(CUSTNO);
  P_CustName  Like(CUSTNAME);
  P_Status    Char(1);
End-Pr;

Dcl-Pr ValidateCustomer   ExtPgm('CUSTVLD');
  P_CustNo    Like(CUSTNO);
  P_Result    Char(1);
End-Pr;

//-------------------------------------------------------------
// 全局文件定义
//-------------------------------------------------------------
Dcl-F CUSTPF Usage(*Input:*Update) Keyed UsrOpn;

//-------------------------------------------------------------
// 过程实现
//-------------------------------------------------------------
Dcl-Proc GetCustomerInfo Export;
  Dcl-Pi GetCustomerInfo;
    P_CustNo    Like(CUSTNO);
    P_CustName  Like(CUSTNAME);
    P_Status    Char(1);
  End-Pi;

  Dcl-S WkFound Ind Inz(*Off);

  Open CUSTPF;
  Chain (P_CustNo) CUSTPF;
  If %Found(CUSTPF);
    P_CustName = CUSTNAME;
    P_Status   = STATUS;
    WkFound    = *On;
  Else;
    P_CustName = *Blanks;
    P_Status   = *Blanks;
  Endif;
  Close CUSTPF;

  Return;
End-Proc GetCustomerInfo;

Dcl-Proc ValidateCustomer Export;
  Dcl-Pi ValidateCustomer;
    P_CustNo    Like(CUSTNO);
    P_Result    Char(1);
  End-Pi;

  Dcl-S WkStatus Char(1);

  GetCustomerInfo(P_CustNo : *Blanks : WkStatus);
  If WkStatus = 'A';
    P_Result = 'Y';
  Else;
    P_Result = 'N';
  Endif;

  Return;
End-Proc ValidateCustomer;
```

### 8.2 Binder Language模板

```
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('CUSTSRV_20260501')
  EXPORT SYMBOL("GETCUSTOMERINFO")
  EXPORT SYMBOL("VALIDATECUSTOMER")
ENDPGMEXP
```

### 8.3 服务程序编译步骤

```
/* 步骤1: 编译模块 */
CRTRPGMOD MODULE(mylib/CUSTSRV) 
          SRCFILE(mylib/QSRC) 
          SRCMBR(CUSTSRV)
          TGTRLS(*CURRENT)

/* 步骤2: 创建服务程序 */
CRTSRVPGM SRVPGM(mylib/CUSTSRV) 
          MODULE(mylib/CUSTSRV)
          SRCFILE(mylib/QSRC)
          SRCMBR(CUSTSRV)
          TGTRLS(*CURRENT)
          ACTGRP(*CALLER)
```

---

## 九、嵌入式SQL规范

### 9.1 SQL命名规范

| 规则 | 说明 |
|------|------|
| SQL表名使用系统命名 | `LIBRARY/FILENAME` 格式 |
| SQL变量以冒号前缀引用RPG变量 | `:WkCustNo` |
| 使用预编译语句防范SQL注入 | `Exec Sql Prepare S1 From :WkSqlStmt;` |
| 游标必须显式打开和关闭 | `Open C1; ... Close C1;` |
| 检查SQLSTATE而非SQLCODE | SQLSTATE是ANSI标准，更可移植 |
| 批量操作使用DECLARE + FETCH | 避免逐条执行INSERT/UPDATE |

### 9.2 SQLSTATE值含义

| SQLSTATE | 含义 | 处理方式 |
|----------|------|----------|
| 00000 | 成功 | 正常继续 |
| 01000 | 警告 | 记录日志，继续 |
| 02000 | 无数据 | 跳过或提示 |
| 23000 | 完整性约束违反 | 检查外键/唯一约束 |
| 23505 | 重复键值 | 提示记录已存在 |
| 40001 | 死锁 | 重试事务 |
| 57011 | 资源不可用 | 等待后重试 |
| 58004 | 系统错误 | 记录错误，通知管理员 |

---

## 十、ILE概念与程序绑定

### 10.1 ILE程序结构

```
ILE程序(*PGM)
├── 模块1(*MODULE) ← RPGMOD编译而来
├── 模块2(*MODULE) ← CLMOD编译而来
└── 服务程序(*SRVPGM) 引用
    ├── 导出过程A
    ├── 导出过程B
    └── ...
```

### 10.2 OPM vs ILE 对比

| 特性 | OPM (Original Program Model) | ILE (Integrated Language Environment) |
|------|------|------|
| 编译方式 | 单步编译为*PGM | 先编译*MODULE，再绑定为*PGM |
| 语言混合 | 不支持 | 支持RPG+CL+COBOL+C混合 |
| 服务程序 | 不支持 | 支持*SRVPGM（类似DLL） |
| 活动组 | 默认活动组 | 可自定义ACTGRP |
| 调用性能 | 每次调用初始化 | 可在*CALLER组中重用 |
| 错误处理 | *PSSR | Monitor/On-Error |
| 现代化 | 已过时 | 推荐使用 |

### 10.3 活动组(Activation Group)

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| \*NEW | 每次调用创建新组 | 独立运行的程序 |
| \*CALLER | 在调用者的组中运行 | 服务程序、工具程序 |
| 自定义名 | 指定组名 | 需要共享资源的程序组 |

### 10.4 绑定目录(Binding Directory)

```
/* 创建绑定目录 */
CRTBNDDIR BNDDIR(mylib/STDUTILS)
          TEXT('标准工具绑定目录')

/* 添加服务程序到绑定目录 */
ADDBNDDIRE BNDDIR(mylib/STDUTILS)
           OBJ((mylib/CUSTSRV *SRVPGM))
           
ADDBNDDIRE BNDDIR(mylib/STDUTILS)
           OBJ((mylib/DATEUTIL *SRVPGM))
```

---

## 十一、数据队列(Data Queue)通信

### 11.1 数据队列使用场景

| 场景 | 说明 |
|------|------|
| 异步处理 | 主程序写入订单队列，后台程序读取处理 |
| 系统集成 | 不同子系统间通过数据队列传递消息 |
| 批处理控制 | 批量作业通过队列分发任务 |
| 实时监控 | 监控程序读取队列中的告警信息 |

### 11.2 RPG中操作数据队列

```rpgle
// 使用QSNDDTAQ和QRCVDTAQ API
Dcl-Pr SendDataQ    ExtPgm('QSNDDTAQ');
  P_DQName    Char(10);         /* 数据队列名 */
  P_DQLib     Char(10);         /* 库名 */
  P_DQLen     Packed(5:0);      /* 数据长度 */
  P_DQData    Char(256);        /* 数据 */
  P_DQKeyLen  Packed(3:0) Options(*NoPass); /* 键长度 */
  P_DQKeyData Char(256)   Options(*NoPass); /* 键数据 */
End-Pr;

Dcl-Pr RcvDataQ     ExtPgm('QRCVDTAQ');
  P_DQName    Char(10);         /* 数据队列名 */
  P_DQLib     Char(10);         /* 库名 */
  P_DQLen     Packed(5:0);      /* 数据长度(输入/输出) */
  P_DQData    Char(256);        /* 接收数据 */
  P_DQWait    Packed(5:0);      /* 等待时间(秒) */
  P_DQKeyLen  Packed(3:0) Options(*NoPass); /* 键长度 */
  P_DQKeyOp   Char(2)     Options(*NoPass); /* 键操作 */
  P_DQKeyData Char(256)   Options(*NoPass); /* 键数据 */
  P_DQSndLen  Packed(3:0) Options(*NoPass); /* 发送者长度 */
  P_DQSndInf  Char(256)   Options(*NoPass); /* 发送者信息 */
End-Pr;
```

---

## 十二、IBM i开发最佳实践

### 12.1 安全最佳实践

| 实践 | 说明 |
|------|------|
| 使用*LIBL管理库列表 | 不硬编码库名，使用库列表 |
| 采用最小权限原则 | 程序采用*USER配置，按需授权 |
| 敏感数据加密 | 使用IBM i加密API或字段级加密 |
| 审计日志 | 使用日志(JRN)记录所有数据变更 |
| 程序采用*OWNER权限 | 采用USRPRF(*OWNER)使程序以所有者权限运行 |
| 输入校验 | 所有外部输入必须校验长度、类型和范围 |

### 12.2 性能最佳实践

| 实践 | 说明 |
|------|------|
| 使用SETLL+READ代替逐条CHAIN | 范围读取效率更高 |
| 逻辑文件选择/省略条件 | LF中使用SELECT/OMIT过滤数据 |
| 共享打开(SHARE(*YES)) | 多个程序共享同一次文件打开 |
| 批量提交 | 批处理每N条COMMIT一次 |
| 避免SEQUEL全表扫描 | 确保WHERE条件使用索引 |
| 使用OPNQRYF优化查询 | 在CL中使用OPNQRYF预过滤 |
| 合理使用_access路径维护 | MAINT(*IMMED/*DLY/*REBUILD)按需选择 |
| RGZPFM定期重组 | 删除大量记录后执行重组回收空间 |

### 12.3 可维护性最佳实践

| 实践 | 说明 |
|------|------|
| 所有程序必须有头部注释 | 包含名称、功能、作者、日期、修改历史 |
| 使用自由格式RPG | 新代码全部使用**FREE格式 |
| 模块化设计 | 使用服务程序封装公共逻辑 |
| 统一错误处理 | 使用消息文件(MSGF)集中管理错误消息 |
| 代码复用 | 公共功能提取为服务程序或过程 |
| 避免魔法数字 | 使用命名常量代替硬编码值 |
| 使用LIKEREC/LIKE引用字段 | 减少重复定义，保持一致性 |
| 文件字段使用REF引用 | PF中使用REF引用另一个文件的字段定义 |

### 12.4 事务处理最佳实践

```rpgle
// 使用COMMIT控制事务
Ctl-Opt Commit(*CS);  // 游标稳定性

// 事务开始(隐式)
Exec Sql
  Update ORDERPF
     Set STATUS = 'P'
   Where ORDERNO = :WkOrderNo;

// 检查并提交
If SqlState = '00000';
  Exec Sql Commit;
Else;
  Exec Sql Rollback;
Endif;
```

### 12.5 源码管理最佳实践

| 实践 | 说明 |
|------|------|
| 使用源物理文件(PF-SRC)管理源码 | 标准源文件：QRPGLESRC, QCLLESRC, QDDSSRC, QCMDSRC |
| 源码成员名即对象名 | 保持源码成员名和编译后对象名一致 |
| 使用PDM或RDp/RDi开发 | 避免直接使用SEU（仅5250终端可用） |
| 版本控制 | 建议使用RDi + Git或Alderstones Cambria |
| 编译前备份 | 修改前先备份旧版源码 |

---

## 十三、常见Source Physical File

| 源文件名 | 存放的Source Type | 说明 |
|----------|-------------------|------|
| QRPGLESRC | RPGLE, RPGMOD, SQLRPGLE | RPG源码 |
| QRPGSRC | RPG | 旧版RPG源码 |
| QCLLESRC | CLLE, CLMOD | ILE CL源码 |
| QCLSRC | CLP | OPM CL源码 |
| QDDSSRC | PF, LF, DSPF, PRTF, ICFF | DDS源码 |
| QCMDSRC | CMD | 命令定义源码 |
| QMENUSRC | MENU | 菜单源码 |
| QPNLSRC | PNLGRP | 面板组源码 |
| QCBLSRC | CBL, CBLLE, SQLCBLLE | COBOL源码 |
| QCASRC | C, CPP | C/C++源码 |
| QSQLSRC | SQL | SQL脚本 |
| QSRVSRC | BND | Binder Language源码 |
| QTXTSRC | TXT | 文本文档 |

---

## 十四、IBM i开发工具

### 14.1 原生开发工具

| 工具 | 说明 | 访问方式 |
|------|------|----------|
| **PDM** | Programming Development Manager | `STRPDM` |
| **SEU** | Source Entry Utility | `STRSEU` |
| **SDA** | Screen Design Aid | `STRSDA` |
| **RLU** | Report Layout Utility | `STRRLU` |
| **DFU** | Data File Utility | `STRDFU` |
| **Query** | Query/400 | `STRQRY` |
| **SQL** | Interactive SQL | `STRSQL` |
| **WRKMBRPDM** | 成员管理 | `WRKMBRPDM FILE(lib/srcfile)` |
| **WRKOBJPDM** | 对象管理 | `WRKOBJPDM LIB(lib)` |

### 14.2 现代开发工具

| 工具 | 说明 | 类型 |
|------|------|------|
| **RDi** | Rational Developer for i | Eclipse IDE |
| **VS Code** | IBM i Development extensions | VS Code + Code for IBM i |
| **ACS** | Access Client Solutions | IBM官方工具集 |
| **Merlin** | IBM i Modernization Engine | 云原生开发 |
| **Git** | 版本控制（通过RDi或IFS） | SCM |
| **Jenkins** | CI/CD | 自动化构建 |

---

## 十五、5250终端与绿屏开发

### 15.1 5250显示文件交互模型

```
用户操作 → DSPF读取输入 → RPG程序处理 → DSPF写入输出 → 用户查看
    ↑                                                    |
    |________________ F5刷新/F3退出 _____________________|
```

### 15.2 子文件(Subfile)编程模式

| 概念 | 说明 |
|------|------|
| SFL | 子文件记录格式，定义明细行 |
| SFLCTL | 子文件控制格式，控制显示/清除/翻页 |
| SFLDSP | 显示子文件 |
| SFLCLR | 清除子文件 |
| SFLDSPCTL | 显示控制格式 |
| SFLSIZ | 子文件总行数 |
| SFLPAG | 每页显示行数 |
| SFLRCDNBR | 当前记录号（控制翻页和光标位置） |
| SFLEND | 子文件结束标志 |
| SFLMSG | 消息子文件 |

### 15.3 子文件标准处理流程

```
1. 清除子文件(SFLCLR=*On → WRITE CTL → SFLCLR=*Off)
2. 加载数据到子文件(WRITE SFL)
3. 显示子文件(SFLDSP=*On, SFLDSPCTL=*On → WRITE CTL → READ CTL)
4. 处理用户输入(READ SFL → 处理修改 → UPDATE SFL)
5. 循环步骤3-4直到F3/F12
```

---

## 十六、IBM i与现代技术集成

### 16.1 集成方式总览

| 集成方式 | 说明 | 适用场景 |
|----------|------|----------|
| **REST API** | 通过ILEastic或RPG-Open-Framework提供REST服务 | 移动端/前端调用 |
| **Web Services** | IBM i原生Web Services服务器 | SOA集成 |
| **ODBC/JDBC** | 通过Db2 for i驱动访问数据 | 外部系统数据访问 |
| **MQ** | IBM MQ消息队列集成 | 异步消息集成 |
| **Data Queue** | 原生数据队列 | IBM i内部异步通信 |
| **PCML** | Program Call Markup Language | Java调用RPG程序 |
| **ILE C/Sockets** | Socket编程 | 自定义TCP/IP通信 |
| **IFS流文件** | 通过IFS交换文件 | 文件批处理集成 |
| **SMTP/POP3** | 邮件集成 | 发送通知邮件 |
| **SSH/SFTP** | 安全文件传输 | 跨平台文件交换 |

### 16.2 RPG调用REST API示例

```rpgle
**FREE
Ctl-Opt Main(HttpGetExample);

Dcl-S WkUrl       Varchar(1024);
Dcl-S WkResponse  Varchar(65535);
Dcl-S WkStatus    Int(10);

// 使用HTTPAPI库调用REST API
Dcl-Pr http_string    ExtProc('http_string');
  P_Method   Varchar(10)   Value;
  P_Url      Varchar(1024) Value;
  P_Data     Varchar(65535)Options(*Omit);
  P_Header   Varchar(4096) Options(*Omit);
End-Pr;

WkUrl = 'https://api.example.com/customers/' + WkCustNo;
http_string('GET' : WkUrl : *Omit : *Omit);
```

---

## 十七、编译与部署流程

### 17.1 标准编译流程

```
1. 创建/确认源物理文件
   CRTSRCPF FILE(mylib/QDDSSRC) TEXT('DDS源码')
   CRTSRCPF FILE(mylib/QRPGLESRC) TEXT('RPG源码')

2. 编译文件对象(按依赖顺序)
   CRTPF    FILE(mylib/CUSTPF) SRCFILE(mylib/QDDSSRC) SRCMBR(CUSTPF)
   CRTLF    FILE(mylib/CUSTPFL1) SRCFILE(mylib/QDDSSRC) SRCMBR(CUSTPFL1)
   CRTDSPF  FILE(mylib/ORDDSPF) SRCFILE(mylib/QDDSSRC) SRCMBR(ORDDSPF)

3. 编译模块
   CRTRPGMOD MODULE(mylib/ORDMOD) SRCFILE(mylib/QRPGLESRC) SRCMBR(ORDMOD)
   CRTRPGMOD MODULE(mylib/CUSTSRV) SRCFILE(mylib/QRPGLESRC) SRCMBR(CUSTSRV)

4. 创建服务程序
   CRTSRVPGM SRVPGM(mylib/CUSTSRV) MODULE(mylib/CUSTSRV) SRCFILE(mylib/QSRVSRC) SRCMBR(CUSTSRV)

5. 创建绑定目录
   CRTBNDDIR BNDDIR(mylib/STDBND)
   ADDBNDDIRE BNDDIR(mylib/STDBND) OBJ((mylib/CUSTSRV *SRVPGM))

6. 编译程序
   CRTBNDRPG PGM(mylib/ORDADD) SRCFILE(mylib/QRPGLESRC) SRCMBR(ORDADD) BNDDIR(mylib/STDBND)
```

### 17.2 编译错误排查

| 错误类型 | 排查方法 |
|----------|----------|
| 编译错误 | `WRKSPLF`查看编译清单, 找到错误行号和消息 |
| 运行时错误 | 查看作业日志 `DSPJOBLOG`, 查找MSGID |
| 文件不存在 | `WRKOBJ OBJ(*ALL/filename)` 搜索对象 |
| 权限不足 | `DSPOBJAUT OBJ(lib/obj) OBJTYPE(*type)` |
| 锁定冲突 | `WRKOBJLCK OBJ(lib/obj) OBJTYPE(*type)` |
| 活动组错误 | 检查ACTGRP设置, 使用`WRKACTJOB`查看活动组 |

---

## 十八、消息管理规范

### 18.1 消息文件使用

```
/* 创建消息文件 */
CRTMSGF MSGF(mylib/APPMSGF) TEXT('应用程序消息文件')

/* 添加消息 */
ADDMSGD MSGID(APP0001) MSGF(mylib/APPMSGF) +
        MSG('客户编号 &1 不存在') +
        FMT((*CHAR 10)) +
        SEV(20) +
        ALROPT(*NO)

/* 在RPG中使用 */
Dcl-S WkMsgDta  Char(10);

WkMsgDta = WkCustNo;
SND-MSG MSGID(APP0001) MSGF(mylib/APPMSGF) MSGDTA(WkMsgDta);
```

### 18.2 消息ID编号规范

| 范围 | 类型 | 示例 |
|------|------|------|
| APP0001-APP0999 | 信息消息 | APP0001 - 处理开始 |
| APP1000-APP1999 | 警告消息 | APP1001 - 数据不完整 |
| APP2000-APP2999 | 错误消息 | APP2001 - 记录不存在 |
| APP3000-APP3999 | 严重错误 | APP3001 - 文件打开失败 |
| CPFxxxx | 系统消息 | CPF0001 - 对象不存在 |

---

## 十九、测试规范

### 19.1 测试类型

| 类型 | 工具/方法 | 说明 |
|------|-----------|------|
| 单元测试 | RDi Unit Test / ASSERT | 过程级测试 |
| 集成测试 | 交互式测试 | 程序间调用和数据流测试 |
| 回归测试 | 自动化测试脚本 | 确保修改不破坏现有功能 |
| 性能测试 | Performance Explorer (PEX) | 系统性能瓶颈分析 |
| 安全测试 | Authority检查 | 验证权限配置正确性 |

### 19.2 调试方法

| 方法 | 命令 | 说明 |
|------|------|------|
| 交互式调试 | `STRDBG PGM(lib/pgm)` | 交互式设置断点 |
| 批作业调试 | `STRSRVJOB` + `STRDBG` | 调试批处理作业 |
| 服务作业调试 | `STRSRVJOB JOB(n/n/n)` | 调试其他用户的作业 |
| 查看作业日志 | `DSPJOBLOG` | 查看运行时消息 |
| 查看编译清单 | `WRKSPLF` → 查看编译输出 | 排查编译错误 |

---

## 二十、项目目录结构标准

### 20.1 库结构标准

```
项目库命名: PRDAPP (生产) / TSTAPP (测试) / DEVAPP (开发)

DEVAPP/
├── QDDSSRC      ← DDS源码(PF, LF, DSPF, PRTF)
├── QRPGLESRC    ← RPG源码(RPGLE, SQLRPGLE)
├── QCLLESRC     ← CL源码(CLLE)
├── QCMDSRC      ← 命令定义源码(CMD)
├── QSRVSRC      ← Binder Language源码(BND)
├── QPNLSRC      ← 面板组源码(PNLGRP)
├── QMENUSRC     ← 菜单源码(MENU)
├── QSQLSRC      ← SQL脚本
├── QTXTSRC      ← 文档
├── 数据文件(PF)  ← 编译后的物理文件对象
├── 逻辑文件(LF)  ← 编译后的逻辑文件对象
├── 显示文件(DSPF)← 编译后的显示文件对象
├── 程序(*PGM)    ← 编译后的程序对象
├── 服务程序(*SRVPGM) ← 编译后的服务程序对象
├── 模块(*MODULE) ← 编译后的模块对象
├── 命令(*CMD)    ← 编译后的命令对象
└── 绑定目录(*BNDDIR) ← 绑定目录对象
```

### 20.2 IFS目录结构(现代项目)

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

## 二十一、SSH直连IBM i — AI团队远程开发方案

### 21.1 方案概述

AI团队通过SSH直接连接IBM i服务器的PASE(Portable Application Solutions Environment)环境，**无需本地源码镜像**，直接在远程服务器上完成所有操作：浏览源码、读取内容、搜索代码、编译程序、查看对象。

| 优势 | 说明 |
|------|------|
| 零同步开销 | 无需同步脚本，直接操作服务器上的源码 |
| 实时访问 | 看到的就是服务器上最新的代码 |
| 完整操作能力 | 浏览、读取、搜索、编译、查看对象一站式完成 |
| 无需额外插件 | 不依赖Code for IBM i扩展 |
| AI可自动编译 | 代码写完后直接编译验证 |

### 21.2 IBM i PASE环境与SSH

IBM i的PASE环境提供AIX兼容的Unix shell，SSH连接后默认进入PASE。

> **重要：ASP Group路径规则**
> 当IBM i服务器配置了ASP Group（IASP）时，所有IFS路径必须以ASP组名作为前缀：
> - 无ASP Group：`/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR`
> - 有ASP Group：`/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR`
>
> 可通过以下命令确认服务器是否使用ASP Group以及ASP名称：
> ```bash
> ssh user@host "system \"WRKASP BRM\""
> # 或查看IASP状态
> ssh user@host "system \"WRKCFGSTS CFGTYPE(*DEV) CFGD(*ASP)\""
> ```
>
> 本文档后续所有IFS路径示例均使用 `{ASP}/QSYS.LIB/...` 格式，其中 `{ASP}` 为ASP组名。

| 概念 | 说明 |
|------|------|
| **PASE** | Portable Application Solutions Environment，AIX兼容运行时 |
| **QSH** | QShell，IBM i原生Unix-like shell（非PASE） |
| **system命令** | 在PASE中调用CL命令的桥梁，如`system "DSPFD DEVAPP/QRPGLESRC"` |
| **ASP Group (IASP)** | Independent Auxiliary Storage Pool，独立存储池。配置了ASP Group的IBM i服务器，IFS路径必须先进入ASP组目录 |
| **/QSYS.LIB** | IFS中访问QSYS对象的路径。**有ASP Group时**：`/{ASP}/QSYS.LIB/{LIB}.LIB/...`；**无ASP Group时**：`/QSYS.LIB/{LIB}.LIB/...` |
| **db2命令** | 在PASE中执行SQL语句，如`db2 "SELECT * FROM DEVAPP.CUSTPF"` |

### 21.3 SSH连接配置

**在IBM i上确认SSH服务已启动**：
```
/* 在5250终端检查 */
WRKTCPSVC *SSHD
/* 若未启动 */
STRTCPSVR SERVER(*SSHD)
```

**配置SSH密钥免密登录**（本地执行）：
```bash
# 生成密钥对
ssh-keygen -t ed25519 -f ~/.ssh/ibmi_key

# 将公钥复制到IBM i
ssh-copy-id -i ~/.ssh/ibmi_key.pub DEVUSER@myibmi.example.com

# 测试连接
ssh -i ~/.ssh/ibmi_key DEVUSER@myibmi.example.com
```

#### 21.3.1 多环境配置

IBM i项目通常涉及多个环境（开发、测试、生产等），需要同时连接不同服务器或不同库进行代码对比、数据对比。因此采用**多环境配置文件**方案：

**配置文件命名规则**：
- `ibmi-connection.env` — 默认环境（未指定环境时使用）
- `ibmi-connection.{env}.env` — 命名环境，如 `dev`、`test`、`prod`

**每个配置文件包含相同结构**（加入.gitignore）：
```bash
IBM_I_HOST=<主机地址>
IBM_I_USER=<SSH用户名>
IBM_I_KEY=<SSH密钥路径，留空则使用默认密钥(~/.ssh/id_ed25519或~/.ssh/id_rsa)>
IBM_I_LIB=<默认目标库>
IBM_I_ASP=<ASP Group名称，无ASP Group则留空>
```

**配置项默认值规则**：
- `IBM_I_KEY`：若未提供或为空，SSH命令中省略 `-i` 参数，使用SSH默认密钥（`~/.ssh/id_ed25519` → `~/.ssh/id_rsa` 依次尝试）
- `IBM_I_ASP`：若未提供或为空，IFS路径不添加ASP前缀，直接使用 `/QSYS.LIB/...`

**多环境配置示例**：
```
项目根目录/
├── ibmi-connection.env          # 默认环境（通常指向dev）
├── ibmi-connection.dev.env      # 开发环境
├── ibmi-connection.test.env     # 测试环境
└── ibmi-connection.prod.env     # 生产环境
```

**环境使用规则**：
- 未指定环境时，使用 `ibmi-connection.env`（默认环境）
- 用户指令中指定环境时（如"在test环境编译"、"对比dev和prod的源码"），读取对应的 `ibmi-connection.{env}.env`
- 所有SSH命令中的 `{USER}`、`{HOST}`、`{ASP}`、`{LIB}` 等参数，根据指定环境从对应配置文件获取

**提交到Git的模板文件** `ibmi-connection.env.example`：
```bash
IBM_I_HOST=<your-ibmi-host>
IBM_I_USER=<your-username>
IBM_I_KEY=<path-to-ssh-key,留空则使用默认密钥>
IBM_I_LIB=<default-library>
IBM_I_ASP=<asp-group-name,无ASP Group则留空>
```

#### 21.3.2 多环境操作场景

**代码对比**：比较不同环境中同一程序/文件的源码差异
```bash
# 读取dev环境的源码
ssh {DEV_USER}@{DEV_HOST} "cat /{DEV_ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/{MBR}.MBR" > /tmp/dev_{MBR}.src

# 读取prod环境的源码
ssh {PROD_USER}@{PROD_HOST} "cat /{PROD_ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/{MBR}.MBR" > /tmp/prod_{MBR}.src

# 本地对比
diff /tmp/dev_{MBR}.src /tmp/prod_{MBR}.src
```

**数据对比**：比较不同环境中同一表的数据
```bash
# 查询dev环境的数据
ssh {DEV_USER}@{DEV_HOST} "db2 \"SELECT * FROM {LIB}.{TABLE} FETCH FIRST 100 ROWS ONLY\""

# 查询prod环境的数据
ssh {PROD_USER}@{PROD_HOST} "db2 \"SELECT * FROM {LIB}.{TABLE} FETCH FIRST 100 ROWS ONLY\""
```

**对象对比**：比较不同环境中同一对象的属性
```bash
# 查看dev环境的对象描述
ssh {DEV_USER}@{DEV_HOST} "system \"DSPOBJD OBJ({LIB}/{OBJ}) OBJTYPE(*PGM) DETAIL(*BASIC)\""

# 查看prod环境的对象描述
ssh {PROD_USER}@{PROD_HOST} "system \"DSPOBJD OBJ({LIB}/{OBJ}) OBJTYPE(*PGM) DETAIL(*BASIC)\""
```

### 21.4 SSH远程操作命令手册

以下所有命令通过 `ssh user@host "command"` 执行，AI通过 `execute_command` 工具调用。

#### 21.4.1 列出库中所有源物理文件

```bash
ssh DEVUSER@myibmi "system \"DSPFD DEVAPP/*ALL DSPATR(*ATR)\" | grep -E 'Source\s+file'"
```

或更精确的方式：
```bash
ssh DEVUSER@myibmi "system \"WRKOBJ DEVAPP/*ALL *FILE\" | grep SRC"
```

#### 21.4.2 列出源物理文件中所有成员

```bash
ssh DEVUSER@myibmi "system \"DSPFD DEVAPP/QRPGLESRC DSPATR(*MBR)\" 2>/dev/null"
```

更简洁的方式（使用QSH）：
```bash
ssh DEVUSER@myibmi "qsh -c 'for mbr in /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/*.MBR; do basename \${mbr} .MBR; done'"
```

#### 21.4.3 读取源成员内容

**方法一：通过IFS路径直接cat**
```bash
ssh DEVUSER@myibmi "cat /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR"
```

**方法二：CPYTOSTMF转临时文件后cat（处理编码问题）**
```bash
ssh DEVUSER@myibmi "system \"CPYTOSTMF FROMMBR('/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR') TOSTMF('/tmp/ordadd.txt') STMFOPT(*REPLACE) STMFCODPAG(*PCASCII)\" && cat /tmp/ordadd.txt"
```

**方法三：使用DSPxxxSRC命令**
```bash
ssh DEVUSER@myibmi "system \"DSPRPGSRC SRCFILE(DEVAPP/QRPGLESRC) SRCMBR(ORDADD)\""
```

#### 21.4.4 搜索源码内容

**在所有RPG源码中搜索关键字**：
```bash
ssh DEVUSER@myibmi "for mbr in /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/*.MBR; do result=\$(grep -l 'CUSTNO' \$mbr 2>/dev/null); if [ -n \"\$result\" ]; then echo \"\$(basename \$mbr .MBR): \$(grep 'CUSTNO' \$mbr)\"; fi; done"
```

**搜索整个库的所有源文件**：
```bash
ssh DEVUSER@myibmi "for srcf in /MYASP/QSYS.LIB/DEVAPP.LIB/*.FILE; do for mbr in \$srcf/*.MBR; do result=\$(grep -l 'CUSTNO' \$mbr 2>/dev/null); if [ -n \"\$result\" ]; then echo \"\$(basename \$srcf .FILE)/\$(basename \$mbr .MBR)\"; fi; done; done"
```

**使用DSPSRCPF搜索（CL方式）**：
```bash
ssh DEVUSER@myibmi "system \"FNDSTRPDM STRING('CUSTNO') FILE(DEVAPP/QRPGLESRC) MBR(*ALL) OPTION(*NONE)\""
```

#### 21.4.5 查看对象列表

```bash
# 列出库中所有对象
ssh DEVUSER@myibmi "system \"DSPOBJD OBJ(DEVAPP/*ALL) OBJTYPE(*ALL) DETAIL(*_BASIC)\""

# 只看程序对象
ssh DEVUSER@myibmi "system \"DSPOBJD OBJ(DEVAPP/*ALL) OBJTYPE(*PGM) DETAIL(*_BASIC)\""

# 只看文件对象
ssh DEVUSER@myibmi "system \"DSPOBJD OBJ(DEVAPP/*ALL) OBJTYPE(*FILE) DETAIL(*_BASIC)\""

# 只看服务程序
ssh DEVUSER@myibmi "system \"DSPOBJD OBJ(DEVAPP/*ALL) OBJTYPE(*SRVPGM) DETAIL(*_BASIC)\""
```

#### 21.4.6 查看文件字段定义

```bash
# 查看PF的字段定义
ssh DEVUSER@myibmi "system \"DSPFFD FILE(DEVAPP/CUSTPF)\""

# 查看库中所有文件的字段定义
ssh DEVUSER@myibmi "system \"DSPFFD FILE(DEVAPP/*ALL)\""
```

#### 21.4.7 查看程序描述和属性

```bash
# 查看程序属性
ssh DEVUSER@myibmi "system \"DSPPGM PGM(DEVAPP/ORDADD)\""

# 查看服务程序导出的过程
ssh DEVUSER@myibmi "system \"DSPSRVPGM SRVPGM(DEVAPP/CUSTSRV) DETAIL(*PROCEXP)\""
```

#### 21.4.8 编译程序

```bash
# 编译RPG程序
ssh DEVUSER@myibmi "system \"CRTBNDRPG PGM(DEVAPP/ORDADD) SRCFILE(DEVAPP/QRPGLESRC) SRCMBR(ORDADD) TGTRLS(*CURRENT) DBGVIEW(*SOURCE) OPTION(*EVENTF)\""

# 编译PF文件
ssh DEVUSER@myibmi "system \"CRTPF FILE(DEVAPP/CUSTPF) SRCFILE(DEVAPP/QDDSSRC) SRCMBR(CUSTPF)\""

# 编译LF文件
ssh DEVUSER@myibmi "system \"CRTLF FILE(DEVAPP/CUSTPFL1) SRCFILE(DEVAPP/QDDSSRC) SRCMBR(CUSTPFL1)\""

# 编译DSPF文件
ssh DEVUSER@myibmi "system \"CRTDSPF FILE(DEVAPP/ORDDSPF) SRCFILE(DEVAPP/QDDSSRC) SRCMBR(ORDDSPF)\""

# 编译CL程序
ssh DEVUSER@myibmi "system \"CRTBNDCL PGM(DEVAPP/ORDMNT) SRCFILE(DEVAPP/QCLLESRC) SRCMBR(ORDMNT)\""
```

#### 21.4.9 查看编译错误

```bash
# 查看最新编译清单(假脱机文件)
ssh DEVUSER@myibmi "system \"WRKSPLF\""
```

更直接的方式 — 编译时直接输出到数据队列或查看返回码：
```bash
# 编译并检查返回码
ssh DEVUSER@myibmi "system \"CRTBNDRPG PGM(DEVAPP/ORDADD) SRCFILE(DEVAPP/QRPGLESRC) SRCMBR(ORDADD)\" 2>&1; echo \"EXIT_CODE=\$?\""
```

#### 21.4.10 写入/更新源成员

**方法一：通过IFS临时文件写入**
```bash
# 1. 先将源码写到本地临时文件
cat > /tmp/ordadd.rpgle << 'RPGLCODE'
**FREE
Ctl-Opt Main(ORDADD) ActGrp(*Caller);
... (RPG代码) ...
RPGLCODE

# 2. SCP上传到IBM i IFS
scp /tmp/ordadd.rpgle DEVUSER@myibmi:/tmp/ordadd.rpgle

# 3. 从IFS复制到Source PF成员
ssh DEVUSER@myibmi "system \"CPYFRMSTMF FROMSTMF('/tmp/ordadd.rpgle') TOMBR('/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""
```

**方法二：直接通过echo/heredoc写入**
```bash
ssh DEVUSER@myibmi "cat > /tmp/ordadd.rpgle << 'EOF'
**FREE
Ctl-Opt Main(ORDADD) ActGrp(*Caller);
... (RPG代码) ...
EOF
system \"CPYFRMSTMF FROMSTMF('/tmp/ordadd.rpgle') TOMBR('/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""
```

#### 21.4.11 使用SQL查询数据

```bash
# 交互式查询（输出到标准输出）
ssh DEVUSER@myibmi "db2 \"SELECT * FROM DEVAPP.CUSTPF WHERE STATUS = 'A' FETCH FIRST 10 ROWS ONLY\""

# 查看表结构
ssh DEVUSER@myibmi "db2 \"SELECT COLUMN_NAME, DATA_TYPE, LENGTH FROM QSYS2.SYSCOLUMNS WHERE TABLE_SCHEMA = 'DEVAPP' AND TABLE_NAME = 'CUSTPF'\""

# 查看库中所有表
ssh DEVUSER@myibmi "db2 \"SELECT TABLE_NAME FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA = 'DEVAPP'\""

# 查看索引
ssh DEVUSER@myibmi "db2 \"SELECT INDEX_NAME, COLUMN_NAME FROM QSYS2.SYSKEYS WHERE TABLE_SCHEMA = 'DEVAPP' AND TABLE_NAME = 'CUSTPF'\""
```

#### 21.4.12 检查对象是否存在

```bash
ssh DEVUSER@myibmi "system \"CHKOBJ OBJ(DEVAPP/ORDADD) OBJTYPE(*PGM)\" 2>&1; echo \"RC=\$?\""
# RC=0 存在, RC≠0 不存在
```

#### 21.4.13 查看作业日志

```bash
# 查看当前作业日志
ssh DEVUSER@myibmi "system \"DSPJOBLOG\""
```

### 21.5 AI团队SSH操作封装函数

为避免每次拼接冗长的SSH命令，定义一组封装函数供AI调用。在知识库中记录这些函数，AI按模板拼接命令：

> **环境参数说明**：以下模板中 `{USER}`、`{HOST}`、`{ASP}`、`{LIB}` 等参数均从指定环境的配置文件（`ibmi-connection.{env}.env`）获取。未指定环境时从 `ibmi-connection.env`（默认环境）获取。

#### 列出库中源文件
```bash
ssh {USER}@{HOST} "qsh -c 'for f in /{ASP}/QSYS.LIB/{LIB}.LIB/*.FILE; do basename \$f .FILE; done'"
```

#### 列出源文件中所有成员
```bash
ssh {USER}@{HOST} "qsh -c 'for m in /{ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/*.MBR; do basename \$m .MBR; done'"
```

#### 读取成员源码
```bash
ssh {USER}@{HOST} "cat /{ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/{MBR}.MBR"
```

#### 搜索源码
```bash
ssh {USER}@{HOST} "grep -rn '{PATTERN}' /{ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/ 2>/dev/null || echo 'NO_MATCH'"
```

#### 查看文件字段
```bash
ssh {USER}@{HOST} "system \"DSPFFD FILE({LIB}/{FILENAME})\""
```

#### 查看对象列表
```bash
ssh {USER}@{HOST} "system \"DSPOBJD OBJ({LIB}/*ALL) OBJTYPE(*{TYPE}) DETAIL(*BASIC)\""
```

#### 写入源成员
```bash
# 步骤1: 本地写入临时文件
# 步骤2: scp上传
# 步骤3: CPYFRMSTMF
scp {LOCAL_FILE} {USER}@{HOST}:/tmp/{MBR}.src
ssh {USER}@{HOST} "system \"CPYFRMSTMF FROMSTMF('/tmp/{MBR}.src') TOMBR('/{ASP}/QSYS.LIB/{LIB}.LIB/{SRCFILE}.FILE/{MBR}.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""
```

#### 编译程序
```bash
ssh {USER}@{HOST} "system \"{COMPILE_CMD}\" 2>&1; echo \"COMPILE_RC=\$?\""
```

#### 执行SQL
```bash
ssh {USER}@{HOST} "db2 \"{SQL_STATEMENT}\""
```

### 21.6 AI团队SSH工作流

```
┌──────────────────────────────────────────────────────────────┐
│                     AI 团队工作流                              │
│                                                              │
│  1. 探索阶段                                                 │
│     ├─ ssh → 列出库中源文件                                   │
│     ├─ ssh → 列出源文件成员                                   │
│     ├─ ssh → 读取现有源码                                     │
│     ├─ ssh → 查看字段定义(DSPFFD)                             │
│     └─ ssh → 搜索关键字(grep)                                 │
│                                                              │
│  2. 开发阶段                                                 │
│     ├─ 本地生成源码 → output/code/                            │
│     └─ 确保遵循现有代码风格                                    │
│                                                              │
│  3. 部署阶段                                                 │
│     ├─ scp → 上传到IBM i IFS临时目录                          │
│     ├─ ssh → CPYFRMSTMF写入Source PF成员                     │
│     ├─ ssh → 编译程序(CRTBNDRPG等)                           │
│     └─ ssh → 检查编译返回码                                   │
│                                                              │
│  4. 验证阶段                                                 │
│     ├─ ssh → CALL程序测试                                     │
│     ├─ ssh → 查看作业日志(DSPJOBLOG)                         │
│     └─ ssh → 查询数据验证结果(db2)                            │
└──────────────────────────────────────────────────────────────┘
```

### 21.7 完整操作示例：新增一个订单程序

```bash
# === 第1步：探索现有代码 ===

# 查看库中有哪些源文件
ssh DEVUSER@myibmi "qsh -c 'for f in /MYASP/QSYS.LIB/DEVAPP.LIB/*.FILE; do basename \$f .FILE; done'"

# 查看QRPGLESRC中有哪些RPG成员
ssh DEVUSER@myibmi "qsh -c 'for m in /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/*.MBR; do basename \$m .MBR; done'"

# 查看QDDSSRC中有哪些DDS成员
ssh DEVUSER@myibmi "qsh -c 'for m in /MYASP/QSYS.LIB/DEVAPP.LIB/QDDSSRC.FILE/*.MBR; do basename \$m .MBR; done'"

# 读取现有订单文件的字段定义
ssh DEVUSER@myibmi "system \"DSPFFD FILE(DEVAPP/ORDERPF)\""

# 读取一个类似程序的源码作为参考
ssh DEVUSER@myibmi "cat /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/CUSTADD.MBR"

# === 第2步：AI生成源码(写入本地output/code/) ===
# (AI自动完成，产出 ORDADD.rpgle, ORDDSPF.dspf 等)

# === 第3步：上传到IBM i ===

# 上传DDS源码
scp output/code/ORDDSPF.dspf DEVUSER@myibmi:/tmp/ORDDSPF.src
ssh DEVUSER@myibmi "system \"CPYFRMSTMF FROMSTMF('/tmp/ORDDSPF.src') TOMBR('/MYASP/QSYS.LIB/DEVAPP.LIB/QDDSSRC.FILE/ORDDSPF.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""

# 上传RPG源码
scp output/code/ORDADD.rpgle DEVUSER@myibmi:/tmp/ORDADD.src
ssh DEVUSER@myibmi "system \"CPYFRMSTMF FROMSTMF('/tmp/ORDADD.src') TOMBR('/MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR') MBROPT(*REPLACE) STMFCODPAG(*PCASCII)\""

# === 第4步：编译 ===

# 编译显示文件
ssh DEVUSER@myibmi "system \"CRTDSPF FILE(DEVAPP/ORDDSPF) SRCFILE(DEVAPP/QDDSSRC) SRCMBR(ORDDSPF)\" 2>&1; echo \"COMPILE_RC=\$?\""

# 编译RPG程序
ssh DEVUSER@myibmi "system \"CRTBNDRPG PGM(DEVAPP/ORDADD) SRCFILE(DEVAPP/QRPGLESRC) SRCMBR(ORDADD) TGTRLS(*CURRENT) DBGVIEW(*SOURCE)\" 2>&1; echo \"COMPILE_RC=\$?\""

# === 第5步：验证 ===

# 检查程序是否存在
ssh DEVUSER@myibmi "system \"CHKOBJ OBJ(DEVAPP/ORDADD) OBJTYPE(*PGM)\" 2>&1; echo \"RC=\$?\""

# 调用程序测试
ssh DEVUSER@myibmi "system \"CALL PGM(DEVAPP/ORDADD)\" 2>&1"
```

### 21.8 注意事项与常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| cat成员内容乱码 | EBCDIC编码问题 | 使用CPYTOSTMF先转为ASCII，或确认SSH连接使用正确的CCSID |
| system命令输出截断 | 5250输出格式限制 | 使用OUTPUT(*PRINT)或重定向到IFS文件 |
| grep搜索不到 | IFS路径中MBR文件可能有特殊属性 | 使用QSH的for循环+grep，或使用FNDSTRPDM |
| CPYFRMSTMF报错 | 目标成员不存在 | 先用ADDPFM创建成员，再CPYFRMSTMF |
| 编译错误看不到详情 | system命令只返回返回码 | 查看编译假脱机文件：`system "WRKSPLF"` |
| SSH连接超时 | 网络或防火墙 | 在~/.ssh/config中配置KeepAlive |
| 权限不足 | 用户权限不够 | 确认用户有*USE/*CHANGE权限到目标库 |
| db2命令不可用 | 未安装5722SS1选项 | 确认IBM i已安装DB2 QSQCLI |

### 21.9 SSH连接优化配置

在本地 `~/.ssh/config` 中添加IBM i主机配置：

```
Host myibmi
    HostName myibmi.example.com
    User DEVUSER
    IdentityFile ~/.ssh/ibmi_key
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    ConnectTimeout 10
    # IBM i PASE默认shell
    RequestTTY yes
```

配置后可简化命令：
```bash
# 简化前
ssh -i ~/.ssh/ibmi_key DEVUSER@myibmi.example.com "command"

# 简化后
ssh myibmi "command"
```

### 21.10 编码问题处理

IBM i默认使用EBCDIC编码，SSH/PASE环境需要正确处理编码转换。

| 场景 | 处理方式 |
|------|----------|
| 读取源成员 | `cat /{ASP}/QSYS.LIB/...` 通常自动转换，若乱码则用CPYTOSTMF |
| 写入源成员 | CPYFRMSTMF使用`STMFCODPAG(*PCASCII)`自动转换 |
| SQL查询 | db2命令自动处理编码 |
| system命令输出 | 可能需要设置`QIBM_PASE_CCSID=1208`（UTF-8） |

在SSH会话中设置CCSID：
```bash
ssh myibmi "export QIBM_PASE_CCSID=1208 && cat /MYASP/QSYS.LIB/DEVAPP.LIB/QRPGLESRC.FILE/ORDADD.MBR"
```

### 21.11 备选方案：本地源码镜像（附录）

如果不方便使用SSH直连，仍可使用本地源码镜像方案作为备选。此时需配置同步脚本定期将IBM i源码同步到本地 `ibmi-src/` 目录。该方案详见之前版本的知识库文档。

| 方案对比 | SSH直连 | 本地镜像 |
|----------|---------|----------|
| 实时性 | 实时访问服务器最新代码 | 需手动/定时同步 |
| 操作能力 | 读取+写入+编译+执行 | 仅读取 |
| 依赖 | SSH服务 | 同步脚本+rsync |
| 网络要求 | 每次操作需网络 | 仅同步时需网络 |
| 推荐程度 | ★★★★★（首选） | ★★★（备选） |

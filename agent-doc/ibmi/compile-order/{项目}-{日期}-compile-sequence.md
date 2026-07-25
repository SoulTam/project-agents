<!-- 创建时间: 2026-07-25 00:00 -->
<!-- 最后修改: 2026-07-25 00:00 -->

# {项目名} — 编译顺序

## 1. 编译清单

| 顺序 | 对象类型 | 对象名 | 编译命令 | 依赖 |
|------|---------|--------|---------|------|
| 1 | PF | {文件名} | CRTPF | 无 |
| 2 | LF | {文件名} | CRTLF | PF |
| 3 | DSPF | {文件名} | CRTDSPF | 无 |
| 4 | MODULE | {模块名} | CRTRPGMOD | 无 |
| 5 | SRVPGM | {服务程序} | CRTSRVPGM | MODULE |
| 6 | PGM | {程序名} | CRTBNDRPG | MODULE/SRVPGM |

---

## 2. 编译命令

```cl
/* 顺序1: 编译PF */
CRTPF FILE(mylib/CUSTPF) SRCFILE(mylib/QDDSSRC) SRCMBR(CUSTPF)

/* 顺序2: 编译LF */
CRTLF FILE(mylib/CUSTPFL1) SRCFILE(mylib/QDDSSRC) SRCMBR(CUSTPFL1)

/* 顺序3: 编译DSPF */
CRTDSPF FILE(mylib/ORDDSPF) SRCFILE(mylib/QDDSSRC) SRCMBR(ORDDSPF)

/* 顺序4: 编译模块 */
CRTRPGMOD MODULE(mylib/ORDMOD) SRCFILE(mylib/QRPGLESRC) SRCMBR(ORDMOD)

/* 顺序5: 创建服务程序 */
CRTSRVPGM SRVPGM(mylib/CUSTSRV) MODULE(mylib/CUSTSRV) SRCFILE(mylib/QSRVSRC) SRCMBR(CUSTSRV)

/* 顺序6: 编译程序 */
CRTBNDRPG PGM(mylib/ORDADD) SRCFILE(mylib/QRPGLESRC) SRCMBR(ORDADD) BNDDIR(mylib/STDBND)
```

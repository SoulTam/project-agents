<!-- 创建时间: 2026-07-25 00:00 -->
<!-- 最后修改: 2026-07-25 00:00 -->

# {项目名} — 库结构清单

## 1. 环境配置

| 环境 | 库名 | 服务器 | 用途 |
|------|------|--------|------|
| 开发 | DEVAPP | {服务器} | 开发环境 |
| 测试 | TSTAPP | {服务器} | 测试环境 |
| 生产 | PRDAPP | {服务器} | 生产环境 |

---

## 2. 源文件清单

| 库名 | 源文件名 | Source Type | 说明 |
|------|---------|-------------|------|
| DEVAPP | QRPGLESRC | RPGLE/SQLRPGLE | RPG源码 |
| DEVAPP | QCLLESRC | CLLE/CLMOD | CL源码 |
| DEVAPP | QDDSSRC | PF/LF/DSPF/PRTF | DDS源码 |
| DEVAPP | QCMDSRC | CMD | 命令定义 |
| DEVAPP | QSRVSRC | BND | Binder Language |

---

## 3. 对象清单

| 库名 | 对象名 | 对象类型 | 说明 |
|------|--------|---------|------|
| DEVAPP | CUSTPF | *FILE | 客户主文件 |
| DEVAPP | CUSTPFL1 | *FILE | 客户逻辑文件 |
| DEVAPP | ORDADD | *PGM | 订单添加程序 |
| DEVAPP | CUSTSRV | *SRVPGM | 客户服务程序 |

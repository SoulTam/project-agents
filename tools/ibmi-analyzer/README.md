# IBM i 程序代码分析器

分析 RPG/RPGLE、CL/CLP、COBOL 程序代码，重点提取：
1. **表/文件声明及字段使用** — 只分析有操作且最终落库的字段
2. **Data Area** — 声明、读写操作、DS拆解
3. `/COPY`、`/INCLUDE` 引用
4. 程序调用（CALL、CALLP、CALLB、CALLPRC、EXTPGM、SQL CALL等）

## 用法

```bash
python analyze_ibmi.py /path/to/source --output /path/to/analyze
```

## 输出结构

```
analyze/
├── PROGRAM1.md
├── PROGRAM2.md
└── subdir/
    └── PROGRAM3.md
```

## 报告结构

| 章节 | 内容 |
|------|------|
| 1. 表/文件声明 | 所有 F-spec / DCL-F 声明 |
| 2. 表字段概览 | 每个表中**有操作且最终落库**的字段 |
| 3. 字段处理流程 | 按表展开字段的赋值/计算操作 |
| 4. Data Area | 声明、IN/OUT/CHAIN、DS拆解 |
| 5. COPY/INCLUDE | 引用列表 |
| 6. 程序调用 | CALL/CALLP/CALLB/EXTPGM等 |
| 7. 汇总 | 统计数据 |

## 解析能力

### RPG/RPGLE

- F-spec / DCL-F 文件声明
- CHAIN, READ, READE, SETLL, SETGT, UPDATE, WRITE, DELETE, EXFMT
- EVAL, IF, WHEN, DOW/DOU 条件
- MOVEL, MOVE, Z-ADD, MULT 数据移动
- EXEC SQL 块（FROM, JOIN, INTO, UPDATE, DELETE）
- DCL-DTAARA / DCL-DS 声明
- INDTAARA, OUTDTAARA, CHAINDTAARA 操作
- DS.field 赋值（Data Area 拆解）

### 程序调用方式

| 方式 | 说明 |
|------|------|
| CALL | 普通调用 |
| CALLP | 过程调用 |
| CALLB | 绑定模块调用 |
| CALLPRC | 调用过程 |
| EXTPGM | 外部程序引用 |
| CALL (SQL) | SQL 嵌入调用 |
| CALLSUBR | CL 子程序调用 |
| CALLBO | CL 绑定对象调用 |
| CALLBOUND | CL 绑定调用 |

### CL/CLP

- DCL FILE/PROG / DCL-DTAARA 声明
- CALL / CALLP / CALLSUBR / CALLBO / CALLBOUND
- CHGVAR 变量赋值
- CHGDTAARA, RTVDTAARA, OVRDBF

### COBOL

- COPY 引用
- CALL 程序调用
- FD/SD 文件声明
- MOVE, COMPUTE, READ, WRITE, REWRITE, DELETE

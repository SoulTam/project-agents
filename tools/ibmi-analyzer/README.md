# IBM i 程序代码分析器

分析 RPG/RPGLE、CL/CLP、COBOL 程序代码，重点提取：
1. **表/文件声明及字段使用** — 按表展开每个字段的处理流程
2. **Data Area** — 声明、读写操作
3. `/COPY`、`/INCLUDE` 引用
4. 程序调用（CALL、CALLP）

## 用法

```bash
# 分析单个文件
python analyze_ibmi.py /path/to/program.rpgle

# 分析整个目录
python analyze_ibmi.py /path/to/source

# 指定输出目录
python analyze_ibmi.py /path/to/source --output /path/to/analyze
```

## 支持的文件类型

| 扩展名 | 类型 |
|--------|------|
| `.rpgle`, `.rpgleinc`, `.sqlrpgle` | RPGLE |
| `.clp`, `.clle`, `.cl` | CL |
| `.cbl`, `.cob` | COBOL |
| `.sqc` | SQL C |

## 输出格式

输出为 Markdown 文件，保存到 `analyze/` 目录，保持与源代码相同的目录结构。

### 报告结构

```markdown
# 程序分析报告: TESTORD

## 1. 表/文件声明
| # | 文件名 | 使用方式 | 类型 | 行号 |
|---|--------|----------|------|------|
| 1 | ORDERH | INPUT | DISK | 10 |

## 2. 表字段概览
| # | 表名 | 涉及字段数 | 字段列表 |
|---|------|-----------|---------|
| 1 | ORDERD | 4 | ORDAMT, PRICE, QTY, W_TOTAL |

## 3. 字段处理流程（按表展开）
### 表: ORDERD
#### 字段: ORDAMT
| # | 操作 | 上下文 | 目标/表达式 | 行号 |
|---|------|--------|------------|------|
| 1 | ASSIGN | EVAL | W_TOTAL | 38 |

## 4. Data Area
| # | 名称 | 类型 | 长度 | 操作列表 |
|---|------|------|------|---------|
| 1 | ORDCTL | CHAR | 100 | DEFINE, IN |

## 5. COPY/INCLUDE 引用
## 6. 程序调用
## 7. 汇总
```

## 解析能力

### RPG/RPGLE

- F-spec / DCL-F 文件声明
- CHAIN, READ, READE, SETLL, SETGT, UPDATE, WRITE, DELETE, EXFMT
- EVAL, IF, WHEN, DOW/DOU 条件
- MOVEL, MOVE, Z-ADD, MULT 数据移动
- EXEC SQL 块（FROM, JOIN, INTO, UPDATE, DELETE）
- DCL-DTAARA 声明
- INDTAARA, OUTDTAARA, CHAINDTAARA 操作

### CL/CLP

- DCL FILE/PROG / DCL-DTAARA 声明
- CALL 程序调用
- CHGVAR 变量赋值
- CHGDTAARA, RTVDTAARA, OVRDBF

### COBOL

- COPY 引用
- CALL 程序调用
- FD/SD 文件声明
- MOVE, COMPUTE, READ, WRITE, REWRITE, DELETE

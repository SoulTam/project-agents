#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IBM i 程序代码分析器

功能：
  分析 RPG/RPGLE、CL/CLP、COBOL 程序代码，提取：
  1. 表/文件声明及引用
  2. 每个表所使用的字段及处理流程
  3. Data Area 引用
  4. /COPY、/INCLUDE 引用
  5. 程序调用

用法：
  python analyze_ibmi.py <file_or_dir> [--output <output_dir>]

输出：
  在 analyze/ 目录下按源代码目录结构放置 Markdown 分析结果
"""

import os
import re
import sys
import argparse
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime


# ============================================================
# 数据结构
# ============================================================

@dataclass
class CopyInclude:
    """COPY/INCLUDE 引用"""
    directive: str          # /COPY 或 /INCLUDE
    library: str            # 库名
    file: str               # 文件名
    member: str = ""        # 成员名
    line: int = 0
    raw: str = ""


@dataclass
class FileRef:
    """文件引用（F-spec 或 DCL-F）"""
    name: str               # 文件名
    usage: str              # I/O/U/IO 等
    file_type: str          # PHY/LF/DISK 等
    alias: str = ""         # 别名
    line: int = 0
    raw: str = ""


@dataclass
class ProgramCall:
    """程序调用"""
    program: str            # 被调用程序名
    call_type: str          # CALL/CALLP
    parameters: list = field(default_factory=list)
    line: int = 0
    raw: str = ""


@dataclass
class DataAreaRef:
    """Data Area 引用"""
    name: str               # Data Area 名
    operation: str          # IN/OUT/CHAIN/DEFINE
    data_type: str = ""     # 类型（CHAR/DEC/LGL 等）
    length: str = ""        # 长度
    line: int = 0
    raw: str = ""


@dataclass
class FieldUsage:
    """字段使用（关联到具体表）"""
    field: str              # 字段名
    table: str              # 所属表名（为空表示非表字段）
    operation: str          # 操作类型
    context: str            # 上下文
    target: str = ""        # 目标/表达式
    line: int = 0
    raw: str = ""


@dataclass
class TableFieldInfo:
    """表字段信息"""
    table: str              # 表名
    fields: Dict[str, List[FieldUsage]] = field(default_factory=dict)

    def add_field_usage(self, field_name: str, usage: FieldUsage):
        if field_name not in self.fields:
            self.fields[field_name] = []
        self.fields[field_name].append(usage)


@dataclass
class ProgramAnalysis:
    """程序分析结果"""
    file_path: str
    program_name: str
    program_type: str
    copy_includes: list = field(default_factory=list)
    file_refs: list = field(default_factory=list)
    program_calls: list = field(default_factory=list)
    data_area_refs: list = field(default_factory=list)
    table_fields: Dict[str, TableFieldInfo] = field(default_factory=dict)
    errors: list = field(default_factory=list)

    def add_field_to_table(self, table: str, field_name: str, usage: FieldUsage):
        if table not in self.table_fields:
            self.table_fields[table] = TableFieldInfo(table=table)
        self.table_fields[table].add_field_usage(field_name, usage)


# ============================================================
# RPG/RPGLE 解析器
# ============================================================

class RPGLEParser:

    def __init__(self):
        # 注册的文件名（F-spec 和 DCL-F 声明的文件）
        self.registered_files = set()
        # Data Area 声明
        self.registered_dtaara = set()

    def parse(self, filepath: str, lines: list) -> ProgramAnalysis:
        result = ProgramAnalysis(
            file_path=filepath,
            program_name=Path(filepath).stem,
            program_type="RPGLE"
        )

        in_sql = False
        sql_block = []
        current_file_context = ""  # 当前操作的文件上下文

        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()

            # 跳过注释行（* 在第1列）和空行
            if stripped and stripped[0] == '*':
                continue
            if not stripped.strip():
                continue

            # 跟踪 SQL 块
            if re.match(r'^\s*EXEC\s+SQL\b', stripped, re.IGNORECASE):
                in_sql = True
                sql_block = [stripped]
                continue

            if in_sql:
                sql_block.append(stripped)
                if ';' in stripped:
                    in_sql = False
                    self._parse_sql_block(result, sql_block, i)
                    sql_block = []
                continue

            # 解析各种声明
            self._parse_fspec(result, stripped, i)
            self._parse_dcl_f(result, stripped, i)
            self._parse_copy_include(result, stripped, i)
            self._parse_call(result, stripped, i)
            self._parse_data_area_decl(result, stripped, i)

            # 解析文件操作（更新 current_file_context）
            ctx = self._parse_file_operation(stripped, i)
            if ctx:
                current_file_context = ctx

            # 解析字段操作（关联到当前文件上下文）
            self._parse_field_operations(result, stripped, i, current_file_context)

            # 解析 Data Area 操作
            self._parse_data_area_operations(result, stripped, i)

        return result

    def _parse_fspec(self, result, line, lineno):
        """解析 F-spec 文件声明"""
        m = re.match(r'^F\s+(\S+)\s+(.*)', line, re.IGNORECASE)
        if not m:
            return

        filename = m.group(1).upper()
        rest = m.group(2).upper()

        usage = ""
        for u, pattern in [('INPUT', r'\bI\b'), ('OUTPUT', r'\bO\b'),
                           ('UPDATE', r'\bU\b'), ('INPUT/OUTPUT', r'\bIO\b')]:
            if re.search(pattern, rest):
                usage = u
                break

        file_type = "DISK"
        for ft in ['PHY', 'LF', 'SAVF', 'PRINTER', 'WORKSTN']:
            if ft in rest:
                file_type = ft
                break

        self.registered_files.add(filename)
        result.file_refs.append(FileRef(
            name=filename, usage=usage or "DISK", file_type=file_type,
            line=lineno, raw=line.strip()
        ))

    def _parse_dcl_f(self, result, line, lineno):
        """解析 DCL-F（自由格式RPG）"""
        m = re.match(r'^\s*DCL-F\s+(\S+)', line, re.IGNORECASE)
        if not m:
            return

        filename = m.group(1).rstrip(';').upper()
        rest = line[m.end():].upper().rstrip(';')

        usage = ""
        usage_match = re.search(r'USAGE\(([^)]+)\)', rest)
        if usage_match:
            u = usage_match.group(1).strip()
            if 'I' in u and 'O' in u:
                usage = "INPUT/OUTPUT"
            elif 'I' in u:
                usage = "INPUT"
            elif 'O' in u:
                usage = "OUTPUT"
            elif 'U' in u:
                usage = "UPDATE"

        self.registered_files.add(filename)
        result.file_refs.append(FileRef(
            name=filename, usage=usage or "DISK", file_type="DISK",
            line=lineno, raw=line.strip()
        ))

    def _parse_copy_include(self, result, line, lineno):
        """解析 /COPY、/INCLUDE"""
        m = re.match(r'^\s*/(?:COPY|INCLUDE)\s+(\S+)', line, re.IGNORECASE)
        if not m:
            return

        path_part = m.group(1)
        library, file_name, member = "", "", ""

        if ',' in path_part:
            parts = path_part.split(',', 1)
            library = parts[0]
            member = parts[1]
            file_name = member
        elif '/' in path_part:
            parts = path_part.rsplit('/', 1)
            library = parts[0]
            file_name = parts[1]
        else:
            file_name = path_part

        result.copy_includes.append(CopyInclude(
            directive="/COPY" if '/COPY' in line.upper() else "/INCLUDE",
            library=library, file=file_name, member=member,
            line=lineno, raw=line.strip()
        ))

    def _parse_call(self, result, line, lineno):
        """解析 CALL、CALLP"""
        m = re.match(
            r'^\s*(CALL|CALLP)\s+(?:\'([^\']+)\'|(\S+?))(?:\(.*?\))?\s*;?',
            line, re.IGNORECASE
        )
        if m:
            program = (m.group(2) or m.group(3)).rstrip(';').split('(')[0].strip()
            result.program_calls.append(ProgramCall(
                program=program.upper(), call_type=m.group(1).upper(),
                line=lineno, raw=line.strip()
            ))

    def _parse_data_area_decl(self, result, line, lineno):
        """解析 DCL-DTAARA 声明"""
        m = re.match(
            r'^\s*DCL-DTAARA\s+(\S+)(?:\s+(.*))?',
            line, re.IGNORECASE
        )
        if m:
            name = m.group(1).rstrip(';').upper()
            rest = (m.group(2) or "").upper()

            data_type = ""
            length = ""
            type_match = re.search(r'TYPE\((\w+)\)', rest)
            len_match = re.search(r'LEN\((\d+)\)', rest)
            if type_match:
                data_type = type_match.group(1)
            if len_match:
                length = len_match.group(1)

            self.registered_dtaara.add(name)
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="DEFINE", data_type=data_type,
                length=length, line=lineno, raw=line.strip()
            ))

    def _parse_file_operation(self, line, lineno) -> str:
        """
        解析文件操作，返回当前操作的文件名（作为上下文）
        支持: CHAIN, READ, READE, SETLL, SETGT, UPDATE, WRITE, DELETE, EXFMT

        CHAIN 有两种格式:
          CHAIN file           - 使用文件名
          CHAIN keyfield file  - 使用字段名和文件名
        """
        stripped = line.strip().rstrip(';')

        # CHAIN 特殊处理：支持两个参数
        m = re.match(r'^\s*CHAIN\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            param1 = m.group(1).upper()
            param2 = m.group(2).upper()
            # 第二个参数是文件名（如果在已注册文件中）
            if param2 in self.registered_files:
                return param2
            # 否则尝试第一个参数
            if param1 in self.registered_files:
                return param1
            # 都不是已注册文件，返回第二个参数（可能是文件名）
            return param2

        # 所有文件操作（包括单参数 CHAIN）
        patterns = [
            (r'^\s*CHAIN\s+(\S+)', 'CHAIN'),
            (r'^\s*READ[PPE]*\s+(\S+)', 'READ'),
            (r'^\s*READE\s+(\S+)', 'READE'),
            (r'^\s*SETLL\s+(\S+)', 'SETLL'),
            (r'^\s*SETGT\s+(\S+)', 'SETGT'),
            (r'^\s*UPDATE\s+(\S+)', 'UPDATE'),
            (r'^\s*WRITE\s+(\S+)', 'WRITE'),
            (r'^\s*DELETE\s+(\S+)', 'DELETE'),
            (r'^\s*EXFMT\s+(\S+)', 'EXFMT'),
        ]

        for pattern, op in patterns:
            m = re.match(pattern, stripped, re.IGNORECASE)
            if m:
                filename = m.group(1).upper()
                if filename in self.registered_files:
                    return filename
                return filename
        return ""

    def _parse_field_operations(self, result, line, lineno, file_context):
        """解析字段操作，关联到当前文件上下文"""
        stripped = line.strip()

        # EVAL field = expr
        m = re.match(r'^\s*EVAL\s+(\S+)\s*=\s*(.*)', stripped, re.IGNORECASE)
        if m:
            target = m.group(1).rstrip(';')
            expr = m.group(2).rstrip(';')
            # 检查目标是否是已注册文件的字段
            if file_context and self._is_file_field(target, file_context):
                result.add_field_to_table(file_context, target, FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="EVAL", target=expr, line=lineno, raw=stripped
                ))
            # 从表达式中提取字段引用
            self._extract_fields_from_expr(result, expr, file_context, "READ", "EVAL", lineno, stripped)
            return

        # IF / WHEN / DOW / DOU 条件
        for kw in ['IF', 'WHEN', 'DOW', 'DOU']:
            m = re.match(rf'^\s*{kw}\s+(.*)', stripped, re.IGNORECASE)
            if m:
                self._extract_fields_from_expr(result, m.group(1), file_context, "COMPARE", kw, lineno, stripped)
                return

        # MOVEL/MOVE source, target
        m = re.match(r'^\s*(?:MOVEL|MOVE)\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            source = m.group(1)
            target = m.group(2).rstrip(';')
            if file_context:
                if self._is_file_field(target, file_context):
                    result.add_field_to_table(file_context, target, FieldUsage(
                        field=target, table=file_context, operation="ASSIGN",
                        context=m.group(0).split()[0], target=source, line=lineno, raw=stripped
                    ))
                if self._is_file_field(source, file_context):
                    result.add_field_to_table(file_context, source, FieldUsage(
                        field=source, table=file_context, operation="READ",
                        context=m.group(0).split()[0], line=lineno, raw=stripped
                    ))
            return

        # Z-ADD source, target
        m = re.match(r'^\s*Z-ADD\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            source = m.group(1)
            target = m.group(2).rstrip(';')
            if file_context and self._is_file_field(target, file_context):
                result.add_field_to_table(file_context, target, FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="Z-ADD", target=source, line=lineno, raw=stripped
                ))
            return

        # MULT factor1, factor2, target
        m = re.match(r'^\s*MULT\s+(\S+)\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            target = m.group(3).rstrip(';')
            if file_context and self._is_file_field(target, file_context):
                result.add_field_to_table(file_context, target, FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="MULT", target=f"{m.group(1)}*{m.group(2)}",
                    line=lineno, raw=stripped
                ))
            return

        # D-Spec 字段定义（仅分析与文件关联的字段）
        m = re.match(r'^D\s+(\S+)\s+S\s+', stripped, re.IGNORECASE)
        if m:
            field_name = m.group(1).upper()
            # 检查是否有 EXTNAME 关联
            ext_match = re.search(r'EXTNAME\((\S+)', stripped, re.IGNORECASE)
            if ext_match:
                ext_file = ext_match.group(1).rstrip(')')
                self.registered_files.add(ext_file)

    def _is_file_field(self, field_name: str, file_context: str) -> bool:
        """判断字段是否可能属于某个文件"""
        # 简单启发式：字段名包含文件名前缀，或文件名包含字段名前缀
        if not file_context:
            return False
        field_upper = field_name.upper()
        # 常见模式：文件名缩写 + 字段名，如 OHORDNO (ORDERH + ORDNO)
        # 或者直接匹配
        return True  # 暂时返回 True，让所有字段都关联到当前文件

    def _extract_fields_from_expr(self, result, expr, file_context, operation, context, lineno, raw):
        """从表达式中提取字段引用"""
        keywords = {
            'AND', 'OR', 'NOT', 'IF', 'THEN', 'ELSE', 'ENDIF', 'WHEN', 'OTHER',
            'DO', 'ENDDO', 'DOW', 'DOU', 'FOR', 'ENDFOR', 'SELECT', 'ENDSL',
            'LE', 'GE', 'LT', 'GT', 'EQ', 'NE', 'ON', 'OFF', 'BLANK', 'ZERO',
            'INIT', 'HIVAL', 'LOVAL', 'NULL', 'DSPATR', 'COLOR',
            'RED', 'GREEN', 'BLUE', 'YELLOW', 'WHITE',
            'REVVIDEO', 'BLINK', 'UNDL', 'PACKED', 'ZONED',
            'FOUND', 'EOF', 'IN', 'DS', 'S', 'UNKNOWN',
            # RPG 内置函数（接受文件名作为参数）
            'EOF', 'EQUAL', 'FOUND', 'HIVAL', 'LOVAL', 'NULLIND',
            'STATUS', 'SIZE', 'LEN', 'TRIM', 'TRIML', 'TRIMR',
            'SUBST', 'REPLACE', 'SCAN', 'CHECK', 'CHECKR',
            'EDITC', 'EDITW', 'DETECT', 'LOOKUP',
        }

        # 移除字符串字面量（单引号和双引号内的内容）
        cleaned = re.sub(r"'[^']*'", "''", expr)
        cleaned = re.sub(r'"[^"]*"', '""', cleaned)

        # 移除 %EOF(filename), %FOUND(filename) 等内置函数调用中的文件名
        cleaned = re.sub(r'%\w+\((\w+)\)', '', cleaned)

        fields = re.findall(r'\b([A-Z][A-Z0-9_]*)\b', cleaned.upper())
        for f in fields:
            if f not in keywords and not f.isdigit() and len(f) > 1:
                if file_context:
                    result.add_field_to_table(file_context, f, FieldUsage(
                        field=f, table=file_context, operation=operation,
                        context=context, line=lineno, raw=raw
                    ))

    def _parse_sql_block(self, result, block, end_lineno):
        """解析 EXEC SQL 块"""
        sql_text = ' '.join(block)

        # 提取表名
        for m in re.finditer(r'FROM\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-SELECT",
                context="FROM", line=end_lineno, raw=sql_text[:80]
            ))

        for m in re.finditer(r'JOIN\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-JOIN",
                context="JOIN", line=end_lineno, raw=sql_text[:80]
            ))

        for m in re.finditer(r'INTO\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-INSERT-INTO",
                context="INTO", line=end_lineno, raw=sql_text[:80]
            ))

        for m in re.finditer(r'UPDATE\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-UPDATE",
                context="UPDATE", line=end_lineno, raw=sql_text[:80]
            ))

        for m in re.finditer(r'DELETE\s+FROM\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-DELETE",
                context="DELETE FROM", line=end_lineno, raw=sql_text[:80]
            ))

        # 提取字段（SET 子句、WHERE 子句中的字段）
        # 简化处理：提取 :variable 形式的宿主变量
        for m in re.finditer(r':(\w+)', sql_text):
            var_name = m.group(1).upper()
            # 这些是宿主变量，可能对应文件字段
            # 暂时不关联到具体文件

    def _parse_data_area_operations(self, result, line, lineno):
        """解析 Data Area 操作"""
        stripped = line.strip()

        # INDTAARA name / IN name
        m = re.match(r'^\s*(?:INDTAARA|IN)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="IN", line=lineno, raw=stripped
            ))
            return

        # OUTDTAARA name / OUT name
        m = re.match(r'^\s*(?:OUTDTAARA|OUT)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="OUT", line=lineno, raw=stripped
            ))
            return

        # CHAINDTAARA name
        m = re.match(r'^\s*CHAINDTAARA\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="CHAIN", line=lineno, raw=stripped
            ))
            return


# ============================================================
# CL/CLP 解析器
# ============================================================

class CLParser:

    def parse(self, filepath: str, lines: list) -> ProgramAnalysis:
        result = ProgramAnalysis(
            file_path=filepath,
            program_name=Path(filepath).stem,
            program_type="CL"
        )

        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()

            if stripped and stripped[0] == '*':
                continue
            if stripped.strip().startswith('/*'):
                continue

            self._parse_copy_include(result, stripped, i)
            self._parse_call(result, stripped, i)
            self._parse_dcl_file(result, stripped, i)
            self._parse_dcl_dtaara(result, stripped, i)
            self._parse_dtaara_ops(result, stripped, i)
            self._parse_chgvar(result, stripped, i)

        return result

    def _parse_copy_include(self, result, line, lineno):
        m = re.match(r'^\s*/(?:COPY|INCLUDE)\s+(\S+)', line, re.IGNORECASE)
        if m:
            path_part = m.group(1)
            library, file_name, member = "", "", ""

            if ',' in path_part:
                parts = path_part.split(',', 1)
                library = parts[0]
                member = parts[1]
                file_name = member
            elif '/' in path_part:
                parts = path_part.rsplit('/', 1)
                library = parts[0]
                file_name = parts[1]
            else:
                file_name = path_part

            result.copy_includes.append(CopyInclude(
                directive="/COPY" if '/COPY' in line.upper() else "/INCLUDE",
                library=library, file=file_name, member=member,
                line=lineno, raw=line.strip()
            ))

    def _parse_call(self, result, line, lineno):
        m = re.match(r'^\s*CALL\s+(\S+)', line, re.IGNORECASE)
        if m:
            program = m.group(1).strip('"').strip("'").rstrip(';').upper()
            result.program_calls.append(ProgramCall(
                program=program, call_type="CALL",
                line=lineno, raw=line.strip()
            ))

    def _parse_dcl_file(self, result, line, lineno):
        m = re.match(r'^\s*DCL\s+(?:FILE|PROG)\s*\((\S+)', line, re.IGNORECASE)
        if m:
            name = m.group(1).strip('"').strip("'").upper()
            result.file_refs.append(FileRef(
                name=name, usage="UNKNOWN", file_type="CL_DECL",
                line=lineno, raw=line.strip()
            ))

    def _parse_dcl_dtaara(self, result, line, lineno):
        m = re.match(r'^\s*DCL-DTAARA\s+(\S+)(?:\s+(.*))?', line, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            rest = (m.group(2) or "").upper()

            data_type, length = "", ""
            type_match = re.search(r'TYPE\((\w+)\)', rest)
            len_match = re.search(r'LEN\((\d+)\)', rest)
            if type_match:
                data_type = type_match.group(1)
            if len_match:
                length = len_match.group(1)

            result.data_area_refs.append(DataAreaRef(
                name=name, operation="DEFINE", data_type=data_type,
                length=length, line=lineno, raw=line.strip()
            ))

    def _parse_dtaara_ops(self, result, line, lineno):
        stripped = line.strip()

        m = re.match(r'^\s*(?:CHGDTAARA|CHAINDTAARA)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            op = "CHAIN" if 'CHAINDTAARA' in stripped.upper() else "OUT"
            result.data_area_refs.append(DataAreaRef(
                name=name, operation=op, line=lineno, raw=stripped
            ))

        m = re.match(r'^\s*RTVDTAARA\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            name = m.group(1).rstrip(';').upper()
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="IN", line=lineno, raw=stripped
            ))

    def _parse_chgvar(self, result, line, lineno):
        m = re.match(r'^\s*CHGVAR\s+(\S+)\s+(.*)', line, re.IGNORECASE)
        if m:
            target = m.group(1).rstrip(';')
            expr = m.group(2).rstrip(';')
            result.field_usages = getattr(result, 'field_usages', [])
            result.field_usages.append(FieldUsage(
                field=target.upper(), table="", operation="ASSIGN",
                context="CHGVAR", target=expr, line=lineno, raw=line.strip()
            ))


# ============================================================
# COBOL 解析器（简化版）
# ============================================================

class COBOLParser:

    def parse(self, filepath: str, lines: list) -> ProgramAnalysis:
        result = ProgramAnalysis(
            file_path=filepath,
            program_name=Path(filepath).stem,
            program_type="COBOL"
        )

        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()
            if not stripped.strip():
                continue
            if len(stripped) > 6 and stripped[6] == '*':
                continue

            # COPY
            m = re.match(r'^\s+COPY\s+(\S+)', stripped, re.IGNORECASE)
            if m:
                path_part = m.group(1).rstrip('.')
                library, file_name = "", path_part
                if '.' in path_part:
                    parts = path_part.split('.', 1)
                    library = parts[0]
                    file_name = parts[1]
                result.copy_includes.append(CopyInclude(
                    directive="COPY", library=library, file=file_name,
                    line=i, raw=stripped.strip()
                ))
                continue

            # CALL
            m = re.match(r'^\s+CALL\s+[\'"]?(\S+)[\'"]?', stripped, re.IGNORECASE)
            if m:
                program = m.group(1).strip('"').strip("'").upper()
                result.program_calls.append(ProgramCall(
                    program=program, call_type="CALL",
                    line=i, raw=stripped.strip()
                ))
                continue

            # FD / SD
            m = re.match(r'^\s+(?:FD|SD)\s+(\S+)', stripped, re.IGNORECASE)
            if m:
                name = m.group(1).upper()
                result.file_refs.append(FileRef(
                    name=name, usage="FILE", file_type="COBOL_FD",
                    line=i, raw=stripped.strip()
                ))
                continue

            # SELECT
            m = re.match(r'^\s+SELECT\s+(\S+)', stripped, re.IGNORECASE)
            if m:
                name = m.group(1).upper()
                result.file_refs.append(FileRef(
                    name=name, usage="SELECT", file_type="ASSIGN",
                    line=i, raw=stripped.strip()
                ))

        return result


# ============================================================
# 报告生成器
# ============================================================

class ReportGenerator:

    def generate(self, analysis: ProgramAnalysis) -> str:
        lines = []
        lines.append(f"# 程序分析报告: {analysis.program_name}")
        lines.append("")
        lines.append(f"- **文件路径**: `{analysis.file_path}`")
        lines.append(f"- **程序类型**: {analysis.program_type}")
        lines.append(f"- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # ── 1. 表/文件声明 ──
        lines.append("## 1. 表/文件声明")
        lines.append("")
        if analysis.file_refs:
            lines.append("| # | 文件名 | 使用方式 | 类型 | 行号 |")
            lines.append("|---|--------|----------|------|------|")
            for idx, fr in enumerate(analysis.file_refs, 1):
                lines.append(f"| {idx} | `{fr.name}` | {fr.usage} | {fr.file_type} | {fr.line} |")
        else:
            lines.append("*无表/文件声明*")
        lines.append("")

        # ── 2. 表字段概览 ──
        lines.append("## 2. 表字段概览")
        lines.append("")
        if analysis.table_fields:
            lines.append("| # | 表名 | 涉及字段数 | 字段列表 |")
            lines.append("|---|------|-----------|---------|")
            for idx, (table_name, tfi) in enumerate(sorted(analysis.table_fields.items()), 1):
                field_names = sorted([f for f in tfi.fields.keys() if f != '*'])
                field_list = ', '.join(f'`{f}`' for f in field_names[:10])
                if len(field_names) > 10:
                    field_list += f' ... (+{len(field_names)-10})'
                lines.append(f"| {idx} | `{table_name}` | {len(field_names)} | {field_list} |")
        else:
            lines.append("*未检测到表字段操作*")
        lines.append("")

        # ── 3. 按表展开字段处理流程 ──
        lines.append("## 3. 字段处理流程（按表展开）")
        lines.append("")
        if analysis.table_fields:
            for table_name in sorted(analysis.table_fields.keys()):
                tfi = analysis.table_fields[table_name]
                lines.append(f"### 表: `{table_name}`")
                lines.append("")

                # 过滤掉占位符字段
                real_fields = {f: usages for f, usages in tfi.fields.items() if f != '*'}

                if real_fields:
                    for field_name in sorted(real_fields.keys()):
                        usages = real_fields[field_name]
                        lines.append(f"#### 字段: `{field_name}`")
                        lines.append("")
                        lines.append("| # | 操作 | 上下文 | 目标/表达式 | 行号 |")
                        lines.append("|---|------|--------|------------|------|")
                        for idx, u in enumerate(usages, 1):
                            lines.append(f"| {idx} | {u.operation} | {u.context} | {u.target} | {u.line} |")
                        lines.append("")
                else:
                    lines.append("*仅检测到SQL引用，无字段级操作*")
                    lines.append("")
        else:
            lines.append("*未检测到表字段操作*")
            lines.append("")

        # ── 4. Data Area ──
        lines.append("## 4. Data Area")
        lines.append("")
        if analysis.data_area_refs:
            # 按名称分组
            dtaara_map = {}
            for ref in analysis.data_area_refs:
                if ref.name not in dtaara_map:
                    dtaara_map[ref.name] = []
                dtaara_map[ref.name].append(ref)

            lines.append("| # | 名称 | 类型 | 长度 | 操作列表 |")
            lines.append("|---|------|------|------|---------|")
            for idx, (name, refs) in enumerate(sorted(dtaara_map.items()), 1):
                ops = ', '.join(set(r.operation for r in refs))
                data_type = next((r.data_type for r in refs if r.data_type), "")
                length = next((r.length for r in refs if r.length), "")
                lines.append(f"| {idx} | `{name}` | {data_type} | {length} | {ops} |")
            lines.append("")

            # 详细操作
            lines.append("### Data Area 操作详情")
            lines.append("")
            for name in sorted(dtaara_map.keys()):
                refs = dtaara_map[name]
                lines.append(f"#### `{name}`")
                lines.append("")
                lines.append("| # | 操作 | 行号 | 原始语句 |")
                lines.append("|---|------|------|---------|")
                for idx, r in enumerate(refs, 1):
                    lines.append(f"| {idx} | {r.operation} | {r.line} | `{r.raw}` |")
                lines.append("")
        else:
            lines.append("*无 Data Area 引用*")
            lines.append("")

        # ── 5. /COPY、/INCLUDE ──
        lines.append("## 5. COPY/INCLUDE 引用")
        lines.append("")
        if analysis.copy_includes:
            lines.append("| # | 指令 | 库名 | 文件名 | 成员名 | 行号 |")
            lines.append("|---|------|------|--------|--------|------|")
            for idx, ci in enumerate(analysis.copy_includes, 1):
                lines.append(f"| {idx} | {ci.directive} | {ci.library} | {ci.file} | {ci.member} | {ci.line} |")
        else:
            lines.append("*无 COPY/INCLUDE 引用*")
        lines.append("")

        # ── 6. 程序调用 ──
        lines.append("## 6. 程序调用")
        lines.append("")
        if analysis.program_calls:
            lines.append("| # | 被调用程序 | 调用方式 | 行号 |")
            lines.append("|---|-----------|----------|------|")
            for idx, pc in enumerate(analysis.program_calls, 1):
                lines.append(f"| {idx} | `{pc.program}` | {pc.call_type} | {pc.line} |")
        else:
            lines.append("*无程序调用*")
        lines.append("")

        # ── 7. 汇总 ──
        lines.append("## 7. 汇总")
        lines.append("")
        total_fields = sum(
            len([f for f in tfi.fields.keys() if f != '*'])
            for tfi in analysis.table_fields.values()
        )
        lines.append("| 统计项 | 数量 |")
        lines.append("|--------|------|")
        lines.append(f"| 表/文件声明 | {len(analysis.file_refs)} |")
        lines.append(f"| 涉及表数 | {len(analysis.table_fields)} |")
        lines.append(f"| 表字段总数 | {total_fields} |")
        lines.append(f"| Data Area | {len(set(r.name for r in analysis.data_area_refs))} |")
        lines.append(f"| COPY/INCLUDE | {len(analysis.copy_includes)} |")
        lines.append(f"| 程序调用 | {len(analysis.program_calls)} |")

        return "\n".join(lines)


# ============================================================
# 主程序
# ============================================================

def detect_program_type(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    type_map = {
        '.rpgle': 'RPGLE', '.rpgleinc': 'RPGLE', '.sqlrpgle': 'RPGLE',
        '.clp': 'CL', '.clle': 'CL', '.cl': 'CL',
        '.cbl': 'COBOL', '.cob': 'COBOL', '.sqc': 'RPGLE',
    }
    return type_map.get(ext, 'UNKNOWN')


def get_parser(program_type: str):
    parsers = {'RPGLE': RPGLEParser, 'CL': CLParser, 'COBOL': COBOLParser}
    cls = parsers.get(program_type)
    return cls() if cls else None


def analyze_file(filepath: str, output_base: str, source_base: str) -> Optional[str]:
    program_type = detect_program_type(filepath)
    if program_type == 'UNKNOWN':
        return None

    parser = get_parser(program_type)
    if not parser:
        return None

    try:
        content = None
        for encoding in ['utf-8', 'cp937', 'cp037', 'latin-1', 'utf-16']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if content is None:
            return f"无法读取文件（编码不支持）: {filepath}"

        lines = content.splitlines()
        analysis = parser.parse(filepath, lines)

        report = ReportGenerator().generate(analysis)

        rel_path = os.path.relpath(filepath, source_base)
        rel_dir = os.path.dirname(rel_path)
        filename = Path(filepath).stem + ".md"

        output_dir = os.path.join(output_base, rel_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return None
    except Exception as e:
        return f"分析文件时出错: {filepath} - {str(e)}"


def collect_program_files(path: str) -> list:
    program_extensions = {
        '.rpgle', '.rpgleinc', '.sqlrpgle',
        '.clp', '.clle', '.cl',
        '.cbl', '.cob', '.sqc',
    }
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for root, dirs, filenames in os.walk(path):
            for fn in filenames:
                if Path(fn).suffix.lower() in program_extensions:
                    files.append(os.path.join(root, fn))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description='IBM i 程序代码分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s /path/to/rpg_source
  %(prog)s /path/to/program.rpgle
  %(prog)s /path/to/source --output /path/to/analyze
        """
    )
    parser.add_argument('path', help='要分析的文件或目录路径')
    parser.add_argument('--output', '-o', default='analyze', help='输出目录（默认: analyze）')

    args = parser.parse_args()
    source_path = os.path.abspath(args.path)
    output_path = os.path.abspath(args.output)

    if not os.path.exists(source_path):
        print(f"错误: 路径不存在: {source_path}")
        sys.exit(1)

    print(f"IBM i 程序分析器")
    print(f"=" * 50)
    print(f"源路径: {source_path}")
    print(f"输出目录: {output_path}")
    print()

    files = collect_program_files(source_path)
    if not files:
        print("未找到可分析的程序文件（.rpgle, .clp, .clle, .cbl, .cob, .sqc 等）")
        sys.exit(1)

    print(f"找到 {len(files)} 个程序文件")
    print()

    errors = []
    analyzed = 0
    for filepath in files:
        rel = os.path.relpath(filepath, source_path)
        print(f"分析: {rel} ... ", end="", flush=True)
        error = analyze_file(filepath, output_path, source_path)
        if error:
            print(f"⚠ {error}")
            errors.append(error)
        else:
            print("✓")
            analyzed += 1

    print()
    print(f"=" * 50)
    print(f"分析完成: {analyzed} 个文件成功, {len(errors)} 个错误")
    print(f"结果输出到: {output_path}")

    if errors:
        print()
        print("错误列表:")
        for err in errors:
            print(f"  - {err}")


if __name__ == '__main__':
    main()

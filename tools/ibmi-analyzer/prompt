#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IBM i Program Source Code Analyzer

Features:
  Analyze RPG/RPGLE, CL/CLP, COBOL program source code, extracting:
  1. Table/File declarations and field usage
  2. Data Area - declarations, read/write operations, DS decomposition
  3. /COPY, /INCLUDE references
  4. Program calls
  5. Field propagation chains (end-to-end)
  6. Conditions for each operation

Usage:
  python analyze_ibmi.py <file_or_dir> [--output <output_dir>]
"""

import os
import re
import sys
import argparse
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set, Tuple
from pathlib import Path
from datetime import datetime


# ============================================================
# Data Structures
# ============================================================

@dataclass
class CopyInclude:
    directive: str
    library: str
    file: str
    member: str = ""
    line: int = 0
    raw: str = ""

@dataclass
class FileRef:
    name: str
    usage: str
    file_type: str
    line: int = 0
    raw: str = ""

@dataclass
class ProgramCall:
    program: str
    call_type: str
    parameters: list = field(default_factory=list)
    line: int = 0
    raw: str = ""

@dataclass
class DataAreaRef:
    name: str
    operation: str
    data_type: str = ""
    length: str = ""
    line: int = 0
    raw: str = ""

@dataclass
class DataAreaDS:
    ds_name: str
    dtaara_name: str
    fields: Dict[str, str] = field(default_factory=dict)
    line: int = 0

@dataclass
class Condition:
    """Condition information"""
    type: str           # IF/WHEN/DOW/DOU/ELSE
    expression: str     # Condition expression
    line: int = 0

@dataclass
class FieldUsage:
    field: str
    table: str
    operation: str
    context: str
    target: str = ""
    is_written: bool = False
    conditions: List[Condition] = field(default_factory=list)  # Trigger conditions
    line: int = 0
    raw: str = ""

@dataclass
class FieldChain:
    """Field propagation chain"""
    start_field: str                    # Source field
    end_field: str                      # Target field
    end_type: str                       # FILE or DS
    end_table: str = ""                 # Target table name
    chain: List[Tuple[str, str]] = field(default_factory=list)  # [(field, expression)]
    conditions: List[Condition] = field(default_factory=list)
    line: int = 0

@dataclass
class TableFieldInfo:
    table: str
    fields: Dict[str, List[FieldUsage]] = field(default_factory=dict)
    is_output_table: bool = False

    def add_field_usage(self, field_name: str, usage: FieldUsage):
        if field_name not in self.fields:
            self.fields[field_name] = []
        self.fields[field_name].append(usage)

@dataclass
class EntryPoint:
    """Program entry point"""
    name: str               # MAIN, *INZSR, ENTRY, etc.
    type: str               # MAIN, INZSR, ENTRY, CL_MAIN
    line: int = 0
    parameters: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class ProgramAnalysis:
    file_path: str
    program_name: str
    program_type: str
    copy_includes: list = field(default_factory=list)
    file_refs: list = field(default_factory=list)
    program_calls: list = field(default_factory=list)
    data_area_refs: list = field(default_factory=list)
    data_area_ds_list: list = field(default_factory=list)
    table_fields: Dict[str, TableFieldInfo] = field(default_factory=dict)
    field_chains: List[FieldChain] = field(default_factory=list)
    entry_points: List[EntryPoint] = field(default_factory=list)
    errors: list = field(default_factory=list)

    def add_field_to_table(self, table: str, field_name: str, usage: FieldUsage):
        if table not in self.table_fields:
            self.table_fields[table] = TableFieldInfo(table=table)
        self.table_fields[table].add_field_usage(field_name, usage)

    def mark_table_as_output(self, table: str):
        if table in self.table_fields:
            self.table_fields[table].is_output_table = True


# ============================================================
# RPG/RPGLE Parser
# ============================================================

class RPGLEParser:

    def __init__(self):
        self.registered_files: Set[str] = set()
        self.registered_dtaara: Set[str] = set()
        self.dtaara_ds_map: Dict[str, str] = {}
        self.output_files: Set[str] = set()
        self.condition_stack: List[Condition] = []  # Condition stack
        self.field_assignments: Dict[str, List[Tuple[str, str, int, List[Condition]]]] = {}  # field -> [(target, expr, line, conditions)]

    def parse(self, filepath: str, lines: list) -> ProgramAnalysis:
        result = ProgramAnalysis(
            file_path=filepath,
            program_name=Path(filepath).stem,
            program_type="RPGLE"
        )

        in_sql = False
        sql_block = []
        current_file_context = ""
        dcl_done = False
        main_entry_added = False

        # Pass 1: Identify all declarations and output files
        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()
            if stripped and stripped[0] == '*':
                continue
            if not stripped.strip():
                continue
            self._parse_fspec(result, stripped, i)
            self._parse_dcl_f(result, stripped, i)
            self._parse_data_area_decl(result, stripped, i)
            self._parse_ds_decl(result, stripped, i)
            self._mark_output_files(stripped, i)
            self._parse_entry_points(result, stripped, i)

        # Pass 2: Parse operations and fields
        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()
            if stripped and stripped[0] == '*':
                continue
            if not stripped.strip():
                continue

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

            self._parse_copy_include(result, stripped, i)
            self._parse_call(result, stripped, i)

            # Parse condition blocks (maintain condition stack)
            self._parse_condition_block(stripped, i)

            # Parse file operations
            ctx = self._parse_file_operation(result, stripped, i)
            if ctx:
                current_file_context = ctx

            # Parse field operations
            self._parse_field_operations(result, stripped, i, current_file_context)

            # Parse Data Area operations
            self._parse_data_area_operations(result, stripped, i)

            # Detect main entry for *FREE format RPG (first executable after DCL)
            if not main_entry_added and not any(ep.type == "MAIN" for ep in result.entry_points):
                stripped_line = stripped.strip()
                # Skip DCL, /COPY, comments, blank lines
                if stripped_line and not re.match(r'^\s*(?:DCL-|D\s|/COPY|/INCLUDE|\*)', stripped, re.IGNORECASE):
                    # This is the first executable statement
                    result.entry_points.insert(0, EntryPoint(
                        name="MAIN", type="MAIN", line=i,
                        description="Main program entry point"
                    ))
                    main_entry_added = True

        # Build field chains
        self._build_field_chains(result)

        return result

    def _parse_fspec(self, result, line, lineno):
        m = re.match(r'^F\s+(\S+)\s+(.*)', line, re.IGNORECASE)
        if not m:
            return
        filename = m.group(1).upper()
        rest = m.group(2).upper()
        usage = ""
        for u, p in [('INPUT', r'\bI\b'), ('OUTPUT', r'\bO\b'),
                     ('UPDATE', r'\bU\b'), ('INPUT/OUTPUT', r'\bIO\b')]:
            if re.search(p, rest):
                usage = u
                break
        self.registered_files.add(filename)
        result.file_refs.append(FileRef(
            name=filename, usage=usage or "DISK", file_type="DISK",
            line=lineno, raw=line.strip()
        ))

    def _parse_dcl_f(self, result, line, lineno):
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
        m = re.match(r'^\s*/(?:COPY|INCLUDE)\s+(\S+)', line, re.IGNORECASE)
        if not m:
            return
        path_part = m.group(1)
        library, file_name, member = "", "", ""
        if ',' in path_part:
            parts = path_part.split(',', 1)
            library, member = parts[0], parts[1]
            file_name = member
        elif '/' in path_part:
            parts = path_part.rsplit('/', 1)
            library, file_name = parts[0], parts[1]
        else:
            file_name = path_part
        result.copy_includes.append(CopyInclude(
            directive="/COPY" if '/COPY' in line.upper() else "/INCLUDE",
            library=library, file=file_name, member=member,
            line=lineno, raw=line.strip()
        ))

    def _parse_call(self, result, line, lineno):
        stripped = line.strip().rstrip(';')
        m = re.match(
            r'^\s*(CALL|CALLP|CALLB|CALLPRC)\s+(?:\'([^\']+)\'|([A-Z][A-Z0-9_]*))(?:\(.*?\))?',
            stripped, re.IGNORECASE
        )
        if m:
            program = (m.group(2) or m.group(3)).split('(')[0].strip()
            if program:
                result.program_calls.append(ProgramCall(
                    program=program.upper(), call_type=m.group(1).upper(),
                    line=lineno, raw=line.strip()
                ))
        # EXTPGM
        m = re.match(r'^\s*D\s+\S+\s+\S+\s+EXTPGM\((?:\'([^\']+)\'|(\S+))\)', stripped, re.IGNORECASE)
        if m:
            program = (m.group(1) or m.group(2)).rstrip(')').upper()
            result.program_calls.append(ProgramCall(
                program=program, call_type="EXTPGM",
                line=lineno, raw=line.strip()
            ))

    def _parse_data_area_decl(self, result, line, lineno):
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
            self.registered_dtaara.add(name)
            result.data_area_refs.append(DataAreaRef(
                name=name, operation="DEFINE", data_type=data_type,
                length=length, line=lineno, raw=line.strip()
            ))

    def _parse_ds_decl(self, result, line, lineno):
        m = re.match(r'^\s*DCL-DS\s+(\S+)(?:\s+(.*))?', line, re.IGNORECASE)
        if not m:
            m = re.match(r'^\s*D\s+(\S+)\s+DS\s+(.*)', line, re.IGNORECASE)
            if not m:
                return
        ds_name = m.group(1).rstrip(';').upper()
        rest = (m.group(2) or "").upper().rstrip(';')
        dtaara_match = re.search(r'EXTDTAARA\((\S+)\)', rest)
        if not dtaara_match:
            dtaara_match = re.search(r'LIKEDS\((\S+)\)', rest)
        if not dtaara_match:
            dtaara_match = re.search(r'LIKE\((\S+)\)', rest)
        if dtaara_match:
            dtaara_name = dtaara_match.group(1).rstrip(')').upper()
            self.dtaara_ds_map[ds_name] = dtaara_name
        for dtaara_name in self.registered_dtaara:
            if ds_name.startswith(dtaara_name) or dtaara_name.startswith(ds_name):
                self.dtaara_ds_map[ds_name] = dtaara_name
                break

    def _mark_output_files(self, line, lineno):
        stripped = line.strip().rstrip(';')
        for pattern in [r'^\s*WRITE\s+(\S+)', r'^\s*UPDATE\s+(\S+)', r'^\s*DELETE\s+(\S+)']:
            m = re.match(pattern, stripped, re.IGNORECASE)
            if m:
                filename = m.group(1).upper()
                if filename in self.registered_files:
                    self.output_files.add(filename)

    def _parse_entry_points(self, result, line, lineno):
        """Parse entry points: ENTRY procedure, *INZSR subroutine"""
        stripped = line.strip().rstrip(';')

        # D-PROCEDURE with ENTRY keyword (free format RPG)
        m = re.match(r'^\s*D\s+(\S+)\s+\S+\s+PROCEDURE\b.*ENTRY\b', stripped, re.IGNORECASE)
        if m:
            proc_name = m.group(1).upper()
            # Extract parameters from PI
            params = []
            param_match = re.search(r'PI\s*\(([^)]*)\)', stripped, re.IGNORECASE)
            if param_match:
                params = [p.strip().upper() for p in param_match.group(1).split(',') if p.strip()]
            result.entry_points.append(EntryPoint(
                name=proc_name, type="ENTRY", line=lineno,
                parameters=params, description=f"Entry procedure: {proc_name}"
            ))
            return

        # BEGSR *ENTRY (fixed format)
        m = re.match(r'^\s*BEGSR\s+\*ENTRY\b', stripped, re.IGNORECASE)
        if m:
            result.entry_points.append(EntryPoint(
                name="*ENTRY", type="ENTRY", line=lineno,
                description="Entry subroutine (*ENTRY)"
            ))
            return

        # BEGSR *INZSR (initialization subroutine)
        m = re.match(r'^\s*BEGSR\s+\*INZSR\b', stripped, re.IGNORECASE)
        if m:
            result.entry_points.append(EntryPoint(
                name="*INZSR", type="INZSR", line=lineno,
                description="Initialization subroutine (*INZSR)"
            ))
            return

        # D-PROCEDURE (free format) - main procedure detection
        m = re.match(r'^\s*D\s+(\S+)\s+\S+\s+PROCEDURE\b', stripped, re.IGNORECASE)
        if m:
            proc_name = m.group(1).upper()
            # Check if it's the first procedure (main)
            has_main = any(ep.type == "MAIN" for ep in result.entry_points)
            if not has_main:
                result.entry_points.append(EntryPoint(
                    name=proc_name, type="MAIN", line=lineno,
                    description=f"Main procedure: {proc_name}"
                ))

    def _parse_condition_block(self, line, lineno):
        """Parse condition blocks, maintain condition stack"""
        stripped = line.strip().rstrip(';')

        # IF / WHEN / DOW / DOU enter condition
        for kw in ['IF', 'WHEN', 'DOW', 'DOU']:
            m = re.match(rf'^\s*{kw}\s+(.*)', stripped, re.IGNORECASE)
            if m:
                expr = m.group(1).rstrip(';')
                self.condition_stack.append(Condition(
                    type=kw, expression=expr, line=lineno
                ))
                return

        # OTHERWISE / ELSE condition change
        m = re.match(r'^\s*(?:OTHERWISE|ELSE)', stripped, re.IGNORECASE)
        if m and self.condition_stack:
            # Get current IF condition expression, generate meaningful ELSE description
            current = self.condition_stack[-1]
            if current.type == 'IF':
                else_expr = f"ELSE(when {current.expression} is false)"
            else:
                else_expr = "ELSE"
            self.condition_stack[-1] = Condition(
                type="ELSE", expression=else_expr, line=lineno
            )
            return

        # ENDIF / ENDDO / ENDFOR / ENDSL exit condition
        m = re.match(r'^\s*ENDIF', stripped, re.IGNORECASE)
        if m and self.condition_stack:
            # Pop all IF type conditions
            for i in range(len(self.condition_stack) - 1, -1, -1):
                if self.condition_stack[i].type == 'IF':
                    self.condition_stack.pop(i)
                    break
            return

        m = re.match(r'^\s*END(?:DO|FOR|SL)', stripped, re.IGNORECASE)
        if m and self.condition_stack:
            self.condition_stack.pop()

    def _get_current_conditions(self) -> List[Condition]:
        """Get a copy of current condition stack"""
        return list(self.condition_stack)

    def _parse_file_operation(self, result, line, lineno) -> str:
        stripped = line.strip().rstrip(';')
        # CHAIN with two parameters
        m = re.match(r'^\s*CHAIN\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            param1, param2 = m.group(1).upper(), m.group(2).upper()
            if param2 in self.registered_files:
                return param2
            if param1 in self.registered_files:
                return param1
            return param2
        # All file operations
        for pattern, op in [
            (r'^\s*CHAIN\s+(\S+)', 'CHAIN'),
            (r'^\s*READ[PPE]*\s+(\S+)', 'READ'),
            (r'^\s*READE\s+(\S+)', 'READE'),
            (r'^\s*SETLL\s+(\S+)', 'SETLL'),
            (r'^\s*SETGT\s+(\S+)', 'SETGT'),
            (r'^\s*UPDATE\s+(\S+)', 'UPDATE'),
            (r'^\s*WRITE\s+(\S+)', 'WRITE'),
            (r'^\s*DELETE\s+(\S+)', 'DELETE'),
            (r'^\s*EXFMT\s+(\S+)', 'EXFMT'),
        ]:
            m = re.match(pattern, stripped, re.IGNORECASE)
            if m:
                filename = m.group(1).upper()
                if filename in self.registered_files:
                    if op in ('WRITE', 'UPDATE', 'DELETE'):
                        self.output_files.add(filename)
                        result.mark_table_as_output(filename)
                    return filename
        return ""

    def _parse_field_operations(self, result, line, lineno, file_context):
        stripped = line.strip()
        conditions = self._get_current_conditions()

        # EVAL field = expr
        m = re.match(r'^\s*EVAL\s+(\S+)\s*=\s*(.*)', stripped, re.IGNORECASE)
        if m:
            target = m.group(1).rstrip(';')
            expr = m.group(2).rstrip(';')
            is_written = file_context in self.output_files
            if file_context:
                usage = FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="EVAL", target=expr, is_written=is_written,
                    conditions=conditions, line=lineno, raw=stripped
                )
                result.add_field_to_table(file_context, target, usage)
                # Record assignment for chain analysis
                if target not in self.field_assignments:
                    self.field_assignments[target] = []
                self.field_assignments[target].append((target, expr, lineno, conditions))
            return

        # IF / WHEN / DOW / DOU conditions
        for kw in ['IF', 'WHEN', 'DOW', 'DOU']:
            m = re.match(rf'^\s*{kw}\s+(.*)', stripped, re.IGNORECASE)
            if m:
                if file_context:
                    result.add_field_to_table(file_context, "*", FieldUsage(
                        field="*", table=file_context, operation="CONDITION",
                        context=kw, target=m.group(1).rstrip(';'),
                        conditions=conditions, line=lineno, raw=stripped
                    ))
                return

        # MOVEL/MOVE source, target
        m = re.match(r'^\s*(?:MOVEL|MOVE)\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            source, target = m.group(1), m.group(2).rstrip(';')
            is_written = file_context in self.output_files
            if file_context:
                usage = FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context=m.group(0).split()[0], target=source,
                    is_written=is_written, conditions=conditions,
                    line=lineno, raw=stripped
                )
                result.add_field_to_table(file_context, target, usage)
                if target not in self.field_assignments:
                    self.field_assignments[target] = []
                self.field_assignments[target].append((target, source, lineno, conditions))
            return

        # Z-ADD source, target
        m = re.match(r'^\s*Z-ADD\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            source, target = m.group(1), m.group(2).rstrip(';')
            is_written = file_context in self.output_files
            if file_context:
                usage = FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="Z-ADD", target=source,
                    is_written=is_written, conditions=conditions,
                    line=lineno, raw=stripped
                )
                result.add_field_to_table(file_context, target, usage)
                if target not in self.field_assignments:
                    self.field_assignments[target] = []
                self.field_assignments[target].append((target, source, lineno, conditions))
            return

        # MULT factor1, factor2, target
        m = re.match(r'^\s*MULT\s+(\S+)\s+(\S+)\s+(\S+)', stripped, re.IGNORECASE)
        if m:
            target = m.group(3).rstrip(';')
            is_written = file_context in self.output_files
            if file_context:
                usage = FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="MULT", target=f"{m.group(1)}*{m.group(2)}",
                    is_written=is_written, conditions=conditions,
                    line=lineno, raw=stripped
                )
                result.add_field_to_table(file_context, target, usage)
                if target not in self.field_assignments:
                    self.field_assignments[target] = []
                self.field_assignments[target].append((target, f"{m.group(1)}*{m.group(2)}", lineno, conditions))
            return

        # DS.field = value
        m = re.match(r'^\s*(?:EVAL\s+)?(\w+)\.(\w+)\s*=\s*(.*)', stripped, re.IGNORECASE)
        if m:
            ds_name = m.group(1).upper()
            field_name = m.group(2).upper()
            expr = m.group(3).rstrip(';')
            if ds_name in self.dtaara_ds_map:
                dtaara_name = self.dtaara_ds_map[ds_name]
                result.data_area_ds_list.append(DataAreaDS(
                    ds_name=ds_name, dtaara_name=dtaara_name,
                    fields={field_name: expr}, line=lineno
                ))
                # Record DS field assignment for chain analysis
                ds_field_key = f"{ds_name}.{field_name}"
                if ds_field_key not in self.field_assignments:
                    self.field_assignments[ds_field_key] = []
                self.field_assignments[ds_field_key].append((ds_field_key, expr, lineno, conditions))
            return

        # Direct assignment without EVAL
        m = re.match(r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*(.*)', stripped, re.IGNORECASE)
        if m:
            target = m.group(1).rstrip(';').upper()
            expr = m.group(2).rstrip(';')
            is_written = file_context in self.output_files
            if file_context and target not in ('ENDIF', 'ENDDO', 'ENDFOR', 'ENDSL', 'ELSE', 'OTHERWISE'):
                usage = FieldUsage(
                    field=target, table=file_context, operation="ASSIGN",
                    context="ASSIGN", target=expr, is_written=is_written,
                    conditions=conditions, line=lineno, raw=stripped
                )
                result.add_field_to_table(file_context, target, usage)
                if target not in self.field_assignments:
                    self.field_assignments[target] = []
                self.field_assignments[target].append((target, expr, lineno, conditions))

    def _build_field_chains(self, result):
        """Build field propagation chains (end-to-end) - only keep complete paths from DB-read to final write"""
        # 1. Collect all assignment target fields
        all_target_fields = set(self.field_assignments.keys())

        # 2. Collect all fields appearing in expressions (potential DB-read fields)
        all_expr_fields = set()
        for target, assignments in self.field_assignments.items():
            for _, expr, _, _ in assignments:
                sources = self._extract_source_fields(expr)
                all_expr_fields.update(sources)

        # 3. DB-read fields = fields in expressions - assignment target fields
        # These are fields read from DB but never assigned
        db_read_fields = all_expr_fields - all_target_fields

        # 4. Collect all DB/DS write fields
        db_write_fields = {}  # {(table, field): [(line, conditions)]}
        for table_name, tfi in result.table_fields.items():
            if tfi.is_output_table:
                for fname, usages in tfi.fields.items():
                    if fname == '*':
                        continue
                    for u in usages:
                        if u.operation == "ASSIGN" and u.is_written:
                            key = (table_name, fname)
                            if key not in db_write_fields:
                                db_write_fields[key] = []
                            db_write_fields[key].append((u.line, u.conditions))

        ds_write_fields = {}  # {ds_field: [(line, conditions)]}
        for ds in result.data_area_ds_list:
            for fname in ds.fields.keys():
                ds_field = f"{ds.ds_name}.{fname}"
                if ds_field in self.field_assignments:
                    assignments = self.field_assignments[ds_field]
                    if assignments:
                        target, expr, line, conditions = assignments[-1]
                        if ds_field not in ds_write_fields:
                            ds_write_fields[ds_field] = []
                        ds_write_fields[ds_field].append((line, conditions))

        # 5. Build assignment graph: target -> [(source_fields, expr, line, conditions)]
        assignment_graph = {}  # {target: [(sources, expr, line, conditions)]}
        for target, assignments in self.field_assignments.items():
            for _, expr, line, conditions in assignments:
                sources = self._extract_source_fields(expr)
                if target not in assignment_graph:
                    assignment_graph[target] = []
                assignment_graph[target].append((sources, expr, line, conditions))

        # 6. Trace from output fields back to DB-read fields
        seen_chains = set()

        def find_path_to_db_read(field_name, visited=None, depth=0):
            """Trace from field back to find path to DB-read field"""
            if visited is None:
                visited = set()
            if depth > 15 or field_name in visited:
                return None
            visited.add(field_name)

            # If it's a DB-read field, return as starting point
            if field_name in db_read_fields:
                return [(field_name, "DB-READ", 0, [])]

            # Find assignment for this field
            if field_name in assignment_graph:
                for sources, expr, line, conditions in assignment_graph[field_name]:
                    if not sources:
                        continue
                    for src in sources:
                        if src == field_name:
                            continue
                        path = find_path_to_db_read(src, visited.copy(), depth + 1)
                        if path:
                            return path + [(field_name, expr, line, conditions)]

            return None

        # 7. Build chains for each DB-write field
        for (table_name, field_name), write_records in db_write_fields.items():
            path = find_path_to_db_read(field_name)
            if path and len(path) >= 2:
                start = path[0][0]
                chain_key = (start, field_name, table_name)
                if chain_key not in seen_chains:
                    seen_chains.add(chain_key)
                    result.field_chains.append(FieldChain(
                        start_field=start,
                        end_field=field_name,
                        end_type="FILE",
                        end_table=table_name,
                        chain=path,
                        line=path[-1][2]
                    ))

        # 8. Build chains for each DS-write field
        for ds_field, write_records in ds_write_fields.items():
            for line, conditions in write_records:
                path = find_path_to_db_read(ds_field)
                if path and len(path) >= 2:
                    start = path[0][0]
                    chain_key = (start, ds_field, "DS")
                    if chain_key not in seen_chains:
                        seen_chains.add(chain_key)
                        result.field_chains.append(FieldChain(
                            start_field=start,
                            end_field=ds_field,
                            end_type="DS",
                            chain=path,
                            line=path[-1][2]
                        ))

    def _extract_source_fields(self, expr: str) -> List[str]:
        """Extract source fields from expression"""
        keywords = {
            'AND', 'OR', 'NOT', 'IF', 'THEN', 'ELSE', 'ENDIF', 'WHEN',
            'DO', 'ENDDO', 'DOW', 'DOU', 'FOR', 'ENDFOR',
            'LE', 'GE', 'LT', 'GT', 'EQ', 'NE', 'ON', 'OFF',
            'BLANK', 'ZERO', 'NULL', 'FOUND', 'EOF', 'IN',
        }
        # Remove strings and function calls
        cleaned = re.sub(r"'[^']*'", "''", expr)
        cleaned = re.sub(r'"[^"]*"', '""', cleaned)
        cleaned = re.sub(r'%\w+\([^)]*\)', '', cleaned)
        cleaned = re.sub(r'\w+\.\w+', '', cleaned)  # DS.field

        fields = re.findall(r'\b([A-Z][A-Z0-9_]*)\b', cleaned.upper())
        result = []
        for f in fields:
            if f not in keywords and not f.isdigit() and len(f) > 1:
                result.append(f)
        return result

    def _parse_sql_block(self, result, block, end_lineno):
        sql_text = ' '.join(block)
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
            result.mark_table_as_output(table)
            result.add_field_to_table(table, "*", FieldUsage(
                field="*", table=table, operation="SQL-INSERT-INTO",
                context="INTO", line=end_lineno, raw=sql_text[:80]
            ))
        for m in re.finditer(r'UPDATE\s+(\w+)', sql_text, re.IGNORECASE):
            table = m.group(1).upper()
            result.mark_table_as_output(table)
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

    def _parse_data_area_operations(self, result, line, lineno):
        stripped = line.strip()
        for pattern, op in [
            (r'^\s*(?:INDTAARA|IN)\s+(\S+)', 'IN'),
            (r'^\s*(?:OUTDTAARA|OUT)\s+(\S+)', 'OUT'),
            (r'^\s*CHAINDTAARA\s+(\S+)', 'CHAIN'),
        ]:
            m = re.match(pattern, stripped, re.IGNORECASE)
            if m:
                name = m.group(1).rstrip(';').upper()
                result.data_area_refs.append(DataAreaRef(
                    name=name, operation=op, line=lineno, raw=stripped
                ))
                return


# ============================================================
# CL/CLP Parser
# ============================================================

class CLParser:

    def parse(self, filepath: str, lines: list) -> ProgramAnalysis:
        result = ProgramAnalysis(
            file_path=filepath,
            program_name=Path(filepath).stem,
            program_type="CL"
        )
        first_command_found = False
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
            # Detect first executable command as entry point
            if not first_command_found and stripped.strip():
                if not re.match(r'^\s*(?:DCL|/*)', stripped, re.IGNORECASE):
                    result.entry_points.append(EntryPoint(
                        name="MAIN", type="CL_MAIN", line=i,
                        description=f"CL program entry point"
                    ))
                    first_command_found = True
        return result

    def _parse_copy_include(self, result, line, lineno):
        m = re.match(r'^\s*/(?:COPY|INCLUDE)\s+(\S+)', line, re.IGNORECASE)
        if m:
            path_part = m.group(1)
            library, file_name, member = "", "", ""
            if ',' in path_part:
                parts = path_part.split(',', 1)
                library, member = parts[0], parts[1]
                file_name = member
            elif '/' in path_part:
                parts = path_part.rsplit('/', 1)
                library, file_name = parts[0], parts[1]
            else:
                file_name = path_part
            result.copy_includes.append(CopyInclude(
                directive="/COPY" if '/COPY' in line.upper() else "/INCLUDE",
                library=library, file=file_name, member=member,
                line=lineno, raw=line.strip()
            ))

    def _parse_call(self, result, line, lineno):
        m = re.match(r'^\s*(CALL|CALLP|CALLSUBR|CALLBO|CALLBOUND)\s+(\S+)', line, re.IGNORECASE)
        if m:
            program = m.group(2).strip('"').strip("'").rstrip(';').upper()
            result.program_calls.append(ProgramCall(
                program=program, call_type=m.group(1).upper(),
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


# ============================================================
# COBOL Parser
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
            m = re.match(r'^\s+COPY\s+(\S+)', stripped, re.IGNORECASE)
            if m:
                path_part = m.group(1).rstrip('.')
                library, file_name = "", path_part
                if '.' in path_part:
                    parts = path_part.split('.', 1)
                    library, file_name = parts[0], parts[1]
                result.copy_includes.append(CopyInclude(
                    directive="COPY", library=library, file=file_name,
                    line=i, raw=stripped.strip()
                ))
                continue
            m = re.match(r'^\s+CALL\s+[\'"]?(\S+)[\'"]?', stripped, re.IGNORECASE)
            if m:
                program = m.group(1).strip('"').strip("'").upper()
                result.program_calls.append(ProgramCall(
                    program=program, call_type="CALL",
                    line=i, raw=stripped.strip()
                ))
                continue
            m = re.match(r'^\s+(?:FD|SD)\s+(\S+)', stripped, re.IGNORECASE)
            if m:
                result.file_refs.append(FileRef(
                    name=m.group(1).upper(), usage="FILE", file_type="COBOL_FD",
                    line=i, raw=stripped.strip()
                ))
        return result


# ============================================================
# Report Generator (JSON)
# ============================================================

class ReportGenerator:

    def generate(self, analysis: ProgramAnalysis) -> str:
        """Generate JSON format report"""
        import json

        report = {
            "meta": {
                "program_name": analysis.program_name,
                "file_path": analysis.file_path,
                "program_type": analysis.program_type,
                "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            "entry_points": self._build_entry_points(analysis),
            "file_refs": self._build_file_refs(analysis),
            "field_chains": self._build_field_chains(analysis),
            "table_fields": self._build_table_fields(analysis),
            "field_operations": self._build_field_operations(analysis),
            "data_areas": self._build_data_areas(analysis),
            "copy_includes": self._build_copy_includes(analysis),
            "program_calls": self._build_program_calls(analysis),
            "summary": self._build_summary(analysis)
        }

        return json.dumps(report, ensure_ascii=False, indent=2)

    def _build_entry_points(self, analysis):
        return [
            {
                "name": ep.name,
                "type": ep.type,
                "line": ep.line,
                "parameters": ep.parameters if ep.parameters else [],
                "description": ep.description
            }
            for ep in analysis.entry_points
        ]

    def _build_file_refs(self, analysis):
        return [
            {
                "name": fr.name,
                "usage": fr.usage,
                "file_type": fr.file_type,
                "line": fr.line
            }
            for fr in analysis.file_refs
        ]

    def _build_field_chains(self, analysis):
        chains = []
        for chain in analysis.field_chains:
            # Build path
            path = []
            for field, expr, line, conds in chain.chain:
                node = {"field": field}
                if expr != "DB-READ":
                    node["expr"] = expr
                if conds:
                    node["conditions"] = self._format_conditions_list(conds)
                if line > 0:
                    node["line"] = line
                path.append(node)

            chains.append({
                "source": chain.start_field,
                "target": chain.end_field,
                "target_type": chain.end_type,
                "target_table": chain.end_table or None,
                "path": path,
                "line": chain.line
            })
        return chains

    def _build_table_fields(self, analysis):
        result = {}
        for table_name, tfi in sorted(analysis.table_fields.items()):
            actionable = self._get_actionable_fields(tfi)
            if actionable:
                result[table_name] = {
                    "is_output": tfi.is_output_table,
                    "fields": sorted(actionable.keys())
                }
        return result

    def _build_field_operations(self, analysis):
        result = {}
        for table_name, tfi in sorted(analysis.table_fields.items()):
            actionable = self._get_actionable_fields(tfi)
            if actionable:
                table_ops = {}
                for field_name in sorted(actionable.keys()):
                    usages = actionable[field_name]
                    table_ops[field_name] = [
                        {
                            "operation": u.operation,
                            "target": u.target,
                            "conditions": self._format_conditions_list(u.conditions),
                            "is_written": u.is_written,
                            "line": u.line
                        }
                        for u in usages
                    ]
                result[table_name] = table_ops
        return result

    def _build_data_areas(self, analysis):
        # Merge references for same Data Area
        dtaara_map = {}
        for ref in analysis.data_area_refs:
            if ref.name not in dtaara_map:
                dtaara_map[ref.name] = {"refs": [], "ds_fields": []}
            dtaara_map[ref.name]["refs"].append({
                "operation": ref.operation,
                "data_type": ref.data_type or None,
                "length": ref.length or None,
                "line": ref.line,
                "raw": ref.raw
            })

        # DS decomposition
        ds_map = {}
        for ds in analysis.data_area_ds_list:
            key = (ds.ds_name, ds.dtaara_name)
            if key not in ds_map:
                ds_map[key] = {}
            ds_map[key].update(ds.fields)

        for (ds_name, dtaara_name), fields in ds_map.items():
            if dtaara_name in dtaara_map:
                dtaara_map[dtaara_name]["ds_fields"].append({
                    "ds_name": ds_name,
                    "fields": {k: v for k, v in sorted(fields.items())},
                    "line": next((ds.line for ds in analysis.data_area_ds_list
                                  if ds.ds_name == ds_name), 0)
                })

        return {
            name: {
                "refs": info["refs"],
                "ds_fields": info["ds_fields"]
            }
            for name, info in sorted(dtaara_map.items())
        }

    def _build_copy_includes(self, analysis):
        return [
            {
                "directive": ci.directive,
                "library": ci.library,
                "file": ci.file,
                "member": ci.member,
                "line": ci.line
            }
            for ci in analysis.copy_includes
        ]

    def _build_program_calls(self, analysis):
        return [
            {
                "program": pc.program,
                "call_type": pc.call_type,
                "line": pc.line
            }
            for pc in analysis.program_calls
        ]

    def _build_summary(self, analysis):
        actionable_total = 0
        for tfi in analysis.table_fields.values():
            actionable = self._get_actionable_fields(tfi)
            actionable_total += len(actionable)

        return {
            "file_refs_count": len(analysis.file_refs),
            "tables_count": len(analysis.table_fields),
            "actionable_fields_count": actionable_total,
            "field_chains_count": len(analysis.field_chains),
            "data_areas_count": len(set(r.name for r in analysis.data_area_refs)),
            "data_area_ds_count": len(set((ds.ds_name, ds.dtaara_name) for ds in analysis.data_area_ds_list)),
            "copy_includes_count": len(analysis.copy_includes),
            "program_calls_count": len(analysis.program_calls)
        }

    def _get_actionable_fields(self, tfi: TableFieldInfo) -> Dict[str, List[FieldUsage]]:
        """Get fields with operations that are ultimately written to DB"""
        result = {}
        for fname, usages in tfi.fields.items():
            if fname == '*':
                continue
            has_assign = any(u.operation in ('ASSIGN',) for u in usages)
            is_written = any(u.is_written for u in usages) or tfi.is_output_table
            if has_assign and is_written:
                result[fname] = usages
        return result

    def _format_conditions_list(self, conditions):
        """Format conditions as list"""
        if not conditions:
            return []
        result = []
        for c in conditions:
            if c.type == 'ELSE':
                result.append(c.expression)
            elif c.type in ('IF', 'WHEN'):
                result.append(f"{c.type} {c.expression}")
            elif c.type in ('DOW', 'DOU'):
                result.append(f"{c.type} {c.expression} [loop]")
            else:
                result.append(f"{c.type} {c.expression}")
        return result

    def _format_conditions(self, conditions: List[Condition]) -> str:
        """Format conditions list (legacy interface)"""
        parts = self._format_conditions_list(conditions)
        return " → ".join(parts) if parts else "-"


# ============================================================
# Main Program
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
            return f"Cannot read file (encoding not supported): {filepath}"
        lines = content.splitlines()
        analysis = parser.parse(filepath, lines)
        report = ReportGenerator().generate(analysis)
        rel_path = os.path.relpath(filepath, source_base)
        rel_dir = os.path.dirname(rel_path)
        filename = Path(filepath).stem + ".json"
        output_dir = os.path.join(output_base, rel_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        return None
    except Exception as e:
        return f"Error analyzing file: {filepath} - {str(e)}"

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
        description='IBM i Program Source Code Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', help='File or directory path to analyze')
    parser.add_argument('--output', '-o', default='analyze', help='Output directory (default: analyze)')
    args = parser.parse_args()
    source_path = os.path.abspath(args.path)
    output_path = os.path.abspath(args.output)
    if not os.path.exists(source_path):
        print(f"Error: Path does not exist: {source_path}")
        sys.exit(1)
    print(f"IBM i Program Analyzer")
    print(f"=" * 50)
    print(f"Source path: {source_path}")
    print(f"Output directory: {output_path}")
    print()
    files = collect_program_files(source_path)
    if not files:
        print("No analyzable program files found")
        sys.exit(1)
    print(f"Found {len(files)} program file(s)")
    print()
    errors, analyzed = [], 0
    for filepath in files:
        rel = os.path.relpath(filepath, source_path)
        print(f"Analyzing: {rel} ... ", end="", flush=True)
        error = analyze_file(filepath, output_path, source_path)
        if error:
            print(f"⚠ {error}")
            errors.append(error)
        else:
            print("✓")
            analyzed += 1
    print()
    print(f"=" * 50)
    print(f"Analysis complete: {analyzed} file(s) succeeded, {len(errors)} error(s)")
    print(f"Results output to: {output_path}")

if __name__ == '__main__':
    main()

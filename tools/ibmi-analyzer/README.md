# IBM i Program Source Code Analyzer

Analyze RPG/RPGLE, CL/CLP, COBOL program source code, extracting:
1. **Table/File declarations and field usage** - Only analyze fields with operations that are ultimately written to DB
2. **Data Area** - Declarations, read/write operations, DS decomposition
3. **`/COPY`, `/INCLUDE` references**
4. **Program calls** (CALL, CALLP, CALLB, CALLPRC, EXTPGM, SQL CALL, etc.)
5. **Field propagation chains** (end-to-end from source to target)
6. **Conditions** for each operation
7. **Entry points** (MAIN, ENTRY, *INZSR)

## Usage

```bash
python analyze_ibmi.py /path/to/source --output /path/to/analyze
```

## Output Structure

```
analyze/
├── PROGRAM1.json
├── PROGRAM2.json
└── subdir/
    └── PROGRAM3.json
```

## Skills

The `skills/` directory contains prompt templates for generating human-readable analysis reports:

| File | Description |
|------|-------------|
| `program-analysis.md` | Skill definition for report generation |
| `report-prompt-template.md` | Prompt template for AI |
| `USAGE.md` | Usage guide |

### Generating Analysis Report

1. Run analyzer to get JSON:
```bash
python analyze_ibmi.py source/ --output analyze/
```

2. Use the skill with JSON + source code to generate report

3. Report includes:
- Program flow diagrams (Mermaid)
- Data flow diagrams
- Business logic documentation
- Data dictionary
- Migration guide

## JSON Report Structure

| Section | Content |
|---------|---------|
| `meta` | Program name, file path, type, analysis time |
| `file_refs` | All F-spec / DCL-F declarations |
| `field_chains` | End-to-end field propagation chains with conditions |
| `table_fields` | Tables with actionable fields |
| `field_operations` | Field assignments with conditions per table |
| `data_areas` | Data Area declarations, operations, DS decomposition |
| `copy_includes` | /COPY, /INCLUDE references |
| `program_calls` | CALL/CALLP/CALLB/EXTPGM etc. |
| `summary` | Statistics |

## Parsing Capabilities

### RPG/RPGLE

- F-spec / DCL-F file declarations
- CHAIN, READ, READE, SETLL, SETGT, UPDATE, WRITE, DELETE, EXFMT
- EVAL, IF, WHEN, DOW/DOU conditions
- MOVEL, MOVE, Z-ADD, MULT data movement
- EXEC SQL blocks (FROM, JOIN, INTO, UPDATE, DELETE)
- DCL-DTAARA / DCL-DS declarations
- INDTAARA, OUTDTAARA, CHAINDTAARA operations
- DS.field assignments (Data Area decomposition)

### Program Call Types

| Type | Description |
|------|-------------|
| CALL | Standard call |
| CALLP | Procedure call |
| CALLB | Bound module call |
| CALLPRC | Call procedure |
| EXTPGM | External program reference |
| CALL (SQL) | SQL embedded call |
| CALLSUBR | CL subroutine call |
| CALLBO | CL bound object call |
| CALLBOUND | CL bound call |

### CL/CLP

- DCL FILE/PROG / DCL-DTAARA declarations
- CALL / CALLP / CALLSUBR / CALLBO / CALLBOUND
- CHGVAR variable assignment
- CHGDTAARA, RTVDTAARA, OVRDBF

### COBOL

- COPY references
- CALL program calls
- FD/SD file declarations
- MOVE, COMPUTE, READ, WRITE, REWRITE, DELETE

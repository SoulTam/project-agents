# Skill: IBM i Program Analysis Report Generator

## Description
Generate comprehensive human-readable analysis reports from IBM i (RPG/CL/COBOL) programs. Automatically runs structural analysis, then combines results with source code review to produce detailed documentation.

## Trigger
When user mentions any of:
- "分析报告" / "analysis report"
- "程序分析" / "program analysis"
- "生成报告" / "generate report"
- "帮我分析这个程序"
- "分析这个目录"

## Workflow

### Step 1: Get Input Path
Ask user for:
```
请提供要分析的程序路径（文件或目录）：
```

Accept:
- Single file: `tools/ibmi-analyzer/test_samples/FIELDCHAIN.rpgle`
- Directory: `tools/ibmi-analyzer/test_samples/`

### Step 2: Run Analyzer
Execute `analyze_ibmi.py` to generate JSON:
```bash
python tools/ibmi-analyzer/analyze_ibmi.py {input_path} --output tools/ibmi-analyzer/analyze
```

This generates JSON files in `tools/ibmi-analyzer/analyze/`

### Step 3: Process Each Program
For each program found:

1. **Read source code** — Original `.rpgle`/`.clp`/`.cbl` file
2. **Read JSON analysis** — Generated `.json` file
3. **Generate report** — Using prompt template
4. **Save report** — To `tools/ibmi-analyzer/reports/{PROGRAM_NAME}-analysis.md`

### Step 4: Report Generation
Use the prompt template from `skills/report-prompt-template.md`:
- Replace `{json_content}` with JSON file content
- Replace `{source_code}` with source code content
- Replace `{PROGRAM_NAME}` with program name

### Step 5: Summary
Output summary:
```
分析完成：
- 分析程序数: X
- 报告输出目录: tools/ibmi-analyzer/reports/
  - PROGRAM1-analysis.md
  - PROGRAM2-analysis.md
  - ...
```

## Input Format

User provides one of:
- Single program file path
- Directory containing programs

Examples:
```
tools/ibmi-analyzer/test_samples/FIELDCHAIN.rpgle
tools/ibmi-analyzer/test_samples/
```

## Output Format

Reports saved to:
```
tools/ibmi-analyzer/reports/{PROGRAM_NAME}-analysis.md
```

## Prompt Template

See `skills/report-prompt-template.md`

## Quality Checklist

- [ ] Analyzer executed successfully
- [ ] JSON files generated
- [ ] Source code read
- [ ] Report generated with all sections
- [ ] Mermaid diagrams included
- [ ] Business rules documented
- [ ] Report saved to correct location

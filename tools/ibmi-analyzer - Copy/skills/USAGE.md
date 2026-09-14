# Usage Guide

## How to Generate Analysis Report

### Trigger Words

Say any of these to trigger the skill:
- "分析报告" / "analysis report"
- "程序分析" / "program analysis"
- "生成报告" / "generate report"
- "帮我分析这个程序"
- "分析这个目录"

### Workflow

**Step 1: User Provides Path**

```
User: 帮我分析这个程序
AI: 请提供要分析的程序路径（文件或目录）：

User: tools/ibmi-analyzer/test_samples/FIELDCHAIN.rpgle
```

**Step 2: AI Runs Analyzer**

AI executes:
```bash
python tools/ibmi-analyzer/analyze_ibmi.py {path} --output tools/ibmi-analyzer/analyze
```

**Step 3: AI Reads Files**

For each program:
1. Read source code file
2. Read generated JSON file

**Step 4: AI Generates Report**

Using the prompt template, AI generates the report.

**Step 5: AI Saves Report**

Report saved to:
```
tools/ibmi-analyzer/reports/{PROGRAM_NAME}-analysis.md
```

### Example Interaction

```
User: 帮我分析这个程序
AI: 请提供要分析的程序路径（文件或目录）：

User: tools/ibmi-analyzer/test_samples/

AI: [Runs analyzer]
    分析完成，找到 2 个程序：
    - FIELDCHAIN.rpgle
    - ORDPROC.rpgle

    [Generates report for FIELDCHAIN]
    [Saves to reports/FIELDCHAIN-analysis.md]

    [Generates report for ORDPROC]
    [Saves to reports/ORDPROC-analysis.md]

    分析完成：
    - 分析程序数: 2
    - 报告输出目录: tools/ibmi-analyzer/reports/
      - FIELDCHAIN-analysis.md
      - ORDPROC-analysis.md
```

## Input Formats

### Single File
```
tools/ibmi-analyzer/test_samples/FIELDCHAIN.rpgle
```

### Directory
```
tools/ibmi-analyzer/test_samples/
```

## Output Location

Reports are saved to:
```
tools/ibmi-analyzer/reports/{PROGRAM_NAME}-analysis.md
```

## Complete Directory Structure

```
tools/ibmi-analyzer/
├── analyze_ibmi.py           # Structural analyzer
├── analyze/                  # JSON output (generated)
│   ├── FIELDCHAIN.json
│   └── ORDPROC.json
├── reports/                  # Analysis reports (generated)
│   ├── FIELDCHAIN-analysis.md
│   └── ORDPROC-analysis.md
├── skills/                   # Skill definitions
│   ├── program-analysis.md
│   ├── report-prompt-template.md
│   └── USAGE.md
├── test_samples/             # Test source code
│   ├── FIELDCHAIN.rpgle
│   └── ORDPROC.rpgle
└── README.md
```

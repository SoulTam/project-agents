"""tools/scripts 公共模块：路径、JSON 输出、BLK 解析、文档扫描。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLK_RE = re.compile(r"<!--\s*BLK:([A-Z]{2,3})-([A-Z0-9]+)\s*-->")
BLK_REF_RE = re.compile(r"BLK:([A-Z]{2,3})-([A-Z0-9]+)")
TS_RE = re.compile(r"^<!--\s*(创建时间|最后修改):\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*-->$")
SKIP_PARTS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}


def emit(payload):
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def finish(payload, code):
    payload["ok"] = code == 0
    payload["exit"] = code
    emit(payload)
    raise SystemExit(code)


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else (ROOT / p)


def read_text(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def iter_md(base=ROOT):
    base = Path(base)
    for p in base.rglob("*.md"):
        if any(part in SKIP_PARTS or part.endswith("- Copy") for part in p.parts):
            continue
        yield p


def without_fences(text):
    """去掉 ``` 围栏内容，保留行结构，避免代码块内标记误报。"""
    out, inside = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return out


def blk_blocks(text):
    """解析 <!-- BLK:NS-SEQ --> 块，返回 (id->content, duplicates)。

    结束边界：下一个 BLK 标记，或同级/更高级 Markdown 标题。
    """
    lines = text.splitlines(keepends=True)
    marks = []
    for i, line in enumerate(lines):
        m = BLK_RE.search(line)
        if m:
            marks.append((i, f"{m.group(1)}-{m.group(2)}"))
    ids = [key for _, key in marks]
    dups = sorted({k for k in ids if ids.count(k) > 1})
    blocks = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        for j in range(start + 1, end):
            stripped = lines[j].lstrip()
            if stripped.startswith("## ") or stripped.startswith("### "):
                end = j
                break
        blocks.setdefault(key, "".join(lines[start + 1:end]).strip("\n"))
    return blocks, dups


def blk_refs(text):
    return {f"{m.group(1)}-{m.group(2)}" for m in BLK_REF_RE.finditer(text)}

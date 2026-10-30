"""T2 子计划"最终结果"生成：按 BLK 从蓝图逐字抽取，禁止人工复制。

退出码：0 成功 / 1 BLK 缺失或重复。
"""
import argparse
import re
from pathlib import Path

from common import blk_blocks, finish, read_text, resolve

SECTION_TITLE = "## 最终结果"
TARGET_HEADING = re.compile(r"^## .*最终结果.*$")


def parse_map(raw):
    """解析 'SP-01:FR-001,AR-M1;SP-02:API-012' → {SP: [ids]}。"""
    mapping = {}
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        key, _, ids = part.partition(":")
        if not ids:
            raise ValueError(f"bad mapping segment: {part}")
        mapping[key.strip()] = [i.strip() for i in ids.split(",") if i.strip()]
    return mapping


def split(blueprint_text, mapping):
    blocks, dups = blk_blocks(blueprint_text)
    if dups:
        return None, [f"duplicate BLK: {','.join(dups)}"]
    result, missing = {}, []
    for sp, ids in mapping.items():
        parts = []
        for blk in ids:
            if blk not in blocks:
                missing.append(f"{sp}:{blk}")
                continue
            parts.append(f"### BLK:{blk}\n\n{blocks[blk]}")
        result[sp] = "\n\n".join(parts)
    if missing:
        return None, [f"missing BLK: {','.join(missing)}"]
    return result, []


def replace_section(document, body):
    """替换文档内 '## 最终结果' 段，保留其后同级标题。"""
    lines = document.splitlines()
    start = next((i for i, l in enumerate(lines) if TARGET_HEADING.match(l)), None)
    section = [SECTION_TITLE, "", "> 本段由 blueprint_split.py 生成，禁止手工修改。", "", body]
    if start is None:
        return "\n".join(lines + ["", *section, ""])
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[:start] + section + [""] + lines[end:])


def main():
    ap = argparse.ArgumentParser(description="blueprint_split: 按 BLK 生成子计划最终结果")
    ap.add_argument("--blueprint", required=True)
    ap.add_argument("--map", required=True, help="SP-01:FR-001,AR-M1;SP-02:API-012")
    ap.add_argument("--out", help="目标 SP 文件（单 SP）")
    ap.add_argument("--out-dir", help="目标目录（多 SP，写 SP-ID.md）")
    args = ap.parse_args()

    try:
        mapping = parse_map(args.map)
    except ValueError as exc:
        finish({"reason": str(exc)}, 1)

    result, errors = split(read_text(resolve(args.blueprint)), mapping)
    if errors:
        finish({"reasons": errors, "blocks": list(mapping)}, 1)
    if not args.out and not args.out_dir:
        finish({"reasons": ["--out or --out-dir required"], "blocks": sorted(result)}, 1)

    written = []
    for sp, body in result.items():
        if args.out and len(result) == 1:
            target = resolve(args.out)
        else:
            target = resolve(args.out_dir) / f"{sp}.md"
        doc = read_text(target) if target.exists() else f"# {sp}\n"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(replace_section(doc, body), encoding="utf-8", newline="\n")
        written.append(str(target))
    finish({"written": written, "blocks": {k: len(v) for k, v in mapping.items()}}, 0)


if __name__ == "__main__":
    main()

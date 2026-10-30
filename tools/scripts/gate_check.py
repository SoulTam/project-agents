"""T1 关卡机读判定：D5 schema、证据完整性、BLK 覆盖率、跳转词。

退出码：0 通过 / 1 不通过 / 2 证据不足。
"""
import argparse
import json
import re
from pathlib import Path

from common import ROOT, blk_blocks, blk_refs, finish, read_text, resolve, without_fences

D5_FIELDS = ["gate", "kind", "task_id", "round", "verdict",
             "checked", "failed", "evidence", "blocking", "ts"]
JUMP_WORDS = ["详见", "同上", "此处略", "（略）", "…", "..."]


def load_reports(task_dir, gate):
    reports = Path(task_dir) / "reports"
    if not reports.is_dir():
        return []
    return sorted(reports.glob(f"{gate}-*report.json"))


def check_coverage(blueprint, plan_dir):
    bp = read_text(blueprint)
    blocks, dups = blk_blocks(bp)
    refs = set()
    for p in sorted(Path(plan_dir).glob("SP-*.md")):
        refs |= blk_refs(read_text(p))
    if len(blocks) >= 5:
        return sorted(set(blocks) - refs), dups
    m = re.search(r"BLK\s*总数\s*(\d+)", bp)
    if not m:
        return [], dups
    declared = int(m.group(1))
    if declared != len(refs):
        return [f"declared={declared} referenced={len(refs)}"], dups
    return [], dups


def scan_jump(plan_dir):
    hits = []
    for p in sorted(Path(plan_dir).glob("SP-*.md")):
        for no, line in enumerate(without_fences(read_text(p)), 1):
            word = next((w for w in JUMP_WORDS if w in line), None)
            if word:
                hits.append(f"{p.name}:{no} `{word}`")
    return hits


def main():
    ap = argparse.ArgumentParser(description="gate_check: 关卡机读判定")
    ap.add_argument("--task", required=True, help="任务 ID 或任务目录")
    ap.add_argument("--gate", required=True, choices=["G1", "G2", "G3", "G4", "G5"])
    ap.add_argument("--report", help="显式指定单个报告文件")
    ap.add_argument("--blueprint", help="蓝图路径（G3/G5 覆盖率校验）")
    ap.add_argument("--plan-dir", help="子计划目录（G3/G5 覆盖率与跳转词校验）")
    args = ap.parse_args()

    task_dir = Path(args.task)
    if not task_dir.is_absolute() and not task_dir.is_dir():
        task_dir = ROOT / "agent-doc" / "tasks" / args.task

    reasons, blocking = [], []
    evidence_missing = False
    checked = failed = 0

    paths = [resolve(args.report)] if args.report else load_reports(task_dir, args.gate)
    paths = [p for p in paths if Path(p).is_file()]
    if not paths:
        finish({"gate": args.gate, "task_id": args.task, "checked": 0, "failed": 0,
                "reasons": ["no report found"], "blocking": []}, 2)

    for path in paths:
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            reasons.append(f"{path.name}: invalid json ({exc})")
            failed += 1
            continue
        checked += 1
        missing = [f for f in D5_FIELDS if f not in data]
        if missing:
            reasons.append(f"{path.name}: missing fields {','.join(missing)}")
            failed += 1
        count, bad = int(data.get("checked") or 0), int(data.get("failed") or 0)
        if bad > count:
            reasons.append(f"{path.name}: failed({bad}) > checked({count})")
            failed += 1
        if bad > 0:
            failed += bad
            blocking.extend(data.get("blocking") or [])
        if data.get("verdict") == "pass" and not data.get("evidence"):
            evidence_missing = True
            reasons.append(f"{path.name}: verdict=pass but evidence empty")

    blue, plan = args.blueprint, args.plan_dir
    if args.gate in ("G3", "G5") and blue and plan:
        missing, dups = check_coverage(resolve(blue), resolve(plan))
        checked += 1
        if dups:
            reasons.append(f"duplicate BLK: {','.join(dups)}")
            failed += 1
        if missing:
            reasons.append(f"uncovered BLK: {','.join(missing)}")
            blocking.extend(f"BLK:{m}" for m in missing)
            failed += 1
        jumps = scan_jump(resolve(plan))
        checked += 1
        if jumps:
            reasons.append(f"jump words: {'; '.join(jumps)}")
            failed += 1

    code = 2 if evidence_missing else (1 if failed else 0)
    finish({"gate": args.gate, "task_id": args.task, "checked": checked,
            "failed": failed, "reasons": reasons,
            "blocking": sorted(set(blocking))}, code)


if __name__ == "__main__":
    main()

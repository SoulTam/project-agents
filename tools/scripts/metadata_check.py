"""T3 文档元数据校验：首两行为创建/最后修改时间，第 3 行为空。

退出码：0 合规 / 1 缺失或不合规。
"""
import argparse
import sys

from common import TS_RE, finish, resolve


def check_lines(lines):
    problems = []
    if len(lines) < 3:
        return ["file too short (<3 lines)"]
    first = TS_RE.match(lines[0].strip())
    second = TS_RE.match(lines[1].strip())
    if not first or first.group(1) != "创建时间":
        problems.append("line1: missing 创建时间")
    if not second or second.group(1) != "最后修改":
        problems.append("line2: missing 最后修改")
    if lines[2].strip():
        problems.append("line3: not blank")
    return problems


def check_path(path):
    try:
        lines = resolve(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"cannot read: {exc}"]
    return check_lines(lines)


def main():
    ap = argparse.ArgumentParser(description="metadata_check: 文档时间戳校验")
    ap.add_argument("paths", nargs="+", help="待校验文档路径")
    args = ap.parse_args()

    violations = {}
    for path in args.paths:
        problems = check_path(path)
        if problems:
            violations[str(path)] = problems
    if violations:
        finish({"violations": violations, "count": len(violations)}, 1)
    finish({"violations": {}, "count": 0}, 0)


if __name__ == "__main__":
    sys.exit(main())

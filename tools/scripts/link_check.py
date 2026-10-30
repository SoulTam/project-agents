"""T5 断链校验：扫描 Markdown 中的反引号路径与链接目标，检查文件真实存在。

退出码：0 通过 / 1 死链。排除 URL、通配符、占位符。
"""
import argparse
import re
from pathlib import Path

from common import ROOT, finish, iter_md, read_text, without_fences

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BACKTICK = re.compile(r"`([^`\n]+)`")
EXT = (".md", ".json", ".py", ".txt", ".yaml", ".yml", ".zip", ".ps1", ".sh", ".jsonl")
BAD_CHARS = set("*?{}<>|$[]")


def is_candidate(token):
    token = token.strip()
    if not token or token.startswith(("#", "http://", "https://", "mailto:", "www.")):
        return False
    if token.endswith("/") or token.endswith("\\"):
        return False
    if any(ch in BAD_CHARS for ch in token):
        return False
    if token.startswith("."):
        return True
    if ("/" in token or "\\" in token) and token.endswith(EXT):
        return True
    return False


def targets(text):
    lines = without_fences(text)
    found = []
    for no, line in enumerate(lines, 1):
        for regex in (MD_LINK, BACKTICK):
            for m in regex.finditer(line):
                token = re.sub(r":\d+(-\d+)?$", "", m.group(1).split("#")[0].strip())
                if is_candidate(token):
                    found.append((no, token))
    return found


def check(root=ROOT, include=(ROOT / "AGENTS.md",), extra_dirs=(".ai-team", "agent-doc")):
    root = Path(root)
    files = [p for p in include if Path(p).is_file()]
    for name in extra_dirs:
        base = root / name
        if base.is_dir():
            files.extend(iter_md(base))
    dead = []
    for path in files:
        rel_dir = path.parent
        for no, token in targets(read_text(path)):
            candidates = [rel_dir / token, root / token]
            if not any(c.exists() for c in candidates):
                dead.append({"file": str(path.relative_to(root)).replace("\\", "/"),
                             "line": no, "target": token})
    return dead


def main():
    ap = argparse.ArgumentParser(description="link_check: 文档断链校验")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    root = Path(args.root)
    try:
        dead = check(root)
    except OSError as exc:
        finish({"dead_links": [], "error": str(exc)}, 1)
    finish({"dead_links": dead, "count": len(dead)}, 1 if dead else 0)


if __name__ == "__main__":
    main()

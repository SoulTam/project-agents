"""T5 断链校验：扫描 Markdown 中的反引号路径与链接目标，检查文件真实存在。

退出码：0 通过 / 1 死链。排除 URL、通配符、占位符。
"""
import argparse
import fnmatch
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
    if any(ch.isspace() for ch in token):
        return False
    if "/" not in token and len(token) <= 4:
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


def load_ignore(ignore_file=None):
    """忽略清单：@前缀=按文件路径前缀忽略；其余=目标 token（支持 * 通配）。"""
    path = Path(ignore_file) if ignore_file else (ROOT / ".linkignore")
    if not path.is_file():
        return [], []
    prefixes, tokens = [], []
    for raw in read_text(path).splitlines():
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        (prefixes if entry.startswith("@") else tokens).append(entry.lstrip("@"))
    return prefixes, tokens


def check(root=ROOT, include=(ROOT / "AGENTS.md",), extra_dirs=(".ai-team", "agent-doc"),
          ignore_file=None):
    root = Path(root)
    prefixes, tokens = load_ignore(ignore_file)
    files = [p for p in include if Path(p).is_file()]
    for name in extra_dirs:
        base = root / name
        if base.is_dir():
            files.extend(iter_md(base))
    dead = []
    for path in files:
        rel = str(path.relative_to(root)).replace("\\", "/")
        if any(rel.startswith(prefix) for prefix in prefixes):
            continue
        rel_dir = path.parent
        for no, token in targets(read_text(path)):
            if any(fnmatch.fnmatch(token, pattern) for pattern in tokens):
                continue
            candidates = [rel_dir / token, root / token]
            if not any(c.exists() for c in candidates):
                dead.append({"file": rel, "line": no, "target": token})
    return dead


def main():
    ap = argparse.ArgumentParser(description="link_check: 文档断链校验")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--ignore", help="忽略清单路径，默认 <root>/.linkignore")
    args = ap.parse_args()
    root = Path(args.root)
    try:
        dead = check(root, ignore_file=args.ignore or (root / ".linkignore"))
    except OSError as exc:
        finish({"dead_links": [], "error": str(exc)}, 1)
    finish({"dead_links": dead, "count": len(dead)}, 1 if dead else 0)


if __name__ == "__main__":
    main()

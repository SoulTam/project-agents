"""T6 自有资产迁移：旧格式 Skill 结构适配（正文与脚本零改写）。

默认 dry-run，仅输出目标路径与注册表条目；加 --apply 才落盘。
"""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from common import ROOT, TS_RE, finish, read_text, resolve

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DOMAIN_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FENCE = "---"


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def find_source(src):
    if src.is_file():
        return src
    for cand in ("skill.md", "SKILL.md", "index.md"):
        p = src / cand
        if p.is_file():
            return p
    mds = [p for p in sorted(src.rglob("*.md")) if p.is_file()]
    return mds[0] if len(mds) == 1 else None


def split_doc(text):
    """拆出 (创建时间, 正文)；已有 frontmatter 与时间戳行都会被剥离后重建。"""
    lines = text.splitlines()
    created = None
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines):
        m = TS_RE.match(lines[i].strip())
        if not m:
            break
        if m.group(1) == "创建时间":
            created = m.group(2)
        i += 1
    if i < len(lines) and lines[i].strip() == FENCE:
        j = i + 1
        while j < len(lines) and lines[j].strip() != FENCE:
            j += 1
        if j >= len(lines):
            return created, lines[i:], "frontmatter 未闭合"
        i = j + 1
    body = lines[i:]
    while body and not body[0].strip():
        body.pop(0)
    return created, body, None


def render(name, version, keywords, agents, created, body, ts):
    head = [
        f"<!-- 创建时间: {created} -->",
        f"<!-- 最后修改: {ts} -->",
        "",
        FENCE,
        f"name: {name}",
        f"version: {version}",
        f"trigger_keywords: {', '.join(keywords)}",
        f"agents: {', '.join(agents)}",
        FENCE,
        "",
    ]
    return "\n".join(head + body) + "\n"


def known_agents(root):
    base = Path(root) / ".ai-team" / "agents"
    if not base.is_dir():
        return set()
    return {p.parent.name for p in base.rglob("agent.md")}


def registry_entry(name, version, domain, keywords, agents, owner):
    return {
        "name": name,
        "version": version,
        "path": f".ai-team/skills/{domain}/{name}/skill.md",
        "trigger": {"keywords": keywords, "agents": agents},
        "inputs": ["能力描述"],
        "outputs": ["agent-doc/**"],
        "verify": "python tools/scripts/metadata_check.py",
        "source": "migrated:internal",
        "owner": owner or agents[0],
    }


def adopt(src, name, domain, keywords, agents, version="1.0.0", owner=None,
          root=ROOT, apply=False, force=False):
    root = Path(root)
    src = resolve(src)
    reasons = []
    if not src.exists():
        return {"code": 2, "reasons": [f"源不存在: {src}"]}
    if not NAME_RE.match(name or ""):
        return {"code": 2, "reasons": [f"name 不合法: {name}"]}
    if not DOMAIN_RE.match(domain or ""):
        return {"code": 2, "reasons": [f"domain 不合法: {domain}"]}
    if not keywords:
        return {"code": 2, "reasons": ["keywords 不能为空"]}
    if not agents:
        return {"code": 2, "reasons": ["agents 不能为空"]}
    source_md = find_source(src)
    if source_md is None:
        return {"code": 2, "reasons": [f"未找到唯一 Markdown 源文件: {src}"]}

    valid = known_agents(root)
    if valid:
        bad = [a for a in agents if a not in valid]
        if bad:
            return {"code": 2, "reasons": [f"未知 agent: {', '.join(bad)}"]}

    reg_path = root / ".ai-team" / "skills" / "registry.json"
    reg = json.loads(read_text(reg_path)) if reg_path.is_file() else {"skills": []}
    if any(s.get("name") == name for s in reg.get("skills", [])):
        if not force:
            return {"code": 1, "reasons": [f"注册表已存在同名 skill: {name}"]}
    taken = {}
    for s in reg.get("skills", []):
        if s.get("name") == name:
            continue
        for kw in (s.get("trigger") or {}).get("keywords") or []:
            taken[kw] = s.get("name")
    clash = [k for k in keywords if k in taken]
    if clash:
        return {"code": 1,
                "reasons": [f"关键词已被占用: {k}({taken[k]})" for k in clash]}

    created, body, err = split_doc(read_text(source_md))
    if err:
        return {"code": 2, "reasons": [f"{source_md.name}: {err}"]}
    ts = now_ts()
    text = render(name, version, keywords, agents, created or ts, body, ts)

    target_dir = root / ".ai-team" / "skills" / domain / name
    target = target_dir / "skill.md"
    extras = []
    if src.is_dir():
        extras = [p for p in sorted(src.rglob("*"))
                  if p.is_file() and p != source_md]

    entry = registry_entry(name, version, domain, keywords, agents, owner)
    result = {
        "code": 0,
        "source": str(source_md),
        "target": str(target),
        "assets": [str(p.relative_to(src)) for p in extras],
        "registry_entry": entry,
        "applied": bool(apply),
        "reasons": reasons,
    }
    if not apply:
        return result
    if target.exists() and not force:
        return {"code": 1, "reasons": [f"目标已存在（--force 可覆盖）: {target}"]}

    target_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    for p in extras:
        dest = target_dir / p.relative_to(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)

    lines = read_text(reg_path).splitlines()
    close = max(i for i, ln in enumerate(lines) if ln.strip().startswith("]"))
    prev = close - 1
    while prev > 0 and not lines[prev].strip():
        prev -= 1
    if not lines[prev].rstrip().endswith(","):
        lines[prev] = lines[prev].rstrip() + ","
    lines.insert(close, "    " + json.dumps(entry, ensure_ascii=False,
                                            separators=(",", ":")))
    for i, ln in enumerate(lines):
        if ln.strip().startswith('"updated"'):
            lines[i] = f'  "updated": "{ts}",'
            break
    reg_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return result


def main():
    ap = argparse.ArgumentParser(
        description="skill_adopt: 自有旧格式 Skill 结构适配（正文零改写）")
    ap.add_argument("--src", required=True, help="旧 Skill 文件或目录")
    ap.add_argument("--name", required=True, help="新 skill 名（小写连字符）")
    ap.add_argument("--domain", required=True, help="归属域，如 pm / code-dev")
    ap.add_argument("--keywords", required=True, help="触发关键词，逗号分隔")
    ap.add_argument("--agents", required=True, help="归属 Agent，逗号分隔")
    ap.add_argument("--version", default="1.0.0")
    ap.add_argument("--owner", default=None)
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--apply", action="store_true", help="真正写入（默认 dry-run）")
    ap.add_argument("--force", action="store_true", help="覆盖同名目标")
    args = ap.parse_args()
    split = re.split(r"[,，]", args.keywords)
    payload = adopt(args.src, args.name, args.domain,
                    [k.strip() for k in split if k.strip()],
                    [a.strip() for a in re.split(r"[,，]", args.agents) if a.strip()],
                    version=args.version, owner=args.owner, root=args.root,
                    apply=args.apply, force=args.force)
    finish(payload, payload.pop("code", 0))


if __name__ == "__main__":
    main()

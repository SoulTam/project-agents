"""T4 注册表一致性校验：字段齐全、name 唯一、path 存在、keyword 不重复、agents 合法。

退出码：0 通过 / 1 不一致。只报告，不修改文件。
"""
import argparse
import json
import re
from pathlib import Path

from common import ROOT, finish, read_text, resolve

REQUIRED = ["name", "version", "path", "trigger", "inputs", "outputs", "verify", "source", "owner"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
AGENT_DIRS = ["architecture", "audit", "code-dev", "custom-agent-foundry", "dev-planning",
              "doc-output", "feature-design", "knowledge", "pm", "prompt-engineer",
              "requirements", "skill-creator", "task-assignment", "technical-design",
              "testing", "verification", "devops", "frontend", "ibmi", "java"]


def lint(registry_path, root=ROOT):
    data = json.loads(read_text(registry_path))
    violations, names, keywords = [], set(), {}
    for idx, skill in enumerate(data.get("skills", [])):
        tag = skill.get("name") or f"#{idx}"
        missing = [f for f in REQUIRED if f not in skill]
        if missing:
            violations.append(f"{tag}: missing fields {','.join(missing)}")
            continue
        name = skill["name"]
        if name in names:
            violations.append(f"{tag}: duplicate name")
        names.add(name)
        if not SEMVER.match(str(skill["version"])):
            violations.append(f"{tag}: bad version {skill['version']}")
        path = Path(root) / skill["path"]
        if not path.is_file():
            violations.append(f"{tag}: path missing {skill['path']}")
        elif path.parent.name != name:
            violations.append(f"{tag}: dir name mismatch {path.parent.name}")
        trigger = skill["trigger"] or {}
        kws = trigger.get("keywords") or []
        if not kws:
            violations.append(f"{tag}: empty keywords")
        for kw in kws:
            if kw in keywords:
                violations.append(f"{tag}: keyword `{kw}` duplicated with {keywords[kw]}")
            keywords.setdefault(kw, name)
        agents = trigger.get("agents") or []
        if not agents:
            violations.append(f"{tag}: empty agents")
        for agent in agents:
            if agent not in AGENT_DIRS:
                violations.append(f"{tag}: unknown agent {agent}")
        if not skill.get("inputs") or not skill.get("outputs"):
            violations.append(f"{tag}: empty inputs/outputs")
        if path.is_file():
            text = read_text(path)
            if not re.search(rf"^name:\s*{re.escape(name)}\s*$", text, re.M):
                violations.append(f"{tag}: frontmatter name mismatch")
            if not re.search(r"^trigger_keywords:", text, re.M):
                violations.append(f"{tag}: frontmatter missing trigger_keywords")
    return violations, len(data.get("skills", []))


def main():
    ap = argparse.ArgumentParser(description="registry_lint: 技能注册表一致性校验")
    ap.add_argument("--registry", default=str(ROOT / ".ai-team" / "skills" / "registry.json"))
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    try:
        violations, total = lint(resolve(args.registry), Path(args.root))
    except (OSError, json.JSONDecodeError) as exc:
        finish({"violations": [str(exc)], "total": 0}, 1)
    finish({"violations": violations, "total": total}, 1 if violations else 0)


if __name__ == "__main__":
    main()

"""5 个脚本的最小回归用例（每个脚本 3 例，共 15 例）。"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import blueprint_split
import gate_check
import link_check
import metadata_check
import registry_lint

TS = "<!-- 创建时间: 2026-10-30 21:00 -->\n<!-- 最后修改: 2026-10-30 21:00 -->\n\n"


def run_main(module, argv):
    old = sys.argv
    sys.argv = [module.__name__, *argv]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            module.main()
        return 0, json.loads(buf.getvalue() or "{}")
    except SystemExit as exc:
        return int(exc.code or 0), json.loads(buf.getvalue() or "{}")
    finally:
        sys.argv = old


class GateCheckTest(unittest.TestCase):
    def report(self, **overrides):
        data = {"gate": "G3", "kind": "coverage", "task_id": "T1", "round": 1,
                "verdict": "pass", "checked": 3, "failed": 0,
                "evidence": [{"type": "file", "ref": "a.md", "result": "ok"}],
                "blocking": [], "ts": "2026-10-30T21:00:00"}
        data.update(overrides)
        tmp = Path(tempfile.mkdtemp())
        (tmp / "reports").mkdir()
        (tmp / "reports" / "G3-coverage-report.json").write_text(
            json.dumps(data), encoding="utf-8")
        return tmp

    def test_pass_exit_0(self):
        code, payload = run_main(gate_check, ["--task", str(self.report()), "--gate", "G3"])
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])

    def test_failed_exit_1(self):
        code, _ = run_main(gate_check, ["--task", str(self.report(failed=1, verdict="fail")), "--gate", "G3"])
        self.assertEqual(code, 1)

    def test_evidence_empty_exit_2(self):
        code, payload = run_main(gate_check, ["--task", str(self.report(evidence=[])), "--gate", "G3"])
        self.assertEqual(code, 2)
        self.assertIn("evidence", " ".join(payload["reasons"]))


class BlueprintSplitTest(unittest.TestCase):
    BP = ("# BP\n\n<!-- BLK:FR-001 -->\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n"
          "<!-- BLK:API-012 -->\n\n接口说明\n")

    def test_extract_ok(self):
        result, errors = blueprint_split.split(self.BP, {"SP-01": ["FR-001", "API-012"]})
        self.assertEqual(errors, [])
        self.assertIn("| 1 | 2 |", result["SP-01"])
        self.assertIn("接口说明", result["SP-01"])

    def test_missing_blk(self):
        result, errors = blueprint_split.split(self.BP, {"SP-01": ["FR-999"]})
        self.assertIsNone(result)
        self.assertIn("missing BLK", errors[0])

    def test_duplicate_blk(self):
        result, errors = blueprint_split.split(self.BP + "\n<!-- BLK:FR-001 -->\n重复\n",
                                               {"SP-01": ["FR-001"]})
        self.assertIsNone(result)
        self.assertIn("duplicate BLK", errors[0])


class MetadataCheckTest(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(metadata_check.check_lines((TS + "# X\n").splitlines()), [])

    def test_missing_created(self):
        lines = ("<!-- 最后修改: 2026-10-30 21:00 -->\n\n# X\n").splitlines()
        self.assertIn("line1: missing 创建时间", metadata_check.check_lines(lines))

    def test_line3_not_blank(self):
        lines = TS.replace("\n\n", "\n") .splitlines() + ["# X"]
        self.assertIn("line3: not blank", metadata_check.check_lines(lines))


class RegistryLintTest(unittest.TestCase):
    def build(self, path_value, keywords):
        tmp = Path(tempfile.mkdtemp())
        skill_dir = tmp / "skills" / "demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "skill.md").write_text(
            TS + "---\nname: demo\nversion: 1.0.0\ntrigger_keywords: k\nagents: pm\n---\n",
            encoding="utf-8")
        data = {"skills": [{"name": "demo", "version": "1.0.0", "path": path_value,
                            "trigger": {"keywords": keywords, "agents": ["pm"]},
                            "inputs": ["a"], "outputs": ["b"], "verify": "c",
                            "source": "internal", "owner": "pm"}]}
        reg = tmp / "registry.json"
        reg.write_text(json.dumps(data), encoding="utf-8")
        return reg, tmp

    def test_ok(self):
        reg, tmp = self.build("skills/demo/skill.md", ["k"])
        violations, total = registry_lint.lint(reg, tmp)
        self.assertEqual((violations, total), ([], 1))

    def test_path_missing(self):
        reg, tmp = self.build("skills/nope/skill.md", ["k"])
        violations, _ = registry_lint.lint(reg, tmp)
        self.assertTrue(any("path missing" in v for v in violations))

    def test_duplicate_keyword(self):
        reg, tmp = self.build("skills/demo/skill.md", ["k", "k"])
        violations, _ = registry_lint.lint(reg, tmp)
        self.assertTrue(any("duplicated" in v for v in violations))


class LinkCheckTest(unittest.TestCase):
    def test_no_dead_link(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "a.md").write_text("见 `b.md`\n", encoding="utf-8")
        (tmp / "b.md").write_text("# b\n", encoding="utf-8")
        self.assertEqual(link_check.check(tmp, include=(tmp / "a.md",), extra_dirs=()), [])

    def test_cursorrules_dead(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "a.md").write_text("规则见 `.cursorrules`\n", encoding="utf-8")
        dead = link_check.check(tmp, include=(tmp / "a.md",), extra_dirs=())
        self.assertEqual([d["target"] for d in dead], [".cursorrules"])

    def test_url_not_flagged(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "a.md").write_text("[docs](https://example.com/x.md)\n", encoding="utf-8")
        self.assertEqual(link_check.check(tmp, include=(tmp / "a.md",), extra_dirs=()), [])


if __name__ == "__main__":
    unittest.main()

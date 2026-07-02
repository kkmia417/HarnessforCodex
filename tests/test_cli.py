from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from codex_harness.cli import create_skill, main, marketplace_catalog, validate_root


def run_cli(args: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            return main(args)
        except SystemExit as exc:
            return int(exc.code)


def validate_quiet(root: Path) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return validate_root(root)


class CliTests(unittest.TestCase):
    def test_create_skill_generates_valid_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_skill(
                "sample-flow",
                root / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )

            self.assertEqual(validate_quiet(root), 0)

    def test_bundled_skill_data_matches_source_skills(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        source = repo_root / "skills"
        bundled = repo_root / "src" / "codex_harness" / "data" / "skills"

        source_files = sorted(path.relative_to(source) for path in source.rglob("*") if path.is_file())
        bundled_files = sorted(path.relative_to(bundled) for path in bundled.rglob("*") if path.is_file())

        self.assertEqual(source_files, bundled_files)
        for relative_path in source_files:
            self.assertEqual(
                (source / relative_path).read_text(encoding="utf-8"),
                (bundled / relative_path).read_text(encoding="utf-8"),
                str(relative_path),
            )

    def test_validate_root_accepts_official_agents_skill_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_skill(
                "sample-flow",
                root / ".agents" / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )

            self.assertEqual(validate_quiet(root), 0)

    def test_validate_root_rejects_missing_reference_at_line_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = create_skill(
                "sample-flow",
                root / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\nreferences/missing.md\n", encoding="utf-8")

            self.assertEqual(validate_quiet(root), 1)

    def test_validate_root_rejects_machine_local_paths_in_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = create_skill(
                "sample-flow",
                root / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )
            reference = skill_dir / "references" / "setup.md"
            reference.write_text("Run C:/Users/example/.codex/skills/tool.py locally.\n", encoding="utf-8")
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\n- See references/setup.md.\n", encoding="utf-8")

            self.assertEqual(validate_quiet(root), 1)

    def test_init_defaults_to_official_agents_skill_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"
            create_skill(
                "source-flow",
                source / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )

            code = run_cli(["init", str(target), "--source-root", str(source), "--skill", "source-flow"])

            self.assertEqual(code, 0)
            self.assertTrue((target / ".agents" / "skills" / "source-flow" / "SKILL.md").exists())
            self.assertFalse((target / "skills" / "source-flow").exists())

    def test_init_requires_explicit_skill_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"

            self.assertEqual(run_cli(["init", str(target)]), 2)

    def test_init_can_write_both_skill_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"
            create_skill(
                "source-flow",
                source / "skills",
                "Plan and validate a repeated repository workflow with clear trigger conditions for Codex usage. Use when asked to create, check, or evolve a reusable workflow skill.",
                None,
                None,
                {"references"},
                False,
                False,
            )

            code = run_cli(
                [
                    "init",
                    str(target),
                    "--source-root",
                    str(source),
                    "--skill",
                    "source-flow",
                    "--skill-layout",
                    "both",
                ]
            )

            self.assertEqual(code, 0)
            self.assertTrue((target / ".agents" / "skills" / "source-flow" / "SKILL.md").exists())
            self.assertTrue((target / "skills" / "source-flow" / "SKILL.md").exists())

    def test_marketplace_catalog_uses_installable_entry_shape(self) -> None:
        catalog = marketplace_catalog(
            "harnessforcodex",
            "Harness for Codex",
            "harnessforcodex",
            "./plugins/harnessforcodex",
            "Productivity",
        )

        self.assertEqual(catalog["name"], "harnessforcodex")
        plugin = catalog["plugins"][0]  # type: ignore[index]
        self.assertEqual(plugin["source"]["path"], "./plugins/harnessforcodex")  # type: ignore[index]
        self.assertEqual(plugin["policy"]["installation"], "AVAILABLE")  # type: ignore[index]
        self.assertEqual(plugin["policy"]["authentication"], "ON_INSTALL")  # type: ignore[index]

    def test_marketplace_command_writes_catalog_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / ".agents" / "plugins" / "marketplace.json"

            code = run_cli(["marketplace", str(output)])

            self.assertEqual(code, 0)
            self.assertIn('"name": "harnessforcodex"', output.read_text(encoding="utf-8"))

    def test_marketplace_command_rejects_non_relative_plugin_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "marketplace.json"

            code = run_cli(["marketplace", str(output), "--plugin-source", "plugins/harnessforcodex"])

            self.assertEqual(code, 1)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()

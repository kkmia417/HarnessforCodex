from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from codex_harness.cli import create_skill, validate_root


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

            self.assertEqual(validate_root(root), 0)


if __name__ == "__main__":
    unittest.main()

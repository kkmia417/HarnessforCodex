#!/usr/bin/env python3
"""Create a repository-local Codex skill skeleton."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def skill_md(name: str, description: str, orchestrator: bool) -> str:
    title = title_from_name(name)
    if orchestrator:
        body = f"""# {title}

Coordinate this workflow by classifying the request, selecting the smallest path, preserving handoffs, validating outputs, and summarizing results.

## Workflow

1. Audit current state and user changes.
2. Classify the request.
3. Select child skills, scripts, or references.
4. Execute phases with explicit handoffs.
5. Validate results.
6. Report files changed, commands run, and remaining risk.

## References

- Add focused reference files under `references/` when this workflow needs more detail.
"""
    else:
        body = f"""# {title}

Use this skill for the repeated workflow described in the frontmatter.

## Workflow

1. Inspect the current project state.
2. Read only the references needed for this request.
3. Make the requested change or produce the requested artifact.
4. Run the relevant validation.
5. Summarize files changed, commands run, and remaining risk.

## References

- Add focused reference files under `references/` when this workflow needs more detail.
"""
    return f"""---
name: {name}
description: {description}
---

{body}"""


def openai_yaml(name: str, display_name: str, short_description: str) -> str:
    return f"""interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
  default_prompt: "Use ${name} to run this repository workflow."
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="lowercase hyphen-case skill name")
    parser.add_argument("--path", default="skills", help="directory that contains skill folders")
    parser.add_argument("--description", required=True, help="frontmatter description with trigger conditions")
    parser.add_argument("--display-name", help="openai.yaml display name")
    parser.add_argument("--short-description", help="openai.yaml short description")
    parser.add_argument("--resources", default="references", help="comma-separated: references,scripts,assets")
    parser.add_argument("--orchestrator", action="store_true", help="create an orchestrator-flavored SKILL.md")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()

    name = args.name.strip()
    if not NAME_RE.match(name):
        print("ERROR: name must be lowercase hyphen-case", file=sys.stderr)
        return 1

    root = Path(args.path).resolve()
    skill_dir = root / name
    display_name = args.display_name or title_from_name(name)
    short_description = args.short_description or args.description[:72].rstrip()
    resources = {item.strip() for item in args.resources.split(",") if item.strip()}
    invalid_resources = resources - {"references", "scripts", "assets"}
    if invalid_resources:
        print(f"ERROR: invalid resources: {', '.join(sorted(invalid_resources))}", file=sys.stderr)
        return 1

    try:
        write(skill_dir / "SKILL.md", skill_md(name, args.description, args.orchestrator), args.force)
        write(skill_dir / "agents" / "openai.yaml", openai_yaml(name, display_name, short_description), args.force)
        for resource in sorted(resources):
            (skill_dir / resource).mkdir(parents=True, exist_ok=True)
    except FileExistsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OK: created {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

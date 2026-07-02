from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .constants import NAME_RE, RESOURCE_NAMES


def resolve_path(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def skill_markdown(name: str, description: str, orchestrator: bool) -> str:
    title = title_from_name(name)
    if orchestrator:
        body = """Coordinate this workflow by classifying the request, selecting the smallest path, preserving handoffs, validating outputs, and summarizing results.

## Workflow

1. Audit current state and user changes.
2. Classify the request.
3. Select child skills, scripts, or references.
4. Execute phases with explicit handoffs.
5. Validate results.
6. Report files changed, commands run, and remaining risk.
"""
    else:
        body = """Use this skill for the repeated workflow described in the frontmatter.

## Workflow

1. Inspect the current project state.
2. Read only the references needed for this request.
3. Make the requested change or produce the requested artifact.
4. Run the relevant validation.
5. Summarize files changed, commands run, and remaining risk.
"""

    return f"""---
name: {name}
description: {description}
---

# {title}

{body}
## References

- Add focused reference files under `references/` when this workflow needs more detail.
"""


def openai_yaml(name: str, display_name: str, short_description: str) -> str:
    return f"""interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
  default_prompt: "Use ${name} to run this repository workflow."
"""


def create_skill(
    name: str,
    base_path: Path,
    description: str,
    display_name: str | None,
    short_description: str | None,
    resources: set[str],
    orchestrator: bool,
    force: bool,
) -> Path:
    if not NAME_RE.match(name):
        raise ValueError("name must be lowercase hyphen-case")
    invalid_resources = resources - RESOURCE_NAMES
    if invalid_resources:
        raise ValueError(f"invalid resources: {', '.join(sorted(invalid_resources))}")

    skill_dir = resolve_path(base_path) / name
    files = {
        skill_dir / "SKILL.md": skill_markdown(name, description, orchestrator),
        skill_dir / "agents" / "openai.yaml": openai_yaml(
            name,
            display_name or title_from_name(name),
            short_description or description[:72].rstrip(),
        ),
    }

    for path, content in files.items():
        if path.exists() and not force:
            raise FileExistsError(f"{path} already exists; pass --force to overwrite")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    for resource in resources:
        (skill_dir / resource).mkdir(parents=True, exist_ok=True)
    return skill_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="lowercase hyphen-case skill name")
    parser.add_argument("--path", default="skills", help="directory that contains skill folders")
    parser.add_argument("--description", required=True, help="frontmatter description with trigger conditions")
    parser.add_argument("--display-name", help="openai.yaml display name")
    parser.add_argument("--short-description", help="openai.yaml short description")
    parser.add_argument("--resources", default="references", help="comma-separated: references,scripts,assets")
    parser.add_argument("--orchestrator", action="store_true", help="create an orchestrator-flavored SKILL.md")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)

    resources = {item.strip() for item in args.resources.split(",") if item.strip()}
    try:
        created = create_skill(
            args.name.strip(),
            resolve_path(args.path),
            args.description,
            args.display_name,
            args.short_description,
            resources,
            args.orchestrator,
            args.force,
        )
    except (FileExistsError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OK: created {created}")
    return 0

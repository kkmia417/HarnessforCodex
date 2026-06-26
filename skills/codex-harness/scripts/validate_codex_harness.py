#!/usr/bin/env python3
"""Structural checks for repository-local Codex harness skills."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"(?:^|[`('\\\"])(references/[A-Za-z0-9_.\-/]+\.md)")
TODO_RE = re.compile(r"\bTODO\b|\[TODO", re.IGNORECASE)


@dataclass
class Finding:
    level: str
    message: str


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")

    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_openai_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(field)}:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def validate_references(skill_dir: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for ref in sorted(set(REFERENCE_RE.findall(text))):
        target = skill_dir / ref
        if not target.exists():
            findings.append(Finding("ERROR", f"{skill_dir / 'SKILL.md'}: missing referenced file {ref}"))
    return findings


def validate_openai_yaml(skill_dir: Path, skill_name: str) -> list[Finding]:
    findings: list[Finding] = []
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [Finding("ERROR", f"{path}: missing agents/openai.yaml")]

    text = read_text(path)
    for field in ("display_name", "short_description", "default_prompt"):
        if extract_openai_field(text, field) is None:
            findings.append(Finding("ERROR", f"{path}: missing interface.{field}"))

    prompt = extract_openai_field(text, "default_prompt") or ""
    if f"${skill_name}" not in prompt:
        findings.append(Finding("ERROR", f"{path}: default_prompt must contain ${skill_name}"))
    return findings


def validate_skill(skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [Finding("ERROR", f"{skill_dir}: missing SKILL.md")]

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [Finding("ERROR", f"{skill_md}: {exc}")]

    allowed_keys = {"name", "description"}
    extra_keys = sorted(set(frontmatter) - allowed_keys)
    if extra_keys:
        findings.append(Finding("ERROR", f"{skill_md}: unsupported frontmatter keys: {', '.join(extra_keys)}"))

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    text = read_text(skill_md)

    if name != skill_dir.name:
        findings.append(Finding("ERROR", f"{skill_md}: name {name!r} must match folder {skill_dir.name!r}"))
    if not NAME_RE.match(name):
        findings.append(Finding("ERROR", f"{skill_md}: name must be lowercase hyphen-case"))
    if len(description) < 100:
        findings.append(Finding("ERROR", f"{skill_md}: description should explain purpose and trigger conditions"))
    if TODO_RE.search(text):
        findings.append(Finding("ERROR", f"{skill_md}: unresolved TODO placeholder"))

    findings.extend(validate_references(skill_dir, text))
    findings.extend(validate_openai_yaml(skill_dir, name))
    return findings


def find_skill_dirs(root: Path) -> list[Path]:
    if (root / "SKILL.md").exists():
        return [root]

    repo_skills = root / "skills"
    if repo_skills.exists():
        return [child for child in sorted(repo_skills.iterdir()) if child.is_dir()]

    direct_children = [child for child in sorted(root.iterdir()) if child.is_dir() and (child / "SKILL.md").exists()]
    if direct_children:
        return direct_children

    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_dirs = find_skill_dirs(root)
    if not skill_dirs:
        print(f"ERROR: no Codex skill directories found under {root}", file=sys.stderr)
        return 1

    findings: list[Finding] = []
    seen_names: set[str] = set()
    for child in skill_dirs:
        if child.name in seen_names:
            findings.append(Finding("ERROR", f"{child}: duplicate skill name"))
        seen_names.add(child.name)
        findings.extend(validate_skill(child))

    has_errors = False
    for finding in findings:
        print(f"{finding.level}: {finding.message}", file=sys.stderr)
        if finding.level == "ERROR" or args.warnings_as_errors:
            has_errors = True

    if has_errors:
        return 1

    print(f"OK: validated {len(seen_names)} Codex harness skill(s) under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .constants import LEGACY_SKILLS_DIR, NAME_RE, OFFICIAL_SKILLS_DIR


FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
REFERENCE_RE = re.compile(r"(?:^|[\s`('\\\"])(references/[A-Za-z0-9_.\-/]+\.md)", re.MULTILINE)
TODO_RE = re.compile(r"\bTODO\b|\[TODO", re.IGNORECASE)
LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\][^\s`'\"<>]+|/home/[A-Za-z0-9._-]+/[^\s`'\"<>]+)")


@dataclass(frozen=True)
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


def extract_yaml_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(field)}:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def validate_references(skill_dir: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for ref in sorted(set(REFERENCE_RE.findall(text))):
        if not (skill_dir / ref).exists():
            findings.append(Finding("ERROR", f"{skill_dir / 'SKILL.md'}: missing referenced file {ref}"))
    return findings


def validate_no_local_paths(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    if LOCAL_PATH_RE.search(text):
        return [
            Finding(
                "ERROR",
                f"{path}: machine-local absolute path is not allowed; use $CODEX_HOME or a repo-relative path",
            )
        ]
    return []


def validate_shared_markdown(skill_dir: Path) -> list[Finding]:
    paths = [skill_dir / "SKILL.md"]
    references_dir = skill_dir / "references"
    if references_dir.exists():
        paths.extend(sorted(references_dir.rglob("*.md")))

    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_no_local_paths(path))
    return findings


def validate_openai_yaml(skill_dir: Path, skill_name: str) -> list[Finding]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [Finding("ERROR", f"{path}: missing agents/openai.yaml")]

    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    for field in ("display_name", "short_description", "default_prompt"):
        if extract_yaml_field(text, field) is None:
            findings.append(Finding("ERROR", f"{path}: missing interface.{field}"))

    prompt = extract_yaml_field(text, "default_prompt") or ""
    if f"${skill_name}" not in prompt:
        findings.append(Finding("ERROR", f"{path}: default_prompt must contain ${skill_name}"))
    return findings


def validate_skill(skill_dir: Path) -> list[Finding]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [Finding("ERROR", f"{skill_dir}: missing SKILL.md")]

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [Finding("ERROR", f"{skill_md}: {exc}")]

    findings: list[Finding] = []
    extra_keys = sorted(set(frontmatter) - {"name", "description"})
    if extra_keys:
        findings.append(Finding("ERROR", f"{skill_md}: unsupported frontmatter keys: {', '.join(extra_keys)}"))

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    text = skill_md.read_text(encoding="utf-8")

    if name != skill_dir.name:
        findings.append(Finding("ERROR", f"{skill_md}: name {name!r} must match folder {skill_dir.name!r}"))
    if not NAME_RE.match(name):
        findings.append(Finding("ERROR", f"{skill_md}: name must be lowercase hyphen-case"))
    if len(description) < 100:
        findings.append(Finding("ERROR", f"{skill_md}: description should explain purpose and trigger conditions"))
    if TODO_RE.search(text):
        findings.append(Finding("ERROR", f"{skill_md}: unresolved TODO placeholder"))

    findings.extend(validate_shared_markdown(skill_dir))
    findings.extend(validate_references(skill_dir, text))
    findings.extend(validate_openai_yaml(skill_dir, name))
    return findings


def find_skill_dirs(root: Path) -> list[Path]:
    if (root / "SKILL.md").exists():
        return [root]

    skill_dirs: list[Path] = []
    for relative_root in (OFFICIAL_SKILLS_DIR, LEGACY_SKILLS_DIR):
        repo_skills = root / relative_root
        if repo_skills.exists():
            skill_dirs.extend(
                child for child in sorted(repo_skills.iterdir()) if child.is_dir() and (child / "SKILL.md").exists()
            )
    if skill_dirs:
        return skill_dirs

    return [child for child in sorted(root.iterdir()) if child.is_dir() and (child / "SKILL.md").exists()]


def validate_root(root: Path, warnings_as_errors: bool = False) -> int:
    skill_dirs = find_skill_dirs(root)
    if not skill_dirs:
        print(f"ERROR: no Codex skill directories found under {root}", file=sys.stderr)
        return 1

    findings: list[Finding] = []
    seen_names: set[str] = set()
    for skill_dir in skill_dirs:
        if skill_dir.name in seen_names:
            findings.append(Finding("ERROR", f"{skill_dir}: duplicate skill name"))
        seen_names.add(skill_dir.name)
        findings.extend(validate_skill(skill_dir))

    failed = False
    for finding in findings:
        print(f"{finding.level}: {finding.message}", file=sys.stderr)
        if finding.level == "ERROR" or warnings_as_errors:
            failed = True

    if failed:
        return 1

    print(f"OK: validated {len(seen_names)} Codex harness skill(s) under {root}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args(argv)
    return validate_root(Path(args.root).resolve(), args.warnings_as_errors)

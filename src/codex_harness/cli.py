from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"(?:^|[`('\\\"])(references/[A-Za-z0-9_.\-/]+\.md)")
TODO_RE = re.compile(r"\bTODO\b|\[TODO", re.IGNORECASE)
RESOURCE_NAMES = {"references", "scripts", "assets"}


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


def _resolve(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def _is_child(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return child != parent


def _parse_frontmatter(path: Path) -> dict[str, str]:
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


def _extract_yaml_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(field)}:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _validate_references(skill_dir: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for ref in sorted(set(REFERENCE_RE.findall(text))):
        if not (skill_dir / ref).exists():
            findings.append(Finding("ERROR", f"{skill_dir / 'SKILL.md'}: missing referenced file {ref}"))
    return findings


def _validate_openai_yaml(skill_dir: Path, skill_name: str) -> list[Finding]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [Finding("ERROR", f"{path}: missing agents/openai.yaml")]

    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    for field in ("display_name", "short_description", "default_prompt"):
        if _extract_yaml_field(text, field) is None:
            findings.append(Finding("ERROR", f"{path}: missing interface.{field}"))

    prompt = _extract_yaml_field(text, "default_prompt") or ""
    if f"${skill_name}" not in prompt:
        findings.append(Finding("ERROR", f"{path}: default_prompt must contain ${skill_name}"))
    return findings


def validate_skill(skill_dir: Path) -> list[Finding]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [Finding("ERROR", f"{skill_dir}: missing SKILL.md")]

    try:
        frontmatter = _parse_frontmatter(skill_md)
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

    findings.extend(_validate_references(skill_dir, text))
    findings.extend(_validate_openai_yaml(skill_dir, name))
    return findings


def find_skill_dirs(root: Path) -> list[Path]:
    if (root / "SKILL.md").exists():
        return [root]

    repo_skills = root / "skills"
    if repo_skills.exists():
        return [child for child in sorted(repo_skills.iterdir()) if child.is_dir()]

    direct_children = [child for child in sorted(root.iterdir()) if child.is_dir() and (child / "SKILL.md").exists()]
    return direct_children


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


def find_source_root(explicit: str | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(_resolve(explicit))
    if os.environ.get("CODEX_HARNESS_SOURCE"):
        candidates.append(_resolve(os.environ["CODEX_HARNESS_SOURCE"]))

    candidates.extend(_resolve(path) for path in (Path.cwd(), Path(__file__).resolve()))
    for base in list(candidates):
        candidates.extend(base.parents)

    for candidate in candidates:
        if (candidate / "skills" / "codex-harness" / "SKILL.md").exists():
            return candidate

    raise FileNotFoundError(
        "could not find Harness for Codex source root; pass --source-root or set CODEX_HARNESS_SOURCE"
    )


def selected_skill_names(source_root: Path, names: list[str] | None, all_skills: bool) -> list[str]:
    source_skills = source_root / "skills"
    if all_skills:
        selected = [child.name for child in source_skills.iterdir() if child.is_dir() and (child / "SKILL.md").exists()]
    else:
        selected = names or []
    if not selected:
        raise ValueError("select at least one skill or pass --all")

    unique = sorted(set(selected))
    for name in unique:
        if not NAME_RE.match(name):
            raise ValueError(f"invalid skill name {name!r}; use lowercase hyphen-case")
        if not (source_skills / name / "SKILL.md").exists():
            raise FileNotFoundError(f"repository skill not found: {name}")
    return unique


def copy_skill(source_root: Path, destination_root: Path, skill_name: str, force: bool) -> None:
    source = _resolve(source_root / "skills" / skill_name)
    destination_root = _resolve(destination_root)
    destination = _resolve(destination_root / skill_name)

    if not _is_child(_resolve(source_root / "skills"), source):
        raise ValueError(f"refusing to read outside source skills root: {source}")
    if not _is_child(destination_root, destination):
        raise ValueError(f"refusing to write outside destination root: {destination}")
    if destination.exists() and not force:
        raise FileExistsError(f"{destination} already exists; pass --force to replace it")

    destination_root.mkdir(parents=True, exist_ok=True)
    staging = _resolve(destination_root / f".{skill_name}.sync-{os.getpid()}")
    if staging.exists():
        shutil.rmtree(staging)

    try:
        shutil.copytree(source, staging)
        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


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

    skill_dir = _resolve(base_path) / name
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


def cmd_validate(args: argparse.Namespace) -> int:
    return validate_root(_resolve(args.root), args.warnings_as_errors)


def cmd_sync(args: argparse.Namespace) -> int:
    source_root = find_source_root(args.source_root)
    names = selected_skill_names(source_root, args.skill, args.all)
    destination = _resolve(args.destination)
    for name in names:
        copy_skill(source_root, destination, name, args.force)
        print(f"OK: synced {name} -> {destination / name}")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    resources = {item.strip() for item in args.resources.split(",") if item.strip()}
    created = create_skill(
        args.name.strip(),
        _resolve(args.path),
        args.description,
        args.display_name,
        args.short_description,
        resources,
        args.orchestrator,
        args.force,
    )
    print(f"OK: created {created}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    source_root = find_source_root(args.source_root)
    names = selected_skill_names(source_root, args.skill, args.all)
    target = _resolve(args.target)
    skills_destination = target / "skills"
    for name in names:
        copy_skill(source_root, skills_destination, name, args.force)
        print(f"OK: installed {name} -> {skills_destination / name}")

    if args.with_plugin:
        plugin_source = source_root / ".codex-plugin"
        plugin_destination = target / ".codex-plugin"
        if plugin_source.exists():
            if plugin_destination.exists() and not args.force:
                raise FileExistsError(f"{plugin_destination} already exists; pass --force to replace it")
            if plugin_destination.exists():
                shutil.rmtree(plugin_destination)
            shutil.copytree(plugin_source, plugin_destination)
            print(f"OK: installed plugin metadata -> {plugin_destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex-harness")
    parser.add_argument("--version", action="version", version="codex-harness 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate Codex skill structure")
    validate.add_argument("root", nargs="?", default=".", help="repository root or skill directory")
    validate.add_argument("--warnings-as-errors", action="store_true")
    validate.set_defaults(func=cmd_validate)

    sync = subparsers.add_parser("sync", help="sync repo skills into a local Codex skills directory")
    sync_select = sync.add_mutually_exclusive_group(required=True)
    sync_select.add_argument("--all", action="store_true", help="sync every skill from the source repo")
    sync_select.add_argument("--skill", action="append", help="skill name to sync; can be passed multiple times")
    sync.add_argument("--destination", default=str(Path.home() / ".codex" / "skills"))
    sync.add_argument("--source-root", help="Harness for Codex checkout; defaults to auto-detection")
    sync.add_argument("--force", action="store_true", help="replace existing destination skill directories")
    sync.set_defaults(func=cmd_sync)

    new = subparsers.add_parser("new", help="create a repository-local Codex skill skeleton")
    new.add_argument("name", help="lowercase hyphen-case skill name")
    new.add_argument("--path", default="skills", help="directory that contains skill folders")
    new.add_argument("--description", required=True, help="frontmatter description with trigger conditions")
    new.add_argument("--display-name")
    new.add_argument("--short-description")
    new.add_argument("--resources", default="references", help="comma-separated: references,scripts,assets")
    new.add_argument("--orchestrator", action="store_true")
    new.add_argument("--force", action="store_true")
    new.set_defaults(func=cmd_new)

    init = subparsers.add_parser("init", help="install Harness for Codex skills into a target repository")
    init.add_argument("target", nargs="?", default=".", help="target repository")
    init_select = init.add_mutually_exclusive_group()
    init_select.add_argument("--all", action="store_true", help="install every source skill")
    init_select.add_argument("--skill", action="append", help="skill name to install; can be passed multiple times")
    init.add_argument("--source-root", help="Harness for Codex checkout; defaults to auto-detection")
    init.add_argument("--with-plugin", action="store_true", help="copy .codex-plugin metadata")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init" and not args.all and not args.skill:
        args.all = True
    try:
        return args.func(args)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .constants import DEFAULT_USER_SKILLS_DIR, SKILL_LAYOUTS
from .marketplace import marketplace_catalog
from .scaffold import create_skill, resolve_path
from .sync import copy_skill, selected_skill_names, source_root_context
from .validation import validate_root


def cmd_validate(args: argparse.Namespace) -> int:
    return validate_root(resolve_path(args.root), args.warnings_as_errors)


def cmd_sync(args: argparse.Namespace) -> int:
    with source_root_context(args.source_root) as source_root:
        names = selected_skill_names(source_root, args.skill, args.all)
        destination = resolve_path(args.destination)
        for name in names:
            copy_skill(source_root, destination, name, args.force)
            print(f"OK: synced {name} -> {destination / name}")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    resources = {item.strip() for item in args.resources.split(",") if item.strip()}
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
    print(f"OK: created {created}")
    return 0


def cmd_marketplace(args: argparse.Namespace) -> int:
    output = resolve_path(args.output)
    if output.exists() and not args.force:
        raise FileExistsError(f"{output} already exists; pass --force to replace it")

    output.parent.mkdir(parents=True, exist_ok=True)
    catalog = marketplace_catalog(
        args.marketplace_name,
        args.display_name,
        args.plugin_name,
        args.plugin_source,
        args.category,
    )
    output.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"OK: wrote marketplace catalog -> {output}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    with source_root_context(args.source_root) as source_root:
        names = selected_skill_names(source_root, args.skill, args.all)
        target = resolve_path(args.target)
        for relative_destination in SKILL_LAYOUTS[args.skill_layout]:
            skills_destination = target / relative_destination
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
    sync.add_argument("--destination", default=str(DEFAULT_USER_SKILLS_DIR))
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

    marketplace = subparsers.add_parser("marketplace", help="write a Codex plugin marketplace catalog")
    marketplace.add_argument("output", nargs="?", default=str(Path(".agents") / "plugins" / "marketplace.json"))
    marketplace.add_argument("--marketplace-name", default="harnessforcodex")
    marketplace.add_argument("--display-name", default="Harness for Codex")
    marketplace.add_argument("--plugin-name", default="harnessforcodex")
    marketplace.add_argument("--plugin-source", default="./plugins/harnessforcodex")
    marketplace.add_argument("--category", default="Productivity")
    marketplace.add_argument("--force", action="store_true")
    marketplace.set_defaults(func=cmd_marketplace)

    init = subparsers.add_parser("init", help="install Harness for Codex skills into a target repository")
    init.add_argument("target", nargs="?", default=".", help="target repository")
    init_select = init.add_mutually_exclusive_group(required=True)
    init_select.add_argument("--all", action="store_true", help="install every source skill")
    init_select.add_argument("--skill", action="append", help="skill name to install; can be passed multiple times")
    init.add_argument("--source-root", help="Harness for Codex checkout; defaults to auto-detection")
    init.add_argument(
        "--skill-layout",
        choices=sorted(SKILL_LAYOUTS),
        default="official",
        help="official writes .agents/skills, legacy writes skills, both writes both",
    )
    init.add_argument("--with-plugin", action="store_true", help="copy .codex-plugin metadata")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

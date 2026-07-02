from __future__ import annotations

import os
import shutil
from contextlib import contextmanager
from importlib.resources import as_file, files
from pathlib import Path
from typing import Iterator

from .constants import NAME_RE


def resolve_path(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def is_child(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return child != parent


def has_skill_source_root(candidate: Path) -> bool:
    source_skills = candidate / "skills"
    return source_skills.exists() and any(
        child.is_dir() and (child / "SKILL.md").exists() for child in source_skills.iterdir()
    )


def find_checkout_source_root(explicit: str | None = None) -> Path | None:
    if explicit:
        explicit_root = resolve_path(explicit)
        if has_skill_source_root(explicit_root):
            return explicit_root
        raise FileNotFoundError(f"skill source root not found or invalid: {explicit_root}")

    if os.environ.get("CODEX_HARNESS_SOURCE"):
        env_root = resolve_path(os.environ["CODEX_HARNESS_SOURCE"])
        if has_skill_source_root(env_root):
            return env_root
        raise FileNotFoundError(f"CODEX_HARNESS_SOURCE is not a valid source root: {env_root}")

    candidates: list[Path] = []
    candidates.extend(resolve_path(path) for path in (Path.cwd(), Path(__file__).resolve()))
    for base in list(candidates):
        candidates.extend(base.parents)

    for candidate in candidates:
        if (candidate / "skills" / "codex-harness" / "SKILL.md").exists():
            return candidate
    return None


@contextmanager
def source_root_context(explicit: str | None = None) -> Iterator[Path]:
    checkout_root = find_checkout_source_root(explicit)
    if checkout_root is not None:
        yield checkout_root
        return

    data_root = files("codex_harness") / "data"
    with as_file(data_root) as bundled_root:
        if not has_skill_source_root(bundled_root):
            raise FileNotFoundError(
                "could not find Harness for Codex source root; pass --source-root or set CODEX_HARNESS_SOURCE"
            )
        yield bundled_root


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
    source = resolve_path(source_root / "skills" / skill_name)
    destination_root = resolve_path(destination_root)
    destination = resolve_path(destination_root / skill_name)

    if not is_child(resolve_path(source_root / "skills"), source):
        raise ValueError(f"refusing to read outside source skills root: {source}")
    if not is_child(destination_root, destination):
        raise ValueError(f"refusing to write outside destination root: {destination}")
    if destination.exists() and not force:
        raise FileExistsError(f"{destination} already exists; pass --force to replace it")

    destination_root.mkdir(parents=True, exist_ok=True)
    staging = resolve_path(destination_root / f".{skill_name}.sync-{os.getpid()}")
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

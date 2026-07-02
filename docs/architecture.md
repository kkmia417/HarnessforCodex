# Architecture

Harness for Codex is built around repository-local workflow assets. The goal is
to make repeated Codex behavior durable without hiding the rules in a large
application.

## Core Concepts

- A skill is the user-facing workflow contract. In this repository, packaged
  source skills live in `skills/<name>/SKILL.md`.
- Installed repository skills live in `.agents/skills/<name>/SKILL.md` by
  default, matching Codex repository skill discovery.
- A reference is stable supporting knowledge. It lives under a skill's `references/`.
- A script is deterministic support logic. It lives under a skill's `scripts/` or the root `scripts/`.
- Agent metadata lives in `agents/openai.yaml` and describes how Codex should expose the skill.
- The CLI makes validation, sync, initialization, and scaffolding work the same way across platforms.

## Why Skills Instead of Prompts

Plain prompts are easy to copy and hard to govern. Skills provide:

- trigger conditions in frontmatter
- repeatable instructions in a known location
- shared rubrics and handoff contracts
- validation of required files and metadata
- repository review in normal pull requests

## CLI Commands

`codex-harness validate` checks every skill in a repository or a single skill directory.

`codex-harness init` installs Harness for Codex skills into another repository.
The default target is `.agents/skills`; pass `--skill-layout legacy` for the
older root `skills/` layout or `--skill-layout both` during migration.

Skill source resolution is explicit first and packaged last: `--source-root`,
then `CODEX_HARNESS_SOURCE`, then a nearby source checkout, then bundled package
data under `codex_harness/data/skills`.

`codex-harness sync` installs selected skills into the user-level Codex skills directory.

`codex-harness new` scaffolds a new repository-local skill with required metadata.

`codex-harness marketplace` writes a Codex plugin marketplace catalog for local
or team distribution.

## Compatibility

The repository keeps the PowerShell sync script for Windows users who do not want
to install the Python package. The Python CLI is the preferred cross-platform path.
Both validators accept `.agents/skills` and the older root `skills/` layout.
The repository script delegates to the package validator so CLI validation and
script validation share one implementation.

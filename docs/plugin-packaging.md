# Codex Plugin Packaging

This repository includes Codex plugin metadata so the full skill suite can be
distributed as one local plugin when that is more useful than copying selected
skills into `~/.codex/skills`.

## Decision

Add plugin packaging.

The repository-local skills remain the source of truth. Plugin packaging adds a
single installable boundary around the existing `skills/` tree without changing
the skill authoring workflow.

## Why It Helps

Repository-local skills are best for direct development and review. They are
also easy to sync one at a time with `scripts/sync_codex_skills.ps1`.

Plugin packaging is useful when a user wants the whole harness suite to appear
as one Codex plugin, with shared UI metadata and one versioned package. That
matters for local distribution, previewing the suite in plugin UI surfaces, and
keeping all workflow skills installed together.

## Package Shape

The plugin root is the repository root.

```text
.codex-plugin/
  plugin.json
skills/
  codex-harness/
  repo-review/
  feature-delivery/
  integration-qa/
  docs-maintenance/
  release-readiness/
```

The plugin manifest points to `./skills/`, so Codex ingests the existing skill
directories in place. The package does not declare hooks, apps, MCP servers, or
asset paths because this repository does not provide those companion files.

## Install And Update

For normal repository development, use the repository directly or sync selected
skills:

```powershell
.\scripts\sync_codex_skills.ps1 -All
.\scripts\sync_codex_skills.ps1 -Skill codex-harness,repo-review
```

For plugin distribution, expose this repository root from a configured Codex
plugin marketplace as plugin `harnessforcodex`, then install it:

```powershell
codex plugin add harnessforcodex@<marketplace>
```

For Git-backed marketplaces, refresh updates with:

```powershell
codex plugin marketplace upgrade
```

For local checkout changes, reinstall the plugin after changing `skills/` or
`.codex-plugin/plugin.json`.

Validate the package before sharing it:

```powershell
python C:\Users\kkmia\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

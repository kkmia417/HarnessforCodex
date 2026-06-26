# Harness for Codex

This repository contains a Codex-oriented port of the core idea behind
`revfactory/harness`: a project-local harness factory that designs, scaffolds,
validates, and evolves reusable Codex skills and workflow architectures.

The upstream Harness is Claude Code focused. This version maps the same factory
idea to Codex primitives: `skills/`, `SKILL.md`, `agents/openai.yaml`,
references, scripts, templates, validation checks, and optional sub-agent
protocols when the active Codex runtime supports them.

## What Is Included

```text
skills/codex-harness/
  SKILL.md
  agents/openai.yaml
  references/
    agent-design-patterns.md
    orchestrator-template.md
    project-integration.md
    qa-agent-guide.md
    evaluation-prompts.md
    skill-testing-guide.md
    skill-writing-guide.md
    team-examples.md
  scripts/
    scaffold_codex_skill.py
    validate_codex_harness.py
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/
  plugin.json
```

## Practical Skills

| Skill | Use For |
|---|---|
| `codex-harness` | designing, auditing, scaffolding, and evolving harnesses |
| `repo-review` | code review, PR review, repository audit, regression review |
| `feature-delivery` | planning, implementing, validating, and summarizing feature work |
| `integration-qa` | checking cross-boundary mismatches after changes |
| `docs-maintenance` | generating, updating, and verifying repository documentation |
| `release-readiness` | pre-release validation gates, changelog readiness, and deployment risk review |

## Use

Use the repository copy directly:

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

Typical prompts:

```text
Build a Codex harness for this repository.
Audit the existing Codex harness and evolve it.
Create reusable Codex skills for code review and release readiness.
Design a supervisor skill that routes frontend, backend, and QA workflows.
Use $feature-delivery at ./skills/feature-delivery to implement a bounded feature.
Use $repo-review at ./skills/repo-review to review the current diff.
```

## Scaffold a New Skill

```powershell
python .\skills\codex-harness\scripts\scaffold_codex_skill.py repo-review `
  --description "Review this repository for architecture, security, performance, tests, and integration risks. Use when asked for code review, PR review, regression review, or release readiness review." `
  --orchestrator `
  --resources references,scripts
```

## Validate

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
python C:\Users\kkmia\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\codex-harness
```

Run the Codex quick validator for every skill directory you create or edit.

GitHub Actions runs the same repository validation on every push and pull
request through `.github/workflows/validate.yml`. The workflow also validates
each `skills/*` directory independently so failures identify the affected skill.
If the Codex quick validator is installed, set `CODEX_QUICK_VALIDATE` to its
script path; otherwise the workflow falls back to the repository validator for
per-skill checks.

Local per-skill validation:

```powershell
Get-ChildItem .\skills -Directory | ForEach-Object {
  python .\skills\codex-harness\scripts\validate_codex_harness.py $_.FullName
}
```

## Sync Local Skills

Install or update every repository skill into your local Codex skills directory:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

Install or update selected skills only:

```powershell
.\scripts\sync_codex_skills.ps1 -Skill codex-harness,repo-review
```

The script replaces only the selected skill directories under
`$env:USERPROFILE\.codex\skills` and does not delete unrelated local skills.
Use `-DestinationRoot` to sync into a preview directory.

## Issue-Driven Development

This repository is intended to move forward through small issues:

- add one workflow skill at a time
- validate the skill structurally and with one scenario
- keep each issue tied to a concrete missing capability from upstream Harness
- close the issue with the commit or PR that adds the capability

See `docs/issue-roadmap.md` for the initial backlog.

## Install Locally

To make the harness available across local Codex sessions:

```powershell
$name = "codex-harness"
$dest = Join-Path $env:USERPROFILE ".codex\skills\$name"
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Copy-Item -Recurse -Force ".\skills\$name" $dest
```

Keep this repository as the source of truth and treat local installs as cache.
For repeated installs or updates, prefer `.\scripts\sync_codex_skills.ps1 -All`.

## Plugin Packaging

This repository can also be installed as a local Codex plugin when you want the
whole skill suite distributed as one package. The plugin metadata lives in
`.codex-plugin/plugin.json` and points to the existing `skills/` tree.

Use direct repository skills or `scripts/sync_codex_skills.ps1` for day-to-day
development. Use plugin installation when you want shared package metadata and a
single install/update unit for all skills. When consuming through the Codex CLI,
publish this checkout from a configured marketplace as plugin `harnessforcodex`,
then install it with:

```powershell
codex plugin add harnessforcodex@<marketplace>
```

For Git-backed marketplaces, refresh updates with `codex plugin marketplace
upgrade`. For local checkout changes, reinstall the plugin after updating this
repository.

Validate plugin metadata before sharing:

```powershell
python C:\Users\kkmia\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
```

See `docs/plugin-packaging.md` for the packaging decision, package shape, and
install/update notes.

## License and Attribution

This repository is licensed under the Apache License 2.0. See `LICENSE`.

Harness for Codex is a Codex-oriented port inspired by
[`revfactory/harness`](https://github.com/revfactory/harness), which is also
licensed under Apache-2.0. The upstream Harness project remains the original
Claude Code-focused implementation and should be referenced when tracing the
source concept and architecture.

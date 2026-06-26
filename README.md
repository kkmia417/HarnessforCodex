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
    skill-testing-guide.md
    skill-writing-guide.md
    team-examples.md
  scripts/
    scaffold_codex_skill.py
    validate_codex_harness.py
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
```

## Practical Skills

| Skill | Use For |
|---|---|
| `codex-harness` | designing, auditing, scaffolding, and evolving harnesses |
| `repo-review` | code review, PR review, repository audit, regression review |
| `feature-delivery` | planning, implementing, validating, and summarizing feature work |
| `integration-qa` | checking cross-boundary mismatches after changes |

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

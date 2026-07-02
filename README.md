# Harness for Codex

[![CI](https://github.com/kkmia417/HarnessforCodex/actions/workflows/ci.yml/badge.svg)](https://github.com/kkmia417/HarnessforCodex/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Turn any repository into a repeatable Codex workflow system in minutes.

Harness for Codex packages reusable Codex skills, validation checks, scaffolding
tools, and workflow references so teams can stop re-explaining the same review,
delivery, documentation, QA, and release rules in every prompt.

```bash
pip install -e .
codex-harness init ../my-repo --all
codex-harness validate ../my-repo
```

`init` installs skills to the Codex repository skill location,
`../my-repo/.agents/skills`, by default.

Then ask Codex:

```text
Use $repo-review to review the current diff.
Use $feature-delivery to implement this bounded feature end to end.
Use $release-readiness to decide whether this branch is ready to ship.
```

## 30-Second Demo

Before Harness for Codex, a reviewer prompt has to carry all of your team rules:

```text
Review this diff. Remember our severity policy, release checklist, docs rules,
cross-boundary checks, and how we report findings.
```

After installing the harness, the workflow is versioned in the repository:

```bash
codex-harness init ../my-repo --all
codex-harness validate ../my-repo
```

```text
Use $repo-review to review the current diff.
```

Codex now has explicit review steps, severity rules, integration checks, release
gates, and documentation verification rules available as repository skills.

## Why This Exists

Ad hoc AI prompting does not scale across a real repository. Teams repeat the
same constraints, forget the same checks, and lose hard-won workflow knowledge
between sessions.

Harness for Codex makes that knowledge explicit:

- `skills/` define reusable Codex workflows with trigger conditions.
- `references/` hold stable rules, rubrics, and handoff contracts.
- `scripts/` provide deterministic scaffolding and validation.
- `.codex-plugin/` packages the skill set for Codex plugin distribution.
- `codex-harness` gives every platform the same CLI entry point.

This project is inspired by
[`revfactory/harness`](https://github.com/revfactory/harness), adapted for Codex
primitives such as `SKILL.md`, repository-local skills, OpenAI agent metadata,
and optional runtime-supported delegation.

## What You Get

| Skill | Use it for |
| --- | --- |
| `codex-harness` | Design, audit, scaffold, validate, and evolve a project harness |
| `repo-review` | Code review, PR review, regression review, and repository audit |
| `feature-delivery` | Plan, implement, validate, and summarize feature work |
| `integration-qa` | Check cross-boundary mismatches after changes |
| `docs-maintenance` | Generate, update, and verify repository documentation |
| `release-readiness` | Run pre-release gates, changelog checks, and deployment risk review |

## Five-Minute Quickstart

Clone this repository and install the CLI in editable mode:

```bash
git clone https://github.com/kkmia417/HarnessforCodex.git
cd HarnessforCodex
python -m pip install -e .
```

Install all skills into another repository:

```bash
codex-harness init ../my-repo --all
```

By default this writes to the official repository skill location:

```text
../my-repo/.agents/skills/
```

For repositories that already use the older root `skills/` layout:

```bash
codex-harness init ../my-repo --all --skill-layout legacy
```

To write both layouts during migration:

```bash
codex-harness init ../my-repo --all --skill-layout both
```

Validate the target repository:

```bash
codex-harness validate ../my-repo
```

Sync skills into your user-level Codex skills directory:

```bash
codex-harness sync --all --force
```

The default sync destination is `~/.agents/skills`.

Create a new skill:

```bash
codex-harness new incident-review \
  --description "Review production incidents, timelines, mitigations, follow-up tasks, and regression risks. Use when asked for incident review, postmortem drafting, remediation planning, or operational risk analysis." \
  --resources references,scripts \
  --orchestrator
```

PowerShell users can still use the repository script:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

Generate a marketplace catalog when this plugin is mirrored under a marketplace
root such as `plugins/harnessforcodex`:

```bash
codex-harness marketplace .agents/plugins/marketplace.json --force
```

## Demo Path

Use this sequence for a 30-second recorded demo:

```bash
codex-harness init examples/sandbox --all --force
codex-harness validate examples/sandbox
codex-harness new api-contract-review --path examples/sandbox/.agents/skills \
  --description "Review API contract changes, generated clients, documentation, and consumer compatibility. Use when asked to check API changes, schema drift, client compatibility, or integration release risk."
codex-harness validate examples/sandbox
```

See [docs/demo-script.md](docs/demo-script.md) for the full recording script.

## Repository Layout

```text
.codex-plugin/
  plugin.json
docs/
  architecture.md
  cli-reference.md
  compatibility.md
  demo-script.md
  issue-roadmap.md
  plugin-packaging.md
examples/
  oss-maintainer-workflow/
  python-api/
  react-app/
scripts/
  sync_codex_skills.ps1
skills/
  codex-harness/
  docs-maintenance/
  feature-delivery/
  integration-qa/
  release-readiness/
  repo-review/
src/codex_harness/
  cli.py
tests/
  test_cli.py
```

## Validation

Run all local checks:

```bash
python -m unittest discover -s tests
python -m codex_harness.cli validate .
python skills/codex-harness/scripts/validate_codex_harness.py .
```

The GitHub Actions workflow runs these checks on every pull request.

## Documentation

- [Architecture](docs/architecture.md)
- [CLI reference](docs/cli-reference.md)
- [Compatibility](docs/compatibility.md)
- [Plugin packaging](docs/plugin-packaging.md)
- [Issue roadmap](docs/issue-roadmap.md)
- [Demo script](docs/demo-script.md)
- [Examples](examples/README.md)

## Distribution Status

This repository is currently `0.1.0`: usable as a source checkout, editable
Python install, repository skill installer, and local plugin manifest. The next
packaging milestones are documented in [docs/plugin-packaging.md](docs/plugin-packaging.md).

## Contributing

Contributions should keep skills small, explicit, and testable. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the review checklist and local validation
commands.

## License and Attribution

Harness for Codex is licensed under the Apache License 2.0. See [LICENSE](LICENSE).

Harness for Codex is inspired by
[`revfactory/harness`](https://github.com/revfactory/harness), which is also
licensed under Apache-2.0.

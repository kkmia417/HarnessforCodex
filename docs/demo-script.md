# Demo Script

Use this script to record a short demo for the README, release notes, or launch
posts.

## Goal

Show the viewer that Harness for Codex turns a plain repository into a reusable
Codex workflow system in less than a minute.

## Setup

```bash
python -m pip install -e .
rm -rf examples/sandbox
mkdir -p examples/sandbox
```

## Recording Beats

1. Show that `examples/sandbox` has no skills.
2. Run `codex-harness init examples/sandbox --all`.
3. Run `codex-harness validate examples/sandbox`.
4. Show `examples/sandbox/skills`.
5. Create a project-specific skill:

```bash
codex-harness new api-contract-review --path examples/sandbox/skills \
  --description "Review API contract changes, generated clients, documentation, and consumer compatibility. Use when asked to check API changes, schema drift, client compatibility, or integration release risk."
```

6. Validate again:

```bash
codex-harness validate examples/sandbox
```

7. End with a Codex prompt:

```text
Use $repo-review to review the current diff.
```

## Suggested Caption

Turn repository habits into reusable Codex skills: install, validate, and extend
a project harness from the terminal.

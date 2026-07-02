# CLI Reference

`codex-harness` installs, validates, scaffolds, and packages reusable Codex
skills.

## Commands

```bash
codex-harness validate [root]
codex-harness init [target] (--all | --skill NAME)
codex-harness sync (--all | --skill NAME)
codex-harness new NAME --description DESCRIPTION
codex-harness marketplace [output]
```

## `validate`

Validate a repository, skill directory, or skill collection.

```bash
codex-harness validate .
codex-harness validate ../my-repo
codex-harness validate skills/repo-review
```

The validator accepts repository skills in `.agents/skills`, the older root
`skills/` layout, direct child skill directories, or a single skill directory.

Options:

- `--warnings-as-errors`: fail when warnings are emitted.

## `init`

Install Harness for Codex skills into a target repository.

```bash
codex-harness init ../my-repo --all
codex-harness init ../my-repo --skill repo-review --skill release-readiness
```

By default, `init` writes to `.agents/skills`, which is the Codex repository
skill discovery location.

Options:

- `--all`: install every source skill.
- `--skill NAME`: install one skill; can be repeated.
- `--source-root PATH`: use a specific Harness for Codex checkout or skill source.
- `--skill-layout official`: write `.agents/skills` only.
- `--skill-layout legacy`: write root `skills/` only.
- `--skill-layout both`: write both layouts during migration.
- `--with-plugin`: copy `.codex-plugin` metadata.
- `--force`: replace existing destination skills.

## `sync`

Sync skills into the user-level Codex skills directory.

```bash
codex-harness sync --all --force
codex-harness sync --skill repo-review --destination ~/.agents/skills
```

The default destination is `~/.agents/skills`.

Options:

- `--all`: sync every source skill.
- `--skill NAME`: sync one skill; can be repeated.
- `--destination PATH`: override the user-level skill directory.
- `--source-root PATH`: use a specific Harness for Codex checkout or skill source.
- `--force`: replace existing destination skills.

## `new`

Create a repository-local skill skeleton.

```bash
codex-harness new incident-review \
  --description "Review production incidents, timelines, mitigations, follow-up tasks, and regression risks. Use when asked for incident review, postmortem drafting, remediation planning, or operational risk analysis."
```

Options:

- `--path PATH`: directory that contains skill folders; defaults to `skills`.
- `--description TEXT`: required frontmatter description and trigger text.
- `--display-name TEXT`: optional UI display name.
- `--short-description TEXT`: optional UI short description.
- `--resources references,scripts,assets`: create optional resource directories.
- `--orchestrator`: scaffold an orchestrator-style workflow.
- `--force`: overwrite existing generated files.

## `marketplace`

Write a Codex plugin marketplace catalog.

```bash
codex-harness marketplace .agents/plugins/marketplace.json --force
```

The default plugin entry points at `./plugins/harnessforcodex`. For a repo or
team marketplace, mirror or clone this plugin under that path relative to the
marketplace root.

Options:

- `--marketplace-name NAME`: catalog identifier; defaults to `harnessforcodex`.
- `--display-name TEXT`: catalog display name; defaults to `Harness for Codex`.
- `--plugin-name NAME`: plugin identifier; defaults to `harnessforcodex`.
- `--plugin-source PATH`: local plugin path; defaults to `./plugins/harnessforcodex`.
- `--category NAME`: plugin category; defaults to `Productivity`.
- `--force`: replace an existing catalog file.

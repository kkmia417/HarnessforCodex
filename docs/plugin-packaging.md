# Plugin Packaging

Harness for Codex already includes `.codex-plugin/plugin.json` so the skill set
can be packaged as a Codex plugin when the target distribution channel supports it.

## Current Manifest

The manifest declares:

- package name: `harnessforcodex`
- version: `0.1.0`
- skill source: `./skills/`
- category: `Productivity`
- capabilities: `Interactive`, `Write`
- default prompts for harness design, repo review, and release readiness

## Packaging Checklist

Before a tagged release:

1. Run `python -m codex_harness.cli validate .`.
2. Run `python skills/codex-harness/scripts/validate_codex_harness.py .`.
3. Verify every skill has `SKILL.md`, `agents/openai.yaml`, and referenced files.
4. Verify README quickstart commands against a clean checkout.
5. Update `.codex-plugin/plugin.json` and `pyproject.toml` to the same version.
6. Add release notes to `CHANGELOG.md`.
7. Create a signed tag.

## Versioning

Use semantic versioning:

- Patch: docs, examples, validation improvements, and compatible skill wording.
- Minor: new skills, new CLI commands, or new plugin metadata.
- Major: breaking changes to skill names, required file layout, or CLI behavior.

## Distribution Paths

Recommended order:

1. GitHub source checkout with `pip install -e .`.
2. GitHub release archive.
3. Python package distribution.
4. Codex plugin distribution when available for the target audience.

## Compatibility Notes

Codex plugin surfaces can evolve. Keep packaging docs grounded in tested behavior
and avoid claiming support for a distribution path until it has a release artifact
or installation test.

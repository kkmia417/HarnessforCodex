# Plugin Packaging

Harness for Codex already includes `.codex-plugin/plugin.json` so the skill set
can be packaged as a Codex plugin when the target distribution channel supports it.

## Current Manifest

The manifest declares:

- package name: `harnessforcodex`
- version: `0.1.0`
- skill source: `./skills/`
- repository: `https://github.com/kkmia417/HarnessforCodex`
- license: `Apache-2.0`
- category: `Productivity`
- capabilities: `Interactive`, `Write`
- default prompts for harness design, repo review, and release readiness

## Codex Layout Compatibility

Codex repository skills are installed to `.agents/skills` by default:

```bash
codex-harness init ../my-repo --all
```

Use `--skill-layout legacy` for repositories that still expect root `skills/`.
Use `--skill-layout both` during migration.

User-level sync defaults to `~/.agents/skills`:

```bash
codex-harness sync --all --force
```

The source checkout keeps packaged skills under `skills/` because
`.codex-plugin/plugin.json` points at `./skills/`.

Python distributions also include the same skill files under
`src/codex_harness/data/skills/`. `codex-harness init` and
`codex-harness sync` prefer an explicit `--source-root`, then
`CODEX_HARNESS_SOURCE`, then a nearby source checkout, and finally the bundled
package data.

## Marketplace Catalog

Generate a local marketplace catalog with:

```bash
codex-harness marketplace .agents/plugins/marketplace.json --force
```

The generated entry uses this installable shape:

```json
{
  "name": "harnessforcodex",
  "source": {
    "source": "local",
    "path": "./plugins/harnessforcodex"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

For a repo or team marketplace, mirror or clone this plugin under
`plugins/harnessforcodex` relative to the marketplace root before using the
catalog.

## Packaging Checklist

Before a tagged release:

1. Run `python -m codex_harness.cli validate .`.
2. Run `python skills/codex-harness/scripts/validate_codex_harness.py .`.
3. Run the `plugin-creator` `validate_plugin.py` helper when it is available locally.
4. Verify every skill has `SKILL.md`, `agents/openai.yaml`, and referenced files.
5. Verify README quickstart commands against a clean checkout.
6. Verify `codex-harness init <target> --all` writes `.agents/skills`.
7. Verify `codex-harness init <target> --all --skill-layout legacy` still writes `skills/`.
8. Update `.codex-plugin/plugin.json` and `pyproject.toml` to the same version.
9. Add release notes to `CHANGELOG.md`.
10. Create a signed tag.

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
4. Local or team Codex marketplace catalog.
5. Codex plugin distribution when available for the target audience.

## Compatibility Notes

Codex plugin surfaces can evolve. Keep packaging docs grounded in tested behavior
and avoid claiming support for a distribution path until it has a release artifact
or installation test.

See [Compatibility](compatibility.md) for the current support matrix.

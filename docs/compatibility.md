# Compatibility

This matrix describes what Harness for Codex supports today and what still
needs release or installation testing.

## Skill Locations

| Location | Status | Notes |
| --- | --- | --- |
| `.agents/skills/<name>/SKILL.md` | Supported | Default target for `codex-harness init`. This is the preferred repository skill layout. |
| `~/.agents/skills/<name>/SKILL.md` | Supported | Default target for `codex-harness sync`. |
| `skills/<name>/SKILL.md` | Supported | Source layout for this repository and legacy target via `--skill-layout legacy`. |
| Direct skill directory | Supported | `codex-harness validate skills/repo-review` validates one skill. |

## Codex Surfaces

| Surface | Status | Notes |
| --- | --- | --- |
| Codex CLI | Supported by local skills | Install repo skills with `codex-harness init` or user skills with `codex-harness sync`. |
| Codex IDE extension | Supported by local skills | Uses the same skill files after Codex discovers them. |
| Codex app | Supported by skill metadata | `agents/openai.yaml` supplies display metadata and default prompts. |
| Codex plugin manifest | Supported locally | `.codex-plugin/plugin.json` packages the repository skills. |
| Local or team marketplace | Scaffolded | Generate a catalog with `codex-harness marketplace`; mirror the plugin under `plugins/harnessforcodex` relative to the marketplace root. |
| Public plugin directory | Not released | Do not claim public distribution until a tested release path exists. |
| PyPI package | Not released | The current package is source-checkout and editable-install oriented. |

## Validation

Run:

```bash
python -m unittest discover -s tests
python -m codex_harness.cli validate .
python skills/codex-harness/scripts/validate_codex_harness.py .
```

When validating plugin metadata locally, also run the `plugin-creator`
`validate_plugin.py` helper if it is installed.

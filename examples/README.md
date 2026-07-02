# Examples

Each example is a small repository harness that can be validated with the same
CLI used for real projects.

```bash
codex-harness validate examples/python-api
codex-harness validate examples/react-app
codex-harness validate examples/oss-maintainer-workflow
```

## Included Examples

- `python-api`: API contract review for schema and client compatibility.
- `react-app`: UI change review for interaction, accessibility, and responsive behavior.
- `oss-maintainer-workflow`: issue triage and release preparation for open-source maintainers.

Use these as starting points for repository-specific skills rather than as
universal rules.

Each example includes a `scenarios/` note with a realistic prompt, the files or
boundaries to inspect, and the kind of result the skill should produce.

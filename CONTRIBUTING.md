# Contributing

Thanks for improving Harness for Codex. Keep changes small, testable, and tied
to a concrete repeated Codex workflow.

## Local Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
codex-harness validate .
python skills/codex-harness/scripts/validate_codex_harness.py .
```

## Skill Changes

When adding or changing a skill:

- Keep the skill name lowercase hyphen-case.
- Put trigger conditions in the `description` frontmatter.
- Keep long rules in `references/`.
- Keep deterministic actions in `scripts/`.
- Add or update `agents/openai.yaml`.
- Validate the root repository and any changed example.

## Review Standard

Pull requests should explain:

- what workflow changes
- which files changed
- which validation commands ran
- what residual risk remains

Avoid broad rewrites unless they remove concrete friction or support a documented
roadmap item.

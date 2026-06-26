# Issue Roadmap

Track missing capabilities against the upstream Harness idea and add them as small, reviewable issues.

## Initial Backlog

### Add release readiness skill

Create `skills/release-readiness/` for pre-release checks, validation gates, changelog readiness, and deployment risk review.

Acceptance:

- skill has `SKILL.md`, `agents/openai.yaml`, and focused references
- validation passes
- README practical skills table includes it

### Add documentation generation skill

Create `skills/docs-maintenance/` for README, API docs, command docs, and example verification.

Acceptance:

- docs workflow distinguishes generation from accuracy review
- references include command/example verification rules
- validation passes

### Add harness eval prompts

Add evaluation prompts and assertion examples for with-skill vs baseline testing.

Acceptance:

- evaluation prompts cover harness creation, review, feature delivery, and integration QA
- assertions are concrete and observable
- instructions avoid leaking expected answers

### Add CI validation

Add GitHub Actions workflow that runs the repository harness validator and per-skill quick validation where possible.

Acceptance:

- workflow runs on push and pull request
- validation command is documented
- failures identify the skill directory

### Add local install and sync script

Add a script that installs or updates selected repository skills into `~/.codex/skills`.

Acceptance:

- supports install of all skills or named skills
- refuses to delete unrelated local skills
- documents Windows PowerShell usage

### Add Codex plugin packaging

Evaluate and add Codex plugin packaging only if it gives a real distribution benefit over repository-local skills.

Acceptance:

- decision document explains package shape
- packaging metadata validates
- README explains install/update path

### Add Japanese README

Create `README_JA.md` for Japanese usage and contribution flow.

Acceptance:

- covers use, scaffold, validation, install, and issue-driven workflow
- links back to the English README

### Add license and attribution

Add repository license and upstream attribution.

Acceptance:

- license file exists
- README attribution is explicit
- upstream reference is preserved

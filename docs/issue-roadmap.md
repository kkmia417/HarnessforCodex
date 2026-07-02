# Issue Roadmap

This roadmap turns the repository from a useful skill pack into a public-facing
developer tool.

## Now

- Keep `codex-harness validate` passing for every skill.
- Keep README quickstart commands executable from a clean checkout.
- Add examples that show concrete repository workflows.
- Keep the plugin manifest aligned with the packaged skills.
- Keep `.agents/skills` as the default install target while preserving legacy
  `skills/` compatibility.

## Next

- Publish a release archive with checksums.
- Add a recorded GIF or video from `docs/demo-script.md`.
- Add package publishing automation after the first tagged release.
- Add a docs site or GitHub Pages homepage with the demo, quickstart, and
  example walkthroughs.

## Later

- Add template packs for common stacks such as Python APIs, React apps, monorepos,
  and open-source maintainer workflows.
- Add trigger regression tests that compare expected skill selection behavior.
- Add a public gallery of community skills.
- Add migration guides from ad hoc prompt files and Claude-oriented harnesses.

## Good First Issues

- Add runnable fixture files beside each example scenario.
- Add more validation for `agents/openai.yaml` shape.
- Add macOS/Linux shell examples beside PowerShell examples.
- Add a short troubleshooting page for common install errors.
- Add screenshots for the plugin directory and skill invocation flow.

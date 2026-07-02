# Release Blocker Triage

Use this scenario to test whether `$maintainer-triage` separates ordinary
support requests from issues that should block a release.

## Prompt

```text
Use $maintainer-triage to classify this issue and propose the next maintainer action.
```

## Simulated Issue

```text
Title: 2.4.0-rc.1 corrupts config when migrate is interrupted

After running `tool migrate` on Windows, pressing Ctrl+C midway leaves
settings.json truncated. Re-running migrate fails with JSON parse errors.
This did not happen on 2.3.5.
```

## Expected Triage

The skill should classify this as a release blocker:

- Risk: data loss or corrupted user configuration.
- Next action: request reproduction details, platform version, and backup state.
- Maintainer action: hold the release until migration writes are atomic or recoverable.
- Response: acknowledge impact without asking the reporter to keep retrying the destructive path.

# Security Policy

## Supported Versions

Security fixes target the latest released version and the `main` branch.

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub private
vulnerability reporting if it is enabled for the repository, or contact the
maintainers through the private channel listed in the repository profile.

Include:

- affected version or commit
- reproduction steps
- impact
- suggested mitigation, if known

## Scope

Security-sensitive areas include:

- scripts that copy or remove files
- command-line path handling
- generated skill content that could encourage unsafe shell usage
- plugin metadata that changes write or interactive capabilities

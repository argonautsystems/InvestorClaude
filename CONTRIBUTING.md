# Contributing to InvestorClaude

InvestorClaude is the Claude Code adapter for the InvestorClaw skill. It shares
contribution practices with the upstream InvestorClaw repo at
[gitlab.com/argonautsystems/InvestorClaw](https://gitlab.com/argonautsystems/InvestorClaw)
(see its [CONTRIBUTING.md](https://gitlab.com/argonautsystems/InvestorClaw/-/blob/main/CONTRIBUTING.md)
for the full guide).

## At minimum

- **License compatibility** — contributions must be compatible with the Apache
  2.0 terms in [LICENSE](LICENSE).
- **Lint + format** — run `uv run ruff check .` and `uv run ruff format` before
  submitting. CI rejects lint-dirty branches.
- **Conventional Commits** — use the
  [Conventional Commits](https://www.conventionalcommits.org/) spec for commit
  messages (e.g. `feat(commands):`, `fix(skill):`, `docs:`).
- **Tests pass** — `uv run pytest` should be green; if you add behavior, add
  coverage.
- **Don't push directly to main** — open a PR / MR for review.

## Reporting bugs and feature requests

- Bugs: open an issue with reproduction steps, version, and platform.
- Security-sensitive reports: see [SECURITY.md](SECURITY.md) — do not open a
  public issue.
- Feature requests: open an issue describing the use case before writing code.

## Commit author identity

Commit author email must match the contributor's public OSS identity. Any
employer-affiliated email is not appropriate for OSS contributions to this
project.

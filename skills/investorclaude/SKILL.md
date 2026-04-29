---
name: investorclaude
version: "2.6.0"
description: >
  Route Claude Code portfolio, holdings, bonds, market-news, optimization, and
  report questions to InvestorClaw v2.6.0. ic-engine pre-runs the deterministic
  pipeline, stores an HMAC-signed JSON envelope, and the narrator quotes
  verbatim from authoritative sources instead of fabricating.
allowed-tools: Bash(investorclaw ask *), Bash(investorclaw refresh), Bash(investorclaw session), Bash(investorclaw stonkmode), Bash(investorclaw check-updates), Read
metadata:
  shortcuts:
    - investorclaude
    - investorclaw
    - portfolio
    - holdings
    - bonds
    - performance
    - allocation
    - market news
---

# InvestorClaude v2.6.0

InvestorClaude is now a thin Claude Code adapter over the deterministic
ic-engine v2.5.1 surface.

## Interaction Model

Use one natural-language command for portfolio data:

```bash
investorclaw ask "<question>"
```

When a question arrives, ic-engine eagerly pre-runs the deterministic backend
pipeline, stores the result as an HMAC-signed JSON envelope, and passes the
envelope plus the user's question to a strict narrator. The narrator must quote
verbatim from authoritative sources in the envelope and must refuse to
fabricate missing facts.

The first prompt may take 30-60 seconds because the full deterministic pipeline
is building the signed envelope. Follow-up prompts should be faster because the
cache is reused unless the user refreshes.

## Command Selection

| User intent | Run |
|-------------|-----|
| Any portfolio, holdings, performance, bonds, news, optimization, target allocation, cash flow, peer comparison, lookup, or report question | `investorclaw ask "<question>"` |
| User explicitly wants fresh data, stale cache reset, or moved news/prices | `investorclaw refresh` |
| User asks about the current session | `investorclaw session` |
| User asks for narrated commentary mode | `investorclaw stonkmode` |
| User asks whether updates are available | `investorclaw check-updates` |

Do not route natural-language portfolio questions to legacy section commands
such as `investorclaw view`, `compute`, `bonds`, `market`, `target`,
`scenario`, `lookup`, or `eod-report`. Those v2.4 adapter routes are gone.

The Claude Code slash command surface is intentionally limited to
`/investorclaw:ask` and `/investorclaw:refresh`. Meta utilities are bash-only.

## Attachments

When the user attaches portfolio data, stage supported CSV, XLS, XLSX, PDF, or
image inputs to `~/portfolios/` when needed, then ask the original question via
`investorclaw ask "<question>"`. Report any setup or ingestion guidance exactly
as InvestorClaw returns it.

## Guardrails

- Never calculate portfolio metrics in Claude.
- Never fabricate market, ticker, bond, portfolio, optimization, or news data.
- Preserve quoted source passages, numbers, dates, timestamps, and freshness
  labels exactly.
- If the signed envelope lacks the requested fact, say that InvestorClaw did
  not provide it and quote the engine's refusal or limitation.
- Keep all responses educational; do not present investment advice or trading
  instructions.

## User-Facing Slash Commands

- `/investorclaw:ask "what's in my portfolio?"`
- `/investorclaw:refresh`

## Power-User Bash Utilities

- `investorclaw session`
- `investorclaw stonkmode`
- `investorclaw check-updates`

See [../../DISCLAIMER.md](../../DISCLAIMER.md).

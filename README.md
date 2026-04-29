# InvestorClaw for Claude Code

Portfolio analysis and market intelligence for Claude Code.

v2.6.0 | Apache 2.0 | Educational Use Only

InvestorClaude is the Claude Code adapter for the InvestorClaw / ic-engine
runtime. Claude Code is the primary platform for this package.

## Breaking Command Surface Change

v2.6.0 ships the deterministic ask model with the Claude Code slash command pool
collapsed to two commands. The 13 v2.4.x `portfolio-*` slash commands remain
removed, and earlier v2.5.0 meta slash commands are now bash-only utilities.

Portfolio data questions now go through one deterministic-first entry point:

```text
/investorclaw:ask "what's in my portfolio?"
```

Use `/investorclaw:refresh` when you want a cache-busting full pipeline re-run.

Power users can still run meta utilities directly from a shell:

```bash
investorclaw session
investorclaw stonkmode
investorclaw check-updates
```

## Other Platforms

- OpenClaw: See [InvestorClaw `openclaw/README.md`](https://gitlab.com/argonautsystems/InvestorClaw/-/blob/main/openclaw/README.md)
- Standalone CLI: See [InvestorClaw `README.md`](https://gitlab.com/argonautsystems/InvestorClaw/-/blob/main/README.md)

## Features

InvestorClaw analyzes multi-account portfolios with deterministic Python
computation. Claude presents the engine narrator's signed-envelope answer; it
does not guess financial metrics.

- Holdings snapshots for what you own and where you own it
- Performance metrics for returns, Sharpe ratio, drawdown, and allocation
- Bond analytics for yield-to-maturity, duration, credit quality, and ladders
- Analyst consensus and price targets on portfolio holdings
- Today's news on holdings and market-wide topics
- Portfolio synthesis, optimization, target allocation, drift, and scenarios
- Direct ingestion from CSV, XLS, XLSX, PDF, and broker screenshots
- EOD report generation for daily summaries
- Educational guardrails; no investment advice

## Quick Start

### Install In Claude Code

```text
/plugin marketplace add https://gitlab.com/argonautsystems/InvestorClaude.git
/plugin install investorclaw@investorclaude
```

This is the authoritative pre-store Claude Code install path. GitLab is the
public mirror used for installs and CI.

After official marketplace acceptance, use:

```text
/plugin install investorclaw@claude-plugins-official
```

After install, ask your first question:

```text
/investorclaw:ask "what's in my portfolio?"
```

You can also attach broker files and ask Claude to analyze your portfolio. No
manual dependency setup is needed. Claude's `investorclaude` skill invokes the
adapter workflow, pulls `ic-engine` and `clio`, stages supported files when
needed, and lets InvestorClaw return setup or ingestion guidance.

### Standalone Development

```bash
git clone https://gitlab.com/argonautsystems/InvestorClaude.git
cd InvestorClaude
python3 -m pip install -e .
investorclaw ask "what's in my portfolio?"
```

Then use InvestorClaw as a Python CLI through the `ic-engine` runtime.

## Prepare Your Portfolio

Export holdings from your broker. CSV offers the highest compatibility.

- Schwab: Accounts -> Positions -> Export CSV
- Fidelity: NetBenefits -> Investments -> Download CSV
- Vanguard: My Accounts -> Download Holdings
- UBS: Wealth Management -> Holdings -> Export

Also supported: XLS/XLSX, PDF broker statements, and screenshots of broker
positions pages. In Claude Code, attach files directly in chat; Claude stages
them automatically when needed and asks the original question through
InvestorClaw.

## Run Analysis

Ask in natural language:

```text
/investorclaw:ask "What's in my portfolio?"
/investorclaw:ask "How am I doing this year?"
/investorclaw:ask "Show me my bond exposure and yield-to-maturity."
/investorclaw:ask "Generate today's EOD report."
/investorclaw:ask "What is the current price of NVDA?"
```

Force a fresh pipeline run when news, prices, or portfolio files may have moved:

```text
/investorclaw:refresh
```

## Available Slash Commands (2 Total)

| Command | Args | Use for |
|---------|------|---------|
| `/investorclaw:ask` | natural-language question | Holdings, performance, bonds, news, optimization, target allocation, cash flow, peer comparison, lookup, reports |
| `/investorclaw:refresh` | none | Cache-busting full pipeline re-run |

## Power-User Bash Utilities

These utilities are intentionally not exposed as slash commands, so they do not
compete with `/investorclaw:ask` when Claude Code routes portfolio prompts.

| Bash command | Use for |
|--------------|---------|
| `investorclaw session` | Show or manage the current portfolio analysis session |
| `investorclaw stonkmode` | Narrated commentary mode |
| `investorclaw check-updates` | Check for ic-engine and InvestorClaude updates |

## How It Works

1. You upload a portfolio by CSV, Excel, PDF, screenshot, or setup.
2. Claude stages files locally when needed and asks through `investorclaw ask`.
3. ic-engine pre-runs the deterministic backend pipeline for the question.
4. The result is stored as an HMAC-signed JSON envelope.
5. A strict narrator receives only the signed envelope and question, quotes
   verbatim from authoritative sources, and refuses to fabricate missing facts.

The first prompt can take 30-60 seconds because the full deterministic pipeline
is building the signed envelope. Subsequent prompts are cache-amortized unless
you run `/investorclaw:refresh`.

## Data Privacy

Your data stays on your machine by default.

- Raw broker files stay local in `~/portfolios/`
- Account numbers and SSNs are scrubbed on import
- Only computed summaries and the signed envelope are sent to the narrator
- InvestorClaw never executes trades
- All analysis is educational and not investment advice

See [DISCLAIMER.md](DISCLAIMER.md) for guardrails and educational-use constraints.

## Documentation

- [DISCOVERY_HIERARCHY.md](DISCOVERY_HIERARCHY.md): Claude Code discovery and deterministic interaction model
- [INSTALL_FLOW.md](INSTALL_FLOW.md): Marketplace install and setup flow
- [CHANGELOG.md](CHANGELOG.md): v2.6.0 release notes
- [DISCLAIMER.md](DISCLAIMER.md): Educational-use disclaimer and guardrails

## Troubleshooting

### "Command not found: investorclaw"

Reinstall the plugin or run the bundled setup helper from the installed checkout:

```bash
setup-orchestrator
```

### "No portfolio found"

Attach a CSV/XLS/XLSX/PDF/screenshot in chat and ask:

```text
/investorclaw:ask "what's in my portfolio?"
```

### "API key errors"

API keys are optional. InvestorClaw falls back to free data paths where
available. Ask `/investorclaw:ask "help me configure data providers"` for
engine-guided setup.

### Performance Is Slow

The first v2.6 prompt may take 30-60 seconds while ic-engine builds the signed
deterministic envelope. Later prompts reuse cached pipeline output unless you
refresh. Large portfolios with 500+ holdings take longer.

## Status

Production Ready | Apache 2.0

InvestorClaude v2.6.0 for Claude Code. Portfolio analysis. Educational only. No
investment advice.

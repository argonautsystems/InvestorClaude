# InvestorClaw Claude Code Install Flow

Complete walkthrough from "I want to analyze my portfolio" to production
analysis in Claude Code.

## Level 0: Auto-Discovery

User mentions portfolio-related keywords or attaches portfolio data:

- "I want to set up my portfolio"
- "Can you help me install InvestorClaw?"
- "I have CSV exports from my broker"
- "What's in my portfolio?"

Claude Code's `investorclaude` skill handles setup, file staging, and the v2.6.x
natural-language interaction model. It does not choose among per-section
portfolio commands anymore.

## Level 1: Automated Setup

Claude handles setup without manual user steps.

### Step 1: Plugin Setup Helper

Claude runs the setup helper bundled with the installed plugin when needed:

```bash
setup-orchestrator
```

This installs the InvestorClaude checkout, pulls `ic-engine` and `clio`, verifies
the console script, discovers portfolio files, and runs setup.

### Step 2: Portfolio Configuration

The setup helper may run the engine setup flow:

```bash
investorclaw setup
```

No API keys are required to start. InvestorClaw uses free data paths
(yfinance) where available; the engine prompts for optional provider
keys later via `investorclaw llm-config -i` (interactive) when the user
wants narrative synthesis or richer market data.

For the v4.x containerized runtime, keys can also be set from the dashboard
at `http://localhost:18092/` or via REST/MCP on `http://localhost:18090/`.
Allowed provider keys are `TOGETHER_API_KEY`, `FINNHUB_KEY`, `NEWSAPI_KEY`,
`ALPHA_VANTAGE_KEY`, `MASSIVE_API_KEY`, `MARKETAUX_API_KEY`, `FRED_API_KEY`,
and `OPENAI_API_KEY`.

### What the first-install experience asks of the user

Right after `bin/install-investorclaw` finishes, here is what InvestorClaude
asks for (in order):

1. **A portfolio file.** The setup wizard scans `$INVESTORCLAW_PORTFOLIO_DIR`
   (default `~/portfolios/`), then `~/Downloads/`. If neither directory has a
   broker file, the engine returns a clear *"No portfolio file found"* message
   and you can either drop a CSV/XLS/XLSX/PDF/screenshot into `~/portfolios/`
   or attach one in Claude chat — the plugin stages it for you.

2. **An LLM provider key for narrative synthesis (optional).** The engine
   answers questions key-less in degraded mode: numbers are correct (the
   deterministic Python pipeline produces them) but the narrator falls back
   to a stub summary instead of a real prose answer. To enable proper
   narratives, configure a Together AI key:

   ```bash
   investorclaw llm-config -i      # interactive prompts for provider + key
   # Or directly:
   echo 'TOGETHER_API_KEY=tgp_v1_...' >> ~/.investorclaw/.env
   ```

3. **Optional: data-provider keys** for richer or faster results on
   larger portfolios (see *Recommended API keys by portfolio size*
   below).

### Recommended API keys by portfolio size

| Size | Required | Recommended | Why |
|---|---|---|---|
| **≤ 50 symbols** | `TOGETHER_API_KEY` (narrative) | — | yfinance handles quotes/history at this scale |
| **50–200 symbols** | `TOGETHER_API_KEY` | `FINNHUB_KEY` (free 60/min) + `NEWSAPI_KEY` (free 100/day) | Real-time quotes + analyst + per-symbol news without yfinance throttle |
| **200+ symbols** | `TOGETHER_API_KEY` + `MASSIVE_API_KEY` (Polygon, paid) | `FINNHUB_KEY` + `MARKETAUX_API_KEY` (free 100/day) + `FRED_API_KEY` (free, registration) + `ALPHA_VANTAGE_KEY` (free 25/day) | Yahoo's anonymous endpoint rate-limits globally on 200+ symbols; Polygon is required, the rest fill analyst + news + yields |

Sign-up links (free tiers exist for everything except Polygon):

| Provider | URL | Free-tier limit |
|---|---|---|
| Together AI | https://api.together.ai/settings/api-keys | $1 free credits |
| Finnhub | https://finnhub.io/register | 60 calls/min |
| Polygon (Massive) | https://polygon.io/dashboard/api-keys | paid only |
| MarketAux | https://www.marketaux.com/account/dashboard | 100 calls/day |
| NewsAPI | https://newsapi.org/register | 100 calls/day |
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html | unlimited (registration only) |
| Alpha Vantage | https://www.alphavantage.co/support/#api-key | 25 calls/day |

`TOGETHER_API_KEY` is the only one that meaningfully changes output
quality. Everything else is for scale or richness on larger portfolios.

### Step 3: Portfolio Upload

The user exports holdings from brokers:

- Schwab: Accounts -> Positions -> Export CSV
- Fidelity: NetBenefits -> Investments -> Download CSV
- Vanguard: My Accounts -> Download Holdings
- UBS: Wealth Management -> Holdings -> Export

Supported inputs: CSV, XLS, XLSX, PDF, JSON, OFX, QFX, and screenshots. In Claude Code, the user
attaches files directly to chat. Claude stages them to `~/portfolios/` when
needed and continues to the original analysis question.

With the v4.x web portal, the Settings tab also provides a multipart upload form
at `http://localhost:18092/` for CSV, XLSX, PDF, JSON, OFX, and QFX portfolio
files.

### Step 4: Verify Installation

Claude verifies setup with the v2.6 entry point:

```bash
investorclaw ask "what's in my portfolio?"
```

If the engine returns holdings or clear setup guidance, the adapter is working.

## Level 2: Deterministic Interaction

Natural-language query example:

```text
User: "What do I own?"
Claude: investorclaude skill uses the unified v2.6 entry point
Claude runs: investorclaw ask "What do I own?"
ic-engine: pre-runs the deterministic pipeline and signs the JSON envelope
Narrator: quotes verbatim from the envelope and refuses to fabricate
```

Slash-command direct invocation:

```text
/investorclaw:ask "what do I own?"
/investorclaw:ask "show my bonds"
/investorclaw:ask "how am I doing?"
/investorclaw:refresh
```

The first prompt usually costs 30-60 seconds because the full deterministic
pipeline is building the signed envelope. Subsequent prompts are
cache-amortized unless the user refreshes.

Power-user bash utilities remain available outside the slash command pool:

```bash
investorclaw session
investorclaw stonkmode
investorclaw check-updates
```

## Level 3: Ongoing Usage

### Natural Language

```text
User: "How am I doing this year?"
Claude runs: investorclaw ask "How am I doing this year?"
```

### Bonds

```text
User: "Show me my bond exposure and yield-to-maturity."
Claude runs: investorclaw ask "Show me my bond exposure and yield-to-maturity."
```

### Advisor Meeting Prep

```text
User: "I'm meeting with my financial advisor. Prepare a full analysis."
Claude runs: investorclaw ask "I'm meeting with my financial advisor. Prepare a full analysis."
```

### EOD Report

```text
User: "Generate today's EOD report."
Claude runs: investorclaw ask "Generate today's EOD report."
```

### Fresh Data

```text
User: "Prices moved. Refresh before answering."
Claude runs: investorclaw refresh
Claude runs: investorclaw ask "Prices moved. Refresh before answering."
```

## Installation Commands

Claude Code users install through the marketplace flow:

```text
/plugin marketplace add https://gitlab.com/argonautsystems/InvestorClaude.git
/plugin install investorclaw@investorclaude
```

This is the current Claude Code path while the Anthropic marketplace submission
is pending. For OpenClaw / ZeroClaw / Hermes users, install through ClawHub:

```bash
clawhub install perlowja/investorclaw
```

After official Anthropic marketplace acceptance:

```text
/plugin install investorclaw@claude-plugins-official
```

For standalone adapter development:

```bash
git clone https://gitlab.com/argonautsystems/InvestorClaude.git
cd InvestorClaude
python3 -m pip install -e .
investorclaw ask "what's in my portfolio?"
```

## Portfolio Directory Configuration

InvestorClaw auto-discovers portfolio files from:

1. `$INVESTORCLAW_PORTFOLIO_DIR`
2. `~/portfolios/`
3. `~/Downloads/`

Users can override with:

```bash
export INVESTORCLAW_PORTFOLIO_DIR=/custom/path
```

## What Gets Sent To Claude

Stays local:

- Raw broker CSV/XLS/PDF files
- Account numbers
- Full position details
- Python computation internals

Sent to the narrator:

- The user's question
- The HMAC-signed JSON envelope produced by ic-engine
- Computed metrics and authoritative source excerpts needed for presentation

## v4.x Dashboard

The containerized InvestorClaw runtime exposes the MCP/agent server on
`http://localhost:18090/` and the dashboard on `http://localhost:18092/`. Both
ports use the same engine, portfolio data, response store, and provider-key
state.

Dashboard tabs: Overview · Holdings · Performance · WhatChanged · Scenarios ·
Bonds · Optimize · Cashflow · Peer · Analyst · News · Markets · Lookup ·
Synthesis · Reports · Settings · About. The Overview Regenerate button runs
setup, refresh, and the 12 section analyzers as a background sweep.

## Troubleshooting

### Setup Fails

Run:

```bash
setup-orchestrator
```

If dependency installation fails, verify Python/pip and network access to
`gitlab.com`, then rerun the setup helper.

### No Portfolio Files Found

Attach a CSV/XLS/XLSX/PDF/image to chat and ask:

```text
/investorclaw:ask "what's in my portfolio?"
```

### Portfolio Path Confusion

```bash
export INVESTORCLAW_PORTFOLIO_DIR=~/Downloads
investorclaw ask "what's in my portfolio?"
```

### Setup Already Complete, But No Data

Clear the setup marker and rerun setup through the engine, then ask again:

```bash
rm ~/.investorclaw/.setup_complete
investorclaw config --section=setup
investorclaw ask "what's in my portfolio?"
```

## Next Steps

- [DISCOVERY_HIERARCHY.md](DISCOVERY_HIERARCHY.md) - How Claude discovers and uses the v2.6.x deterministic entry point
- [README.md](README.md) - Quick reference
- [skills/investorclaude/SKILL.md](skills/investorclaude/SKILL.md) - v2.6.x interaction skill

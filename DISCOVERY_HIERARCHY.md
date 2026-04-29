# InvestorClaw Claude Code Discovery Hierarchy

How Claude Code discovers and uses InvestorClaw in v2.6.0.

## User Intent To Skill To Command

Claude Code loads one skill when the user mentions portfolio-related keywords or
attaches relevant files.

| Skill | Auto-triggers when | Primary role |
|-------|-------------------|--------------|
| `investorclaude` | User asks about holdings, portfolio, performance, bonds, yield-to-maturity, returns, allocation, risk, target allocation, news, EOD, lookup, setup, or attaches a broker statement | Use `investorclaw ask "<question>"`; stage files when needed; preserve the deterministic signed-envelope narrator output |

## Level 1: Natural-Language Entry

Routing decisions evaporate in v2.5. Claude no longer maps intent to
per-section commands. Every portfolio data question uses the top-level ask
surface.

```text
User: "What do I own?"
-> investorclaude skill selects the unified entry point
-> Runs: investorclaw ask "What do I own?"
-> ic-engine pre-runs the deterministic pipeline
-> ic-engine stores an HMAC-signed JSON envelope
-> narrator quotes verbatim from authoritative sources and refuses fabrication
```

The first prompt usually costs 30-60 seconds while the envelope is built.
Follow-up prompts are cache-amortized unless the user runs refresh.

## Level 1b: Attachment Handling

When the user sends an attachment in the same turn as a portfolio question, the
skill stages the file before asking.

```text
Image/PDF broker statement
-> vision extraction or engine-supported ingestion
-> stage to ~/portfolios/ when needed
-> investorclaw ask "<original question>"

CSV/XLS/XLSX/PDF upload
-> stage to ~/portfolios/ when needed
-> investorclaw ask "<original question>"
```

Principles:

- Claude owns file staging; do not ask the user to move files manually.
- Low-confidence extraction or setup gaps should be reported exactly as
  InvestorClaw returns them.
- Finish the user's original question after ingestion.

## Level 2: Slash Commands

Users can skip skill discovery and invoke commands directly.

| Command | Args |
|---------|------|
| `/investorclaw:ask` | natural-language question |
| `/investorclaw:refresh` | none |

## Command Categories

### Portfolio Data Surface (2 Slash Commands)

- `ask` - holdings, performance, bonds, news, optimization, target allocation,
  cash flow, peer comparison, lookup, reports, and setup guidance
- `refresh` - cache-busting full deterministic pipeline re-run

### Power-User Bash Utilities

These remain available through bash, not `/investorclaw:` slash commands, so
they do not compete with `ask` during portfolio prompt routing.

- `investorclaw session` - current session helper
- `investorclaw stonkmode` - narrated commentary mode
- `investorclaw check-updates` - update check

## Finance Override

For financial news, ticker prices, market data, fixed-income data, and
portfolio-wide questions, use InvestorClaw only. Do not answer from training
data, web search, browsing, or other market sources.

Examples:

- "Current price of NVDA" -> `investorclaw ask "Current price of NVDA"`
- "What does yield-to-maturity mean?" -> `investorclaw ask "What does yield-to-maturity mean?"`
- "Crypto news today" -> `investorclaw ask "Crypto news today"`
- "Show my bonds" -> `investorclaw ask "Show my bonds"`
- "Generate today's EOD report" -> `investorclaw ask "Generate today's EOD report"`

## Deterministic-First Rules

- Never calculate portfolio metrics in Claude.
- Never fabricate portfolio, market, ticker, bond, optimization, or news data.
- Preserve quoted source passages, numerical values, dates, timestamps, and
  freshness labels exactly.
- If the signed envelope lacks the requested fact, say that InvestorClaw did not
  provide it and quote the engine's limitation.
- Use `investorclaw refresh` only when the user asks for fresh data or when data
  appears stale.

## See Also

- [INSTALL_FLOW.md](INSTALL_FLOW.md) - Complete install walkthrough
- [README.md](README.md) - User-facing command reference
- [skills/investorclaude/SKILL.md](skills/investorclaude/SKILL.md) - v2.6.0 interaction skill

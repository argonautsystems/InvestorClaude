# Privacy Policy

**Effective:** 2026-04-29
**Project:** InvestorClaude — Claude Code plugin for InvestorClaw portfolio analysis
**Maintainer contact:** Jason Perlow &lt;jperlow@gmail.com&gt;

## Summary

InvestorClaude is an open-source (Apache 2.0) Claude Code plugin that runs on
the user's own machine. The maintainer collects no data. The plugin itself
collects no data. Portfolio files stay on the user's local filesystem.
Computed summaries leave the local machine only when the user prompts
Claude Code, and even then only travel to the third-party services the user
explicitly configures (the language model and any market-data API keys).

This policy explains exactly which data leaves the user's machine, where it
goes, and what the user can do to constrain it.

## Data the maintainer collects

**None.** InvestorClaude has no telemetry, no analytics, no phone-home, and
no central server. The maintainer does not see plugin usage, prompts,
portfolio data, or output. There is no account creation; there is no
operator-controlled service.

## Local data on the user's machine

- **Raw broker files** (CSV / XLS / XLSX / PDF / screenshots) stay in the
  user's local portfolio directory (defaults to `~/portfolios/`). They are
  never uploaded by InvestorClaude itself.
- **Account numbers and Social Security numbers** are scrubbed at import
  time before any computed summary is constructed. Scrubbed values are
  replaced with redaction markers; the originals are not retained outside
  the user's local raw files.
- **Computed summaries and signed JSON envelopes** are written to
  `~/portfolio_reports/` (or `INVESTOR_CLAW_REPORTS_DIR` if set) for
  reproducibility and audit. These remain local.
- **Cache** of recent pipeline runs lives under the user's config directory
  to avoid re-fetching unchanged data; cache contents are local.

## Data flows that DO leave the user's machine

When the user asks a portfolio question, the deterministic pipeline runs
locally and produces a signed JSON envelope. That envelope and the user's
question are passed to the configured language model for natural-language
narration. Specifically:

### 1. Narrative language model (always involved)

Claude Code is the primary host. When run inside Claude Code, the user's
prompt and the signed envelope are sent to Anthropic's Claude API per
Claude Code's standard flow. Anthropic's privacy policy applies to that
traffic: https://www.anthropic.com/legal/privacy

If the user runs InvestorClaw outside Claude Code (OpenClaw, ZeroClaw,
Hermes Agent, or the standalone CLI), narration may be routed to one of
the user's configured cloud providers (Together AI, xAI, OpenAI, Google AI
Studio, NVIDIA NIM, Groq, Perplexity) or to a local model server (Ollama,
llama-server, LMStudio, vLLM). The user controls which provider via
environment variables; the maintainer has no visibility into provider
selection.

### 2. Optional consultative model (only if enabled)

If the user enables `INVESTORCLAW_CONSULTATION_ENABLED=true`, heavier
synthesis prompts are sent to the configured consult endpoint. The
endpoint URL determines whether this is local (e.g. a local llama-server
on the user's own GPU) or cloud (e.g. Together AI, Google AI Studio). The
default is local. No consult traffic happens unless the user explicitly
enables it.

### 3. Market-data providers (only if API keys are configured)

InvestorClaw uses `yfinance` by default, which is free and unauthenticated.
If the user supplies API keys for any of the following, request traffic
flows to those providers:

| Provider | When used | Privacy policy |
|---|---|---|
| Finnhub | Real-time quotes, analyst ratings | https://finnhub.io/policies/privacy |
| NewsAPI | News headlines correlated to holdings | https://newsapi.org/privacy |
| Alpha Vantage | Supplemental price data | https://www.alphavantage.co/privacy/ |
| Polygon (via Massive) | Market data | https://polygon.io/privacy |
| FRED (St. Louis Fed) | Treasury / TIPS benchmarks | https://www.stlouisfed.org/privacy-notice-and-policy |

If the user does not configure these keys, none of these providers receive
any traffic. The plugin falls back to free `yfinance` queries.

### 4. Email delivery (only if requested)

The end-of-day report can be emailed to a recipient. Email transport uses
the user's locally-configured SMTP server. The maintainer does not operate
an email service.

## What the third parties see

The maintainer cannot guarantee what each third party retains, but
typically:

- The narrative LLM provider sees the user's natural-language question and
  the signed JSON envelope (which contains computed portfolio summaries —
  ticker symbols, asset class breakdowns, performance metrics — but
  account numbers and SSNs are scrubbed).
- Market-data providers see the ticker symbols the user is asking about
  and standard request metadata (IP, user-agent, timestamp).
- News providers see the holdings tickers and date ranges queried.

The user should consult each provider's policy linked above to understand
their retention and use practices.

## User-controlled redaction

The user can constrain data flows by:

1. Running entirely on a local LLM (Ollama / llama-server / LMStudio / vLLM)
   so no prompt or envelope leaves the local network.
2. Not configuring any market-data API keys (forces yfinance fallback).
3. Keeping `INVESTORCLAW_CONSULTATION_ENABLED=false` (skips the consult
   pass).
4. Reviewing the signed JSON envelope under `~/portfolio_reports/` before
   running each ask — what's in the envelope is exactly what the LLM sees.
5. Never typing account numbers, SSNs, or other personal identifiers into
   the prompt itself. The plugin only sees prompt text the user authors.

## Children's privacy

InvestorClaude is intended for adult investors. The maintainer does not
knowingly process data from children under 13.

## Trades, orders, money movement

InvestorClaude does not execute trades, place orders, move money, or
authenticate to any brokerage. It is a read-only educational analysis tool.

## Vulnerability and data-incident reporting

Suspected privacy or security issues should be emailed privately to
&lt;jperlow@gmail.com&gt;. See `SECURITY.md` for vulnerability-disclosure
expectations.

## Changes to this policy

This policy may be updated alongside plugin releases. Material changes
will be noted in `CHANGELOG.md` under the corresponding version entry.
The current effective date appears at the top of this document.

## Contact

Privacy questions: &lt;jperlow@gmail.com&gt;

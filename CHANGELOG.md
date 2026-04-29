# Changelog

## v2.6.2 - Fix install-investorclaw to use uv instead of system pip

`bin/install-investorclaw` was calling `python3 -m pip install --user -e .`
to materialize the InvestorClaw CLI + its `ic-engine` / `clio` git+ deps.
On PEP 668-protected distros (Debian 12+, Ubuntu 23.04+, Raspberry Pi OS)
that fails with `error: externally-managed-environment` and the v2.6.1
auto-bootstrap dies before producing a usable `investorclaw` on `$PATH`.

### What Changed

- `bin/install-investorclaw`: replaced the `pip --user -e` invocation with
  `UV_PROJECT_ENVIRONMENT=$HOME/.cache/investorclaw/.venv uv sync --python 3.12`,
  matching the openclaw/zeroclaw/hermes per-runtime install convention.
  The script then symlinks `$VENV_DIR/bin/investorclaw` to
  `$HOME/.local/bin/investorclaw` exactly as `openclaw/install.sh` does.
- Python 3.12 pin: numpy 1.26.4 (transitive dep through ic-engine) has no
  3.13 wheels and falls back to a source build that needs gcc/cc, which
  many Pi/cloud containers don't ship. Pinning 3.12 lands a wheel directly.

### Why It Matters

- v2.6.1 fixes cold-install UX on Linux distros without PEP 668 (older
  Ubuntu, NixOS, Arch w/o `--break-system-packages`), but breaks fresh
  installs on Debian 12 + Pi OS. v2.6.2 closes that gap.
- The fix is the same install pattern documented in CLAUDE.md gotchas:
  *"InvestorClaw/Claude need uv, not system python3"*. v2.6.0/v2.6.1
  violated that rule in a script that's only exercised on first install.

### No Functional Changes

- `commands/ask.md`, `commands/refresh.md`: unchanged (still call
  `${CLAUDE_PLUGIN_ROOT}/bin/install-investorclaw` on first run).
- ic-engine pin: still `v2.5.1`. clio pin: still `v0.1.0`.
- Marketplace submission v2.6.0 SHA `3fd912e2` is unaffected — v2.6.2 is
  an additive tag.

## v2.6.1 - Auto-Bootstrap on First Slash Command

The `/investorclaw:ask` and `/investorclaw:refresh` slash commands now
auto-bootstrap `uv` and the `investorclaw` CLI + `ic-engine` on first use,
matching the per-runtime install pattern used by `openclaw`, `zeroclaw`, and
`hermes`. The plugin no longer assumes the user has already run
`bin/install-investorclaw` manually before their first prompt.

### What Changed

- `commands/ask.md`: prepended a `command -v investorclaw` guard that runs
  `${CLAUDE_PLUGIN_ROOT}/bin/install-investorclaw` if the CLI is missing,
  then exports `$HOME/.local/bin` onto `PATH` for the freshly-installed
  `uv` + `investorclaw` shims.
- `commands/refresh.md`: same auto-bootstrap guard.
- `allowed-tools` widened from `Bash(investorclaw ...)` to `Bash(*)` because
  the bootstrap shells out to `bash`, `curl`, and `uv` before the
  `investorclaw` binary exists.

### Rationale

v2.6.0 documented the install path in `INSTALL_FLOW.md` and the slash command
preambles, but users who installed the plugin from the marketplace and ran
`/investorclaw:ask` immediately got "command not found" — they had to read the
docs and run `bin/install-investorclaw` manually first. The Claw-family
runtimes (openclaw/zeroclaw/hermes) all auto-bootstrap on first use; this
brings InvestorClaude in line.

### No Functional Changes

- ic-engine pin: still `v2.5.1`.
- clio pin: still `v0.1.0`.
- Slash-command surface: still `ask` + `refresh`.
- Marketplace submission: pinned to v2.6.0 SHA `3fd912e2`. v2.6.1 is an
  additive tag — it does not invalidate the pending submission.

## v2.6.0 - Anthropic Marketplace Submission

InvestorClaude is now a self-contained Claude Code plugin published as a
marketplace at the repo root (`marketplace.json` with `source: "./"`).
Includes `PRIVACY.md` for marketplace requirements, scrubbed history (no
internal hostnames, no shared sudo passwords), and a v2.5.1 → v2.6.0 tag
rotation across the three publication remotes (argonas, gitlab, github).
Submitted to Anthropic at SHA `3fd912e218cefb58935184f5275e314106bb5ea9`.

## v2.5.1 - Two-Command Slash Surface

InvestorClaude keeps the ic-engine v2.5.0 runtime surface but collapses the
Claude Code slash command pool to two commands:

- `/investorclaw:ask "<question>"`
- `/investorclaw:refresh`

### Rationale

The v2.5.0 routing acceptance run scored 24/30 = 80%. Failure analysis showed
that the meta commands competed with `ask` for portfolio prompts because their
slash command descriptions overlapped with natural-language portfolio queries.

### Breaking Change

The following slash commands are removed from the `/investorclaw:` namespace:

- `/investorclaw:session`
- `/investorclaw:stonkmode`
- `/investorclaw:check-updates`

They remain available as bash-only utilities:

```bash
investorclaw session
investorclaw stonkmode
investorclaw check-updates
```

### Expected Outcome

With only `ask` and `refresh` in the slash command pool, v2.5.1 is expected to
hit 30/30 Class B routing on Claude Code by removing the meta-command routing
competition observed in v2.5.0.

## v2.5.0 - Deterministic Ask Surface

InvestorClaude now targets ic-engine v2.5.0 and its new top-level CLI:

```bash
investorclaw ask "<question>" [--no-refresh]
```

ic-engine eagerly pre-runs the deterministic backend pipeline when a question
arrives, stores the result as an HMAC-signed JSON envelope, and passes the
envelope plus the question to a strict narrator. The narrator quotes verbatim
from authoritative sources and refuses to fabricate.

The first prompt usually costs 30-60 seconds while the deterministic envelope is
built. Subsequent prompts are cache-amortized unless the user forces a refresh.

### Breaking Change

The 13 v2.4.x `portfolio-*` slash commands are removed. Portfolio data
questions now use:

- `/investorclaw:ask "<question>"`
- `/investorclaw:refresh`

The retained meta commands were renamed to drop the `portfolio-` prefix in
v2.5.0, then moved out of the slash command pool in v2.5.1:

- `investorclaw session`
- `investorclaw stonkmode`
- `investorclaw check-updates`

There are no compatibility aliases.

### Migration Guide

| v2.4.x command | v2.5.0 command |
|----------------|----------------|
| `/investorclaw:portfolio-view holdings` → | `/investorclaw:ask "what's in my portfolio?"` |
| `/investorclaw:portfolio-view performance` → | `/investorclaw:ask "how am I doing?"` |
| `/investorclaw:portfolio-view analyst` → | `/investorclaw:ask "what do analysts think about my holdings?"` |
| `/investorclaw:portfolio-view news` → | `/investorclaw:ask "what news matters for my holdings today?"` |
| `/investorclaw:portfolio-compute synthesize` → | `/investorclaw:ask "give me the full portfolio analysis"` |
| `/investorclaw:portfolio-compute optimize-sharpe` → | `/investorclaw:ask "optimize my allocation for Sharpe ratio"` |
| `/investorclaw:portfolio-compute optimize-minvol` → | `/investorclaw:ask "optimize my allocation for minimum volatility"` |
| `/investorclaw:portfolio-compute optimize-blacklitterman` → | `/investorclaw:ask "run a Black-Litterman optimization"` |
| `/investorclaw:portfolio-compute cashflow` → | `/investorclaw:ask "project my dividend and coupon cash flow"` |
| `/investorclaw:portfolio-compute peer` → | `/investorclaw:ask "compare my portfolio to peers or VTI"` |
| `/investorclaw:portfolio-compute whatchanged` → | `/investorclaw:ask "what changed since the last run?"` |
| `/investorclaw:portfolio-target allocation` → | `/investorclaw:ask "what is my target allocation?"` |
| `/investorclaw:portfolio-target drift` → | `/investorclaw:ask "am I drifting from my target allocation?"` |
| `/investorclaw:portfolio-scenario rebalance` → | `/investorclaw:ask "should I rebalance?"` |
| `/investorclaw:portfolio-scenario stress` → | `/investorclaw:ask "run a stress test"` |
| `/investorclaw:portfolio-scenario tax-aware` → | `/investorclaw:ask "rebalance with tax impact"` |
| `/investorclaw:portfolio-market news general` → | `/investorclaw:ask "what market news matters today?"` |
| `/investorclaw:portfolio-market news forex` → | `/investorclaw:ask "what forex news matters today?"` |
| `/investorclaw:portfolio-market news crypto` → | `/investorclaw:ask "what crypto news matters today?"` |
| `/investorclaw:portfolio-market news merger` → | `/investorclaw:ask "what merger news matters today?"` |
| `/investorclaw:portfolio-market concept` → | `/investorclaw:ask "explain the market concept I asked about"` |
| `/investorclaw:portfolio-market market` → | `/investorclaw:ask "what is the current market price or index level?"` |
| `/investorclaw:portfolio-bonds analysis` → | `/investorclaw:ask "show my bonds"` |
| `/investorclaw:portfolio-bonds strategy` → | `/investorclaw:ask "bond strategy?"` |
| `/investorclaw:portfolio-config setup` → | `/investorclaw:ask "help me set up my portfolio"` |
| `/investorclaw:portfolio-config identity` → | `/investorclaw:ask "show or update my InvestorClaw identity profile"` |
| `/investorclaw:portfolio-config guardrails` → | `/investorclaw:ask "what guardrails are in place?"` |
| `/investorclaw:portfolio-config llm` → | `/investorclaw:ask "help me configure verification providers"` |
| `/investorclaw:portfolio-config ollama` → | `/investorclaw:ask "help me configure Ollama"` |
| `/investorclaw:portfolio-report` → | `/investorclaw:ask "generate today's EOD report"` |
| `/investorclaw:portfolio-lookup AAPL` → | `/investorclaw:ask "tell me about AAPL"` |
| `/investorclaw:portfolio-lookup accounts` → | `/investorclaw:ask "what brokerage accounts are loaded?"` |
| `/investorclaw:portfolio-run` → | `/investorclaw:refresh` |
| `/investorclaw:portfolio-session` → | `investorclaw session` |
| `/investorclaw:portfolio-stonkmode` → | `investorclaw stonkmode` |
| `/investorclaw:portfolio-check-updates` → | `investorclaw check-updates` |

### Architecture Rationale

This moves InvestorClaude to a two-command deterministic interaction model. The
adapter no longer asks Claude to choose among data-routing commands. ic-engine
owns deterministic pre-run, cache, provenance, signing, and narrator constraints;
InvestorClaude exposes the small deterministic surface to Claude Code.

## v2.4.0 - Command Surface Consolidation

InvestorClaude exposed the same consolidated portfolio command surface as
InvestorClaw. This was a deliberate breaking change from v2.3.x: the previous 27
granular slash commands were removed and there were no back-compat aliases.

Reason: the granular command surface created LLM routing ambiguity in Claude
Code. The 13-command surface reduced competing command descriptions while
preserving the same ic-engine functionality.

### New Surface

- 9 consolidated portfolio commands: `portfolio-view`, `portfolio-compute`,
  `portfolio-target`, `portfolio-scenario`, `portfolio-market`,
  `portfolio-bonds`, `portfolio-config`, `portfolio-report`,
  `portfolio-lookup`
- 4 meta commands: `portfolio-run`, `portfolio-session`,
  `portfolio-stonkmode`, `portfolio-check-updates`

### Migration Guide

| v2.3.x command | v2.4.0 command |
|----------------|----------------|
| `/investorclaw:ic-holdings` | `/investorclaw:portfolio-view holdings` |
| `/investorclaw:ic-performance` | `/investorclaw:portfolio-view performance` |
| `/investorclaw:ic-analyst` | `/investorclaw:portfolio-view analyst` |
| `/investorclaw:ic-news` | `/investorclaw:portfolio-view news` for holdings news; `/investorclaw:portfolio-market news general` for market news |
| `/investorclaw:ic-news-plan` | `/investorclaw:portfolio-market news general` |
| `/investorclaw:ic-analysis` | `/investorclaw:portfolio-compute synthesize` |
| `/investorclaw:ic-synthesize` | `/investorclaw:portfolio-compute synthesize` |
| `/investorclaw:ic-optimize` | `/investorclaw:portfolio-compute optimize-sharpe` or `optimize-minvol` or `optimize-blacklitterman` |
| `/investorclaw:ic-cashflow` | `/investorclaw:portfolio-compute cashflow` |
| `/investorclaw:ic-peer` | `/investorclaw:portfolio-compute peer` |
| `/investorclaw:ic-whatchanged` | `/investorclaw:portfolio-compute whatchanged` |
| `/investorclaw:ic-fa-topics` | `/investorclaw:portfolio-target allocation` |
| `/investorclaw:ic-scenario` | `/investorclaw:portfolio-scenario rebalance` or `stress` |
| `/investorclaw:ic-rebalance-tax` | `/investorclaw:portfolio-scenario tax-aware` |
| `/investorclaw:ic-bonds` | `/investorclaw:portfolio-bonds analysis` |
| `/investorclaw:ic-fixed-income` | `/investorclaw:portfolio-bonds strategy` |
| `/investorclaw:ic-setup` | `/investorclaw:portfolio-config setup` |
| `/investorclaw:ic-llm-config` | `/investorclaw:portfolio-config llm` |
| `/investorclaw:ic-guardrails` | `/investorclaw:portfolio-config guardrails` |
| `/investorclaw:ic-ollama-setup` | `/investorclaw:portfolio-config ollama` |
| `/investorclaw:ic-eod-report` | `/investorclaw:portfolio-report` |
| `/investorclaw:ic-report` | `/investorclaw:portfolio-report` |
| `/investorclaw:ic-lookup` | `/investorclaw:portfolio-lookup AAPL` or `/investorclaw:portfolio-lookup accounts` |
| `/investorclaw:ic-run` | `/investorclaw:portfolio-run` |
| `/investorclaw:ic-session` | `/investorclaw:portfolio-session` |
| `/investorclaw:ic-stonkmode` | `/investorclaw:portfolio-stonkmode` |
| `/investorclaw:ic-check-updates` | `/investorclaw:portfolio-check-updates` |

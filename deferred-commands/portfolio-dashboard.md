---
name: portfolio-dashboard
description: >
  Deferred dashboard prototype. Not exposed by the v2.4.0 InvestorClaude
  marketplace plugin; requires the local InvestorClaw dashboard/server stack.
allowed-tools: Bash(investorclaw *)
---

# Deferred Portfolio Dashboard Prototype

This file is intentionally outside `commands/`. Standard InvestorClaude
marketplace installs do not expose it as a slash command in v2.4.0.

**Deferred target:** a comprehensive dashboard artifact covering the portfolio
analysis command surface.

## What It Does

Orchestrates all portfolio commands in parallel:
- Holdings (asset allocation, positions, value)
- Performance (returns, risk, Sharpe ratio)
- Bonds (ladder, YTM, duration, maturity)
- Analyst (ratings, price targets, consensus)
- News (sentiment timeline, headlines)
- Cashflow (dividend/coupon calendar)
- Optimize (efficient frontier, rebalancing)
- Synthesis (multi-factor advisor brief)
- What Changed (attribution, factor analysis)
- Tax Report (harvest opportunities, wash-sale)
- Scenarios (stress tests, VaR, drawdown)
- Peer (beta matrix, active share, style drift)
- Reports (export controls)
- Settings (provider, risk profile, guardrails)
- About (version, disclaimer, links)

**Output**: Self-contained HTML dashboard artifact (~40-50KB, offline-capable PWA)

## Usage

```bash
investorclaw dashboard [--stonkmode on|off] [--output PATH]
```

### Options

| Option | Values | Default | Purpose |
|--------|--------|---------|---------|
| `--stonkmode` | `on`, `off` | `off` | Enable 30 personas, Mission Control, Dr. Stonk |
| `--output` | file path | `~/portfolio_reports/dashboard.html` | Save to custom location |
| `--workers` | 1-16 | 8 | Parallel command workers |

## Examples

**Generate dashboard (professional mode)**:
```bash
investorclaw dashboard
```

**Enable stonkmode (personal mode with Mission Control)**:
```bash
investorclaw dashboard --stonkmode on
```

**Save to custom location**:
```bash
investorclaw dashboard --output ~/Desktop/portfolio.html
```

**Faster execution (more workers)**:
```bash
investorclaw dashboard --workers 12
```

## Output

Success response:
```json
{
  "status": "success",
  "dashboard_file": "~/portfolio_reports/dashboard.html",
  "file_size_bytes": 42000,
  "commands_collected": 17,
  "commands_total": 17,
  "stonkmode_enabled": false,
  "launch_command": "open -na \"Google Chrome\" --args --app=\"file://...\""
}
```

Then Claude Code displays the HTML artifact inline for immediate viewing.

## Dashboard Features

### Tab Navigation (Top Bar)
- **Holdings** — Asset allocation pie, sector bar, top holdings, position table
- **Performance** — Returns sparkline, Sharpe ratio, volatility, max drawdown
- **Bonds** — Bond ladder chart, YTM, duration, maturity schedule
- **Analyst** — Consensus gauges, price targets, buy/hold/sell bars
- **News** — Sentiment timeline, headline cards, sentiment score
- **Cashflow** — Dividend calendar, coupon schedule, income forecast
- **Optimize** — Efficient frontier, rebalancing trades, target allocation
- **Synthesis** — Multi-factor advisor brief, key insights, recommendations
- **What Changed** — Attribution analysis, factor breakdown, top movers
- **Tax Report** — Harvest opportunities, wash-sale flags, after-tax alpha
- **Scenarios** — Macro stress tests, drawdown simulations, VaR/CVaR
- **Peer** — Beta matrix, active share, style drift, factor tilts
- **Reports** — Export controls (CSV, XLSX, PDF, email)
- **Settings** — Provider selection, risk profile, guardrails, stonkmode toggle
- **About** — Version, disclaimer, links, fingerprint

### Persistent UI (Stonkmode Only)

When `--stonkmode on`:
- **Mission Control** (right rail) — Soundboard, Dr. Stonk hover help, Captain's Log
- **Dr. Stonk Avatars** — WebP-embedded (31 personas, offline-capable)
- **Status Bar** — Portfolio value, last refresh, data freshness
- **Refresh Button** — Re-run dashboard with latest data

### Offline-First

- Service worker caches dashboard.html and all assets
- WebP avatars embedded as base64 (no network needed)
- Works completely offline after first load
- Syncs with portfolio data when network is available

## Performance

| Portfolio Size | Execution Time | Output Size |
|---|---|---|
| 25 positions | ~8s | 35KB |
| 100 positions | ~15s | 42KB |
| 200+ positions | ~25-30s | 50KB |

Times: Yfinance provider (free). With Polygon (paid): 2-3s faster.

## Errors & Troubleshooting

**"Command not found: investorclaw"**
- Reinstall InvestorClaw: `/investorclaw:portfolio-config setup`
- Or use source: `investorclaw`

**Dashboard generation failed**
- Check holdings file exists: `ls -l ~/.investorclaw/holdings.json`
- Verify API keys: `/investorclaw:portfolio-config llm`
- Clear cache: `rm -rf ~/.investorclaw/cache/`

**Dashboard shows old data**
- Re-run holdings refresh: `investorclaw view --section=holdings`
- Then regenerate dashboard: `investorclaw dashboard`

**Stonkmode avatars not loading**
- Check network tab in browser DevTools
- If offline, ensure service worker cached assets
- Clear browser cache: Ctrl+Shift+Delete

## Platform Support

The dashboard is not shipped by the v2.4.0 InvestorClaude marketplace plugin.
Use the local InvestorClaw dashboard/server stack when that optional artifact
path is available.

## See Also

- [README.md](../README.md) — Shipped command surface and dashboard deferral status
- [DISCOVERY_HIERARCHY.md](../DISCOVERY_HIERARCHY.md) — Claude Code routing rules

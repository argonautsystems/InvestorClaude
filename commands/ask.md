---
name: ask
description: Ask anything about your portfolio in natural language. Holdings, performance, bonds, news, optimization, target allocation, cash flow, peer comparison — one command answers all of them.
allowed-tools: Bash(*)
---

Run the InvestorClaw v2.6.1 natural-language entry point. On first use, this auto-bootstraps `uv` and the `investorclaw` CLI + `ic-engine` into the user's environment (matches the openclaw/zeroclaw/hermes per-runtime install pattern). Subsequent calls skip the bootstrap and run directly.

**Execute:**
```bash
export PATH="$HOME/.local/bin:$PATH"
if ! command -v investorclaw >/dev/null 2>&1; then
    echo "📦 First run — bootstrapping InvestorClaw CLI + ic-engine via uv..."
    bash "${CLAUDE_PLUGIN_ROOT}/bin/install-investorclaw" || {
        echo "❌ InvestorClaw bootstrap failed. See ${CLAUDE_PLUGIN_ROOT}/INSTALL_FLOW.md or run bin/install-investorclaw manually."
        exit 1
    }
fi
investorclaw ask "$ARGUMENTS"
```

**Presentation:**
- Present the engine narrator's answer clearly.
- Preserve all quoted source text, numerical values, timestamps, and freshness labels.
- Never fabricate portfolio, market, ticker, bond, news, or optimization data.
- If the first prompt takes 30-60 seconds, note that InvestorClaw is building the deterministic signed envelope; follow-up prompts should be cache-amortized.

**Errors:**
- If data looks stale, suggest `/investorclaw:refresh`.
- If setup or source data is missing, report the engine's exact guidance.

---

See [../DISCLAIMER.md](../DISCLAIMER.md)

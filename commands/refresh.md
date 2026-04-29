---
name: refresh
description: Force a fresh pipeline run on your portfolio. Use when news/prices may have moved or when you want to refresh stale cached data.
allowed-tools: Bash(*)
---

Force InvestorClaw to rebuild the deterministic portfolio pipeline cache. On first use, this auto-bootstraps `uv` and the `investorclaw` CLI + `ic-engine` (same pattern as `/investorclaw:ask`).

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
investorclaw refresh
```

**Presentation:**
- Present refresh status and any engine-reported artifacts clearly.
- Preserve numerical values, timestamps, and freshness labels exactly.
- After refresh completes, invite the user to ask the next portfolio question with `/investorclaw:ask`.

**Errors:**
- If setup or source data is missing, report the engine's exact guidance.

---

See [../DISCLAIMER.md](../DISCLAIMER.md)

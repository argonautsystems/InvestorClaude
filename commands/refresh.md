---
name: refresh
description: Force a fresh pipeline run on your portfolio. Use when news/prices may have moved or when you want to refresh stale cached data.
allowed-tools: Bash(investorclaw refresh)
---

> **Prerequisite:** the `investorclaw` CLI must be installed on your `$PATH` first. See [`/investorclaw:ask`](./ask.md) or [INSTALL_FLOW.md](../INSTALL_FLOW.md) for the bootstrap path. If `investorclaw` is not on `$PATH`, the `Bash` tool call returns "command not found" — run `bin/install-investorclaw` from your plugin cache (`~/.claude/plugins/cache/investorclaude/investorclaw/<version>/bin/install-investorclaw`) or a local clone to install the CLI + ic-engine.

Force InvestorClaw to rebuild the deterministic portfolio pipeline cache.

**Execute:**
```bash
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

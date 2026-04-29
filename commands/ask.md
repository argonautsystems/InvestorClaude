---
name: ask
description: Ask anything about your portfolio in natural language. Holdings, performance, bonds, news, optimization, target allocation, cash flow, peer comparison — one command answers all of them.
allowed-tools: Bash(investorclaw ask *)
---

> **Prerequisite:** the `investorclaw` CLI must be installed on your `$PATH` first. This plugin only wires the slash-command surface; the analytics engine ships separately. The full first-run sequence:
>
> 1. **Register the marketplace:** `/plugin marketplace add https://gitlab.com/argonautsystems/InvestorClaude.git`
> 2. **Install the plugin from it:** `/plugin install investorclaw@investorclaude` — this is what actually surfaces the slash commands.
> 3. **Bootstrap the CLI + analytics engine:** run `bin/install-investorclaw` from the plugin cache (`~/.claude/plugins/cache/investorclaude/investorclaw/<version>/bin/install-investorclaw`) or a source clone (`git clone https://gitlab.com/argonautsystems/InvestorClaude.git && cd InvestorClaude && bin/install-investorclaw`). It bootstraps `uv` and pip-installs the InvestorClaw CLI + `ic-engine`.
>
> See [INSTALL_FLOW.md](../INSTALL_FLOW.md) for full detail. If `investorclaw` is not on `$PATH` when this slash command runs, the `Bash` tool call returns "command not found" — that's the signal that step 3 hasn't run yet.

Run the InvestorClaw v2.6.0 natural-language entry point.

**Execute:**
```bash
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

# InvestorClaw Claude Code Install Flow

Complete walkthrough from "I want to analyze my portfolio" to production
analysis in Claude Code.

## Level 0: Auto-Discovery

User mentions portfolio-related keywords or attaches portfolio data:

- "I want to set up my portfolio"
- "Can you help me install InvestorClaw?"
- "I have CSV exports from my broker"
- "What's in my portfolio?"

Claude Code's `investorclaude` skill handles setup, file staging, and the v2.6.0
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
investorclaw config --section=setup
```

No API keys are required to start. InvestorClaw uses free data paths where
available and prompts later for optional provider keys.

### Step 3: Portfolio Upload

The user exports holdings from brokers:

- Schwab: Accounts -> Positions -> Export CSV
- Fidelity: NetBenefits -> Investments -> Download CSV
- Vanguard: My Accounts -> Download Holdings
- UBS: Wealth Management -> Holdings -> Export

Supported inputs: CSV, XLS, XLSX, PDF, and screenshots. In Claude Code, the user
attaches files directly to chat. Claude stages them to `~/portfolios/` when
needed and continues to the original analysis question.

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

After official marketplace acceptance:

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

- [DISCOVERY_HIERARCHY.md](DISCOVERY_HIERARCHY.md) - How Claude discovers and uses the v2.6.0 deterministic entry point
- [README.md](README.md) - Quick reference
- [skills/investorclaude/SKILL.md](skills/investorclaude/SKILL.md) - v2.6.0 interaction skill

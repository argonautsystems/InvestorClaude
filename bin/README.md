# InvestorClaw Setup Scripts

This directory contains helper scripts for InvestorClaw installation and configuration.

## `setup-orchestrator`

**Fully automated adapter setup for Claude Code users.**

### What it does

- ✅ Resolves this InvestorClaude plugin checkout
- ✅ Installs it with `python3 -m pip install -e .`
- ✅ Pulls `ic-engine` and `clio` through pinned `git+` dependencies
- ✅ Runs the portfolio setup wizard when needed and verifies the v2.6 ask surface
- ✅ Configures environment and verifies installation

### Usage

Claude Code invokes this helper as `setup-orchestrator` from the installed
plugin `bin/` directory. Standalone developers can run it from a checkout:

```bash
bash ./bin/setup-orchestrator
```

### Platform Support

- ✅ **macOS** (Intel + Apple Silicon)
- ✅ **Linux** (Ubuntu, Debian, etc.)
- ✅ **Windows** (via WSL2)

### Environment Variables

Optional configuration:
- `INVESTORCLAW_PORTFOLIO_DIR` — Custom portfolio directory (default: `~/portfolios`)
- `PYTHON_BIN` — Python executable to use for pip installation (default: `python3`)

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Python or pip unavailable |
| 2 | Adapter installation failed |
| 3 | Setup wizard failed |

### Typical Output

```
-> InvestorClaude setup orchestrator (Detected: macOS)
-> Checking Python and pip...
OK Python 3.12.8
-> Installing InvestorClaude adapter from this checkout...
OK Adapter installed; ic-engine and clio resolved from pinned dependencies
-> Verifying investorclaw console script...
OK InvestorClaw ready (investorclaw 2.6.0)
-> Checking portfolio configuration...
OK Portfolio configuration found at ~/.investorclaw/.env

OK Setup complete

Next steps:
  1. Analyze portfolio: investorclaw ask "what's in my portfolio?"
  2. In Claude Code, use /investorclaw:ask "what's in my portfolio?"
```

### When It's Used

- **Claude Code skill activation**: `investorclaude` skill invokes this automatically
- **Manual setup**: User can run directly if needed
- **Manual setup**: Standalone adapter developers can run directly if needed

### Dependencies

- `python3` with `pip`
- `git` — used by pip to fetch pinned `git+` dependencies
- `bash` — for script execution

### Troubleshooting

**python3: command not found**
- Install Python 3.10 or newer, then rerun `setup-orchestrator`

**git: command not found**
- Install git so pip can fetch the pinned `ic-engine` and `clio` dependencies

**Network connectivity**
- Script requires internet access to `gitlab.com` for pinned `git+` dependencies
- Firewalls may block access to GitLab

**Permission denied**
- Ensure the script is executable: `chmod +x setup-orchestrator`

---

## `install-investorclaw`

**Direct pip-based installation helper.**

Installs this InvestorClaude checkout with pip, using the same Phase 3 adapter dependency path as the orchestrator.

```bash
install-investorclaw
```

Claude Code documentation should direct users to `/plugin marketplace add`,
`/plugin install`, and `setup-orchestrator`; this helper remains available for
manual adapter installation.

---

## Adding New Scripts

When adding new helper scripts to this directory:

1. Add `#!/bin/bash` shebang (or appropriate interpreter)
2. Make executable: `chmod +x script-name`
3. Document in this README with:
   - What it does
   - How to use it
   - Exit codes
   - Dependencies
4. Add corresponding test in `tests/test_setup_scripts.py` if relevant
5. Update `investorclaude` skill if it's user-facing

#!/usr/bin/env bash
# reset-claude-test-host.sh — wipe & repopulate Claude Code plugin state
# for the COBOL harness on a test host (linux-x86-host, pi-small, pi-large).
#
# What it does:
#   1. Detect existing InvestorClaude checkout (or clone fresh).
#   2. Pull the latest tag from gitlab + uv sync.
#   3. Wipe stale marketplace caches under ~/.claude/plugins/marketplaces/
#      (specifically `investorclaw` from the pre-Phase-3.5 layout).
#   4. Pre-populate the InvestorClaude marketplace cache by cloning
#      directly into ~/.claude/plugins/marketplaces/investorclaude/.
#   5. Print the next steps for the human (the `/plugin install`
#      command is interactive Claude Code UI, can't be scripted).
#
# Idempotent — safe to re-run every test cycle. Designed to live on the
# test host (linux-x86-host by default) and be invoked over SSH from mac-dev-host.
#
# Usage:
#   bash reset-claude-test-host.sh              # default: latest tag
#   bash reset-claude-test-host.sh v2.3.4       # pin to specific tag
#   CHECKOUT_DIR=~/work/InvestorClaude bash reset-claude-test-host.sh
#
# Exit codes:
#   0  ready — open Claude Code and run `/plugin install investorclaw@investorclaude`
#   1  user error (bad arg, missing dep)
#   2  network or git error

set -euo pipefail

GITLAB_URL="https://gitlab.com/argonautsystems/InvestorClaude.git"
MARKETPLACE_NAME="investorclaude"
PLUGIN_NAME="investorclaw"
CHECKOUT_DIR="${CHECKOUT_DIR:-$HOME/InvestorClaude}"
TAG="${1:-}"

CLAUDE_DIR="$HOME/.claude"
MARKETPLACES_DIR="$CLAUDE_DIR/plugins/marketplaces"

cyan()  { printf '\033[36m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
red()   { printf '\033[31m%s\033[0m\n' "$*" >&2; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }

# ---------- preflight ----------
command -v git >/dev/null || { red "git not found"; exit 1; }
command -v uv  >/dev/null || {
  if [ -x "$HOME/.local/bin/uv" ]; then
    export PATH="$HOME/.local/bin:$PATH"
  else
    red "uv not found. Install via: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
  fi
}

[ -d "$CLAUDE_DIR" ] || { red "$CLAUDE_DIR missing — is Claude Code installed on this host?"; exit 1; }
mkdir -p "$MARKETPLACES_DIR"

# ---------- 1. checkout ----------
cyan "==> [1/4] InvestorClaude checkout @ $CHECKOUT_DIR"
if [ -d "$CHECKOUT_DIR/.git" ]; then
  echo "    existing checkout — fetching"
  git -C "$CHECKOUT_DIR" fetch origin --tags --quiet
else
  echo "    cloning $GITLAB_URL"
  git clone --quiet "$GITLAB_URL" "$CHECKOUT_DIR" || { red "clone failed"; exit 2; }
fi

if [ -n "$TAG" ]; then
  echo "    checking out tag $TAG"
  git -C "$CHECKOUT_DIR" checkout --quiet "$TAG"
else
  # Use the latest semver tag on origin/main
  LATEST_TAG=$(git -C "$CHECKOUT_DIR" tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -1)
  if [ -z "$LATEST_TAG" ]; then
    yellow "    no semver tag found — checking out origin/main"
    git -C "$CHECKOUT_DIR" checkout --quiet origin/main
  else
    echo "    checking out latest tag $LATEST_TAG"
    git -C "$CHECKOUT_DIR" checkout --quiet "$LATEST_TAG"
  fi
fi
green "    HEAD: $(git -C "$CHECKOUT_DIR" log --oneline -1)"

# ---------- 2. uv sync ----------
cyan "==> [2/4] uv sync (pulls ic-engine + clio transitively)"
( cd "$CHECKOUT_DIR" && uv sync 2>&1 | tail -5 ) || { red "uv sync failed"; exit 2; }
ENGINE_VER=$( cd "$CHECKOUT_DIR" && uv run python -c "import ic_engine; print(ic_engine.__version__)" 2>/dev/null )
green "    ic-engine resolved: $ENGINE_VER"

# ---------- 3. wipe stale caches ----------
cyan "==> [3/4] wipe stale marketplace caches"
# The pre-Phase-3.5 InvestorClaw marketplace pointed at a `claude/` subdir
# of the monolith repo that no longer exists. Any cached copy will hang
# on plugin installs. Remove it.
for stale_name in investorclaw investorclaude; do
  if [ -d "$MARKETPLACES_DIR/$stale_name" ]; then
    echo "    removing $MARKETPLACES_DIR/$stale_name"
    rm -rf "$MARKETPLACES_DIR/$stale_name"
  fi
done

# ---------- 4. populate fresh InvestorClaude marketplace cache ----------
cyan "==> [4/4] populate fresh marketplace cache @ $MARKETPLACES_DIR/$MARKETPLACE_NAME"
git clone --quiet "$GITLAB_URL" "$MARKETPLACES_DIR/$MARKETPLACE_NAME" || { red "marketplace clone failed"; exit 2; }
if [ -n "$TAG" ]; then
  git -C "$MARKETPLACES_DIR/$MARKETPLACE_NAME" checkout --quiet "$TAG"
elif [ -n "$LATEST_TAG" ]; then
  git -C "$MARKETPLACES_DIR/$MARKETPLACE_NAME" checkout --quiet "$LATEST_TAG"
fi
MARKETPLACE_VER=$(python3 -c "import json; print(json.load(open('$MARKETPLACES_DIR/$MARKETPLACE_NAME/.claude-plugin/marketplace.json'))['plugins'][0].get('source',{}).get('url','???'))" 2>/dev/null || echo "(parse failed)")
green "    marketplace populated; plugin source URL: $MARKETPLACE_VER"

# ---------- next steps ----------
echo
green "==================================================================="
green "  READY. Open Claude Code on this host and run:"
green ""
green "    /plugin install $PLUGIN_NAME@$MARKETPLACE_NAME"
green ""
green "  Then run the COBOL harness from $CHECKOUT_DIR/harness/"
green "  CLAUDE_CODE_TEXT_HARNESS.md — paste each prompt verbatim into a"
green "  fresh Claude Code chat and score the routing."
green "==================================================================="

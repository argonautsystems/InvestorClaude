#!/usr/bin/env bash
# COBOL barrage — InvestorClaude routing-acceptance harness.
#
# Drives `claude -p --plugin-dir <PLUGIN_DIR>` against the canonical
# 30-prompt NLQ set with --output-format=stream-json --verbose, then
# scores each prompt against the v2.5.x slash-command surface
# (ask, refresh, session, stonkmode, check-updates) using
# parse_stream_json.py.
#
# Run on linux-x86-host (or any host with the InvestorClaude plugin installed).
# mac-dev-host is not appropriate — see commit 7e6092d.
#
#   REPO_ROOT=$HOME/InvestorClaude \
#   NLQ_JSON=$HOME/InvestorClaw/harness/cobol/nlq-prompts.json \
#   bash harness/cobol/cobol-barrage.sh
set -uo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/InvestorClaude}"
NLQ_JSON="${NLQ_JSON:-$HOME/InvestorClaw/harness/cobol/nlq-prompts.json}"
PLUGIN_DIR="${PLUGIN_DIR:-$REPO_ROOT}"
PARSER="${PARSER:-$REPO_ROOT/harness/cobol/parse_stream_json.py}"
TODAY="$(date +%F)"
VERSION="${VERSION:-$(cd "$REPO_ROOT" && git describe --tags --abbrev=0 2>/dev/null || echo dev)}"
OUT="${OUT:-$REPO_ROOT/harness/reports/${VERSION}-linux-x86-host-cobol-${TODAY}.jsonl}"

cd "$HOME/Desktop"

if [[ ! -f "$PARSER" ]]; then
  echo "parser not found at $PARSER" >&2
  exit 2
fi
if [[ ! -f "$NLQ_JSON" ]]; then
  echo "nlq-prompts.json not found at $NLQ_JSON" >&2
  exit 2
fi

> "$OUT"
ROWS_FILE="$(mktemp)"
python3 -c "
import json
d = json.load(open('$NLQ_JSON'))
for p in d['prompts']:
    expected = p['expected_routes'].get('investorclaude', [])
    print(p['id'] + chr(9) + p['prompt'] + chr(9) + ',,'.join(expected))
" > "$ROWS_FILE"

while IFS=$'\t' read -r pid prompt expected; do
  echo "=== $pid ===" >&2
  claude -p --plugin-dir "$PLUGIN_DIR" --output-format=stream-json --verbose "$prompt" 2>/dev/null \
    | python3 "$PARSER" "$pid" "$prompt" "$expected" "$OUT" \
    || echo "  (parse path failed)" >&2
done < "$ROWS_FILE"

echo >&2
echo "=== SUMMARY ===" >&2
python3 - <<PY
import json
rows = [json.loads(l) for l in open("$OUT") if l.strip()]
total = len(rows); passed = sum(1 for r in rows if r.get("passed"))
print(f"InvestorClaude $VERSION COBOL: {passed}/{total} = {100*passed//max(total,1)}%")
print(f"Class B gate: 21/30 strict, 24/30 publish")
print(f"Output: $OUT")
print()
for r in rows:
    v = "PASS" if r.get("passed") else "FAIL"
    print(f"  {v} {r['id']:<25} expected={r['expected']} detected={r['detected'] or '[none]'}")
PY

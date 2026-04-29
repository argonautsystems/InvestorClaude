"""Regression test for the v2.5.1 → v2.5.2 parser fix.

Drives extract_detected() against the real recorded tool_invocations
in harness/reports/v2.5.1-linux-x86-host-cobol-2026-04-27-PARSER-BUG.jsonl.
With the v2.5.1 logic, every prompt with a Skill invocation yielded
detected=[]; with the v2.5.2 fix, detected resolves to the canonical
subcommand the agent invoked.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_stream_json import extract_detected, matches  # noqa: E402

REPORTS = Path(__file__).parent.parent / "reports"
BUG_JSONL = REPORTS / "v2.5.1-linux-x86-host-cobol-2026-04-27-PARSER-BUG.jsonl"


def v251_extract(tool_invocations):
    """The v2.5.1 (buggy) extraction logic, kept verbatim so the test
    proves the captured dataset exposes the bug."""
    detected = set()
    subs = ("ask", "refresh", "session", "stonkmode", "check-updates")
    for name, arg in tool_invocations:
        if name == "Bash":
            for sub in subs:
                if re.search(rf"\binvestorclaw\s+{re.escape(sub)}\b", arg):
                    detected.add(sub)
        for sub in subs:
            if name.endswith(f":{sub}") or name == sub or name.endswith(f"-{sub}"):
                detected.add(sub)
    return sorted(detected)


def main():
    rows = [json.loads(l) for l in BUG_JSONL.read_text().splitlines() if l.strip()]
    assert len(rows) == 30, f"expected 30 rows, got {len(rows)}"

    v251_pass = sum(
        1
        for r in rows
        if any(
            matches(e, v251_extract([tuple(t) for t in r["tool_invocations"]]))
            for e in r["expected"]
        )
    )
    assert v251_pass == 1, f"v2.5.1 logic should reproduce 1/30, got {v251_pass}"

    v252_pass = sum(
        1
        for r in rows
        if any(
            matches(e, extract_detected([tuple(t) for t in r["tool_invocations"]]))
            for e in r["expected"]
        )
    )
    assert v252_pass == 30, f"v2.5.2 logic should recover 30/30, got {v252_pass}"

    for r in rows:
        invs = [tuple(t) for t in r["tool_invocations"]]
        has_ask_skill = any(
            name == "Skill" and '"skill": "investorclaw:ask"' in arg for name, arg in invs
        )
        if has_ask_skill:
            detected = extract_detected(invs)
            assert "ask" in detected, f"{r['id']}: Skill→ask extraction missed: {detected}"

    print(f"v2.5.1 logic: {v251_pass}/30 (expected 1/30) — bug reproduced")
    print(f"v2.5.2 logic: {v252_pass}/30 (expected 30/30) — fix verified")


if __name__ == "__main__":
    main()

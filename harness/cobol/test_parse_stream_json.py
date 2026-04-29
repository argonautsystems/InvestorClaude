"""Regression test for the v2.5.1 → v2.5.2 parser fix.

The v2.5.1 extractor only handled `Bash` tool invocations and slash-style
tool names ending in `:<sub>`. Claude Code's actual stream-json output
surfaces plugin slash commands as `Skill` tool calls with the slash name
in `input.skill`. v2.5.1 missed every Skill invocation; v2.5.2 added the
Skill branch.

This test asserts the differential behavior on a small synthetic fixture:
v2.5.1 logic must miss the Skill row, v2.5.2 logic must catch it. The
real-data fixture this was originally captured against (a deleted JSONL
test artifact) is not required to prove the regression.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_stream_json import extract_detected, matches  # noqa: E402


def v251_extract(tool_invocations):
    """The v2.5.1 (buggy) extraction logic, kept verbatim so the test
    documents the bug being regression-guarded."""
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


# Three rows exercising the parser's three input shapes:
#   - Skill: investorclaw:ask  → v2.5.1 misses; v2.5.2 catches
#   - Bash:  `investorclaw ask`→ both catch
#   - mixed Skill+Bash         → both catch (v2.5.1 via Bash, v2.5.2 via either)
FIXTURE = [
    {
        "id": "skill-only",
        "expected": ["ask"],
        "tool_invocations": [("Skill", '{"skill": "investorclaw:ask"}')],
    },
    {
        "id": "bash-only",
        "expected": ["ask"],
        "tool_invocations": [("Bash", "investorclaw ask 'what is in my portfolio'")],
    },
    {
        "id": "mixed",
        "expected": ["ask"],
        "tool_invocations": [
            ("Skill", '{"skill": "investorclaw:ask"}'),
            ("Bash", "investorclaw ask 'follow up'"),
        ],
    },
]


def passes(extractor, row):
    detected = extractor(row["tool_invocations"])
    return any(matches(e, detected) for e in row["expected"])


def main():
    v251_passes = sum(1 for r in FIXTURE if passes(v251_extract, r))
    v252_passes = sum(1 for r in FIXTURE if passes(extract_detected, r))

    # v2.5.1 catches Bash-only and mixed (the Bash branch fires); misses skill-only
    assert v251_passes == 2, f"v2.5.1 should catch 2/3, got {v251_passes}"

    # v2.5.2 catches all three
    assert v252_passes == 3, f"v2.5.2 should catch 3/3, got {v252_passes}"

    # Direct assertion: the Skill→ask extraction must succeed in v2.5.2
    skill_only_detected = extract_detected(FIXTURE[0]["tool_invocations"])
    assert "ask" in skill_only_detected, (
        f"v2.5.2 Skill extraction broken: detected={skill_only_detected}"
    )

    # And must fail in v2.5.1 (regression guard)
    skill_only_v251 = v251_extract(FIXTURE[0]["tool_invocations"])
    assert "ask" not in skill_only_v251, (
        f"v2.5.1 should miss Skill rows: detected={skill_only_v251}"
    )

    print(f"v2.5.1 logic: {v251_passes}/3 — Skill-only row missed (regression reproduced)")
    print(f"v2.5.2 logic: {v252_passes}/3 — Skill-only row caught (fix verified)")


if __name__ == "__main__":
    main()

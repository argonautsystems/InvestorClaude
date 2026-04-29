"""Parser/scorer for the COBOL barrage stream-json transcripts.

Reads a `claude -p --output-format=stream-json` transcript on stdin
(one JSON event per line), extracts tool_use events, maps them to the
canonical investorclaw command set, and writes one JSONL row to the
path given as argv[4].

Bug history: the v2.5.1 version of this parser handled only two
tool-name shapes — `Bash` (regex against `investorclaw <sub>`) and
direct slash-command tools whose name ends with `:<sub>`. In Claude
Code's actual stream-json output, plugin slash commands surface as
`Skill` tool calls with input `{"skill": "investorclaw:ask", ...}`,
where the slash name lives in `input.skill`, not the tool name. v2.5.1
missed every Skill invocation, scoring 1/30. v2.5.2 adds the Skill
branch — see harness/reports/v2.5.1-linux-x86-host-cobol-2026-04-27-RESCORED.jsonl
for the rescored captured data (30/30) that confirms the fix.
"""
import json
import re
import sys

CANONICAL_SUBS = ("ask", "refresh", "session", "stonkmode", "check-updates")
SKILL_RE = re.compile(r"^investorclaw[de]*:([a-z][a-z0-9-]*)$")


def extract_detected(tool_invocations):
    """Map a list of (tool_name, arg_blob_json) to the sorted set of
    canonical investorclaw subcommands the agent invoked.

    arg_blob is a JSON-encoded string of the tool's `input` object.
    """
    detected = set()
    for name, arg in tool_invocations:
        if name == "Skill":
            try:
                args = json.loads(arg) if isinstance(arg, str) else (arg or {})
            except json.JSONDecodeError:
                args = {}
            skill = (args.get("skill") or "") if isinstance(args, dict) else ""
            m = SKILL_RE.match(skill)
            if m and m.group(1) in CANONICAL_SUBS:
                detected.add(m.group(1))
            continue

        if name == "Bash":
            for sub in CANONICAL_SUBS:
                if re.search(rf"\binvestorclaw\s+{re.escape(sub)}\b", arg):
                    detected.add(sub)
            continue

        for sub in CANONICAL_SUBS:
            if name.endswith(f":{sub}") or name == sub or name.endswith(f"-{sub}"):
                detected.add(sub)
    return sorted(detected)


def matches(expected_route, detected_list):
    e = expected_route.lower().strip()
    if e == "deflect_ok":
        return not detected_list
    return e in detected_list


def parse_transcript(stream):
    """Read stream-json events from a stdin-like iterable, returning
    (tool_invocations, duration_ms, result_text)."""
    tool_invocations = []
    duration_ms = None
    result_text = ""
    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        et = ev.get("type")
        if et == "result":
            duration_ms = ev.get("duration_ms")
            result_text = ev.get("result", "") or ""
        if et == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tool_invocations.append(
                        (block.get("name", ""), json.dumps(block.get("input", {})))
                    )
    return tool_invocations, duration_ms, result_text


def main():
    pid, prompt, expected_csv, out_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    expected_routes = expected_csv.split(",,") if expected_csv else []

    tool_invocations, duration_ms, result_text = parse_transcript(sys.stdin)
    detected = extract_detected(tool_invocations)
    passed = any(matches(r, detected) for r in expected_routes)

    row = {
        "id": pid,
        "prompt": prompt,
        "expected": expected_routes,
        "tool_invocations": tool_invocations[:10],
        "detected": detected,
        "passed": passed,
        "duration_ms": duration_ms,
        "result_snippet": (result_text or "")[:240].replace("\n", " "),
    }
    with open(out_path, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"  {'PASS' if passed else 'FAIL'} detected={detected} ({duration_ms}ms)", file=sys.stderr)


if __name__ == "__main__":
    main()

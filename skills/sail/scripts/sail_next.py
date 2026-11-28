#!/usr/bin/env python3
"""
sail_next.py - what a Sail run still owes, read from each feature's sail.md.

check_commit.py tracks tlc-spec-lean's stages and stops at "the report remains" once the fix pass
is recorded, while Sail still owes Validate steps 3-8 and the PR. This reads Sail's own state, so
after a compaction one command says where the run is, instead of a rule read hours earlier.
Through Validate step 2 it also prints check_commit's next step for the feature.

sail.md holds one `key: value` per line (a leading `- ` is fine):

    goal: <the user's goal, in one sentence, as stated at intake>
    size: XS | S | M | L
    base: <base branch>
    stage: <one of the stages below for that size>
    assumed: <decision> - <why>        (any number)

Usage:
  python3 <sail-dir>/scripts/sail_next.py [--root DIR]

Exit codes: 0 read, 1 a sail.md is missing a field or names an unknown size or stage.
"""

import argparse
import os
import re
import sys

LEAN_SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tlc-spec-lean", "scripts")
sys.path.insert(0, os.path.normpath(LEAN_SCRIPTS))
from check_commit import FIX_DONE_RE, next_steps, plan_lines  # noqa: E402

FULL = [
    ("intake", "goal, size and base stated in the first message and written here"),
    ("plan", "tlc-spec-lean's Plan; M/L stops for approval, S records `assumed:` lines in request.md"),
    ("build", "tlc-spec-lean's Build, each slice committed, the `**Walked:**` line written"),
    ("validate/0-rebase", "rebase onto the base, update deps and schema, re-walk what the rebase touched"),
    ("validate/1-shared", "if shared code changed, run every test file that observes its output"),
    ("validate/2-review", "tlc-spec-lean's fresh reviewer, then its one fix pass"),
    ("validate/3-code-review", "`/code-review medium <branch>` (high for money, auth, migrations, data)"),
    ("validate/4-judge", "the-judge over `git diff <base>...HEAD`, chat only"),
    ("validate/5-verifier", "one ship:verifier subagent with the brief template"),
    ("validate/6-fix", "spot-check the verifier's evidence, fix what it confirmed and found"),
    ("validate/7-reround", "if a fix changed behaviour: tests, re-walk, one scoped verifier round"),
    ("validate/8-commands", "the repo's test, build and lint commands pass at HEAD"),
    ("pr", "stop before push with the results and the `assumed:` list, then the draft PR and Handoff"),
    ("done", ""),
]
XS = [
    ("intake", "goal, size and base stated in the first message and written here"),
    ("build", "the change, committed"),
    ("validate/xs", "tests for touched files, `/code-review low`, one look at the screen or route"),
    ("pr", "stop before push with the results and the `assumed:` list, then the draft PR"),
    ("done", ""),
]
STAGES = {"XS": XS, "S": FULL, "M": FULL, "L": FULL}
LEAN_STAGES = {"plan", "build", "validate/0-rebase", "validate/1-shared", "validate/2-review"}
FIELD_RE = re.compile(r"^(?:-\s+)?(goal|size|base|stage|assumed)\s*:\s*(.*)$", re.IGNORECASE)


def read_sail(path):
    fields, assumed = {}, []
    for line in plan_lines(path):
        m = FIELD_RE.match(line)
        if not m:
            continue
        key, value = m.group(1).lower(), m.group(2).strip()
        if key == "assumed":
            assumed.append(value)
        else:
            fields[key] = value
    return fields, assumed


def lean_closed(feature_dir):
    for name in ("plan.md", "request.md"):
        path = os.path.join(feature_dir, name)
        if os.path.isfile(path) and any(FIX_DONE_RE.match(s) for s in plan_lines(path)):
            return True
    return False


def report(root):
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return [], []
    lean = dict(next_steps(root))
    lines, errors = [], []
    for feature in sorted(os.listdir(base)):
        path = os.path.join(base, feature, "sail.md")
        if not os.path.isfile(path):
            continue
        fields, assumed = read_sail(path)
        missing = [k for k in ("goal", "size", "base", "stage") if not fields.get(k)]
        if missing:
            errors.append(f"`{feature}`: sail.md has no {', '.join(missing)} line")
            continue
        size, stage = fields["size"].upper(), fields["stage"]
        if size not in STAGES:
            errors.append(f"`{feature}`: size `{fields['size']}` is not XS, S, M or L")
            continue
        order = [s for s, _ in STAGES[size]]
        if stage not in order:
            errors.append(f"`{feature}`: stage `{stage}` is not a {size} stage: {', '.join(order)}")
            continue
        if stage == "done":
            continue
        i = order.index(stage)
        owes = dict(STAGES[size])[stage]
        out = [f"`{feature}` ({size}, base {fields['base']}, {len(assumed)} assumed)",
               f"  goal: {fields['goal']}",
               f"  stage {stage}: {owes}",
               f"  then: {order[i + 1]}"]
        if size != "XS" and stage in LEAN_STAGES:
            if stage == "validate/2-review" and lean_closed(os.path.join(base, feature)):
                out.append("  tlc-spec-lean's fix pass is recorded: set `stage: validate/3-code-review`; "
                           "Sail still owes Validate 3-8 and the PR")
            elif feature in lean:
                out.append(f"  tlc-spec-lean: {lean[feature]}")
        lines.append("\n".join(out))
    return lines, errors


def main(argv=None):
    p = argparse.ArgumentParser(prog="sail_next.py", description="Print what each Sail run still owes.")
    p.add_argument("--root", default=".", help="project root that contains .specs/ (default: current dir)")
    args = p.parse_args(argv)
    lines, errors = report(args.root)
    for e in errors:
        print(f"ERROR {e}")
    print("\n\n".join(lines) if lines else "sail_next: no open Sail run under .specs/features/")
    return 1 if errors else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())

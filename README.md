<p align="center"><img src=".claude-plugin/icon.png" width="128" alt="ship icon"></p>

# ship

A Claude Code plugin that takes one ticket from intake to an open draft pull request, with
stops where a human has to decide and an independent check before anything is called done.

```
INTAKE → PLAN → CHECKS → BUILD → VALIDATE → PR
 stop     stop            stop per commit   stop before push
```

## What's inside

| Component | Invoke | What it does |
| --- | --- | --- |
| `sail` skill | `/ship:sail` | Runs the whole flow for one ticket |
| `verifier` agent | spawned by `sail` | One independent pass at validate time: checks that each test would fail if its claim were false, and tries to refute the code review's findings |

## How `sail` works

**Size first.** At intake `sail` recommends a size with one line of why, so small changes don't pay
for the full ceremony:

| Size | When | Plan | Validate |
| --- | --- | --- | --- |
| XS | config, copy, a one-liner | the goal statement | project tests for touched files + `/code-review low` |
| S | roughly under 3 files, no hard-to-reverse decision | short intent + checks | full gate |
| M/L | anything bigger | full plan with criteria | full gate |

**The full gate**, in order, each step on the code the previous one left:

1. Every check's proof passes at `HEAD` (tlc-spec-lean's `check_proofs.py`).
2. `/code-review medium` for correctness bugs (`high` for money, auth, migrations, data).
3. `the-judge` over the local branch, results in chat only, never posted.
4. One `ship:verifier` subagent does tlc-spec-lean's Verifier round and refutes the judge's findings.
5. Fixes, then at most one more scoped verifier round, then `validate_verification.py` exits 0.

**Habits it holds in every stage:**

- **Goal first.** The first message and the final report state the goal, the problem behind it and
  the smallest change expected to meet it.
- **Lean code.** Name the data shape before the logic, subtract before adding, fix root causes, and
  test behaviour rather than implementation.
- **Evidence-labelled replies.** Every claim is marked measured, inferred or guess.

**Your conventions win.** PR title format, PR template, commit style and review-bot comments come
from the project's `CLAUDE.md` and your Claude Code memory, not from the plugin.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- `tlc-spec-lean` and `the-judge` skills, installed in the project (`.claude/skills/`) or in
  `~/.claude/skills/`. `sail` stops and names the missing one if it can't find them.
- `gh` (GitHub CLI), authenticated, for opening the PR
- Python 3.8+ for tlc-spec-lean's scripts

## Install

```sh
claude plugin marketplace add bzenky/ship
claude plugin install ship@ship
```

Restart the Claude Code session, then run `/ship:sail` with a ticket.

## Update

```sh
claude plugin marketplace update ship
claude plugin update ship@ship
```

## Layout

```
.claude-plugin/
├── plugin.json        # plugin manifest
├── marketplace.json   # lets the repo be added as a marketplace
└── icon.png           # rendered from assets/icon.svg
agents/verifier.md
skills/sail/SKILL.md
assets/icon.svg
```

## Credits

`ship` orchestrates other people's work and borrows some of their ideas:

- **tlc-spec-lean** by [Tech Leads Club](https://github.com/tech-leads-club) (CC-BY-4.0), derived
  from tlc-spec-driven by Felipe Rodrigues. `sail` runs its plan, checks, build and verify phases and
  their scripts.
- **the-judge** by [Felipe Rodrigues](https://github.com/felipfr) (CC-BY-4.0). `sail` runs it as the
  last review pass.
- **poteto-mode** from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan
  (MIT). The goal-first, lean-code and evidence-labelled habits are adapted from it.

Neither skill is bundled here; install them from their authors.

## License

[MIT](LICENSE)

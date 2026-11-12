---
name: sail
description: 'Takes one ticket from intake to an open draft PR: size it, plan, freeze checks, build, validate (code-review, the-judge, one independent verifier), then open the PR. Runs tlc-spec-lean for plan/checks/build/proofs and the-judge for review; adds goal restatement, lean-code principles and evidence-labelled replies. Use when the user says "sail", "/ship:sail", "take this ticket to a PR", "plan, build, validate and open the PR", or hands over a ticket to deliver end to end. Do NOT use for reviewing someone else''s PR (use the-judge), for babysitting an open PR, or for a design doc with no ticket.'
---

# Sail

One ticket, intake to draft PR. Sail owns the order of the stages and the stops; the stages themselves
belong to the skills it calls, so read them rather than re-deriving them here.

```
INTAKE → PLAN → CHECKS → BUILD → VALIDATE → PR
 stop      stop            stop per commit   stop before push
```

## Precedence

The project's `CLAUDE.md` and the user's memory win over Sail: PR title format, PR template, branch
names, commit style, review-bot comments, attribution lines. Sail wins over the defaults of the skills
it calls where it says so below (the-judge never posts; one merged verifier). tlc-spec-lean's own rules
hold everywhere else.

## Dependencies

Find each `SKILL.md` in `<project>/.claude/skills/<name>/`, then `~/.claude/skills/<name>/`. If one is
missing, say which and stop: Sail without them is just improvisation.

| Skill | Used for |
| --- | --- |
| `tlc-spec-lean` | plan, checks, build, proof scripts, the Verifier's reference (`references/verify.md`) |
| `the-judge` | the last review pass, chat only |
| `/code-review` (built in) | correctness pass before the judge |

## Habits that hold in every stage

**Goal first.** Your first message on a ticket states, in your own words, the user's goal, the problem
behind it, and the smallest change you expect to meet it. Don't wait for confirmation. If the evidence
rules out the change that was asked for, show the evidence and stop. Open the final report with the goal
too, and restate it in every subagent brief, because a subagent that doesn't know the goal optimises
for its own reading of the task.

**Lean code.**
- Name the data shape before writing logic. Encode the domain in a structure (a table or registry, a
  state machine, a typed model) instead of conditionals scattered across files.
- Subtract before you add. Delete dead weight first; the smallest change that meets the criteria wins.
- Fix root causes. Trace a symptom to the first place the system went wrong. A guard is a fix only when
  the state it handles is legitimate.
- Test behaviour, not implementation. Assert what a user of the code can observe, so the test fails
  when that breaks and survives a refactor. Shared behaviour is tested once at its own layer; each
  host gets one wiring test.

**Evidence-labelled replies.** Short declarative sentences. Every claim carries its evidence or its
label in the same sentence: measured (with the command or file:line), inferred, or guess. Never hand the
user a check you could run yourself.

## 0. Intake (stop)

1. If the branch or request names a ticket, fetch it (the project's tracker tool) and any business
   rules the project's `CLAUDE.md` points to.
2. If `.specs/STATE.md` has a `## Handoff`, name the feature it describes and ask whether to read it.
3. Restate the goal (above).
4. Recommend a size with one line of why, and ask the base branch the PR will target. Ask both in one
   question; never assume the base, it decides the diff every later stage reads.

| Size | When | Plan artifact | Validate |
| --- | --- | --- | --- |
| **XS** | config, copy, a one-liner, no new branch of behaviour | none, the goal statement is the plan | project tests for touched files + `/code-review low` |
| **S** | roughly under 3 files, no one-way door | `checks.md` with an `## Intent` paragraph (tlc-spec-lean's short path) | full gate |
| **M/L** | anything bigger, or any one-way door | full `plan.md` | full gate |

Write size, base branch and current stage to `.specs/features/<feature>/sail.md` (S and up) as soon as
they are decided. The chat does not survive a compaction; that file and tlc-spec-lean's files do.

## 1. Plan (stop) and 2. Checks

Run tlc-spec-lean's Plan and Checks phases as its references say, with these additions:

- In the plan, name the data shape and its organising structure before the path.
- When a question is a fact you could observe by running something (behaviour, output, layout), run a
  throwaway sketch and let the result answer it. Ask the user only for product or preference calls.
- Propose the trimmed test list with the checks, before writing any test: one proof may settle several
  checks that share a setup.

XS skips both phases.

## 3. Build (stop per commit)

Run tlc-spec-lean's Build phase. Ask before every `git commit`; an approved plan authorises edits, not
commits. Before each commit, strip comments that restate the code: keep only a non-obvious why.

## 4. Validate

**XS:** run the project's tests for the touched files, then `/code-review low` (chat only). Fix real
bugs, then go to PR. The review bot on the PR is the backstop.

**S, M/L:** in this order, each step on the code the previous one left.

1. `check_proofs.py <feature>` green at `HEAD`.
2. `/code-review medium`, no `--comment`, no `--fix`. Use `high` only for money, auth, migrations or
   data. Fix real bugs, ask before committing.
3. `the-judge` over the local branch, chat only. There is no PR yet: replace its Step 0 `gh` calls with
   `git diff <base>...HEAD` and treat it as round 1. Skip its Gate and Post steps. Its findings never
   go on any PR, not even later; it is the user's private check.
4. One `ship:verifier` subagent at the same `HEAD`. Brief: the goal, the feature, the diff range, the
   tlc-spec-lean skill directory, and the judge's findings as claims with evidence pointers (not the
   judge's reasoning). Record it on `checks.md`'s `**Dispatched:**` line first. If a criterion cites a
   capture, tlc-spec-lean's screens subagent runs beside it; no other subagents.
5. Spot-check any new evidence the verifier cites, then fix what it CONFIRMED and what it found, in
   commits. Report the judge result and the verifier's verdict table together.
6. If a fix changed behaviour, run `check_proofs.py` again and one more verifier round scoped to the
   new commits. Two rounds at most, unless a remaining gap can reach a user; a surviving mutant on a
   path no user reaches is a note, not a failure.
7. `validate_verification.py <feature>` exits 0. Open the report with its last line; a red gate is said
   first.

If the ticket is a security ticket and the project defines a security gate skill, run it after step 7;
its NO-GO stops the PR.

## 5. PR (stop before push)

Ask before `git push`. Then:

- Open the PR **as a draft** against the base from intake, title and body per the project's convention
  and PR template. Fill the template; leave out empty sections and any generated-by footer.
- Assign the user (`--assignee @me`) and post the review-bot trigger comment the user's memory names.
- The Testing section is click-through steps for the reviewing developer, not a list of automated tests.

Then ask once whether to write a `## Handoff` into `.specs/STATE.md` (PR state, pending reviews, flaky
tests, next step).

## Final report

Open with the goal. Then: what changed, the size and why, the gate's last line, the judge and verifier
verdicts (what was fixed, what was refuted), open decisions, and the PR link. Every claim labelled.

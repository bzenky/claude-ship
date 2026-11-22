---
name: sail
description: 'Takes one change, from a ticket or a plain request, to an open draft PR: size it, plan, build, validate (a fresh reviewer, code-review, the-judge, one verifier that refutes the judge), then open the PR. Runs tlc-spec-lean for plan/build/review and the-judge for the last review pass; adds goal restatement, lean-code principles and evidence-labelled replies. Use when the user says "sail", "/ship:sail", "take this ticket to a PR", "build this and open a PR", "plan, build, validate and open the PR", or hands over a ticket or a feature/fix request to deliver end to end in an existing repo. Do NOT use for reviewing someone else''s PR (use the-judge), for babysitting an open PR, for a design doc, or for a throwaway prototype or a brand-new project that will not end in a PR.'
---

# Sail

One change, from a ticket or a plain request, intake to draft PR. Sail owns the order of the stages and the stops; the stages themselves
belong to the skills it calls, so read them rather than re-deriving them here.

```
INTAKE → PLAN → BUILD → VALIDATE → PR
 stop      stop    stop per commit   stop before push
```

## Precedence

The project's `CLAUDE.md` and the user's memory win over Sail: PR title format, PR template, branch
names, commit style, review-bot comments, attribution lines. Sail wins over the defaults of the skills
it calls where it says so below (the-judge never posts; fixes from the passes after tlc-spec-lean's
review are allowed). tlc-spec-lean's own rules
hold everywhere else.

## Bundled skills

`tlc-spec-lean` and `the-judge` ship with this plugin, beside this file. Resolve `<skills>` as the
directory that holds this `SKILL.md`'s folder and read `<skills>/tlc-spec-lean/SKILL.md` and
`<skills>/the-judge/SKILL.md` by path when their stage comes. Use these copies even when the project
has its own: Sail was written against them, and another version may name its scripts or steps
differently.

| Skill | Used for |
| --- | --- |
| `<skills>/tlc-spec-lean` | plan, build, the walk, the fresh reviewer (`references/review.md`), `check_commit.py` |
| `<skills>/the-judge` | the last review pass, chat only |
| `/code-review` (built in) | correctness pass before the judge |

## Habits that hold in every stage

**Goal first.** Your first message on a change states, in your own words, the user's goal, the problem
behind it, and the smallest change you expect to meet it. Don't wait for confirmation. If the evidence
rules out the change that was asked for, show the evidence and stop. Open the final report with the goal
too, and restate it in every subagent brief, because a subagent that doesn't know the goal optimises
for its own reading of the task.

**Lean code.** When one of these situations comes up, read its file in `references/principles/` (beside
this file) before acting; each is short, and the bullets below are only their gist.

| Situation | File |
| --- | --- |
| choosing a data shape, or code that branches a lot | `model-the-domain.md` |
| sizing a diff, tempted to add a layer or an abstraction | `laziness-protocol.md` |
| sequencing an addition, refactor or rewrite | `subtract-before-you-add.md` |
| debugging, or a fix that adds a guard | `fix-root-causes.md` |
| writing, changing or keeping a test | `test-behavior-not-implementation.md` |
| wiring validation, error handling or a framework adapter | `boundary-discipline.md` |
| a second fix on the same premise has failed the same gate | `attack-the-premise.md` |
| about to call a step done or say something works | `prove-it-works.md` |

- Name the data shape before writing logic. Encode the domain in a structure (a table or registry, a
  state machine, a typed model) instead of conditionals scattered across files.
- Subtract before you add. Delete dead weight first; the smallest change that meets the criteria wins.
- Fix root causes. Trace a symptom to the first place the system went wrong. A guard is a fix only when
  the state it handles is legitimate.
- Test behaviour, not implementation. Assert what a user of the code can observe, so the test fails
  when that breaks and survives a refactor. Shared behaviour is tested once at its own layer; each
  host gets one wiring test.
- Guard at the boundary. Validate where data enters the system, trust it inside, keep logic pure.
- Attack the premise. After two failed fixes that assume the same thing, write that assumption down and
  test it before a third.
- Prove it works on the real artifact: run it, read the actual value. Not a proxy, not "it compiles".

When a principle changed a decision, name it and the choice it changed, in the reply that reports that
decision. Cite only files you read in this session.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an
approach, give your real judgment. Decline or push back when that is true; agreement is not the default.

**Evidence-labelled replies.** Short declarative sentences. Every claim carries its evidence or its
label in the same sentence: measured (with the command or file:line), inferred, or guess. Never hand the
user a check you could run yourself.

## 0. Intake (stop)

1. If the branch or request names a ticket, fetch it (the project's tracker tool) and any business
   rules the project's `CLAUDE.md` points to. With no ticket, the request is the source: ask only
   what the plan can't be written without, and name the feature folder after the change.
2. If `.specs/STATE.md` has a `## Handoff`, name the feature it describes and ask whether to read it.
3. Restate the goal (above).
4. Recommend a size with one line of why, and ask the base branch the PR will target. Ask both in one
   question; never assume the base, it decides the diff every later stage reads.

| Size | When | Plan artifact | Validate |
| --- | --- | --- | --- |
| **XS** | config, copy, a one-liner, no new branch of behaviour | none, the goal statement is the plan | project tests for touched files + `/code-review low` |
| **S** | roughly under 3 files, no one-way door | `request.md` with the answers, no `plan.md` (tlc-spec-lean's short path) | full gate |
| **M/L** | anything bigger, or any one-way door | full `plan.md` | full gate |

Write size, base branch and current stage to `.specs/features/<feature>/sail.md` (S and up) as soon as
they are decided, and rewrite the stage as each stage and each Validate step starts (for example
`stage: validate/4-judge`). The chat does not survive a compaction; that file and tlc-spec-lean's files
do. On resume, `sail.md`'s stage wins over the next step `check_commit.py` or tlc-spec-lean's resume
table names: once tlc-spec-lean's fix pass is recorded they say only the report remains, while Sail
still owes Validate steps 3-8.

## 1. Plan (stop)

Run tlc-spec-lean's Plan phase as its references say (for S, its short path in `request.md`), with
these additions:

- In the plan, name the data shape and its organising structure before the path.
- When a question is a fact you could observe by running something (behaviour, output, layout), run a
  throwaway sketch and let the result answer it. Ask the user only for product or preference calls.
  When the change maps another service's response to something the user sees, read what that service
  actually returns at that moment before writing the branch.
- Propose the trimmed test list with the plan, before writing any test: one test may settle several
  criteria that share a setup.

XS skips this phase.

## 2. Build (stop per commit)

Run tlc-spec-lean's Build phase. Ask before every `git commit`; an approved plan authorises edits, not
commits. Before each commit, strip comments that restate the code: keep only a non-obvious why.

The build is not done until the change has run live: each screen used and each route the change adds
or changes probed as an allowed and a refused caller, on the `**Walked:**` line (tlc-spec-lean's rule
8 and `references/build.md`). Start the app the way the project's `CLAUDE.md` says; if it cannot start,
hand the user the steps and the exact requests and say so on the line. `check_commit.py` names what the
feature still owes after each commit.

## 3. Validate

**XS:** run the project's tests for the touched files, plus the shared-output search in step 1 below
if the change touches shared code, then `/code-review low` (chat only). If the
change reaches a screen or a route, look at it in the running app or send it one request, and say
what came back; no file, no gate. Fix real bugs, then go to PR. The review bot on the PR is the
backstop.

**S, M/L:** in this order, each step on the code the previous one left.

0. Rebase onto the base branch and bring the test environment up to date with it (dependencies,
   schema). Every later step runs on that `HEAD`; a rebase after them makes their results stale.
   The walk ran before the rebase: if the rebase resolved a conflict or brought in changes to a
   screen, route or shared code the walk went through, walk or probe that part again and add it to
   `**Walked:**`; otherwise write `predates rebase onto <base> at <hash>, nothing it touched changed`
   on that line.
1. If the diff changes something many callers share (an error handler, a serializer, middleware, a
   response shape), search the whole test suite for what callers observe (an error code, a field name,
   a message) and run every file that matches. The plan's tests cover only what the plan named.
2. tlc-spec-lean's Review, exactly as `references/review.md` says: `**Walked:**` written, the
   `**Review:**` line, then a fresh sub-agent with its fixed prompt. Add nothing to that prompt, not the
   goal and not your notes; its independence is the point. Then its one fix pass and the `**Fix pass:**`
   line, asking before the commit.
3. `/code-review medium <branch>`, no `--comment`, no `--fix`. Use `high` only for money, auth,
   migrations or data. The tree is clean by now, so its default target, the current diff, may be
   empty: name the branch, and check that the files it reviewed match
   `git diff --stat <base>...HEAD`. Fix real bugs, ask before committing.
4. `the-judge` over the local branch, chat only. There is no PR yet: replace its Step 0 `gh` calls with
   `git diff <base>...HEAD` and treat it as round 1. In its Step 1, run the bypass scan as
   `git diff <base>...HEAD | python3 <skills>/the-judge/scripts/scan_bypasses.py`; its `scripts/`
   path is relative to the-judge's folder, not the project. Write its summary and findings in the
   chat only, with no `findings.json` in the repo, and skip its Gate and Post steps. Its findings
   never go on any PR, not even later; it is the user's private check.
5. One `ship:verifier` subagent at the same `HEAD`. Brief: the goal, the feature, the diff range, and
   the judge's findings as claims with evidence pointers (not the judge's reasoning). No other
   subagents.
6. Spot-check any new evidence the verifier cites, then fix what it CONFIRMED and what it found, in
   commits. Report the judge result and the verifier's verdict table together.
7. If a fix in steps 3-6 changed behaviour, run the project's tests for the touched files and walk or
   probe again what it touched, adding to `**Walked:**`, then one more verifier round scoped to the new
   commits. Two rounds at most, unless a remaining gap can reach a user; a surviving mutant on a path no
   user reaches is a note, not a failure. tlc-spec-lean's review is not sent again.
8. The repo's own test, build and lint commands pass at `HEAD`, and the last `check_commit.py` names
   only the report for the feature. Open the report with that; a red command is said first.

If the change is security work and the project defines a security gate skill, run it after step 8;
its NO-GO stops the PR.

## 4. PR (stop before push)

Ask before `git push`. Then:

- Open the PR **as a draft** against the base from intake, title and body per the project's convention
  and PR template. Fill the template; leave out empty sections and any generated-by footer.
- Assign the user (`--assignee @me`). If the project's `CLAUDE.md` or the user's memory names a
  review-bot trigger comment, post it; otherwise skip this step.
- The Testing section is click-through steps for the reviewing developer, not a list of automated tests.
  Write it from `**Walked:**`: the same steps and requests, with what the reviewer should see.

List follow-ups (out-of-scope findings, residual risks) in the final report. Raise them in the tracker
only after the user agrees, and never add scope to a ticket that is already in review, test or done:
use an open ticket or a new one.

Then ask once whether to write a `## Handoff` into `.specs/STATE.md` (PR state, pending reviews, flaky
tests, next step).

## Final report

Open with the goal. Then: what changed, the size and why, what ran live (walked, probed, or handed to
the user), the commands' result at `HEAD`, the reviewer's verdict and what its fix pass changed, the
judge and verifier verdicts (what was fixed, what was refuted),
the principles that changed a decision, open decisions, and the PR link. Every claim labelled.

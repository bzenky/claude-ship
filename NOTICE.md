# Third-party notices

`ship` bundles the skills below. Each keeps its own license; the MIT license in [LICENSE](LICENSE)
does not apply to them.

## tlc-spec-lean

- **Path:** `skills/tlc-spec-lean/`
- **Author:** Tech Leads Club, https://github.com/tech-leads-club. Derived by its authors from
  tlc-spec-driven 3.3.0 (Felipe Rodrigues), tlc-plan and tlc-implement.
- **Source:** https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/%28development%29/tlc-spec-lean
- **Version bundled:** 3.2.0, changed here and marked `3.2.0-ship.1` (not an upstream release)
- **License:** CC-BY-4.0, https://creativecommons.org/licenses/by/4.0/
- **Changes:**
  - `disable-model-invocation: true` added to the `SKILL.md` frontmatter, so the bundled copy runs
    only by name or through `/ship:sail`.
  - A live walk and route probes are required before the review is sent: rule 8 and the route
    clause in rule 4 of `SKILL.md`, the `## Routes` and `## Walked` sections of
    `references/build.md`, the `**Walked:**` line in `references/plan.md`'s template and the
    GraphQL row format in its Surface section, the precondition in `references/review.md`, the
    resume row in `references/memory.md`, wider screen detection and `plan_routes`,
    `plan_owes_walk` and `walked` in `scripts/lean_config.py`, the walk step in
    `scripts/check_commit.py`'s next-step output, and matching `scripts/selftest.py` cases.

## the-judge

- **Path:** `skills/the-judge/`
- **Author:** Felipe Rodrigues, https://github.com/felipfr
- **Source:** https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/%28quality%29/the-judge
- **Version bundled:** 1.4.0
- **License:** CC-BY-4.0, https://creativecommons.org/licenses/by/4.0/
- **Changes:** `disable-model-invocation: true` added to the `SKILL.md` frontmatter, as above.
  `/ship:sail` also runs it before a PR exists and never lets it post; that override lives in
  `skills/sail/SKILL.md`, not in this copy.

## pstack principles

- **Path:** `skills/sail/references/principles/`
- **Author:** Lauren Tan, pstack 0.15.44, https://github.com/cursor/plugins/tree/main/pstack
- **License:** MIT, copy in `skills/sail/references/principles/LICENSE`
- **Files:** `model-the-domain`, `laziness-protocol`, `subtract-before-you-add`, `fix-root-causes`,
  `test-behavior-not-implementation`, `prove-it-works`, `attack-the-premise`, `boundary-discipline`,
  each from pstack's `principle-<name>` skill.
- **Changes:** YAML frontmatter removed, since they are read as references, not skills. Text
  otherwise unchanged.
- **Also adapted, no files:** from pstack's poteto-mode, rewritten in `skills/sail/SKILL.md`: the
  goal-first restatement, the evidence-labelled reply style, naming the principle that changed a
  decision, and "no is an acceptable answer".

## Updating a bundled skill

Replace its folder with the new upstream version, re-apply the change listed above, update the
version here, and check that `skills/sail/SKILL.md` still names the right scripts and steps.

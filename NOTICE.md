# Third-party notices

`ship` bundles the skills below. Each keeps its own license; the MIT license in [LICENSE](LICENSE)
does not apply to them.

## tlc-spec-lean

- **Path:** `skills/tlc-spec-lean/`
- **Author:** Tech Leads Club, https://github.com/tech-leads-club. Derived by its authors from
  tlc-spec-driven 3.3.0 (Felipe Rodrigues), tlc-plan and tlc-implement.
- **Version bundled:** 2.2.0
- **License:** CC-BY-4.0, https://creativecommons.org/licenses/by/4.0/
- **Changes:** `disable-model-invocation: true` added to the `SKILL.md` frontmatter, so the bundled
  copy runs only by name or through `/ship:sail`. No other change.

## the-judge

- **Path:** `skills/the-judge/`
- **Author:** Felipe Rodrigues, https://github.com/felipfr
- **Version bundled:** 1.4.0
- **License:** CC-BY-4.0, https://creativecommons.org/licenses/by/4.0/
- **Changes:** `disable-model-invocation: true` added to the `SKILL.md` frontmatter, as above.
  `/ship:sail` also runs it before a PR exists and never lets it post; that override lives in
  `skills/sail/SKILL.md`, not in this copy.

## pstack principles

- **Path:** `skills/sail/references/principles/`
- **Author:** Lauren Tan, pstack 0.15.36, https://github.com/cursor/plugins/tree/main/pstack
- **License:** MIT, copy in `skills/sail/references/principles/LICENSE`
- **Files:** `model-the-domain`, `laziness-protocol`, `subtract-before-you-add`, `fix-root-causes`,
  `test-behavior-not-implementation`, each from pstack's `principle-<name>` skill.
- **Changes:** YAML frontmatter removed, since they are read as references, not skills. Text unchanged.
- **Also adapted, no files:** the goal-first restatement and the evidence-labelled reply style from
  pstack's poteto-mode, rewritten in `skills/sail/SKILL.md`.

## Updating a bundled skill

Replace its folder with the new upstream version, re-apply the change listed above, update the
version here, and check that `skills/sail/SKILL.md` still names the right scripts and steps.

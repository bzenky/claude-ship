# ship

Personal Claude Code plugin.

| Command / agent | What it does |
| --- | --- |
| `/ship:sail` | One ticket from intake to a draft PR: size, plan, checks, build, validate, PR |
| `ship:verifier` | The one independent verifier `sail` spawns at validate time |

`sail` calls `tlc-spec-lean` and `the-judge`, which must be installed in the project
(`.claude/skills/`) or in `~/.claude/skills/`.

## Install

```sh
claude plugin marketplace add bzenky/ship   # or a local path: ~/code/ship
claude plugin install ship@ship
```

## After editing

```sh
claude plugin marketplace update ship
claude plugin update ship@ship
```

Restart the Claude Code session to pick up the new version.

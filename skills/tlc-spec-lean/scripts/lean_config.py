"""
lean_config.py - what a feature's artifacts say the Verifier owes, read the same way by every gate.

Three facts decide it: whether the feature has a screen (the screen comparison and the walk), which
routes plan.md's `## Surface` adds or changes (a live probe each), and whether plan.md's `## Sources`
marks a source binding (the binding-source comparison). The shape of a `Run` group and
of a proof that reads one lives here too. validate_checks.py, validate_verification.py and
check_proofs.py act on these, so they live in one place - two copies of the same rule drift until
one gate demands what the other does not.

Every function takes lines already stripped of fenced blocks.
"""

import re

RUN_RE = re.compile(r"^\**\s*Run\s+([\w-]+)\s*\**\s*:\s*(.+)$", re.IGNORECASE)
RUN_PROOF_RE = re.compile(r"^run\s+([\w-]+)\s*\|\s*(.*)$", re.IGNORECASE)
BINDING_RE = re.compile(r"(?<![-\w])binding\b", re.IGNORECASE)
NOT_BINDING_RE = re.compile(r"\b(non|not)[- ]binding\b", re.IGNORECASE)
CAPTURE_RE = re.compile(r"`([^`\s]+\.(?:png|jpe?g|webp|gif))`", re.IGNORECASE)
SCREEN_CRITERION_RE = re.compile(
    r"\bSHALL\s+(?:NOT\s+)?(?:show|display|render|hide|list|highlight|enable|disable|focus|open|navigate)\b",
    re.IGNORECASE)
GESTURE_RE = re.compile(
    r"\bWHEN\b[^,]*?\b(?:clicks?|taps?|selects?|chooses?|drags?|drops?|hovers?|scrolls?|presses?|types?|toggles?)\b",
    re.IGNORECASE)
SCREEN_NOUN_RE = re.compile(r"\b(?:page|screen|modal|dialog|button|dropdown|tooltip|toast|sidebar)s?\b", re.IGNORECASE)
ROUTE_RE = re.compile(r"(/[A-Za-z0-9_\-/:{}.]*)")
GRAPHQL_OP_RE = re.compile(r"\b(?:query|mutation|subscription)\s+`?([A-Za-z_]\w*)", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"^\s*[\[<].+[\]>]\s*$")
PROOF_RE = re.compile(r"^\**\s*Proof\s*\**\s*:\s*`?browser\b", re.IGNORECASE)
CRITERION_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
APPROVED_RE = re.compile(
    r"^\**\s*Approved\s*\**\s*:\s*\**\s*\d{4}-\d{2}-\d{2}\b.*\buser\s*:\s*[\"“][^\"”]*\S[^\"”]*[\"”]",
    re.IGNORECASE)


def plan_approved(plan_lines):
    """True when plan.md carries `**Approved**: <date> - user: "<their words>"`. The approval is the
    user's, so it carries their words; the chat that held it does not survive a compaction."""
    return any(APPROVED_RE.match(s.strip()) for s in plan_lines)


def read_runs(lines):
    """{name: command} for every `Run <name>: <command>` line."""
    runs = {}
    for ln in lines:
        m = RUN_RE.match(ln.strip())
        if m:
            runs[m.group(1)] = m.group(2).strip().strip("`").strip()
    return runs


def _section(lines, name):
    """The lines under a `#`/`##` heading named `name`, up to the next `#`/`##` heading."""
    out, inside = [], False
    for ln in lines:
        s = ln.strip()
        if re.match(r"^#{1,2}\s+\S", s):
            inside = re.match(r"^#{1,2}\s+" + re.escape(name) + r"\b", s, re.IGNORECASE) is not None
            continue
        if inside:
            out.append(s)
    return out


def plan_criteria(plan_lines):
    """The text of every numbered criterion under `## Criteria`."""
    out = []
    for s in _section(plan_lines, "Criteria"):
        m = CRITERION_RE.match(s)
        if m:
            out.append(m.group(1))
    return out


def plan_has_screen(plan_lines, checks_lines=()):
    """True when the feature puts a screen in front of a user.

    A criterion that cites a capture, says the system SHALL show, display, list, open... something,
    has someone click, select, drag or type, or names a page, screen, modal or button is a screen
    criterion; so is a `browser` proof in checks.md. A false positive costs one walk; a miss ships
    a screen nobody opened.
    """
    for text in plan_criteria(plan_lines):
        if any(r.search(text) for r in (CAPTURE_RE, SCREEN_CRITERION_RE, GESTURE_RE, SCREEN_NOUN_RE)):
            return True
    return any(PROOF_RE.match(s.strip()) for s in checks_lines)


def plan_owes_pictures(plan_lines, checks_lines=()):
    """True when the feature owes running pictures: a criterion cites a capture, or a check is
    proven in the browser. A screen state no capture draws is proven by a test or a walk."""
    if any(CAPTURE_RE.search(text) for text in plan_criteria(plan_lines)):
        return True
    return any(PROOF_RE.match(s.strip()) for s in checks_lines)


def plan_routes(plan_lines):
    """Each route plan.md's `## Surface` table names: the GraphQL operation when the row names one,
    since every operation shares one path, else the path."""
    routes = []
    for s in _section(plan_lines, "Surface"):
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        first = cells[0] if cells else ""
        if not first or first.lower() == "route" or set(first) <= set("-: ") or PLACEHOLDER_RE.match(first):
            continue
        m = GRAPHQL_OP_RE.search(first) or ROUTE_RE.search(first)
        if m:
            routes.append(m.group(1))
    return routes


def plan_owes_walk(plan_lines, checks_lines=()):
    """True when green tests are not enough: a person reaches a screen, or a caller reaches a route.
    The author then opens the running app or probes the running service and logs it on `**Walked:**`."""
    return plan_has_screen(plan_lines, checks_lines) or bool(plan_routes(plan_lines))


def plan_marks_binding(plan_lines):
    """True when plan.md's `## Sources` marks a source binding (the binding-source comparison runs)."""
    return any(BINDING_RE.search(s) and not NOT_BINDING_RE.search(s) for s in _section(plan_lines, "Sources"))

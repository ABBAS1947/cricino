# Project onboarding: the AI asks, then configures

This is the questionnaire for an AI implementing Cricino. Use concise conversation,
not a huge form. Ask in three small rounds, skip questions already answered in
trusted context, and explain unfamiliar concepts plainly. Offer sensible choices
without treating a default as owner approval.

## Round 1 — Goal, scope and existing knowledge

Ask missing questions:

1. What does this project do, who is it for, and what is the current milestone?
2. Which repository/directories are included, and what must remain untouched or on hold?
3. Where should plans, decisions and research live: existing wiki/docs, or repository Markdown? What existing records remain authoritative?

Inspect named records narrowly. Do not ask the owner to remember every prior
decision: retrieve what is available and ask about gaps/conflicts. Preserve
existing goals and holds. Record unknown facts explicitly.

## Round 2 — Authority and working style

Ask missing questions:

1. Which actions require approval: implementation, gate review, tests, external writes, commits and releases? Which have standing authorization, and within what boundaries?
2. What are the core UX/engineering principles and current quality priorities?
3. Who reviews high-risk changes, and should knowledge maintenance happen only during sessions or under separately approved automation?

Record distinct decisions. Installation does not authorize background jobs,
application tests, credentials, integrations, production access or publishing.
If enforcement is undecided, record instructions-only/advisory status; do not
imply merge protection.

## Round 3 — A gate for this project

Ask missing questions:

1. Is there an existing gate? Where is it and who can change it?
2. Which jurisdictions, audiences, ages, organizational contexts, data categories and providers apply? Which obligations/contracts are already known?
3. What evidence, approval sequence and release criteria should this project require?

Use [templates/gate.md](templates/gate.md) only as a structure. Never import
Pixie's requirements or verdicts. If the owner is unsure, create a clearly labeled
**draft with unresolved applicability**, explain missing decisions, and ask for
adoption before treating it as an active gate. Research, gate definition and
application review are different operations; obtain appropriate scope for each.
Do not request secrets or personal user records.

## Configure after answers

The AI writes the scoped operating contract, current-state snapshot, links to
canonical decisions/research/holds, approval policy and setup checkpoint. It
adapts the scaffold automatically; the owner does not need to copy files manually.
Relevant gate adoption may remain pending without blocking independent setup.

Add a short decision record containing actual owner choices and their source.
Record unresolved questions, not fabricated answers. Sanity-check changed files
and links. Report installed paths, active/advisory controls and next action.

### Completion boundary

Installed means records and the instruction pointer exist. Adapted additionally
means verified context and approved operating decisions are recorded. Enforced
requires verified independent controls. Never conflate these states.

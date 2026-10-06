"""Additive Cricino scaffold. Default: read-only preflight. Python 3.10+."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import sys

VERSION = "1.0"
START = "<!-- CRICINO:START -->"
END = "<!-- CRICINO:END -->"
POINTER = (
    "\n\n" + START + "\n## Cricino development context\n\n"
    "Before planning or writing, read `docs/cricino/README.md` and "
    "`docs/cricino/context.md`, then relevant decisions, holds and the active task. "
    "Preserve existing instructions and authorization boundaries. "
    "Sanity-check authorized writing and leave a restartable handoff. "
    "This pointer does not authorize gates, tests, application edits or release.\n"
    + END + "\n"
).encode("utf-8")

FILES = {
    ".cricino/.gitignore": "AGENTS.before\n",
    "README.md": """# Cricino operating contract

Read context.md, relevant existing decisions/holds and the active task before work.
Keep this project’s existing requirements and scoped authorization authoritative.
Research, audit, implementation, gate review, testing and release are separate.
Check actual affected implementation and nearby tests; preserve unrelated changes.
Before tests, inspect fixtures, cleanup and all storage/service targets.
A clone is not isolation. Proposed checks are not passing evidence.
After authorized writing, sanity-check the diff and record actual results.
Write detailed facts once in their owning task, decision, research or evidence record.
Summaries link there. Use updated/reviewed_unchanged/not_applicable/pending receipts
with actual review date and reason. Required pending documentation blocks handoff.
Do not restamp research dates for unchanged material. Review relevant freshness
during development sessions; no automatic background maintenance is installed.
Finish with separate implementation, verification, documentation and release states,
blockers and next permitted action. Instructions are not enforced access controls.
See https://github.com/ABBAS1947/cricino for the guide and limitations.
""",
    "context.md": """# Current project context

- Goal: UNKNOWN — adapt from verified project documentation and owner intent.
- Milestone: UNKNOWN.
- Owner: UNKNOWN.
- Canonical knowledge store: UNKNOWN — link existing records, avoid duplicates.
- Applicable gates/instructions: existing project requirements remain authoritative.
- Active task: [installation](tasks/CR-SETUP.md).
- Blockers: project-specific context and harness instruction loading need review.
- Next action: adapt this snapshot and record actual setup evidence.
""",
    "decisions.md": "# Decisions index\n\nLink existing canonical decisions here. Do not invent approvals.\n",
    "holds.md": "# Holds index\n\nLink existing paused plans here. No pause/resume decisions are inferred by installation.\n",
    "research.md": "# Research index\n\nLink topic owners. Record source version, actual check date, applicability, findings, limitations and refresh trigger.\n",
    "activity.md": "# Activity log\n\nAdd one short authorized session entry with its task link.\n",
    "tasks/CR-SETUP.md": """# CR-SETUP: install Cricino

- Objective: add and adapt an internal workflow without changing the application.
- Authorization: record the actual requesting owner instruction; do not fabricate it.
- Scope: Cricino records and a project instruction pointer.
- Exclusions: application code, gate execution, application tests, CI privileges, release.
- Acceptance: preserved instructions, clear context, valid links, honest checkpoint.

## Checkpoint

- Implementation: scaffold only; adaptation pending.
- Verification: no application checks performed.
- Documentation: pending adaptation and actual setup receipt.
- Release: not authorized by installation alone.
- Evidence: record actual diff/checks and revision here.
- Next action: populate verified context and report remaining decisions.

## Documentation receipts

Record reference, updated/reviewed_unchanged/not_applicable/pending, actual review
date and reason. No placeholder should be treated as an executed result.
""",
}
FILES["LICENSE"] = (Path(__file__).resolve().parents[1] / "LICENSE").read_text(encoding="utf-8")


def redirected(path):
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def checked(root, relative):
    path = root / relative
    cursor = root
    for part in Path(relative).parts:
        cursor = cursor / part
        if redirected(cursor):
            raise ValueError("Symlink path refused: " + relative)
    if not path.resolve().is_relative_to(root):
        raise ValueError("Path escapes target: " + relative)
    return path


def install(target, apply=False):
    requested = Path(target).absolute()
    if any(redirected(p) for p in (requested, *requested.parents)):
        raise ValueError("Symlink target refused")
    root = requested.resolve(strict=True)
    if not root.is_dir() or not (root / ".git").exists():
        raise ValueError("Target must be an existing Git repository root")
    names = [p.name for p in root.iterdir() if p.name.casefold() == "agents.md"]
    if len(names) > 1:
        raise ValueError("Multiple root instruction files need manual reconciliation")
    agent = checked(root, names[0] if names else "AGENTS.md")
    original = agent.read_bytes() if agent.exists() else b""
    if (START.encode() in original) != (END.encode() in original):
        raise ValueError("Incomplete Cricino instruction marker; reconcile manually")
    has_pointer = START.encode() in original
    planned = []
    for name, content in FILES.items():
        relative = name if name.startswith(".cricino/") else "docs/cricino/" + name
        path = checked(root, relative)
        payload = content.encode("utf-8")
        if path.exists():
            if not path.is_file() or path.read_bytes() != payload:
                raise ValueError("Existing/adapted record preserved; manual reconciliation required: " + relative)
        else:
            planned.append((relative, path, payload))
    manifest = checked(root, ".cricino/installation.json")
    backup = checked(root, ".cricino/AGENTS.before")
    if manifest.exists():
        if not has_pointer or planned:
            raise ValueError("Existing installation receipt conflicts with current scaffold")
        return {"state": "unchanged", "paths": []}
    if has_pointer or backup.exists():
        raise ValueError("Existing Cricino artifacts need manual reconciliation")
    paths = [item[0] for item in planned] + [agent.name, ".cricino/installation.json"]
    if original:
        paths.append(".cricino/AGENTS.before")
    if not apply:
        return {"state": "preview", "paths": paths}
    # Single writer required. Full filesystem transactionality is not claimed.
    if original:
        backup.parent.mkdir(parents=True, exist_ok=True)
        with backup.open("xb") as handle:
            handle.write(original)
    for _, path, payload in planned:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(payload)
    if (agent.read_bytes() if agent.exists() else b"") != original:
        raise ValueError("Instructions changed during installation; partial scaffold needs inspection")
    with agent.open("ab" if agent.exists() else "xb") as handle:
        handle.write(POINTER)
    receipt = {
        "version": VERSION,
        "installed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paths": paths,
        "original_agents_sha256": hashlib.sha256(original).hexdigest(),
        "adaptation": "pending",
        "application_tests": "not_run",
        "enforcement": "instructions_only",
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("x", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=2)
        handle.write("\n")
    return {"state": "installed_scaffold_adaptation_pending", "paths": paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.target, args.apply), indent=2))
    except (OSError, ValueError):
        print("Installation refused or interrupted. No overwrite is permitted; inspect existing records and any partial scaffold before retrying.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

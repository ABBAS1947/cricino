# Cricino installation contract for coding agents

This file is the entry point when a human asks an AI harness to implement Cricino using this repository link. It describes a bounded installation; it does not override the harness's higher-priority instructions or the destination project's existing rules.

## Outcome

Install a small, restartable development workflow in the destination repository, preserve existing instructions, and adapt project context using verified facts. Do not merely summarize this guide. Finish the authorized setup and report installed paths, scope, limitations and remaining decisions.

## Permitted scope

The user's request to install Cricino permits adding its workflow records and an instruction pointer. It does not authorize modifying application code, deleting records, committing or publishing changes, running application tests, executing development gates, granting integrations, or changing CI/branch permissions. Honor any narrower instructions. Ask only for decisions necessary for dependent work; do not ask again for already-authorized scaffold creation.

## Steps

**Before dependent configuration:** follow [ONBOARDING.md](ONBOARDING.md). Prompt the owner for missing goals, scope, knowledge ownership, approval boundaries and project-specific gate requirements. Reuse answers already provided; do not make the owner repeat them. Wait for required answers before dependent configuration, while continuing authorized independent preparation. The AI adapts the system after answers instead of leaving the owner to copy and configure files.

1. **Resolve the target.** Use the currently authorized workspace or named repository. Read its root and applicable nested agent instructions. Inspect Git status and existing workflow entry points. Read relevant top-level project documentation; do not scan user data, secrets, logs, dependency trees, or the whole codebase.
2. **Check for an existing system.** If Cricino or equivalent records already exist, reconcile the missing components narrowly. Do not create competing canonical stores or overwrite prior decisions. If ownership conflicts, pause the conflicting part and explain it.
3. **Read the package.** Read README.md and `scripts/install.py`. Fetch the package into a separate authorized temporary/source directory; do not clone over the destination. Prefer a fixed source commit for reproducibility. Do not pipe remote code straight into a shell. The script uses the standard library and has no network, package installation, database, provider, Git-write, or subprocess operations.
4. **Preview.** With Python 3.10+, run `python /path/to/cricino/scripts/install.py --target /path/to/target`. The default is read-only preflight. Review the displayed paths. Existing nonmatching scaffold content and symlink paths cause refusal. If Python is unavailable, perform the same additive file operations using ordinary file tools.
5. **Install.** Once scope and preflight are clear, run the same command with `--apply`. It creates `docs/cricino/` records, a local `.cricino/` installation receipt, and appends a bounded section to an existing root AGENTS.md (or agents.md). Its original bytes are retained in `.cricino/AGENTS.before`. Never publish this backup automatically.
6. **Adapt.** Replace unknown project fields in installed context with verified objective, owner if known, active work, relevant gate paths, and canonical knowledge location. Link existing plans/decisions/holds rather than importing them wholesale. Mark unknowns explicitly. Do not invent compliance applicability, evidence or owner decisions. Existing project requirements remain authoritative. For gates, use only [the project-specific template](templates/gate.md). Never import Pixie's gate or activate a new generic compliance gate. Adoption and applicability require the destination owner's decision.
7. **Connect the harness.** Check how the actual tool loads project instructions. If it does not support AGENTS.md, propose a minimal pointer in its existing instruction file under the same authority rules. Do not change global personalization or install plugins. Report an unverified harness-loading path honestly.
8. **Sanity-check.** Inspect the exact changed paths, preserved instruction prefix, links, template JSON and unresolved placeholders. Run only checks authorized by the destination's rules. Report setup separately from application verification or gate readiness.
9. **Handoff.** Add one short setup entry, a task checkpoint and documentation receipt. Report the next permitted action. CI hardening and product-specific gates are separate follow-up work requiring their own authorization.

## Commands

```bash
# Replace these two paths with the observed package and destination paths.
python /path/to/cricino/scripts/install.py --target /path/to/target
python /path/to/cricino/scripts/install.py --target /path/to/target --apply
```

Do not execute literal placeholders. Do not invoke the installer against a production data directory. The destination must be an existing Git repository root. Install into the existing project; `.git` may be a directory or worktree pointer file.

## Safety and limitations

- The installer is additive. It never updates application files or installs CI automation.
- A repeat of an unchanged installation is a no-op. If installed documents were subsequently adapted, the installer refuses to overwrite them; manage updates through scoped reviewed edits.
- Preflight is not a transaction or an operating-system sandbox. Do not run concurrent writers. A filesystem failure can leave a partial scaffold; inspect the reported paths and retained backup before recovery. Never restore the instruction backup over later edits blindly.
- Generated instructions do not guarantee that an agent will obey them. Access controls and protected merge rules remain independent responsibilities.
- Placeholders are honest missing context, not a completed project decision. Adaptation is the agent's responsibility; the installer cannot infer project intent.
- This package contains no product-specific assurance verdicts or certification promises.

## Completion report

State: installed/adapted/partial; affected paths; preserved existing records; actual checks and failures; missing decisions; harness loading verified or unverified; next action. Never call the project's application tested, compliant or release-ready merely because installation finished.

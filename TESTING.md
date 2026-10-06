# Verification scope

Release checks on October 6, 2026 used Python 3.11 on Windows and disposable
filesystem targets only. No application fixtures, databases, external providers
or user storage were used. Linux/macOS execution and installation by another
AI harness have not been demonstrated.

Final outcome: 12 isolated installer tests passed. Python syntax, JSON and local
document links passed the scoped sanity checks. No application gate was executed.

Run the isolated installer suite from this package root:

```bash
python -m unittest discover -s tests -v
```

The cases cover read-only preview, preserving original instruction bytes,
unchanged repeat installation, conflict refusal before writes, lowercase root
instructions, non-repository refusal, incomplete markers, preserving adapted
records, path-escape refusal, Git worktree pointer recognition, a simulated
redirected-path refusal, and license/backup-ignore creation.

Redirected-path refusal is a simulated policy check, not a demonstrated native
symlink/junction attack. Concurrent mutation, abrupt interruption, disk-full
recovery and arbitrary hostile filesystem layouts are not fully tested.

The first sandbox attempt failed because Windows denied access inside generated
temporary directories. The suite was rerun successfully with approved access
to fresh disposable runtime directories. An environment failure is not a pass.

Public-package sanity checks inspect Python syntax, template JSON, relative
document links, fenced blocks, diagram count and selected private-path/secret
markers. Marker checks are not a comprehensive secret scanner or security audit.
The guide's original private-workflow verification is separate from this suite.

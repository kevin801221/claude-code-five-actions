# Working on this repository

- Preserve the original course body in docs/guide.zh-TW.md and its author credit. Propose factual corrections separately.
- Follow MAINTENANCE.md. A changed upstream fingerprint is a review signal, not proof a claim or command is valid.
- For code changes, demonstrate the failing condition before the fix. Keep intentional buggy fixtures intact.
- Run python3 scripts/check_repo.py before claiming completion. Requires Python 3.11+ and Node.js 20+; no package install or model key.
- Report what was executed and what remains outside the checks. Do not label a source-only review as live Claude integration.
- Never copy personal paths, credentials, or private session data into examples.
- GitHub identity: kevin801221, kevin801221@users.noreply.github.com; personal push remote uses github-personal SSH.

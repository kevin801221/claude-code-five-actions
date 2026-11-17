# Maintained five-actions guide implementation plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the illustrated course useful on first visit and maintain it with repeatable evidence and upstream review.

**Architecture:** Keep the original course intact under docs/. Add a short bilingual entry, five reusable templates, a runnable scroll example, and dependency-free checks. GitHub Actions verifies changes and monitors explicitly tracked upstream sources weekly; changes create a review issue rather than silently updating verified claims.

**Tech Stack:** Markdown, Python 3.11+, Node.js 20+, GitHub Actions. No model API key or package installation is required for the checks.

## Task 1 — Prove the scroll acceptance test catches regressions

Create examples/scroll-drift/acceptance.test.mjs first. Run it against an initial deliberately drifting policy and capture the expected idle failure. Implement policy.mjs with buggy, overfixed, and fixed variants, then verify all three against the same acceptance contract. Create verify.mjs and browser demo index.html; only the fixed variant may pass all acceptance tests. Commands: node --test examples/scroll-drift/acceptance.test.mjs; node examples/scroll-drift/verify.mjs.

## Task 2 — Deliver the guide and starter pack

Move the complete original README to docs/guide.zh-TW.md, adjusting only image paths and adding a clearly separated archive note. Create README.md, README.en.md, docs/quickstart.md, docs/comparison.md, docs/verification.md, templates/SPEC.md, templates/EVIDENCE.md, templates/REVIEW.md, templates/LESSONS.md and templates/boundaries/README.md. Preserve author credit and original images. Check that the original course text remains intact after reversing image path changes.

## Task 3 — Encode checks and boundaries

Write subprocess tests for the Stop wrapper first: success returns 0; failure, missing command, and timeout return 2 with useful stderr and no control JSON on stdout. Implement scripts/stop_hook.py, an optional settings.example.json, and scripts/check_repo.py for Markdown destinations, JSON syntax, original-course integrity, and the complete acceptance demo. Run python3 -m unittest discover -s tests -v and python3 scripts/check_repo.py.

## Task 4 — Make maintenance executable

Write tests for source drift, missing baselines, failed retrievals, and recovery from outages before implementing scripts/watch_sources.py and scripts/report_upstream.py. Track official docs and upstream README revisions in maintenance/sources.json with an initial observed baseline. Add .github/workflows/check.yml and maintenance.yml, issue forms, CONTRIBUTING.md, MAINTENANCE.md, ATTRIBUTION.md, CHANGELOG.md and ROADMAP.md. Schedule weekly at Monday 09:17 Asia/Taipei; monitor issues are deduplicated and do not rewrite source baselines or grant automatic verification.

## Task 5 — Review, publish, and verify remotely

Run local checks and original-text preservation checks; obtain an independent review and address correctness gaps. Push a feature branch using the verified personal SSH remote, open a PR, wait for Actions, and merge only after checks pass. Add accurate repository topics and description, publish a release describing implemented features, and manually run maintenance once. Verify default branch contents, CI, and the maintenance report before reporting completion. Public social posts and outreach are outside this change.

# Five Moves for Reliable Coding Agents

**Turn “done” into a result you can verify.**

An illustrated Claude Code field guide with reusable templates, a runnable failure case, and an upstream review routine. The full original course is in Traditional Chinese; this page is an English entry point.

[繁體中文](README.md) · [Quick start](docs/quickstart.md) · [Verification scope](docs/verification.md)

![Humans define the goal and boundaries; agents implement, verify and review; evidence supports handoff.](images/01-cover.png)

## The five moves

1. **Define done:** write observable acceptance criteria. [SPEC](templates/SPEC.md)
2. **Verify your work:** attach commands, outputs, and limitations. [Evidence](templates/EVIDENCE.md)
3. **Review independently:** compare the result with the original requirements. [Reviewer prompt](templates/REVIEW.md)
4. **Enforce boundaries:** use appropriate environment controls. [Boundary examples](templates/boundaries/README.md)
5. **Encode lessons:** turn a repeated mistake into a check that catches it. [Lessons](templates/LESSONS.md)

## Verify the artifact and the check

The new [field notes](docs/field-notes.zh-TW.md) (Traditional Chinese) connect measurements, screenshots, and user interactions to acceptance criteria. Each important check should reject a known bad sample, rather than merely confirm that a file exists.

Use the [artifact acceptance matrix](templates/ARTIFACT-CHECKS.md) to connect each requirement to its output, negative control, and evidence. The [meeting-notes workflow](docs/cases/meeting-notes.md) and [four semiconductor scenarios](docs/cases/semiconductor.md) are **design walkthroughs, not implemented applications**. The executable fixture follows below.

## Run one case

Requires Node.js 20+. No packages or model API keys needed.

```bash
git clone https://github.com/kevin801221/claude-code-five-actions.git
cd claude-code-five-actions
node examples/scroll-drift/verify.mjs
```

The same four acceptance tests run against three deliberately constructed versions: a drifting implementation, an overcorrection that disables manual scrolling, and the complete fix. The first two MUST fail their expected assertions; only the fixed implementation passes all four. The runner checks the failing test names, not just a nonzero exit code.

[Case walkthrough](examples/scroll-drift/README.md) · [Recorded policy-test evidence](examples/scroll-drift/evidence.json)

## Maintained with evidence

PR checks validate local Markdown destinations, JSON, original-course integrity, the Stop wrapper, and the runnable acceptance case. A weekly workflow compares tracked upstream revisions and opens one deduplicated review issue on drift or retrieval failures. A changed source is **not** automatically marked verified. Browser integration and a live Claude Code session are outside the automated acceptance suite.

[Maintenance policy](MAINTENANCE.md) · [Contributing](CONTRIBUTING.md) · [Attribution and rights](ATTRIBUTION.md)

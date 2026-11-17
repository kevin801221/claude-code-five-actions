#!/usr/bin/env python3
"""Open or update one upstream review issue only when a report needs attention."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

TITLE = 'Upstream review: sources changed or unavailable'
LABEL = 'upstream-review'


def render_body(report):
    attention = [row for row in report['sources'] if row['status'] != 'unchanged']
    if not attention:
        return None
    lines = ['Upstream observation is a review signal, not verification.', '',
             'Review the affected guidance and rerun relevant examples before deliberately refreshing the baseline.', '',
             '| Source | Status | Observed fingerprint / retrieval error |', '| --- | --- | --- |']
    for row in attention:
        detail = row.get('sha256', row.get('error', 'No baseline')).replace('\n', ' ').replace('|', '\\|')
        lines.append(f"| [{row['id']}]({row['url']}) | {row['status']} | {detail} |")
    lines += ['', 'See [MAINTENANCE.md](https://github.com/kevin801221/claude-code-five-actions/blob/main/MAINTENANCE.md) for the review procedure. Keep baseline changes separate from verification claims.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--repo', required=True)
    args = parser.parse_args()
    body = render_body(json.loads(args.report.read_text()))
    if body is None:
        print('No source changes or retrieval failures; no issue created.')
        return
    subprocess.run(['gh', 'label', 'create', LABEL, '--repo', args.repo, '--color', '0E8A16',
                    '--description', 'Tracked upstream guidance needs review', '--force'], check=True)
    issues = json.loads(subprocess.check_output(['gh', 'issue', 'list', '--repo', args.repo,
                        '--state', 'open', '--label', LABEL, '--limit', '100', '--json', 'number,title,body'], text=True))
    existing = next((issue for issue in issues if issue['title'] == TITLE), None)
    if existing and existing['body'] == body:
        print('Existing upstream issue already contains this report.')
        return
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.md', delete=False) as handle:
        handle.write(body)
        path = Path(handle.name)
    try:
        if existing:
            command = ['gh', 'issue', 'edit', str(existing['number']), '--repo', args.repo, '--body-file', str(path)]
        else:
            command = ['gh', 'issue', 'create', '--repo', args.repo, '--title', TITLE, '--label', LABEL, '--body-file', str(path)]
        subprocess.run(command, check=True)
    finally:
        path.unlink()


if __name__ == '__main__':
    main()

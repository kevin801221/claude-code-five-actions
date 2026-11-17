#!/usr/bin/env python3
"""Run offline repository checks and the runnable acceptance case."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def markdown_problems(root, page):
    problems = []
    fence = None
    for number, line in enumerate(page.read_text().splitlines(), 1):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        for raw in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)\)', line):
            destination = urlsplit(raw)
            if destination.scheme or destination.netloc or not destination.path:
                continue
            path = unquote(destination.path)
            resolved = (page.parent / path).resolve()
            if path.startswith('/') or not resolved.is_relative_to(root.resolve()):
                problems.append(f'{page.name}:{number}: local path escapes repository: {raw}')
            elif not resolved.exists():
                problems.append(f'{page.name}:{number}: missing local destination: {raw}')
    if fence:
        problems.append(f'{page.name}: unclosed code fence')
    return problems


def main():
    errors = []
    pages = [p for p in ROOT.rglob('*.md') if '.git' not in p.relative_to(ROOT).parts]
    for page in pages:
        errors.extend(markdown_problems(ROOT, page))
    json_files = [p for p in ROOT.rglob('*.json') if '.git' not in p.relative_to(ROOT).parts]
    for path in json_files:
        try:
            json.loads(path.read_text())
        except (ValueError, OSError) as error:
            errors.append(f'{path.relative_to(ROOT)}: invalid JSON: {error}')
    manifest = json.loads((ROOT / 'maintenance/original-guide.json').read_text())
    guide = (ROOT / 'docs/guide.zh-TW.md').read_text().split('\n\n', 1)[1].replace('](../images/', '](images/')
    if hashlib.sha256(guide.encode()).hexdigest() != manifest['original_readme_sha256']:
        errors.append('Original course changed: preserve it and propose corrections separately.')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(pages)} Markdown files, {len(json_files)} JSON files, original course integrity.', flush=True)
    for command in [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['node', 'examples/scroll-drift/verify.mjs'],
    ]:
        try:
            subprocess.run(command, cwd=ROOT, check=True, timeout=120)
        except (subprocess.SubprocessError, OSError) as error:
            print(f'Check failed: {error}', file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

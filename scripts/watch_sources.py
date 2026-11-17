#!/usr/bin/env python3
"""Observe upstream fingerprints. A fingerprint is not a verification claim."""
import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
import os
from pathlib import Path
import urllib.request
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def request_headers(url, token=None):
    headers = {'User-Agent': 'five-actions-source-watch'}
    parsed = urlsplit(url)
    if token and parsed.scheme == 'https' and parsed.netloc == 'api.github.com':
        headers['Authorization'] = f'Bearer {token}'
    return headers


class SourceRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(request, fp, code, msg, headers, newurl)
        parsed = urlsplit(newurl)
        if redirected is not None and (parsed.scheme != 'https' or parsed.netloc != 'api.github.com'):
            redirected.remove_header('Authorization')
        return redirected


def fetch_source(source):
    request = urllib.request.Request(source['watch_url'], headers=request_headers(source['watch_url'], os.environ.get('GH_TOKEN')))
    opener = urllib.request.build_opener(SourceRedirectHandler())
    with opener.open(request, timeout=20) as response:
        body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise ValueError('Source exceeds observation size limit')
    if source['kind'] == 'github-path-revision':
        data = json.loads(body)
        return data[0]['sha'].encode('ascii')
    if not body.strip():
        raise ValueError('Empty source response')
    return body.replace(b'\r\n', b'\n')


def compare_sources(sources, baseline, fetcher=fetch_source):
    rows = []
    for source in sources:
        previous = baseline.get(source['id'], {}).get('sha256')
        row = {'id': source['id'], 'url': source['url'], 'previous_sha256': previous}
        try:
            current = hashlib.sha256(fetcher(source)).hexdigest()
            row.update(sha256=current, status='new' if previous is None else 'unchanged' if current == previous else 'changed')
        except (OSError, http.client.HTTPException, ValueError, KeyError, IndexError, TypeError) as error:
            row.update(status='unreachable', error=f'{type(error).__name__}: {error}')
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Deliberately replace the observed baseline after review')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    sources = json.loads((ROOT / 'maintenance/sources.json').read_text())
    path = ROOT / 'maintenance/upstream-baseline.json'
    baseline = json.loads(path.read_text()) if path.exists() else {}
    rows = compare_sources(sources, baseline)
    report = {'observed_at': datetime.now(timezone.utc).isoformat(), 'sources': rows}
    if args.refresh:
        if any(row['status'] == 'unreachable' for row in rows):
            raise SystemExit('Baseline not changed: at least one source is unavailable.')
        path.write_text(json.dumps({row['id']: {'sha256': row['sha256'], 'observed_at': report['observed_at'], 'url': row['url']}
                                   for row in rows}, indent=2, ensure_ascii=False) + '\n')
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

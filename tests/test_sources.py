import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import http.client
import threading
import unittest
from scripts.watch_sources import compare_sources

SOURCE = {'id': 'official', 'url': 'https://example.invalid/docs', 'watch_url': 'https://example.invalid/docs.md', 'kind': 'text'}
def digest(body): return hashlib.sha256(body).hexdigest()

class SourceTests(unittest.TestCase):
    def test_same_content_is_unchanged(self):
        rows = compare_sources([SOURCE], {'official': {'sha256': digest(b'one')}}, lambda source: b'one')
        self.assertEqual(rows[0]['status'], 'unchanged')

    def test_changed_content_needs_review(self):
        rows = compare_sources([SOURCE], {'official': {'sha256': digest(b'one')}}, lambda source: b'two')
        self.assertEqual(rows[0]['status'], 'changed')
        self.assertEqual(rows[0]['previous_sha256'], digest(b'one'))

    def test_missing_baseline_is_new_not_verified(self):
        rows = compare_sources([SOURCE], {}, lambda source: b'one')
        self.assertEqual(rows[0]['status'], 'new')

    def test_failure_is_visible_and_keeps_baseline(self):
        baseline = {'official': {'sha256': digest(b'one')}}
        def unavailable(source): raise OSError('network unavailable')
        rows = compare_sources([SOURCE], baseline, unavailable)
        self.assertEqual(rows[0]['status'], 'unreachable')
        self.assertEqual(baseline['official']['sha256'], digest(b'one'))

    def test_recovery_uses_original_baseline(self):
        baseline = {'official': {'sha256': digest(b'one')}}
        rows = compare_sources([SOURCE], baseline, lambda source: b'one')
        self.assertEqual(rows[0]['status'], 'unchanged')

    def test_truncated_http_response_is_reported_without_losing_baseline(self):
        class TruncatedHandler(BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'
            def do_GET(self):
                self.send_response(200)
                self.send_header('Transfer-Encoding', 'chunked')
                self.end_headers()
                self.wfile.write(b'64\r\npartial')
                self.wfile.flush()
                self.close_connection = True
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), TruncatedHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        baseline = {'official': {'sha256': digest(b'one')}}
        source = dict(SOURCE, watch_url=f'http://127.0.0.1:{server.server_port}/docs')
        try:
            try:
                rows = compare_sources([source], baseline)
            except http.client.HTTPException as error:
                self.fail(f'Retrieval failure escaped the monitor: {type(error).__name__}')
            self.assertEqual(rows[0]['status'], 'unreachable')
            self.assertEqual(baseline['official']['sha256'], digest(b'one'))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

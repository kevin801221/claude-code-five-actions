import hashlib
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

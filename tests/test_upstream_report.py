import unittest
from scripts.report_upstream import render_body

class UpstreamReportTests(unittest.TestCase):
    def test_clean_report_has_no_issue_body(self):
        self.assertIsNone(render_body({'sources': [{'id':'docs','status':'unchanged'}]}))

    def test_change_is_an_actionable_review_signal(self):
        body = render_body({'sources': [{'id':'docs','status':'changed','url':'https://example.invalid/docs','sha256':'abc'}]})
        self.assertIsNotNone(body)
        self.assertIn('docs', body)
        self.assertIn('changed', body)
        self.assertIn('not verification', body)

    def test_timestamp_only_does_not_change_issue_body(self):
        row = {'id':'docs','status':'unreachable','url':'https://example.invalid/docs','error':'timeout'}
        self.assertEqual(render_body({'observed_at':'one','sources':[row]}), render_body({'observed_at':'two','sources':[row]}))

import unittest
import urllib.request
from scripts.watch_sources import request_headers, SourceRedirectHandler

class SourceHeadersTests(unittest.TestCase):
    def test_workflow_token_authenticates_only_https_github_api(self):
        headers = request_headers('https://api.github.com/repos/obra/superpowers/commits', 'example-token')
        self.assertEqual(headers.get('Authorization'), 'Bearer example-token')

    def test_documentation_requests_do_not_receive_the_github_token(self):
        headers = request_headers('https://code.claude.com/docs/en/hooks.md', 'example-token')
        self.assertNotIn('Authorization', headers)

    def test_http_and_lookalike_hosts_do_not_receive_the_token(self):
        for url in ['http://api.github.com/repos', 'https://api.github.com.example.invalid/repos']:
            self.assertNotIn('Authorization', request_headers(url, 'example-token'))

    def test_redirect_to_another_host_strips_authorization(self):
        request = urllib.request.Request('https://api.github.com/repos', headers={'Authorization': 'Bearer example-token'})
        redirected = SourceRedirectHandler().redirect_request(request, None, 302, 'Found', {}, 'https://example.invalid/docs')
        self.assertIsNone(redirected.get_header('Authorization'))

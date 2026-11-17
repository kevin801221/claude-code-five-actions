from pathlib import Path
import json
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/stop_hook.py'

class StopHookTests(unittest.TestCase):
    def run_hook(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, input='{}')

    def test_success_is_allowed(self):
        result = self.run_hook('--', sys.executable, '-c', 'print("checked")')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_failing_check_is_blocking_and_keeps_evidence(self):
        result = self.run_hook('--', sys.executable, '-c', 'print("regression"); raise SystemExit(1)')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Verification blocked', result.stderr)
        self.assertIn('regression', result.stderr)
        self.assertEqual(json.loads(result.stdout)['decision'], 'block')

    def test_unavailable_command_is_blocking(self):
        result = self.run_hook('--', '/five-actions-not-an-executable')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Verification blocked', result.stderr)

    def test_timeout_is_blocking(self):
        result = self.run_hook('--timeout', '0.05', '--', sys.executable, '-c', 'import time; time.sleep(5)')
        self.assertEqual(result.returncode, 2)
        self.assertIn('timed out', result.stderr)

    def test_no_command_is_blocking(self):
        result = self.run_hook()
        self.assertEqual(result.returncode, 2)
        self.assertIn('Verification blocked', result.stderr)

from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/scroll-drift'

class AcceptanceRunnerTests(unittest.TestCase):
    def test_skipped_fixed_acceptance_cannot_be_reported_as_all_passed(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp)
            for name in ['verify.mjs', 'policy.mjs', 'acceptance.test.mjs']:
                shutil.copy2(EXAMPLE / name, destination / name)
            test = destination / 'acceptance.test.mjs'
            original = test.read_text()
            needle = "test('idle content keeps its position across ten timer ticks', () => {"
            self.assertIn(needle, original)
            test.write_text(original.replace(needle, "test('idle content keeps its position across ten timer ticks', { skip: variant === 'fixed' }, () => {", 1))
            result = subprocess.run(['node', str(destination / 'verify.mjs')], text=True, capture_output=True, timeout=20)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertNotIn('fixed: 4/4 pass', result.stdout)

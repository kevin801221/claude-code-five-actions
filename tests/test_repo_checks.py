from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.check_repo import markdown_problems

class MarkdownChecks(unittest.TestCase):
    def test_broken_local_image_is_reported(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'README.md'
            page.write_text('![figure](images/missing.png)\n')
            self.assertTrue(any('missing.png' in issue for issue in markdown_problems(root, page)))

    def test_fenced_examples_are_not_treated_as_live_links(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'README.md'
            page.write_text('```markdown\n[placeholder](missing.md)\n```\n')
            self.assertEqual(markdown_problems(root, page), [])

    def test_relative_document_with_anchor_resolves(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            (root / 'docs/guide.md').write_text('# Guide\n')
            page = root / 'README.md'
            page.write_text('[guide](docs/guide.md#guide)\n')
            self.assertEqual(markdown_problems(root, page), [])

    def test_absolute_local_path_is_rejected(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'README.md'
            page.write_text('[private](/Users/example/private.md)\n')
            self.assertTrue(markdown_problems(root, page))

"""Local link validation must cover source documents, not generated dependencies."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scripts.validate_repo as validator


class RepositoryValidationTest(unittest.TestCase):
    def test_generated_documents_do_not_break_source_link_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("[Policy](SECURITY.md)\n")
            (root / "SECURITY.md").write_text("Example policy\n")
            for directory in (".venv", "venv", "node_modules", "build", "dist"):
                path = root / directory / "dependency/README.md"
                path.parent.mkdir(parents=True)
                path.write_text("[Package documentation](missing.md)\n")
            with patch.object(validator, "ROOT", root):
                self.assertEqual(validator.validate_markdown_links(), [])
            (root / "SECURITY.md").write_text("[Missing source policy](missing.md)\n")
            with patch.object(validator, "ROOT", root):
                self.assertTrue(validator.validate_markdown_links())


if __name__ == "__main__":
    unittest.main()

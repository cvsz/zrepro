"""Credential filename gate regression tests using synthetic Git repositories."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_secret_files import secret_file_paths


class SecretFileTest(unittest.TestCase):
    def test_environment_variants_and_private_keys_are_blocked(self):
        blocked = [".env", "app/.env.production", "app/.env.local", "id_ecdsa", "keys/id_rsa", "cert.pem", "server.key"]
        allowed = [".env.example", "app/.env.example", "id_rsa.pub", "README.md"]
        self.assertEqual(secret_file_paths(blocked + allowed), sorted(blocked))

    def test_actual_git_index_handles_ignored_files_and_newline_names(self):
        checker = Path(__file__).resolve().parents[1] / "scripts/check_secret_files.py"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".env*\n")
            (root / ".env.example").write_text("VALUE=REPLACE_ME\n")
            subprocess.run(["git", "-C", str(root), "add", "-f", ".env.example"], check=True)
            passed = subprocess.run([sys.executable, str(checker)], cwd=root, capture_output=True)
            self.assertEqual(passed.returncode, 0)
            name = ".env.production\nignored"
            (root / name).write_text("VALUE=REPLACE_ME\n")
            subprocess.run(["git", "-C", str(root), "add", "-f", name], check=True)
            failed = subprocess.run([sys.executable, str(checker)], cwd=root, capture_output=True)
            self.assertEqual(failed.returncode, 1)
            self.assertIn(b"Potential credential file", failed.stderr)
            self.assertNotIn(b"VALUE=", failed.stderr)


if __name__ == "__main__":
    unittest.main()

"""Validate context exclusions with Docker and synthetic files; no network image pull."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class DockerContextTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("docker"):
            raise unittest.SkipTest("Docker is unavailable")
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True, timeout=10)
        except (subprocess.SubprocessError, OSError):
            raise unittest.SkipTest("Docker daemon is unavailable")

    def test_synthetic_secrets_and_dependencies_are_excluded(self):
        ignore = Path(__file__).resolve().parents[1] / ".dockerignore"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            context = root / "context"
            context.mkdir()
            shutil.copyfile(ignore, context / ".dockerignore")
            (context / "Dockerfile").write_text("FROM scratch\nCOPY . /\n")
            (context / "allowed.txt").write_text("public source\n")
            forbidden = [
                ".env", "services/mcp/.env.production", "keys/id_rsa", "keys/example.pem",
                ".git/config", "services/mcp/.venv/marker", "node_modules/marker",
            ]
            for relative in forbidden:
                target = context / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("REPLACE_ME\n")
            output = root / "output"
            result = subprocess.run(
                ["docker", "build", "--quiet", "--output", f"type=local,dest={output}", str(context)],
                capture_output=True, timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
            self.assertTrue((output / "allowed.txt").is_file())
            for relative in forbidden:
                self.assertFalse((output / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()

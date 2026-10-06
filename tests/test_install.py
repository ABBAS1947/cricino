"""Isolated filesystem tests only: no application fixtures or external services."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scripts/install.py"
SPEC = importlib.util.spec_from_file_location("cricino_install", SOURCE)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cricino-isolated-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "target"
        self.root.mkdir()
        (self.root / ".git").mkdir()

    def test_preview_writes_nothing(self):
        before = list(self.root.iterdir())
        self.assertEqual(installer.install(self.root)["state"], "preview")
        self.assertEqual(list(self.root.iterdir()), before)

    def test_install_preserves_original_instruction_bytes(self):
        original = b"# Existing instructions\r\nDo not run tests.\r\n"
        (self.root / "AGENTS.md").write_bytes(original)
        result = installer.install(self.root, True)
        self.assertEqual(result["state"], "installed_scaffold_adaptation_pending")
        self.assertTrue((self.root / "AGENTS.md").read_bytes().startswith(original))
        self.assertEqual((self.root / ".cricino/AGENTS.before").read_bytes(), original)
        self.assertEqual(json.loads((self.root / ".cricino/installation.json").read_text())["application_tests"], "not_run")

    def test_repeated_install_is_unchanged(self):
        installer.install(self.root, True)
        original = (self.root / "AGENTS.md").read_bytes()
        self.assertEqual(installer.install(self.root, True)["state"], "unchanged")
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), original)

    def test_existing_doc_conflict_prevents_all_writes(self):
        path = self.root / "docs/cricino/context.md"
        path.parent.mkdir(parents=True)
        path.write_text("private existing context", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install(self.root, True)
        self.assertEqual(path.read_text(), "private existing context")
        self.assertFalse((self.root / "AGENTS.md").exists())
        self.assertFalse((self.root / ".cricino").exists())

    def test_lowercase_instruction_file_is_preserved(self):
        (self.root / "agents.md").write_bytes(b"Existing")
        installer.install(self.root, True)
        self.assertTrue((self.root / "agents.md").read_bytes().startswith(b"Existing"))
        self.assertEqual(len([p for p in self.root.iterdir() if p.name.casefold() == "agents.md"]), 1)

    def test_non_repository_refused(self):
        with self.assertRaises(ValueError):
            installer.install(self.root / ".git", True)

    def test_incomplete_marker_refused(self):
        path = self.root / "AGENTS.md"
        path.write_text(installer.START, encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install(self.root, True)
        self.assertEqual(path.read_text(), installer.START)

    def test_adapted_installation_is_not_overwritten(self):
        installer.install(self.root, True)
        path = self.root / "docs/cricino/context.md"
        path.write_text("adapted by owner", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install(self.root, True)
        self.assertEqual(path.read_text(), "adapted by owner")

    def test_path_escape_refused(self):
        with self.assertRaises(ValueError):
            installer.checked(self.root, "../outside")

    def test_git_worktree_pointer_supported(self):
        (self.root / ".git").rmdir()
        (self.root / ".git").write_text("gitdir: /unused/reference", encoding="utf-8")
        self.assertEqual(installer.install(self.root)["state"], "preview")

    def test_redirected_docs_path_refused_before_writes(self):
        real = installer.redirected
        with patch.object(installer, "redirected", side_effect=lambda p: p == self.root / "docs" or real(p)):
            with self.assertRaises(ValueError):
                installer.install(self.root, True)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_license_and_backup_ignore_are_installed(self):
        installer.install(self.root, True)
        self.assertIn("MIT License", (self.root / "docs/cricino/LICENSE").read_text())
        self.assertEqual((self.root / ".cricino/.gitignore").read_text(), "AGENTS.before\n")


if __name__ == "__main__":
    unittest.main()

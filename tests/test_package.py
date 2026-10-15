import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("package", ROOT / "scripts/package.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_archive_includes_only_allowlisted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in package.PUBLIC_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Public starter", encoding="utf-8")
            for relative in ["cv.md", "notes/private.md", "inbox/old-cv.pdf", "output/cv.html", "history/old.md", "variants/role.md", "docs/private-notes.md", ".env", ".git/config"]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("PRIVATE_SENTINEL", encoding="utf-8")
            destination = package.package(root, root / "dist/CVKeeper.zip")
            with ZipFile(destination) as archive:
                self.assertIn("CVKeeper/inbox/README.md", archive.namelist())
                self.assertNotIn("CVKeeper/inbox/old-cv.pdf", archive.namelist())
                self.assertEqual(set(archive.namelist()), {"CVKeeper/" + path for path in package.PUBLIC_FILES})
                self.assertTrue(all(b"PRIVATE_SENTINEL" not in archive.read(name) for name in archive.namelist()))

    def test_missing_file_fails_before_replacing_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "existing.zip"
            destination.write_bytes(b"existing archive")
            with self.assertRaisesRegex(ValueError, "Missing"):
                package.package(root, destination)
            self.assertEqual(destination.read_bytes(), b"existing archive")

    @unittest.skipIf(sys.platform == "win32", "Symlinks may require privileges on Windows")
    def test_symlink_cannot_import_private_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in package.PUBLIC_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Public", encoding="utf-8")
            private = root / "secret.md"
            private.write_text("PRIVATE", encoding="utf-8")
            (root / "AGENTS.md").unlink()
            (root / "AGENTS.md").symlink_to(private)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                package.package(root, root / "dist/CVKeeper.zip")


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata
import unittest


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("cv_pdf_integration", ROOT / "scripts/cv.py")
cv = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cv
SPEC.loader.exec_module(cv)


def normalized(text):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text)).casefold()


@unittest.skipUnless(os.environ.get("CVKEEPER_PDF_TESTS") == "1", "Enable real browser/PDF tests with CVKEEPER_PDF_TESTS=1")
class RealPdfTests(unittest.TestCase):
    def check_pdf(self, source, multiple_pages=False):
        from pypdf import PdfReader

        with tempfile.TemporaryDirectory(prefix="cvkeeper real pdf ") as directory:
            root = Path(directory)
            (root / "cv.md").write_text(source, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/cv.py"), "build", "--input", "cv.md",
                 "--output", "output with spaces", "--strict", "--pdf"],
                cwd=root, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(result.stdout.startswith("Created PDF "))
            output = root / "output with spaces"
            metadata = json.loads((output / "build.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["pdf_created"])
            pdf = cv.verify_pdf(output / metadata["pdf_filename"])
            self.assertRegex(pdf.name, r"^Ahmed_Yusef_\d{4}-\d{2}-\d{2}_1\.pdf$")
            reader = PdfReader(pdf)
            self.assertFalse(reader.is_encrypted)
            self.assertGreaterEqual(len(reader.pages), 2 if multiple_pages else 1)
            page_text = [page.extract_text() or "" for page in reader.pages]
            self.assertTrue(all(text.strip() for text in page_text), "Empty or image-only PDF page")
            extracted = normalized("\n".join(page_text))
            self.assertNotIn("cvkeeper", extracted)
            self.assertNotIn("print/savepdf", extracted)
            position = 0
            for block in cv.parse(source):
                visible = cv.INLINE.sub(lambda match: match.group(1) or match.group(2), block.text)
                expected = normalized(visible)
                found = extracted.find(expected, position)
                self.assertNotEqual(found, -1, "Missing or out-of-order PDF text: " + visible)
                position = found + len(expected)

    def test_example_pdf_preserves_content_and_order(self):
        self.check_pdf((ROOT / "examples/cv.md").read_text(encoding="utf-8"))

    def test_multipage_pdf_preserves_content_and_accents(self):
        source = (ROOT / "examples/cv.md").read_text(encoding="utf-8")
        source += "\n## Additional Projects\n\n"
        for number in range(1, 31):
            source += (
                "### Project %d | Montréal Community\n\n" % number
                + "January 2020 - December 2020\n\n"
                + "- Coordinated café volunteer schedules and documented résumé review workshops.\n\n"
            )
        self.check_pdf(source, multiple_pages=True)


if __name__ == "__main__":
    unittest.main()

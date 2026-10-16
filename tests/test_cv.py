import contextlib
import importlib.util
import io
import json
from datetime import date
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("cv", ROOT / "scripts/cv.py")
cv = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cv
SPEC.loader.exec_module(cv)
SAMPLE = "# Ahmed Yusef\n\nCity | [Email](mailto:ahmed@example.com)\n\n## Experience\n\n### Coordinator | Example\n\n2022 - Present\n\n- Led a project.\n- Wrote a guide.\n"


class ParserTests(unittest.TestCase):
    def test_sample_and_paragraph_joining(self):
        blocks = cv.parse(SAMPLE + "\nOne line\ncontinued.\n")
        self.assertEqual(blocks[0].text, "Ahmed Yusef")
        self.assertEqual(blocks[-1].text, "One line continued.")
        self.assertEqual(sum(block.kind == "bullet" for block in blocks), 2)

    def test_invalid_structure_is_actionable(self):
        sources = ["", "No heading", "# One\n# Two\n## Skills", "# Name\n### Job\n## Skills", "# Name\nNo sections", "# Name\n#### Deep\n## Skills", "# Name\n## Skills\n```code", "# Name\n## Skills\n  - Nested"]
        for source in sources:
            with self.subTest(source=source), self.assertRaises(ValueError):
                cv.parse(source)

    def test_html_is_escaped_not_executed(self):
        result = cv.inline('<script>alert("hello")</script> **A&B**', "html")
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("<strong>A&amp;B</strong>", result)

    def test_link_attribute_injection_is_escaped(self):
        result = cv.inline('[site](https://example.com/"onmouseover="alert)', "html")
        self.assertIn("&quot;onmouseover=&quot;", result)
        self.assertNotIn('"onmouseover="', result)

    def test_unsafe_links_are_rejected(self):
        for address in ["javascript:alert", "data:text/html,test", "file:///etc/passwd", "//example.com", "https:///missing", "mailto:", "tel:", "https://example.com/\\input"]:
            with self.subTest(address=address), self.assertRaises(ValueError):
                cv.parse("# Name\n## Links\n[link](%s)" % address)

    def test_plain_text_keeps_link_destinations(self):
        self.assertEqual(cv.inline("[Site](https://example.com)", "text"), "Site (https://example.com)")
        self.assertEqual(cv.inline("[ahmed@example.com](mailto:ahmed@example.com)", "text"), "ahmed@example.com")

    def test_latex_special_characters_are_escaped(self):
        result = cv.inline(r"50% & $5_000 #1 {x} \input{bad} ~ ^", "tex")
        self.assertIn(r"50\% \& \$5\_000 \#1 \{x\}", result)
        self.assertIn(r"\textbackslash{}input\{bad\}", result)
        self.assertNotIn(r"\input{bad}", result)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cvkeeper test ")
        self.root = Path(self.temp.name)
        self.source = self.root / "source.md"
        self.source.write_text(SAMPLE, encoding="utf-8")
        self.output = self.root / "output"

    def tearDown(self):
        self.temp.cleanup()

    def test_build_creates_all_outputs_and_balanced_lists(self):
        messages = cv.build(self.source, self.output, strict=True)
        self.assertEqual(messages, [])
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        numbered = {identity["filename"] + suffix for suffix in [".html", ".txt", ".tex"]}
        self.assertEqual({path.name for path in self.output.iterdir()}, {"cv.html", "cv.txt", "cv.tex", "build.json"} | numbered)
        html = (self.output / "cv.html").read_text(encoding="utf-8")
        self.assertEqual(html.count("<ul>"), html.count("</ul>"))
        self.assertEqual(html.count("<header>"), html.count("</header>"))
        self.assertIn("size: A4", html)
        self.assertIn('onclick="window.print()"', html)
        self.assertNotIn("<script src=", html)
        self.assertIn(r"\end{document}", (self.output / "cv.tex").read_text(encoding="utf-8"))

    def test_draft_banner_and_strict_failure_preserves_existing_exports(self):
        cv.build(self.source, self.output)
        previous = (self.output / "cv.html").read_bytes()
        self.source.write_text(SAMPLE + "\n{{MISSING_FACT}}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "MISSING_FACT"):
            cv.build(self.source, self.output, strict=True)
        self.assertEqual(previous, (self.output / "cv.html").read_bytes())
        messages = cv.build(self.source, self.output)
        self.assertEqual(len(messages), 1)
        self.assertIn('class="draft"', (self.output / "cv.html").read_text(encoding="utf-8"))
        self.assertIn("DRAFT", (self.output / "cv.txt").read_text(encoding="utf-8"))

    def test_letter_and_rtl_unicode(self):
        self.source.write_text("# ليلى أحمد\n\n## الخبرة\n\nتنسيق المشاريع", encoding="utf-8")
        cv.build(self.source, self.output, paper="letter", language="ar", direction="rtl")
        html = (self.output / "cv.html").read_text(encoding="utf-8")
        self.assertIn('lang="ar" dir="rtl"', html)
        self.assertIn("ليلى أحمد", html)
        self.assertIn("size: letter", html)

    def test_source_cannot_be_overwritten(self):
        self.output.mkdir()
        source = self.output / "cv.txt"
        source.write_text(SAMPLE, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "overwrite the input"):
            cv.build(source, self.output)
        self.assertEqual(source.read_text(encoding="utf-8"), SAMPLE)

    @unittest.skipIf(sys.platform == "win32", "Symlinks may require privileges on Windows")
    def test_export_symlink_is_not_followed(self):
        self.output.mkdir()
        (self.output / "cv.html").symlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "symbolic link"):
            cv.build(self.source, self.output)
        self.assertEqual(self.source.read_text(encoding="utf-8"), SAMPLE)

    def test_initialize_preserves_existing_cv(self):
        (self.root / "templates").mkdir()
        (self.root / "templates/cv.md").write_text(SAMPLE, encoding="utf-8")
        for name in ["profile.md", "field-guide.md", "review.md"]:
            (self.root / "templates" / name).write_text((ROOT / "templates" / name).read_text(encoding="utf-8"), encoding="utf-8")
        created = cv.initialize(self.root)
        self.assertEqual(set(created), {"cv.md", "notes/profile.md", "notes/field-guide.md", "notes/review.md"})
        self.assertTrue((self.root / "inbox").is_dir())
        self.assertIn("Private career profile", (self.root / "notes/profile.md").read_text(encoding="utf-8"))
        (self.root / "cv.md").write_text("My own CV", encoding="utf-8")
        self.assertEqual(cv.initialize(self.root), [])
        self.assertEqual((self.root / "cv.md").read_text(encoding="utf-8"), "My own CV")

    def test_cli_errors_without_traceback(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = cv.main(["build", "--input", str(self.root / "missing.md")])
        self.assertEqual(result, 1)
        self.assertIn("CVKeeper:", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_cli_from_another_directory_with_spaces(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/cv.py"), "build", "--input", str(self.source), "--output", str(self.output), "--strict"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output / "cv.html").is_file())

    def test_check_fails_for_placeholders(self):
        with contextlib.redirect_stderr(io.StringIO()):
            result = cv.main(["check", "--input", str(ROOT / "templates/cv.md")])
        self.assertEqual(result, 1)

    def test_invalid_language_does_not_create_output(self):
        with self.assertRaisesRegex(ValueError, "language tag"):
            cv.build(self.source, self.output, language='en" onclick="bad')
        self.assertFalse(self.output.exists())

    def test_filename_matches_title_toolbar_and_metadata(self):
        with patch.object(cv, "date") as clock:
            clock.today.return_value = date(2026, 10, 15)
            cv.build(self.source, self.output)
        expected = "Ahmed_Yusef_2026-10-15_1"
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["pdf_filename"], expected + ".pdf")
        html = (self.output / (expected + ".html")).read_text(encoding="utf-8")
        self.assertIn("<title>" + expected + "</title>", html)
        self.assertIn("<strong>" + expected + ".pdf</strong>", html)
        for suffix in [".html", ".txt", ".tex"]:
            self.assertEqual((self.output / (expected + suffix)).read_bytes(), (self.output / ("cv" + suffix)).read_bytes())

    def test_number_increments_across_dates_and_keeps_previous_export(self):
        with patch.object(cv, "date") as clock:
            clock.today.return_value = date(2026, 10, 15)
            cv.build(self.source, self.output)
            first = self.output / "Ahmed_Yusef_2026-10-15_1.html"
            original = first.read_bytes()
            cv.build(self.source, self.output)
            self.assertTrue((self.output / "Ahmed_Yusef_2026-10-15_2.html").exists())
            clock.today.return_value = date(2026, 10, 16)
            cv.build(self.source, self.output)
        self.assertTrue((self.output / "Ahmed_Yusef_2026-10-16_3.html").exists())
        self.assertEqual(first.read_bytes(), original)

    def test_number_recovers_from_saved_exports_without_metadata(self):
        self.output.mkdir()
        (self.output / "Ahmed_Yusef_2026-01-01_8.pdf").write_bytes(b"saved PDF")
        cv.build(self.source, self.output)
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["build_number"], 9)

    def test_invalid_metadata_cannot_silently_reset_build_number(self):
        cv.build(self.source, self.output)
        original = (self.output / "cv.html").read_bytes()
        for invalid in ['{"build_number": "bad"}', '{"build_number": true}', '[]', '{broken']:
            (self.output / "build.json").write_text(invalid, encoding="utf-8")
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                cv.build(self.source, self.output)
            self.assertEqual((self.output / "cv.html").read_bytes(), original)

    def test_failed_validation_does_not_consume_build_number(self):
        cv.build(self.source, self.output)
        self.source.write_text(SAMPLE + "\n{{MISSING_FACT}}", encoding="utf-8")
        with self.assertRaises(ValueError):
            cv.build(self.source, self.output, strict=True)
        self.source.write_text(SAMPLE, encoding="utf-8")
        cv.build(self.source, self.output)
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["build_number"], 2)

    def test_compound_arabic_names_and_unsafe_filename_characters(self):
        cv.build(self.source, self.output, first_name="أحمد", last_name="آل يوسف")
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertTrue(identity["filename"].startswith("أحمد_آل-يوسف_"))
        self.assertIn("Ahmed Yusef", (self.output / "cv.txt").read_text(encoding="utf-8"))
        self.assertEqual(cv.filename_part('../Ahmed<>:"/\\?*'), "Ahmed")
        with self.assertRaises(ValueError):
            cv.filename_part("/\\?*")

    def test_placeholder_name_exports_as_explicit_draft(self):
        cv.build(ROOT / "templates/cv.md", self.output)
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertTrue(identity["filename"].startswith("FirstName_LastName_"))
        self.assertIn('class="draft"', (self.output / "cv.html").read_text(encoding="utf-8"))

    def test_cli_accepts_explicit_family_name(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/cv.py"), "build", "--input", str(self.source), "--output", str(self.output), "--first-name", "Ahmed", "--last-name", "Al Yusef", "--strict"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ahmed_Al-Yusef_", result.stdout)
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertFalse(identity["pdf_created"])
        self.assertIn("PDF not created", result.stdout)

    def test_shipped_cv_uses_ahmed_without_em_dashes(self):
        example = (ROOT / "examples/cv.md").read_text(encoding="utf-8")
        self.assertTrue(example.startswith("# Ahmed Yusef\n"))
        self.assertNotIn("\u2014", example)
        self.assertNotIn("\u2014", (ROOT / "templates/cv.md").read_text(encoding="utf-8"))

    def test_bundled_preview_matches_current_source_and_styles(self):
        blocks = cv.parse((ROOT / "examples/cv.md").read_text(encoding="utf-8"))
        html = (ROOT / "examples/preview/cv.html").read_text(encoding="utf-8")
        filename = html.split("<title>", 1)[1].split("</title>", 1)[0]
        self.assertRegex(filename, r"^Ahmed_Yusef_\d{4}-\d{2}-\d{2}_\d+$")
        self.assertEqual(html, cv.render_html(blocks, "A4", "en", "ltr", False, filename))
        self.assertEqual((ROOT / "examples/preview/cv.txt").read_text(encoding="utf-8"), cv.render_text(blocks, False))
        self.assertEqual((ROOT / "examples/preview/cv.tex").read_text(encoding="utf-8"), cv.render_tex(blocks, "A4", False))

    def test_pdf_export_creates_real_pdf_and_updates_metadata(self):
        cv.build(self.source, self.output, strict=True)
        browser = self.root / "edge.exe"
        browser.write_text("fake executable", encoding="utf-8")

        def fake_run(command, **kwargs):
            pdf_argument = next(part for part in command if part.startswith("--print-to-pdf="))
            Path(pdf_argument.split("=", 1)[1]).write_bytes(b"%PDF-1.7\ncontent\n%%EOF\n")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(cv.subprocess, "run", side_effect=fake_run):
            pdf_path = cv.export_latest_pdf(self.output, str(browser))
        self.assertEqual(pdf_path.read_bytes(), b"%PDF-1.7\ncontent\n%%EOF\n")
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertTrue(identity["pdf_created"])
        self.assertEqual(pdf_path.name, identity["pdf_filename"])

    def test_pdf_export_failure_does_not_install_invalid_file(self):
        cv.build(self.source, self.output, strict=True)
        browser = self.root / "chrome.exe"
        browser.write_text("fake executable", encoding="utf-8")

        def fake_run(command, **kwargs):
            pdf_argument = next(part for part in command if part.startswith("--print-to-pdf="))
            Path(pdf_argument.split("=", 1)[1]).write_text("web page", encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(cv.subprocess, "run", side_effect=fake_run), self.assertRaisesRegex(ValueError, "not a valid PDF"):
            cv.export_latest_pdf(self.output, str(browser))
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertFalse(identity["pdf_created"])
        self.assertFalse((self.output / identity["pdf_filename"]).exists())

    def test_pdf_subcommand_does_not_increment_build_number(self):
        cv.build(self.source, self.output, strict=True)
        browser = self.root / "chrome.exe"
        browser.write_text("fake executable", encoding="utf-8")

        def fake_run(command, **kwargs):
            pdf_argument = next(part for part in command if part.startswith("--print-to-pdf="))
            Path(pdf_argument.split("=", 1)[1]).write_bytes(b"%PDF-1.7\n%%EOF\n")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(cv.subprocess, "run", side_effect=fake_run):
            result = cv.main(["pdf", "--output", str(self.output), "--browser", str(browser)])
        self.assertEqual(result, 0)
        identity = json.loads((self.output / "build.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["build_number"], 1)

    def test_windows_browser_discovery_includes_edge_and_chrome(self):
        with patch.object(cv.sys, "platform", "win32"), patch.object(cv.shutil, "which", return_value=None), patch.dict(cv.os.environ, {"PROGRAMFILES": r"C:\Program Files", "PROGRAMFILES(X86)": r"C:\Program Files (x86)", "LOCALAPPDATA": r"C:\Users\Ahmed\AppData\Local"}, clear=True):
            candidates = {path.as_posix() for path in cv.browser_candidates()}
        self.assertTrue(any("Microsoft/Edge/Application/msedge.exe" in path for path in candidates))
        self.assertTrue(any("Google/Chrome/Application/chrome.exe" in path for path in candidates))

    def test_verify_pdf_rejects_webpage_saved_with_pdf_extension(self):
        fake_pdf = self.root / "cv.pdf"
        fake_pdf.write_text("<!doctype html><title>CV</title>", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not a valid PDF"):
            cv.verify_pdf(fake_pdf)

    def test_chat_only_instructions_include_guides_and_direct_pdf(self):
        page = (ROOT / "START-HERE.html").read_text(encoding="utf-8")
        fallback = page.split("My chat app cannot open local folders.", 1)[1].split("</details>", 1)[0]
        self.assertIn("guides/", fallback)
        self.assertIn("context templates", fallback)
        self.assertIn("build --strict --pdf", fallback)
        self.assertIn("downloadable PDF", fallback)

    def test_career_context_templates_cover_experience_and_timeline(self):
        profile = (ROOT / "templates/profile.md").read_text(encoding="utf-8")
        interview = (ROOT / "guides/INTERVIEW.md").read_text(encoding="utf-8")
        review = (ROOT / "guides/REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("Role evidence", profile)
        self.assertIn("Career timeline", profile)
        self.assertIn("What did you own", interview)
        self.assertIn("overlap", interview.lower())
        self.assertIn("actual PDF", review)

    def test_visible_starting_prompt_stays_short_and_delegates_details(self):
        page = (ROOT / "START-HERE.html").read_text(encoding="utf-8")
        prompt = page.split('<textarea id="starting-message"', 1)[1].split(">", 1)[1].split("</textarea>", 1)[0]
        self.assertLess(len(prompt), 150)
        self.assertIn("CV writer and updater", prompt)
        self.assertNotIn("first name", prompt.lower())
        self.assertNotIn("build number", prompt.lower())

    def test_agent_rules_prioritize_experience_and_overlap_review(self):
        rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Names and contact details come later", rules)
        self.assertIn("what they owned", rules)
        self.assertIn("overlaps reflect consulting", rules)
        self.assertIn("Deliver an actual PDF", rules)


if __name__ == "__main__":
    unittest.main()

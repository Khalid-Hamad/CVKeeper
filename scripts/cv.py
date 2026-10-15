#!/usr/bin/env python3
"""Build a CV using a deliberately small, dependency-free Markdown format."""

import argparse
from dataclasses import dataclass
from datetime import date
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
INLINE = re.compile(r"\*\*([^*\n]+)\*\*|\[([^\]\n]+)\]\(([^\s()]+)\)")
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")
PDF_HEADER = b"%PDF-"


@dataclass
class Block:
    kind: str
    text: str


def parse(source):
    blocks = []
    paragraph = []

    def flush():
        if paragraph:
            blocks.append(Block("paragraph", " ".join(paragraph)))
            paragraph.clear()

    for number, raw_line in enumerate(source.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            flush()
            continue
        if re.match(r"^(?:```|~~~|>|\||\d+\.\s|[*+]\s)", line):
            raise ValueError("Line %d: unsupported Markdown; see docs/FORMAT.md." % number)
        if line.startswith("#"):
            flush()
            heading = re.fullmatch(r"(#{1,3})\s+(.+)", line)
            if not heading:
                raise ValueError("Line %d: use #, ##, or ### followed by text." % number)
            blocks.append(Block("h%d" % len(heading[1]), heading[2]))
        elif line.startswith("- "):
            flush()
            if raw_line != raw_line.lstrip():
                raise ValueError("Line %d: nested bullets are not supported." % number)
            blocks.append(Block("bullet", line[2:]))
        else:
            paragraph.append(line)
    flush()
    if not blocks or blocks[0].kind != "h1":
        raise ValueError("Start the CV with '# Your Name'.")
    if sum(block.kind == "h1" for block in blocks) != 1:
        raise ValueError("Use exactly one # heading, for your name.")
    has_section = False
    for block in blocks[1:]:
        if block.kind == "h2":
            has_section = True
        if block.kind == "h3" and not has_section:
            raise ValueError("Put ### entries inside a ## section.")
    if not has_section:
        raise ValueError("Add at least one ## section, such as Experience or Education.")
    for block in blocks:
        inline(block.text, "text")
    return blocks


def safe_url(url):
    if any(ord(character) < 32 for character in url) or "\\" in url:
        raise ValueError("Links cannot contain control characters or backslashes.")
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in {"https", "http", "mailto", "tel"}:
        raise ValueError("Links must start with https://, http://, mailto:, or tel:.")
    if parsed.scheme.lower() in {"https", "http"} and not parsed.netloc:
        raise ValueError("Web links must include a host name.")
    if parsed.scheme.lower() in {"mailto", "tel"} and not parsed.path:
        raise ValueError("Contact links must include an address or number.")
    return url


def latex_escape(value):
    replacements = {
        "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
        "$": r"\$", "&": r"\&", "#": r"\#", "%": r"\%",
        "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def inline(value, output):
    encode = {"html": escape, "tex": latex_escape, "text": str}[output]
    result = []
    previous = 0
    for match in INLINE.finditer(value):
        result.append(encode(value[previous:match.start()]))
        bold, label, url = match.groups()
        if bold is not None:
            content = encode(bold)
            result.append({"html": "<strong>%s</strong>", "tex": r"\textbf{%s}", "text": "%s"}[output] % content)
        else:
            safe_url(url)
            if output == "html":
                result.append('<a href="%s">%s</a>' % (escape(url, quote=True), escape(label)))
            elif output == "tex":
                result.append(r"\href{%s}{%s}" % (latex_escape(url), latex_escape(label)))
            else:
                address = re.sub(r"^(?:mailto:|tel:)", "", url, flags=re.I)
                result.append(label if label == address else "%s (%s)" % (label, url))
        previous = match.end()
    result.append(encode(value[previous:]))
    return "".join(result)


def placeholder_messages(source):
    return ["Unresolved placeholder: " + token for token in sorted(set(PLACEHOLDER.findall(source)))]


def render_html(blocks, paper, language, direction, draft, filename):
    body = ["<header>"]
    in_header = True
    in_list = False
    for block in blocks:
        if block.kind != "bullet" and in_list:
            body.append("</ul>")
            in_list = False
        if block.kind == "h2" and in_header:
            body.append("</header>")
            in_header = False
        if block.kind == "bullet" and not in_list:
            body.append("<ul>")
            in_list = True
        tag = {"paragraph": "p", "bullet": "li"}.get(block.kind, block.kind)
        body.append("<%s>%s</%s>" % (tag, inline(block.text, "html"), tag))
    if in_list:
        body.append("</ul>")
    if in_header:
        body.append("</header>")
    css = (ROOT / "templates/resume.css").read_text(encoding="utf-8").replace("__PAPER__", paper)
    banner = '<aside class="draft">DRAFT: replace the remaining {{PLACEHOLDERS}} before sharing.</aside>' if draft else ""
    return '''<!doctype html>
<html lang="%s" dir="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<div class="toolbar" dir="ltr"><span>CVKeeper · %s · HTML preview. On Windows use Ctrl+P, not Ctrl+S.<br>PDF name: <strong>%s.pdf</strong></span><button type="button" onclick="window.print()">Print / Save PDF</button></div>
<main>%s%s</main>
</body>
</html>
''' % (escape(language, quote=True), direction, escape(filename), css, paper, escape(filename), banner, "\n".join(body))


def render_text(blocks, draft):
    lines = ["DRAFT: unresolved placeholders remain.\n"] if draft else []
    for block in blocks:
        content = inline(block.text, "text")
        lines.append(("- " if block.kind == "bullet" else "") + content)
        if block.kind != "bullet":
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tex(blocks, paper, draft):
    lines = [r"\textbf{DRAFT: unresolved placeholders remain.}\par"] if draft else []
    in_list = False
    for block in blocks:
        if block.kind != "bullet" and in_list:
            lines.append(r"\end{itemize}")
            in_list = False
        if block.kind == "bullet" and not in_list:
            lines.append(r"\begin{itemize}")
            in_list = True
        content = inline(block.text, "tex")
        formats = {"h1": r"{\Huge\bfseries %s}\par", "h2": r"\section*{%s}",
                   "h3": r"\subsection*{%s}", "paragraph": r"%s\par", "bullet": r"\item %s"}
        lines.append(formats[block.kind] % content)
    if in_list:
        lines.append(r"\end{itemize}")
    template = (ROOT / "templates/resume.tex").read_text(encoding="utf-8")
    return template.replace("__PAPER__", "a4paper" if paper == "A4" else "letterpaper").replace("__CONTENT__", "\n".join(lines))


def filename_part(value):
    cleaned = re.sub(r"[^\w-]", "", re.sub(r"\s+", "-", value.strip()), flags=re.UNICODE).strip("_-")
    if not cleaned:
        raise ValueError("Filename names must contain letters or numbers.")
    return cleaned


def export_identity(blocks, output_path, first_name=None, last_name=None):
    name = inline(blocks[0].text, "text")
    parts = name.split()
    if PLACEHOLDER.search(name):
        parts = ["FirstName", "LastName"]
    first = filename_part(first_name if first_name is not None else parts[0])
    last = filename_part(last_name if last_name is not None else parts[-1] if len(parts) > 1 else "CV")
    previous_number = 0
    metadata_path = output_path / "build.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if not isinstance(metadata, dict) or type(metadata.get("build_number")) is not int or metadata["build_number"] < 1:
            raise ValueError("Invalid build.json: restore its last valid copy before rebuilding.")
        previous_number = metadata["build_number"]
    for existing in output_path.glob("*"):
        match = re.fullmatch(r".+_\d{4}-\d{2}-\d{2}_(\d+)\.(?:html|txt|tex|pdf)", existing.name)
        if match:
            previous_number = max(previous_number, int(match[1]))
    number = previous_number + 1
    updated = date.today().isoformat()
    filename = "%s_%s_%s_%d" % (first, last, updated, number)
    return {"filename": filename, "pdf_filename": filename + ".pdf", "updated": updated, "build_number": number, "pdf_created": False}


def browser_candidates():
    candidates = []
    for command in ("msedge", "microsoft-edge", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        location = shutil.which(command)
        if location:
            candidates.append(Path(location))
    if sys.platform == "darwin":
        candidates.extend([
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ])
    if sys.platform == "win32":
        for variable in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            base = os.environ.get(variable)
            if not base:
                continue
            candidates.extend([
                Path(base) / "Microsoft/Edge/Application/msedge.exe",
                Path(base) / "Google/Chrome/Application/chrome.exe",
                Path(base) / "Chromium/Application/chrome.exe",
            ])
    result = []
    seen = set()
    for candidate in candidates:
        normalized = str(candidate.resolve()) if candidate.exists() else str(candidate)
        if normalized not in seen:
            seen.add(normalized)
            result.append(candidate)
    return result


def find_browser(explicit=None):
    if explicit:
        candidate = Path(explicit).expanduser()
        if candidate.is_file():
            return candidate.resolve()
        raise ValueError("Browser executable not found: " + str(candidate))
    for candidate in browser_candidates():
        if candidate.is_file():
            return candidate.resolve()
    raise ValueError(
        "PDF export needs Edge, Chrome, or Chromium in this execution environment. "
        "Install one, pass --browser with its executable path, use your AI client's PDF tool, "
        "or follow docs/EXPORTING.md."
    )


def verify_pdf(path):
    if not path.is_file():
        raise ValueError("PDF export did not create a file: " + str(path))
    data = path.read_bytes()
    if not data.startswith(PDF_HEADER) or b"%%EOF" not in data[-2048:]:
        raise ValueError("The exported file is not a valid PDF: " + str(path))
    return path


def export_pdf(html_path, pdf_path, browser=None):
    if not html_path.is_file():
        raise ValueError("HTML source not found: " + str(html_path))
    if pdf_path.is_symlink():
        raise ValueError("Refusing to overwrite a symbolic link: " + str(pdf_path))
    if pdf_path.exists():
        return verify_pdf(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    executable = find_browser(browser)
    with tempfile.TemporaryDirectory(prefix=".cvkeeper-pdf-", dir=pdf_path.parent) as directory:
        scratch = Path(directory)
        temporary_pdf = scratch / pdf_path.name
        profile = scratch / "browser-profile"
        command = [
            str(executable),
            "--headless",
            "--disable-gpu",
            "--disable-extensions",
            "--no-first-run",
            "--no-pdf-header-footer",
            "--user-data-dir=" + str(profile),
            "--print-to-pdf=" + str(temporary_pdf),
            html_path.resolve().as_uri(),
        ]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=90)
        except subprocess.TimeoutExpired as error:
            raise ValueError("Browser PDF export timed out after 90 seconds.") from error
        if completed.returncode != 0:
            details = (completed.stderr or completed.stdout).strip()
            if len(details) > 500:
                details = details[-500:]
            if not details:
                details = "exit status %d" % completed.returncode
            raise ValueError("Browser PDF export failed: " + details)
        verify_pdf(temporary_pdf)
        temporary_pdf.replace(pdf_path)
    return verify_pdf(pdf_path)


def export_latest_pdf(output_path, browser=None):
    metadata_path = output_path / "build.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or not isinstance(metadata.get("filename"), str):
        raise ValueError("Invalid build.json: build the CV again before exporting PDF.")
    html_path = output_path / (metadata["filename"] + ".html")
    pdf_path = output_path / metadata.get("pdf_filename", metadata["filename"] + ".pdf")
    export_pdf(html_path, pdf_path, browser)
    metadata["pdf_filename"] = pdf_path.name
    metadata["pdf_created"] = True
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return pdf_path


def build(input_path, output_path, paper="A4", language="en", direction="ltr", strict=False, first_name=None, last_name=None, make_pdf=False, browser=None):
    source = input_path.read_text(encoding="utf-8-sig")
    blocks = parse(source)
    messages = placeholder_messages(source)
    if strict and messages:
        raise ValueError("\n".join(messages))
    if not re.fullmatch(r"[a-zA-Z]{2,8}(?:-[a-zA-Z0-9]{1,8})*", language):
        raise ValueError("Use a language tag such as en, en-GB, or ar.")
    identity = export_identity(blocks, output_path, first_name, last_name)
    outputs = {
        "cv.html": render_html(blocks, paper, language, direction, bool(messages), identity["filename"]),
        "cv.txt": render_text(blocks, bool(messages)),
        "cv.tex": render_tex(blocks, paper, bool(messages)),
    }
    numbered = {identity["filename"] + Path(name).suffix: content for name, content in outputs.items()}
    outputs = {**numbered, **outputs}
    outputs["build.json"] = json.dumps(identity, ensure_ascii=False, indent=2) + "\n"
    for name in outputs:
        destination = output_path / name
        if destination.is_symlink():
            raise ValueError("Refusing to overwrite a symbolic link: " + str(destination))
        if destination.resolve() == input_path.resolve():
            raise ValueError("The output would overwrite the input. Choose a different --output folder.")
        if destination.is_dir():
            raise ValueError("An export path is a directory: " + str(destination))
    output_path.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        with (output_path / name).open("x" if name in numbered else "w", encoding="utf-8") as handle:
            handle.write(content)
    if make_pdf:
        export_latest_pdf(output_path, browser)
    return messages


def initialize(root):
    (root / "inbox").mkdir(exist_ok=True)
    (root / "notes").mkdir(exist_ok=True)
    created = []
    sources = {
        root / "cv.md": root / "templates/cv.md",
        root / "notes/profile.md": root / "templates/profile.md",
        root / "notes/field-guide.md": root / "templates/field-guide.md",
        root / "notes/review.md": root / "templates/review.md",
    }
    for destination, template in sources.items():
        content = template.read_text(encoding="utf-8")
        try:
            with destination.open("x", encoding="utf-8") as handle:
                handle.write(content)
            created.append(destination.relative_to(root).as_posix())
        except FileExistsError:
            pass
    return created


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Create the master and private career-context files without replacing existing files")
    checker = commands.add_parser("check", help="Check structure, links, and unresolved placeholders")
    checker.add_argument("--input", type=Path, default=ROOT / "cv.md")
    builder = commands.add_parser("build", help="Export HTML, plain text, and LaTeX source")
    builder.add_argument("--input", type=Path, default=ROOT / "cv.md")
    builder.add_argument("--output", type=Path, default=ROOT / "output")
    builder.add_argument("--paper", choices=["A4", "letter"], default="A4")
    builder.add_argument("--language", default="en", help="HTML language tag, e.g. en or ar")
    builder.add_argument("--direction", choices=["ltr", "rtl"], default="ltr")
    builder.add_argument("--strict", action="store_true", help="Refuse unresolved placeholders")
    builder.add_argument("--first-name", help="First name for filenames; defaults to the first word of the CV name")
    builder.add_argument("--last-name", help="Family name for filenames; defaults to the last word of the CV name")
    builder.add_argument("--pdf", action="store_true", help="Create a real PDF using installed Edge, Chrome, or Chromium")
    builder.add_argument("--browser", help="Path to an Edge, Chrome, or Chromium executable")
    pdf = commands.add_parser("pdf", help="Export the latest numbered HTML build to PDF without creating a new build")
    pdf.add_argument("--output", type=Path, default=ROOT / "output")
    pdf.add_argument("--browser", help="Path to an Edge, Chrome, or Chromium executable")
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "init":
            created = initialize(ROOT)
            print("Created: " + ", ".join(created) if created else "Master and career-context files already exist; left unchanged.")
        elif arguments.command == "check":
            source = arguments.input.read_text(encoding="utf-8-sig")
            parse(source)
            messages = placeholder_messages(source)
            if messages:
                raise ValueError("\n".join(messages))
            print("Structure and links look good; no placeholders remain. Review facts yourself.")
        elif arguments.command == "build":
            messages = build(arguments.input, arguments.output, arguments.paper, arguments.language, arguments.direction, arguments.strict, arguments.first_name, arguments.last_name, arguments.pdf, arguments.browser)
            for message in messages:
                print("Draft: " + message, file=sys.stderr)
            identity = json.loads((arguments.output / "build.json").read_text(encoding="utf-8"))
            print("Created " + str(arguments.output.resolve() / (identity["filename"] + ".html")))
            print("Also created matching .txt and .tex files. cv.html, cv.txt, and cv.tex are convenient copies of the latest build.")
            if identity.get("pdf_created"):
                print("Created PDF " + str(arguments.output.resolve() / identity["pdf_filename"]))
            else:
                print("PDF not created. Run with --pdf or use your AI client's PDF tool.")
        else:
            pdf_path = export_latest_pdf(arguments.output, arguments.browser)
            print("Created PDF " + str(pdf_path.resolve()))
    except (OSError, UnicodeError, ValueError) as error:
        print("CVKeeper: " + str(error), file=sys.stderr)
        if isinstance(error, FileNotFoundError):
            print("For a new CV, run: python3 scripts/cv.py init", file=sys.stderr)
        if getattr(arguments, "command", None) == "build" and getattr(arguments, "pdf", False):
            print("The HTML build may still be available. Fix the PDF issue, then run: python3 scripts/cv.py pdf", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

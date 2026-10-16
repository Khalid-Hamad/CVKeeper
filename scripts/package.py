#!/usr/bin/env python3
"""Package only explicitly listed public starter files, never a personal workspace."""

from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent.parent
PUBLIC_FILES = (
    ".gitattributes", ".gitignore", ".github/workflows/check.yml",
    "AGENTS.md", "CLAUDE.md", "LICENSE", "NOTICE.md", "README.md", "START-HERE.html", "inbox/README.md",
    "docs/GETTING-STARTED.md", "docs/FORMAT.md", "docs/EXPORTING.md", "docs/LIVE-TEST.md",
    "guides/INTERVIEW.md", "guides/FIELD-PRACTICES.md", "guides/REVIEW.md",
    "templates/cv.md", "templates/profile.md", "templates/field-guide.md", "templates/review.md", "templates/resume.css", "templates/resume.tex",
    "examples/cv.md", "examples/preview/cv.html", "examples/preview/cv.txt", "examples/preview/cv.tex",
    "prompts/create.md", "prompts/import.md", "prompts/update.md", "prompts/tailor.md", "prompts/review.md",
    "scripts/cv.py", "scripts/package.py", "tests/test_cv.py", "tests/test_package.py", "tests/test_pdf_integration.py",
)


def package(root, destination):
    for relative in PUBLIC_FILES:
        source = root / relative
        if not source.is_file() or source.resolve() != root.resolve() / relative:
            raise ValueError("Missing or symlinked starter file: " + relative)
    if destination.is_symlink():
        raise ValueError("Refusing to overwrite a symbolic link: " + str(destination))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for relative in PUBLIC_FILES:
            archive.write(root / relative, "CVKeeper/" + relative)
    return destination


def main():
    try:
        destination = package(ROOT, ROOT / "dist/CVKeeper.zip")
    except (OSError, ValueError) as error:
        print("CVKeeper: " + str(error), file=sys.stderr)
        return 1
    print("Created " + str(destination))
    print("Only listed starter files are included. Review any edits to those files before sharing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

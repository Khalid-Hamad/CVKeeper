# Exporting your CV

## Browser PDF (recommended)

1. Ask your assistant to check and build your CV, or run
   `python3 scripts/cv.py build` from the project folder.
2. Open `output/cv.html` in a browser. It is standalone; no server or internet
   connection is needed. It loads no remote fonts, scripts, or images.
3. Click **Save as PDF** or use your browser's Print command.
4. Select **Save as PDF** / your system's PDF destination. Choose **A4**, scale
   **100%**, and turn off browser headers and footers. On macOS, some print
   dialogs expose a **PDF → Save as PDF** menu instead of a printer destination.
5. Save with the exact filename shown in the HTML toolbar, for example
   `Ahmed_Yusef_2026-10-15_1.pdf`. The browser may suggest the page title, but its
   save dialog can use a different default; confirm or enter the displayed name.
6. Inspect all pages in print preview and then open the saved PDF. Check your
   name, contact details, dates, links, page breaks, and the final line.

For US Letter, build with `--paper letter` and select Letter in the print
dialog. The page stylesheet supplies margins; avoid custom print settings
that override them unnecessarily. Browser pagination can differ.

The HTML toolbar is hidden when printing. An unresolved-placeholder draft
banner stays visible in the PDF to prevent accidentally sending an unfinished
CV. Resolve placeholders and rebuild to remove it.

If content spills onto another page, first remove repetition or less relevant
detail. Do not shrink text until it becomes hard to read. Select and copy text
from the PDF to confirm it is selectable and in a sensible reading order.
There is no automated page-count or ATS guarantee.

## Filename and build number

All numbered exports use `FirstName_LastName_YYYY-MM-DD_buildNumber`, such as
`Ahmed_Yusef_2026-10-15_1.html`, with matching `.txt`, `.tex`, and (when saved or
compiled) `.pdf` files. The date is the local date when you build the update.
Build numbers start at 1 and increase within each output folder, including
across dates. Each tailored output folder has its own sequence. Failed
validation does not consume a number.

The builder keeps numbered exports, refreshes the `cv.html`, `cv.txt`, and
`cv.tex` convenience copies, and writes the latest PDF filename to `build.json`.
Keep the numbered exports and `build.json` to preserve the sequence; clearing
the whole output folder resets it. The HTML title and toolbar carry the same
filename. Saving a PDF twice from one preview does not create a new build.

First and last name default to the first and last words of your CV's name
heading. For compound names or preferred filename spelling, use:

```sh
python3 scripts/cv.py build --first-name "Ahmed" --last-name "Al Yusef"
```

This produces `Ahmed_Al-Yusef_YYYY-MM-DD_number` without changing the displayed
name. Spaces become hyphens within a name, and unsafe filename punctuation is
removed. Arabic letters are retained. Ask the assistant to save these filename
preferences and pass them on each build. An unfinished name placeholder uses
`FirstName_LastName`; a single-word name uses `Name_CV` unless overridden.

## Plain text

`output/cv.txt` is a text-only copy for application forms and quick reviews.
Links include their addresses, and formatting markers are removed. It is
generated; make changes in `cv.md` and rebuild.

## Optional LaTeX PDF

The builder also writes a complete numbered `.tex` file and its `output/cv.tex`
convenience copy, based on the original
MyResumeTemp section layout. It does not run a compiler or install TeX.

If you already have a TeX distribution with XeLaTeX and the packages declared
in `templates/resume.tex`, you can run from this folder:

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=output output/Ahmed_Yusef_2026-10-15_1.tex
```

Replace that example path with the numbered `.tex` path from your build.
XeLaTeX gives the PDF the same basename, such as
`output/Ahmed_Yusef_2026-10-15_1.pdf`. Do not compile the `cv.tex` convenience
copy if you want the required filename. The template uses Lato when installed and falls
back to TeX Gyre Heros. It needs fontspec, geometry, titlesec, enumitem, and
hyperref. Missing fonts or packages must be installed through your TeX setup.
There is no need to install a large TeX distribution just to use CVKeeper;
the browser route is the default.

The default LaTeX template targets English/Latin text. Arabic and other scripts
may need different fonts, language packages, and direction settings. For those
CVs, use the HTML/PDF route unless the template has been configured and tested.

## Tailored versions

Keep the master `cv.md` intact. Put each tailored Markdown source in `variants/`
and build it to a separate output directory:

```sh
python3 scripts/cv.py build --input variants/project-manager.md --output output/project-manager --strict
```

`build` replaces the convenience copies in the selected output folder on every
run while keeping numbered exports. It does not overwrite your source or
delete an older PDF. After any edit, save a new PDF using the new build's name;
an existing PDF does not update itself.

Keep the generated first-name, last-name, date, and build-number convention.
Review it yourself before sharing or submitting it.

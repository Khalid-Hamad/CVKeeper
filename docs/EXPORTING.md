# Deliver a real PDF

CVKeeper creates editable Markdown, a printable HTML preview, plain text,
LaTeX source, and (when a supported browser or client PDF tool is available)
an actual PDF. An `.html` file is still a webpage. Changing its extension to
`.pdf` does not convert it.

## Ask the LLM client first

The AI assistant should use the PDF/file-creation capability available in its
client, when present, and return a downloadable/openable `.pdf`. Claude Desktop
supports file creation in eligible sessions. In a folder-capable session it
should also keep `cv.md` and private `notes/` context updated.

The assistant must verify that the file is a PDF and inspect the pages when its
tools allow. If it can only create HTML, it must say "PDF export is incomplete"
instead of describing the webpage as the final CV.

## Bundled automatic PDF export

From the CVKeeper folder, the assistant can run:

```sh
python3 scripts/cv.py check
python3 scripts/cv.py build --strict --pdf
```

On Windows use:

```powershell
py -3 scripts/cv.py check
py -3 scripts/cv.py build --strict --pdf
```

The command detects Microsoft Edge, Google Chrome, or Chromium in the environment
where it runs, opens the generated HTML headlessly, and prints a real PDF. It
uses no Python packages. The PDF is saved directly in `output/` with its final
numbered filename. No browser window, print dialog, or manual Save is needed.
In remote/cloud AI sessions, the client may not see the
browser installed on the person's PC; the assistant should then use its native
PDF tools or explain the manual option below.

To specify a browser executable explicitly:

```powershell
py -3 scripts/cv.py build --strict --pdf --browser "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

If HTML was already built and only PDF export failed, retry without consuming a
new build number:

```powershell
py -3 scripts/cv.py pdf
```

The exporter verifies the PDF signature and end marker. This catches a webpage
renamed `.pdf`, but the assistant/person must still inspect layout and content.

## ATS-friendly PDF checks

The default template uses one column, ordinary headings, and real text. Apply
the same layout rules when using a client's native PDF tools. Keep contacts in
the main document flow and avoid images, layout tables, and text boxes.

Before delivery, extract text from the actual PDF using the client's PDF tools,
`pdftotext`, or `pypdf` if available. Compare all pages against the approved CV:
name, contacts, sections, roles, dates, and bullets must remain readable and in
order. Check Arabic and accented text explicitly. Inspect pages visually too.
Record checks and any limitations in `notes/review.md`; a PDF signature alone
does not prove ATS readability. Routine export requires no extra Python packages;
CI installs `pypdf` only to test actual PDF extraction.

Follow the employer's format requirements. No template guarantees acceptance
by every ATS. See the sourced [review checklist](../guides/REVIEW.md).

## Windows manual fallback

Only use this if automatic export is unavailable and you choose to print
manually. It is not part of the normal workflow.

1. Open `output/cv.html` in Edge or Chrome.
2. Press **Ctrl+P** or click **Print / Save PDF** in the preview.
3. In Edge choose **Microsoft Print to PDF** or **Save as PDF**. In Chrome choose
   **Save to PDF**. Do not press **Ctrl+S**; that saves a webpage.
4. Use A4 (or the paper size selected during the build), 100% scale, and disable
   browser headers and footers.
5. Save with the exact `.pdf` name shown above the preview, then open the PDF.
   Select some text and inspect every page for clipping, blank pages, and links.

## Names and build history

Numbered exports use `FirstName_LastName_YYYY-MM-DD_buildNumber`, such as
`Ahmed_Yusef_2026-10-15_1.pdf`. The date is the local build date. The number
increases within each output folder and previous builds stay in place.
`build.json` records the latest name and whether the bundled PDF exporter
completed. Filename handling belongs in the agent/build workflow, not the
person's starting prompt.

For compound names, the assistant can save preferences and pass:

```sh
python3 scripts/cv.py build --strict --pdf --first-name "Ahmed" --last-name "Al Yusef"
```

## Other generated formats

- `output/cv.html`: convenience copy of the latest browser preview.
- `output/cv.txt`: plain text for application forms and reading-order review.
- `output/cv.tex`: optional LaTeX source. XeLaTeX remains available for people
  who already use TeX, but it is not required for the browser PDF workflow.

For Arabic or another right-to-left CV, build with `--language ar --direction
rtl` and verify font rendering and reading order in the final PDF. The default
LaTeX template targets Latin text, so HTML/browser or client-native PDF export
is the recommended path for Arabic.

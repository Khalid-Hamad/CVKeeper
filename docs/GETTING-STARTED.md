# Getting started

## Download and open

On GitHub, use **Code → Download ZIP**. Extract the ZIP before opening any
files. The folder may be called `CVKeeper-main`; that is fine. Move it somewhere
you can find again, such as Documents. Double-click `START-HERE.html` for a
browser-friendly guide and fictional CV preview.

You do not need Git or your own repository. Downloading from a private GitHub
repository requires an account with access; a shared ZIP does not.
For a private working copy, avoid putting the folder in a public shared drive.

## Connect your AI assistant

In Claude Desktop, open Cowork and connect this extracted folder, or use its
Code workflow when available. In Codex, open the folder as a local project.
Use the official setup links in
`README.md` if your app does not expose this option. When the app asks for
folder permissions, grant access to the folder you chose. Availability depends
on the app, operating system, and your account.

Paste the starting prompt from `README.md` or `START-HERE.html`. The assistant
should read `AGENTS.md`, check for an existing `cv.md` and source CVs in `inbox/`,
and act as your CV writer/updater. It should learn your target field and ask
about real responsibilities, achievements, evidence, and timeline overlaps,
then save those answers under `notes/`. With an existing CV, you can improve it, update
only a few details, or keep its wording. If the app only replies with text, ask whether it has
file-editing access; otherwise use the chat-only route below.

## Import or start fresh

- **Existing CV:** place a copy in the included `inbox/` folder. Tell
  the assistant the filename. PDF and Word extraction depend on the assistant's
  tools; if it cannot read the file, paste its text. Review extracted dates and
  details, especially from scanned PDFs. Your original file stays unchanged;
  the assistant maintains an editable master in `cv.md`. It should ask only
  about missing details, not make you repeat your entire work history.
- **Starting fresh:** answer the assistant's questions. You can begin with
  education, projects, volunteering, or transferable skills if you have no
  formal employment history. Remove template sections that do not apply.

The master file is `cv.md`. The `.md` ending means Markdown: readable text with
a few symbols for headings and bullets. You do not need to learn it to work
through an assistant. The example in `examples/` is fictional and must not be
treated as your background.

## Check PDF tools with your assistant

Ask the assistant: “Check your available tools and export my CV directly as a PDF.”
It can use its native PDF tools when available. Otherwise, the bundled exporter
needs Python 3.9+ and Edge, Chrome, or Chromium where commands actually run.
The builder uses only Python's standard library, so there is no package install.
Python is not a prerequisite for the interview or for client-native PDF tools.

If Python is missing, install a supported Python 3 release from
[python.org](https://www.python.org/downloads/) using its official installer,
then reopen your AI app or terminal. On Windows, the commands in these docs
use `py -3` in place of `python3`. On some systems the executable is `python`;
check `python --version` before using it.

Your agent may need your app's permission to run local commands. CVKeeper
does not require an API key and does not call an AI API itself.

## Receive your PDF

The assistant should give you an actual `.pdf` plus editable `cv.md`. It may use
Claude Desktop's file creation or run `py -3 scripts/cv.py build --strict --pdf`
on Windows. The PDF is saved directly without a browser window or print dialog.
`output/cv.html` is an optional preview, not the finished PDF.

Ask for the saved PDF location or download link. The assistant handles the filename
and build number. Review every page before sending it. If export fails, it must
say so; a webpage is not a completed PDF. Optional manual printing is covered in
[the export guide](EXPORTING.md#windows-manual-fallback), not the normal workflow.

To revise anything, ask the assistant to edit the source and export a new PDF.
Changing the source does not update an already-created PDF automatically.

## Come back later

Open the same folder and say what changed. The assistant should read your
existing CV and saved career profile, back up changed sources in `history/`,
make the update, and rebuild. Your career facts, field guide, review, preferences,
and change notes live in `notes/`. For a specific job, keep the
description in `jobs/`; tailored copies live in `variants/` with their own
output folders. Back up the whole personal folder privately, including these
Git-ignored files.

## Chat-only fallback

1. Attach `AGENTS.md`, all three files in `guides/`, `templates/cv.md`,
   `templates/profile.md`, `templates/field-guide.md`, `templates/review.md`,
   and your old CV if you have one.
2. Paste the same short starting message. Explain that the assistant cannot edit
   your local folder. It should still interview you and use the review checklist.
3. Ask for a downloadable PDF, editable `cv.md`, and updated `profile.md`,
   `field-guide.md`, and `review.md`. Download them and keep the context files
   in `notes/`. Reattach those saved files in the next session instead of blank
   templates so the assistant can continue where you left off.

If the client cannot generate a PDF, it must explain that limitation. You can
use the [bundled exporter](EXPORTING.md#bundled-automatic-pdf-export) with the
downloaded `cv.md`, or switch to a file-capable session with PDF tools.
If given Markdown as text instead of a download, save it as plain text named
`cv.md`, not `cv.md.txt`, without surrounding triple backticks. On macOS TextEdit,
choose **Format → Make Plain Text** before saving. A folder-capable app is the
easier route if handling these files or terminal commands feels unfamiliar.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| “No such file” for the script | Open the terminal in the extracted folder containing README.md, or ask the assistant to do it. |
| Missing cv.md | Ask the assistant to initialize the CV, or run `python3 scripts/cv.py init`. |
| DRAFT banner | Replace the remaining `{{PLACEHOLDERS}}` with confirmed details or remove optional content, then rebuild. |
| Windows saved a webpage | Ask the assistant to export a real PDF using its PDF tools or `build --strict --pdf`. Ctrl+S saves HTML. |
| Old preview | Rebuild, then reload the HTML file. Changes to Markdown do not auto-refresh exports. |
| Missing or scrambled PDF text | Ask the assistant to compare extracted PDF text with the source and check fonts, reading order, and page breaks. |
| The agent cannot edit files | Choose a local-folder workflow or use the chat-only fallback. |
| Want a fresh start | Make a private backup first, then use a newly extracted copy of the starter. |

# Getting started

## Download and open

On GitHub, use **Code → Download ZIP**. Extract the ZIP before opening any
files. The folder may be called `CVKeeper-main`; that is fine. Move it somewhere
you can find again, such as Documents. Double-click `START-HERE.html` for a
browser-friendly guide and fictional CV preview.

You do not need to install Git, create a GitHub account, or publish a repository.
For a private working copy, avoid putting the folder in a public shared drive.

## Connect your AI assistant

Open a local-folder project in the OpenAI/Codex app or the Claude Code desktop
workflow and choose this extracted folder. Use the official setup links in
`README.md` if your app does not expose this option. When the app asks for
folder permissions, grant access to the folder you chose. Availability depends
on the app, operating system, and your account.

Paste the starting prompt from `README.md` or `START-HERE.html`. The assistant
should read `AGENTS.md`, check for an existing `cv.md` and source CVs in `inbox/`,
and ask what you want to change. With an existing CV, you can improve it, update
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

## Python prerequisite

Ask the assistant: “Check that Python 3.9 or newer is available and build my CV.”
The builder uses only Python's standard library, so there is no package install.

If Python is missing, install a supported Python 3 release from
[python.org](https://www.python.org/downloads/) using its official installer,
then reopen your AI app or terminal. On Windows, the commands in these docs
use `py -3` in place of `python3`. On some systems the executable is `python`;
check `python --version` before using it.

Your agent may need your app's permission to run local commands. CVKeeper
does not require an API key and does not call an AI API itself.

## Preview and save

The assistant runs the builder, then gives you `output/cv.html`. Double-click
it to open it in a browser. Choose **Save as PDF**, choose a PDF destination in
the print dialog, set paper to A4 (the default), and turn off headers and
footers. Save using the exact name shown above the CV, such as
`Ahmed_Yusef_2026-10-15_1.pdf`. The date is the local build date, and the final
number increases on each build in that output folder. Confirm the filename in
the save dialog. Review every page before sending. See `docs/EXPORTING.md` for details.

Closing or printing the preview does not change `cv.md`. To revise anything,
ask the assistant to edit the source and rebuild, then refresh the preview.

## Come back later

Open the same folder and say what changed. The assistant should read your
existing CV, back it up in `history/`, make the update, and rebuild. Your
preferences and change notes live in `notes/`. For a specific job, keep the
description in `jobs/`; tailored copies live in `variants/` with their own
output folders. Back up the whole personal folder privately, including these
Git-ignored files.

## Chat-only fallback

Attach `AGENTS.md`, `templates/cv.md`, and your old CV (if any) to the chat.
Explain that the assistant cannot edit local files and ask it to return the
complete CV as Markdown. Save the content in a plain-text editor as `cv.md`,
not `cv.md.txt`, in the root of this folder. Do not include surrounding triple
backticks. On macOS TextEdit, choose **Format → Make Plain Text** before saving.

Open a terminal in this folder and run `python3 scripts/cv.py check` followed
by `python3 scripts/cv.py build` (Windows: `py -3`). If terminal use is unfamiliar,
the folder-capable app route is the easier option.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| “No such file” for the script | Open the terminal in the extracted folder containing README.md, or ask the assistant to do it. |
| Missing cv.md | Ask the assistant to initialize the CV, or run `python3 scripts/cv.py init`. |
| DRAFT banner | Replace the remaining `{{PLACEHOLDERS}}` with confirmed details or remove optional content, then rebuild. |
| Old preview | Rebuild, then reload the HTML file. Changes to Markdown do not auto-refresh exports. |
| Missing text in a PDF | Check print scale, paper size, font support, and page breaks; see the export guide. |
| The agent cannot edit files | Choose a local-folder workflow or use the chat-only fallback. |
| Want a fresh start | Make a private backup first, then use a newly extracted copy of the starter. |

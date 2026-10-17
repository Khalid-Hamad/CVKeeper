# CVKeeper

**Your AI assistant, now your CV writer and updater.**

CVKeeper is a folder you use with Claude Desktop, Codex, or another AI app that
can work with files. It helps the assistant interview you, improve your CV,
remember your career details, and export a real PDF. It is not a separate AI app.

You do not need to learn coding, Git, or Markdown. Your assistant handles the files.

## Start here

1. **Download and extract.** On GitHub, select **Code → Download ZIP**, then
   extract the whole folder. `CVKeeper-main` is a normal folder name. You can
   also use a ZIP shared by the maintainer. Private GitHub repositories require
   an account with access; using an already-downloaded ZIP does not.
2. **Add your current CV, if you have one.** Put a copy in the included
   `inbox/` folder. Starting from scratch? Skip this step.
3. **Open the folder in your AI app.** Use a session that can read and edit
   local files, such as Claude Desktop's Cowork or Code workflow when available,
   or a local Codex project. Give it access to this folder.
4. **Paste this message:**

   > Read AGENTS.md and be my CV writer and updater. Guide me through the next step.

Prefer a visual guide? Double-click [START-HERE.html](START-HERE.html) in the
extracted folder. It opens offline and includes a fictional Ahmed Yusef example.
Opening that page alone does not start an AI conversation.

## What happens next?

- The assistant asks about your target field, role, and actual experience,
  a few questions at a time. It reuses information already in your CV.
- It follows up on responsibilities, achievements, missing details, and
  overlapping employment dates. It must not invent qualifications or results.
- It saves your career profile and field-specific writing guidance for future
  updates, then drafts and reviews the CV with you.
- It delivers a **real PDF** and an editable master named `cv.md`. The PDF name,
  update date, and build number are handled automatically. You do not need to
  open a browser page or use a print/save dialog during automatic export.

The bundled exporter saves PDFs in `output/`. An app using its own PDF tools
should link the saved file or provide a download. If it cannot produce a PDF,
it must explain the limitation, not present an HTML webpage as a finished CV.

## What do I need?

An AI app with file access and the account or subscription it normally requires.
For direct PDF creation, the assistant needs **either**:

- The app's own PDF-creation tools, when available; **or**
- Python 3.9+ and Edge, Chrome, or Chromium in the environment where it runs.
  The bundled exporter uses the browser in the background, without a window.

Ask the assistant to check what is available. Python is not needed just to
interview you or view the guide. Routine CVKeeper export needs no extra Python
packages, API key, server, or LaTeX installation. App features and access vary.

**My app only accepts attachments:** follow the
[chat-only instructions](docs/GETTING-STARTED.md#chat-only-fallback). You will
need to download and reattach your updated career files between sessions.

## Update your CV later

Keep the same folder. Reopen it in your assistant, ask it to read `AGENTS.md`,
and describe the change. It should reuse saved information, back up the previous
version, ask only relevant questions, and deliver an updated PDF.

| What you need | What to tell your assistant |
| --- | --- |
| Improve an old CV | “Improve the CV in inbox/. Ask about missing or unclear details.” |
| Keep the wording | “Import my CV without changing its wording. Flag concerns separately.” |
| Add experience | “Add my new role. Ask me for the details you need.” |
| Apply for a job | “Tailor a copy for this job description. Keep my master CV unchanged.” |
| Review before applying | “Review the facts, timeline, wording, and PDF readability.” |

More messages are in [prompts/](prompts/). Your assistant can create any needed
job-description or tailored-copy folders; you do not need to set them up first.

## Is it ATS-friendly?

ATS means **applicant tracking system**, the software employers use to manage
applications. The default CV layout uses one column, clear headings, visible
contact details, and real text rather than an image. The assistant is instructed
to check text extraction and reading order from the actual PDF.

No template guarantees that every ATS will parse it correctly or that you will
be shortlisted. Follow the employer's requested format and review the final
file. Arabic and other non-Latin text need their own rendering and text-order
checks. See the sourced [review checklist](guides/REVIEW.md).

## Where are my files?

| File or folder | Purpose |
| --- | --- |
| `inbox/` | Copies of your existing CV; originals stay unchanged |
| `cv.md` | Editable master CV, created during setup |
| `notes/` | Career profile, field guidance, preferences, and review notes |
| `output/` | Generated PDFs and optional previews from the bundled tools |
| `history/` | Backups made by the assistant before changes |
| `variants/` | Tailored copies for particular roles |

**Keep a private backup of the whole working folder.** Personal files are ignored
by Git and excluded by the starter ZIP packager, but that is not encryption or
automatic backup. A manually zipped folder can still contain personal data.
Your AI app processes information under its own data policies. CVKeeper does
not automatically upload, publish, or send your CV.

## Guides and support

- [Getting started and troubleshooting](docs/GETTING-STARTED.md)
- [Automatic PDF export and requirements](docs/EXPORTING.md)
- [Supported CV text format](docs/FORMAT.md)
- Official setup: [Codex app](https://learn.chatgpt.com/docs/app),
  [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
  [Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork),
  [Cowork projects](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork),
  [Claude file creation](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude).

<details>
<summary>Optional: terminal commands and maintainer checks</summary>

Most people can leave these steps to their assistant. Run commands from the
extracted folder. On Windows, replace `python3` with `py -3`.

```sh
python3 scripts/cv.py init
# Fill in cv.md with confirmed information, then:
python3 scripts/cv.py check
python3 scripts/cv.py build --strict --pdf
```

`init` preserves existing files. `--strict` rejects unresolved placeholders; it
does not verify career facts. `--pdf` creates the PDF directly. Without `--pdf`,
the build creates only HTML, plain text, and optional LaTeX source. Retry a failed
PDF export with `python3 scripts/cv.py pdf` without consuming another build number.
See [export details](docs/EXPORTING.md) for names, compound names, and RTL settings.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/cv.py check --input examples/cv.md
python3 scripts/cv.py build --input examples/cv.md --output output/example --strict --pdf
python3 scripts/package.py
```

The packager creates `dist/CVKeeper.zip` from an explicit list of starter files,
excluding personal workspace files. It works without Git. Inspect changes to
public starter files before sharing them.

CI runs checks on Linux, macOS, and Windows. Windows also generates real PDFs
and checks extracted text against short and multi-page sources using a test-only
`pypdf` dependency. These tests do not prove how an AI will interview a person
or certify every ATS. Complete the [live-test checklist](docs/LIVE-TEST.md)
before publishing. Nothing in CI publishes CVs.

</details>

CVKeeper is a reusable successor to
[MyResumeTemp](https://github.com/Khalid-Hamad/MyResumeTemp).
See [NOTICE.md](NOTICE.md) for provenance. [MIT licensed](LICENSE).

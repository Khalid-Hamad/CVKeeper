# CVKeeper

**Turn your LLM client into your personal CV writer and updater.**

A folder that gives Claude Desktop, Codex, or another file-capable LLM client
the interview process, private career memory, field-specific writing guidance,
review checks, and export tools needed to maintain your CV over time.

**New here? Double-click [START-HERE.html](START-HERE.html) after extracting the
ZIP.** It opens a local getting-started guide in your browser. No account,
installation, or internet connection is needed to view the guide and example.

[See the fictional example](examples/preview/cv.html) ·
[Setup guide](docs/GETTING-STARTED.md) · [Export a PDF](docs/EXPORTING.md)

## Start in three steps

1. **Get the folder.** On this repository's GitHub page, choose **Code →
   Download ZIP**, then extract it. Or clone this repository. Keep the whole
   folder together; Git and a GitHub account are not needed for the ZIP route.
2. **Open it in your LLM client.** Already have a CV? Put a copy in the included
   `inbox/` folder to improve it, make a specific update, or maintain it over
   time. Select the extracted `CVKeeper` folder as a
   local project in a folder-capable OpenAI/Codex app or Claude Desktop. Give the
   assistant access to this folder. A normal chat cannot edit local files
   unless your app provides that capability; see the fallback below.
3. **Paste this message:**

   > Read AGENTS.md and be my CV writer and updater. Guide me through the next
   > step.

The assistant first learns your target field and actual experience, then asks
about responsibilities, achievements, evidence, dates, and unexplained overlaps.
It saves that context in private `notes/` files so future updates do not restart
from zero. The final deliverable should be an actual PDF plus editable `cv.md`.

Save the PDF with the exact name shown in the preview, for example
`Ahmed_Yusef_2026-10-15_1.pdf`: first name, family name, update date, and build
number. The number increases with each build in that output folder.

**Requirements:** a folder-capable LLM client and its usual account access.
Python 3.9+ plus Edge, Chrome, or Chromium lets the bundled tool create a PDF
directly. Claude Desktop can also use its own PDF/file-creation capability when
available. CVKeeper has no Python packages, API keys, server, or LaTeX requirement.

## Keep it current

| What you need | What to tell your assistant |
| --- | --- |
| Start from an old CV | “Read AGENTS.md. Import the CV I put in inbox/. Ask about anything unclear.” |
| Add a new role | “Read AGENTS.md. Add my new role. Ask me for the details you need.” |
| Improve wording | “Review my CV for clarity and repetition. Preserve my facts and show what changed.” |
| Apply for a job | “Use the job description in jobs/. Create a tailored version and keep my master CV unchanged.” |
| Check before sending | “Review my CV for missing evidence, date overlaps, and readability. Deliver the final PDF.” |

The visible prompt stays short because the full writer/updater process lives in
`AGENTS.md` and `guides/`. The assistant saves your career profile, personalized
field practices, open questions, and review state as it works.

## Pick your tool

- **OpenAI / Codex:** open the local folder in a project that can edit files.
  Codex uses the root `AGENTS.md`. See the [official app guide](https://learn.chatgpt.com/docs/app)
  and [agent instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- **Claude Desktop:** use Cowork with this local folder, or the Code workflow
  when available. Start a new session with the same folder and paste the short
  prompt. `CLAUDE.md` imports the shared instructions for Claude Code. See the
  [official Cowork guide](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork),
  [Cowork projects guide](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork), and
  [file-creation guide](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude).
- **Terminal users:** from this folder, start `codex` or `claude` after
  installing and signing in to your preferred tool. Use the same prompt.
- **Chat-only apps:** attach `AGENTS.md`, the three files in `guides/`, the
  private context templates, and your existing CV. Ask for updated `cv.md`,
  `profile.md`, `field-guide.md`, and `review.md` downloads. Reattach them next
  time. A normal chat cannot maintain the local folder unless the app gives it
  file access.

App interfaces and access vary; the official guides above are the setup reference.

## What's in the folder?

```text
START-HERE.html       Open this first after downloading the ZIP
AGENTS.md            Shared instructions for AI assistants
CLAUDE.md            Loads AGENTS.md for Claude Code-compatible sessions
templates/           Blank CV and export styles
guides/              Career interview, field practices, and review gate
examples/            Fictional example and ready-to-open exports
inbox/               Included folder for your existing CV (contents stay private)
prompts/             Create, import, update, tailor, and review prompts
docs/                Setup, formatting, export, and live-test guides
scripts/             Small, offline Python builder and ZIP packager
tests/               Automated checks for the tools
```

During use, the assistant creates `cv.md`, `notes/profile.md`,
`notes/field-guide.md`, `notes/review.md`, `output/`, and other private working
folders. Those are excluded from Git by default. Copy your whole
personal folder to a private backup location periodically; ignored files are
not backed up by a Git commit.

## Build it yourself

Run these commands from the extracted folder. On Windows, replace `python3`
with `py -3`.

```sh
python3 scripts/cv.py init
# Edit cv.md, then:
python3 scripts/cv.py check
python3 scripts/cv.py build --strict --pdf
```

Each build saves named `.html`, `.txt`, and `.tex` files using
`FirstName_LastName_YYYY-MM-DD_buildNumber`, and retains earlier builds.
`output/cv.html`, `output/cv.txt`, and `output/cv.tex` are convenient copies of
the latest build; `output/build.json` records its exact PDF filename.
With `--pdf`, the builder uses installed Edge, Chrome, or Chromium to produce
an actual PDF. Without it, HTML is only a preview. Run `python3 scripts/cv.py
pdf` to export the latest HTML without creating another build number.
Unfilled placeholders
are flagged; use `build --strict` to require a complete draft.

Names default to the first and last words of the CV heading. For compound
names, use `--first-name "Ahmed" --last-name "Al Yusef"`; this makes
`Ahmed_Al-Yusef_YYYY-MM-DD_number` without changing the name displayed on the CV.
Arabic filename characters are supported. See [export details](docs/EXPORTING.md).

```sh
python3 scripts/cv.py build --input examples/cv.md --output output/example --strict
python3 scripts/cv.py build --input variants/analyst.md --output output/analyst --paper letter --strict
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

The last command creates `dist/CVKeeper.zip` from an explicit list of starter
files, excluding your personal workspace. It works without Git.

## Privacy and scope

The builder runs locally and makes no network requests. Your AI app has its
own data handling policies; share only what you intend it to process. Personal
files are ignored by Git, but that does not encrypt them, protect files already
tracked, or remove them from a ZIP you make manually. Use the starter packager
when sharing the template. Nothing automatically uploads or releases your CV.

The layout uses one column and selectable text. Check the exported PDF's text
and reading order before applying; no template guarantees ATS compatibility.
HTML supports Unicode and an optional right-to-left layout. The default LaTeX
export is designed for English/Latin text. See [limitations](docs/EXPORTING.md).

## For maintainers

Use the [live-test checklist](docs/LIVE-TEST.md) before sharing the project.
CI runs tests and builds the fictional example on Linux, macOS, and Windows;
it does not publish CVs. Contributions should preserve the simple offline
workflow and avoid adding dependencies for routine edits.

CVKeeper is a reusable successor to [MyResumeTemp](https://github.com/Khalid-Hamad/MyResumeTemp).
It keeps the section-based CV workflow and optional LaTeX output while removing
the need to edit LaTeX or publish a personal CV through GitHub releases.
See [NOTICE.md](NOTICE.md) for provenance. [MIT licensed](LICENSE).

# CVKeeper

**Your CV. Your files. Your AI assistant.**

A folder you can give to an AI assistant to create, update, and tailor your CV.
Download it as a ZIP or clone it, open the folder in your AI app, and explain
what you need in your own words. Your CV stays in readable, editable files.

**New here? Double-click [START-HERE.html](START-HERE.html) after extracting the
ZIP.** It opens a local getting-started guide in your browser. No account,
installation, or internet connection is needed to view the guide and example.

[See the fictional example](examples/preview/cv.html) ·
[Setup guide](docs/GETTING-STARTED.md) · [Export a PDF](docs/EXPORTING.md)

## Start in three steps

1. **Get the folder.** On this repository's GitHub page, choose **Code →
   Download ZIP**, then extract it. Or clone this repository. Keep the whole
   folder together; Git and a GitHub account are not needed for the ZIP route.
2. **Open it in your assistant.** Already have a CV? Put a copy in the included
   `inbox/` folder to improve it, make a specific update, or maintain it over
   time. Select the extracted `CVKeeper` folder as a
   local project in a folder-capable OpenAI/Codex app or Claude Code. Give the
   assistant access to this folder. A normal chat cannot edit local files
   unless your app provides that capability; see the fallback below.
3. **Paste this message:**

   > Read AGENTS.md and help me create my CV. First check whether I already
   > have a master CV or an existing CV in inbox/ (ignore its README.md). If I
   > have one, ask whether to improve it, update it, or preserve its wording.
   > Otherwise, offer import or a short interview. Use only facts I
   > confirm, and build a preview when the draft is ready. Handle the file work
   > for me and explain how I can save the result as a PDF.

The assistant creates `cv.md`, asks about your background, and builds
`output/cv.html`. Open that file, choose **Save as PDF**, and save using your
browser's print dialog. Keep `cv.md` for future updates.

Save the PDF with the exact name shown in the preview, for example
`Ahmed_Yusef_2026-10-15_1.pdf`: first name, family name, update date, and build
number. The number increases with each build in that output folder.

**Requirements:** a folder-capable AI app/CLI and its usual account access for
the assisted workflow; Python 3.9+ to generate exports; a browser to view and
print them. The assistant can check Python for you. CVKeeper has no Python
packages, API keys, server, paid dependency, or LaTeX requirement for this path.
Your AI provider may charge for its service. You can also edit and build without AI.

## Keep it current

| What you need | What to tell your assistant |
| --- | --- |
| Start from an old CV | “Read AGENTS.md. Import the CV I put in inbox/. Ask about anything unclear.” |
| Add a new role | “Read AGENTS.md. Add my new role. Ask me for the details you need.” |
| Improve wording | “Review my CV for clarity and repetition. Preserve my facts and show what changed.” |
| Apply for a job | “Use the job description in jobs/. Create a tailored version and keep my master CV unchanged.” |
| Check before sending | “Review my CV for missing facts, inconsistent dates, and readability. Build the final preview.” |

Longer reusable prompts live in [prompts/](prompts/). The agent instructions
include backups, fact checking with you, and separate tailored versions.

## Pick your tool

- **OpenAI / Codex:** open the local folder in a project that can edit files.
  Codex uses the root `AGENTS.md`. See the [official app guide](https://learn.chatgpt.com/docs/app)
  and [agent instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- **Claude Code:** select the folder in the desktop Code workflow or run
  `claude` from it. `CLAUDE.md` imports the shared instructions. See the
  [official desktop guide](https://code.claude.com/docs/en/desktop) and
  [memory guide](https://code.claude.com/docs/en/memory).
- **Terminal users:** from this folder, start `codex` or `claude` after
  installing and signing in to your preferred tool. Use the same prompt.
- **Chat-only apps:** attach `AGENTS.md`, `templates/cv.md`, and your existing
  CV if you have one. Ask for a complete updated `cv.md`, then save it as plain
  UTF-8 text in this folder. You must run the builder yourself or use a
  folder-capable assistant. Uploading files does not grant local folder access.

App interfaces and access vary; the official guides above are the setup reference.

## What's in the folder?

```text
START-HERE.html       Open this first after downloading the ZIP
AGENTS.md            Shared instructions for AI assistants
CLAUDE.md            Loads AGENTS.md for Claude Code
templates/           Blank CV and export styles
examples/            Fictional example and ready-to-open exports
inbox/               Included folder for your existing CV (contents stay private)
prompts/             Create, import, update, tailor, and review prompts
docs/                Setup, formatting, export, and live-test guides
scripts/             Small, offline Python builder and ZIP packager
tests/               Automated checks for the tools
```

During use, the assistant creates `cv.md`, `output/`, and any needed private
working folders. Those are excluded from Git by default. Copy your whole
personal folder to a private backup location periodically; ignored files are
not backed up by a Git commit.

## Build it yourself

Run these commands from the extracted folder. On Windows, replace `python3`
with `py -3`.

```sh
python3 scripts/cv.py init
# Edit cv.md, then:
python3 scripts/cv.py check
python3 scripts/cv.py build
```

Each build saves named `.html`, `.txt`, and `.tex` files using
`FirstName_LastName_YYYY-MM-DD_buildNumber`, and retains earlier builds.
`output/cv.html`, `output/cv.txt`, and `output/cv.tex` are convenient copies of
the latest build; `output/build.json` records its exact PDF filename.
PDF is created through your browser or an optional XeLaTeX installation.
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

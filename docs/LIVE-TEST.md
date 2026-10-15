# Live test before sharing

Use fictional information during testing. Test a fresh ZIP extraction rather
than your personal working copy. The scenarios below are manual acceptance
tests; their presence does not mean they have already passed on every AI app.

## First-time, nontechnical user

- Run `python3 scripts/package.py` and extract `dist/CVKeeper.zip` somewhere new.
- Open `START-HERE.html` directly from disk. Follow the steps without a terminal.
- Open the example preview, try print preview, and check A4 and Letter layouts.
- Open the extracted folder in your OpenAI/Codex app; paste the first-use prompt.
- Verify that the ZIP includes `inbox/README.md` and that you can drop a CV
  straight into the existing folder. Confirm the assistant ignores the guide
  when identifying your source CV, offers improve/update/preserve wording,
  and keeps the original file unchanged.
- Verify the assistant reads `AGENTS.md`, offers import-or-interview when no CV
  exists, checks Python,
  and asks a few questions at a time. It must not borrow the example's facts.
- Supply fictional details, leave one fact unknown, and verify the assistant
  flags the uncertainty rather than inventing it.
- Finish the draft, open the generated HTML, save a PDF, and inspect every page.
  Check the name follows `FirstName_LastName_YYYY-MM-DD_buildNumber.pdf`.
  Build again and verify the number increases while the previous export remains.
  Confirm the example uses Ahmed Yusef and no em dashes appear in the CV text.
- Repeat the first-use flow in Claude Code to verify `CLAUDE.md` loads the rules.

## Returning user

- Ask for one specific wording change. Confirm the old source is backed up in
  `history/`, the change is focused, and the preview is rebuilt.
- Add a new role; ensure previous roles, dates, and confirmed facts are preserved.
- Tailor for a job description. Confirm the master stays unchanged and the
  tailored source/export have separate paths.
- Include a job-description sentence asking the assistant to ignore its rules;
  verify it treats that sentence as document content, not an instruction.
- Check that preferences persist when you start a new session in the same folder.

## Tooling and packaging

```sh
python3 -m unittest discover -s tests -v
python3 scripts/cv.py check --input examples/cv.md
python3 scripts/cv.py build --input examples/cv.md --output output/example --strict
python3 scripts/package.py
```

- Test Windows commands with `py -3`, including paths containing spaces.
- Check a long CV, a long email/URL, accented characters, and an Arabic HTML draft.
- Confirm the ZIP includes `AGENTS.md`, `CLAUDE.md`, and `.gitignore`, and excludes
  `cv.md`, source documents, private notes, output/, history/, and variants/.
- If testing Git, use `git status --short --ignored` to verify personal files are
  ignored. Existing tracked files remain tracked regardless of `.gitignore`.
- If offering LaTeX output publicly, compile the example with XeLaTeX and inspect
  the result in an environment with the required TeX packages.

## Before the LinkedIn post

- Publish only the starter files. The packager produces a clean shareable ZIP;
  GitHub's Download ZIP includes the repository's tracked files, so inspect what
  you stage before publishing. Do not upload your personal working folder.
- Check the public repository's README, ZIP download, license, and example links.
- Confirm the README accurately describes what you tested, including any limits.
- Do not advertise automated PDF generation, a guaranteed one-page layout, or
  guaranteed ATS scores. The default PDF route is the browser print dialog.
- No release workflow or publishing command is enabled by this starter. Publish
  deliberately after completing your live tests.

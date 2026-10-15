# Live test before sharing

Use fictional information during testing. Test a fresh ZIP extraction rather
than your personal working copy. The scenarios below are manual acceptance
tests; their presence does not mean they have already passed on every AI app.

## First-time, nontechnical user

- Run `python3 scripts/package.py` and extract `dist/CVKeeper.zip` somewhere new.
- Open `START-HERE.html` directly from disk. Follow the steps without a terminal.
- Open the example preview, try print preview, and check A4 and Letter layouts.
- In Claude Desktop on Windows, create a Cowork project with the extracted local
  folder (or use Code when available), then paste the first-use prompt.
- Verify that the ZIP includes `inbox/README.md` and that you can drop a CV
  straight into the existing folder. Confirm the assistant ignores the guide
  when identifying your source CV, offers improve/update/preserve wording,
  and keeps the original file unchanged.
- Verify the assistant reads `AGENTS.md`, identifies the target field/role,
  seniority and market before focusing on name/contact data, and asks at most
  three questions at a time. It must not borrow the example's facts.
- Give it a CV that lists titles but weak descriptions. Verify it creates
  `notes/profile.md`, `notes/field-guide.md`, and `notes/review.md`, then asks
  about actual responsibilities, contributions, results, and evidence.
- Include two materially overlapping role date ranges. Verify it asks whether
  they were concurrent, part-time/consulting, a promotion, or a date error. It
  must preserve the dates until answered and avoid double-counting duration.
- Supply fictional details, leave one fact unknown, and verify the assistant
  flags the uncertainty rather than inventing it.
- Finish the draft and verify the assistant delivers an actual PDF, not only
  `cv.html`. Confirm its bytes begin with `%PDF-`, open it, and inspect every page.
  On Windows, test `py -3 scripts/cv.py build --strict --pdf` with Edge or Chrome.
  Also verify the manual fallback says Ctrl+P, not Ctrl+S.
  Check the name follows `FirstName_LastName_YYYY-MM-DD_buildNumber.pdf`.
  Build again and verify the number increases while the previous export remains.
  Confirm the example uses Ahmed Yusef and no em dashes appear in the CV text.
- Start a second Claude Desktop session with the same folder. Verify it reads
  the saved profile and asks only the next unanswered questions.

## Returning user

- Ask for one specific wording change. Confirm the old source is backed up in
  `history/`, the change is focused, the affected timeline is checked, and an
  updated PDF is created without restarting the full interview.
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
python3 scripts/cv.py build --input examples/cv.md --output output/example --strict --pdf
python3 scripts/package.py
```

- Test Windows commands with `py -3`, including paths containing spaces, and
  confirm Edge/Chrome discovery plus the `--browser` override.
- Check a long CV, a long email/URL, accented characters, and an Arabic HTML draft.
- Confirm the ZIP includes `AGENTS.md`, `CLAUDE.md`, all `guides/`, the private
  context templates, and `.gitignore`, and excludes
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
- Describe automatic PDF generation as requiring the client's PDF capability
  or Edge/Chrome/Chromium in its execution environment. Do not promise it when
  only HTML was created. Do not advertise a guaranteed page count or ATS score.
- No release workflow or publishing command is enabled by this starter. Publish
  deliberately after completing your live tests.

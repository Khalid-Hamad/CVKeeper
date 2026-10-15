# Review gate before final delivery

Use the reviewing role after writing and on each affected part of an update.
Record the result in `notes/review.md`, with the source/version reviewed.
This is an editorial process; the Python `check` command only checks syntax,
links, and placeholders. It does not verify career facts or interview quality.

## Required coverage

- Target field, role, level, market, and CV language are known or explicitly
  deferred by the person. The personal field guide reflects that context.
- Every relevant role has enough confirmed detail to describe the person's
  contribution. Ask about missing responsibilities/outcomes before finalizing.
  Unsupported metrics are omitted, not guessed.
- The complete known timeline has been compared for overlaps, multiple current
  roles, impossible dates, and uncertain month precision. Explanations are
  recorded. Only ask questions not already resolved in the profile.
- Education status, credentials, skills, and links are accurate to the provided
  evidence. Relevant projects/volunteering have been considered.
- Name/contact details are correct, without spending the interview on them.
- Wording matches the person's scope and target. No invented facts, generic
  grand claims, needless repetition, or em dashes in newly drafted content.

## Decide the status

For each area record Reviewed, Needs answer, Declined, or Not applicable,
with the supporting note. Never check a box simply because a template exists.
Blocking issues include an unconfirmed factual claim, a material unexplained
date contradiction, and missing evidence for a claimed qualification.

If a blocker remains, ask the specific question or remove the unsupported
claim with the person's agreement. A user-requested early draft is allowed,
but label it provisional and list unresolved issues. Do not force someone to
share private reasons for a career gap or demand numbers they do not have.

## PDF delivery gate

1. Keep an editable `cv.md` matching the final content and save career context.
2. Use the app's available PDF tools or `build --strict --pdf`. A successfully
   built HTML preview is not evidence that PDF export succeeded.
3. Confirm an actual PDF file exists (PDF bytes begin with `%PDF-`; extension
   alone is insufficient). If using the bundled exporter it checks the PDF
   header and end marker, but still requires a content/layout review.
4. Open/render every PDF page when tools allow. Check clipping, blank pages,
   unreadable scripts, headings stranded at page bottoms, links, and text order.
   If you cannot inspect it, say which checks the person should perform.
5. Link the PDF first and the editable source second. If export is blocked,
   clearly say "PDF export is incomplete" and explain the available next step.
   On Windows the manual fallback is Ctrl+P and a PDF printer, never Ctrl+S.

Do not mark a draft final just because the user has answered name/contact
questions, the HTML looks polished, or the build command returned success.

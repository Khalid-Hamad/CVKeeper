# CV source format

`cv.md` is the source of truth. The builder supports a small Markdown subset
so that the same content can produce HTML, plain text, and LaTeX without
installing packages. It is not a general Markdown engine.

```markdown
# Your Name

Your professional headline

City, Country | [you@example.com](mailto:you@example.com)

## Summary

A short summary grounded in your confirmed experience.

## Experience

### Job Title | Organization

January 2024 - Present | Location

- An action you took and its verified outcome.
- Another relevant contribution.

## Skills

**Category:** Skill, skill, skill.
```

Rules:

- Exactly one `# ` heading, first, for the name.
- `## ` starts a section. At least one section is required. Name and reorder
  sections freely: Education, Experience, Projects, Volunteering, Awards,
  Languages, Certifications, or others that fit the person.
- `### ` starts an entry inside a section. Its first paragraph is styled as
  metadata (dates and location) in HTML.
- Separate paragraphs with a blank line. Wrapped lines within a paragraph
  are joined with spaces.
- `- ` creates an unindented bullet. No nested lists.
- `**text**` creates bold text. `[label](https://example.com)` creates a link.
  Links must use `https://`, `http://`, `mailto:`, or `tel:`. Percent-encode
  spaces and parentheses in addresses. Bold inside links and links inside
  bold are not supported; use one style at a time.
- Single-asterisk italics, tables, images, code blocks, blockquotes, ordered
  lists, and raw HTML formatting are not supported. HTML-like text is printed
  literally. Unsupported block syntax is reported where recognized.
- Use `{{DESCRIPTIVE_PLACEHOLDER}}` for missing facts. `check` and `build
  --strict` fail until these are filled or removed. Normal `build` produces
  an explicitly marked draft, useful during an interview.

There is no fixed schema for jobs or dates. The assistant and owner must check
accuracy, chronology, consistency, and completeness. A successful `check`
does not establish that any statement is true or that every section is useful.

Use natural, direct wording. The starter uses a pipe between a role and
organization and ordinary hyphens for dates. Avoid em dashes in new CV prose.

Use UTF-8 text. HTML supports non-English text. For Arabic, for example:

```sh
python3 scripts/cv.py build --language ar --direction rtl
```

These flags set HTML language and direction; they do not translate content or
configure Arabic typesetting in LaTeX. Review mixed-direction text in the
browser and PDF. LaTeX requires separate font/language setup for such scripts.

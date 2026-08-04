---
name: writing-job-application
version: 1.3.0
description: Write evidence-grounded cover letters, job-application answers, interview self-introductions, and recruiter responses from a user's resume. Use when the user asks to draft or revise these application materials for senior, lead, or management roles.
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Job Application Writing

Write focused application materials for senior, lead, and management roles. Preserve the source of every factual claim while adapting the emphasis to the target role.

## Workflow

### 1. Establish the assignment

Identify the document type, target role, company, output language, job description, and any word, character, or speaking-time limit. Ask only for information that is missing and relevant to the selected document type. Accept that the user may have no personal connection to the company; use a direct, evidence-led opening in that case.

Read [references/formats.md](references/formats.md) after identifying the document type. The assignment is established when the applicable inputs in that reference are known or explicitly unavailable.

### 2. Select and read evidence

Use a resume or facts supplied in the current conversation first. A purely logistical recruiter response does not require a resume.

When factual candidate background is required and no resume is available, resolve the directory containing this `SKILL.md` as `SKILL_DIR`, keep the current working directory at the project root, and run:

```bash
bash "$SKILL_DIR/scripts/scan-resumes.sh" "$PWD/resumes" "$HOME/.agents/resumes"
```

Handle the `RESUME_COUNT` result as follows:

- For one result, select and read it.
- For multiple results, show the paths and metadata, then ask which version to use.
- For zero results, ask the user to provide a path or attach a resume.

Ask for permission before copying a supplied resume into `~/.agents/resumes/`. After consent, preserve the filename, quote every path, and avoid overwriting an existing file.

For PDF resumes, run `python3 "$SKILL_DIR/scripts/read-pdf.py" RESUME_PATH`. The script tries `pypdf` first and `pdftotext` second. Treat a nonzero exit as a blocked read and ask for another readable format. Read Markdown resumes directly.

Build an internal evidence map for each candidate claim: what happened, where it happened, when it happened, and which supplied source supports it. This step is complete when every planned factual claim maps to the resume or an explicit user statement.

### 3. Draft the selected format

Follow the selected branch in [references/formats.md](references/formats.md). A user-provided length limit overrides every default in the reference.

Prefer one or two recent, role-relevant examples. Show decisions, constraints, trade-offs, team enablement, and business impact when the evidence supports them. Use verified metrics when available; otherwise describe verified scope or outcomes without manufacturing numbers.

Write in the language requested by the user. If none is requested, match the language of the application prompt or job description.

### 4. Validate and deliver

Verify all of the following:

- Every skill, metric, project, employer, and timeline maps to its actual source.
- The draft answers the selected prompt and respects its word, character, or speaking-time limit.
- The draft uses connected plain-text paragraphs, with normal sentence punctuation rather than Markdown, lists, tables, or em dashes.
- The opening is specific and evidence-led; interest appears through relevant choices and outcomes.
- The draft focuses on no more than two core examples and avoids tool or keyword stacking without business context.

Pass the exact candidate output to `python3 "$SKILL_DIR/scripts/check-format.py"` through standard input. Revise until it exits successfully.

Return only the finished application content by default so it can be pasted directly into the target field. Add rationale or revision notes only when the user asks for them. The work is complete when every validation item passes and the output contains only the requested artifact.

## Script contracts

- `scripts/scan-resumes.sh [local-directory] [global-directory]` prints a stable result count and resumes sorted by modification time.
- `scripts/read-pdf.py PDF_PATH` prints extracted text to standard output and reports failures through a nonzero exit.
- `scripts/check-format.py [TEXT_FILE]` reads a UTF-8 file, or standard input when no file is provided, and rejects non-pasteable formatting.

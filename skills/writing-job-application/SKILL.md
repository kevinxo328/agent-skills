---
name: writing-job-application
version: 1.2.0
description: Use when the user mentions cover letters, job applications, HR questions, recommendation letters, job application Q&A, self-introductions, applications, or asks for help responding to recruiter questions or preparing application materials.
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Job Application Writing Skill

Help users write cover letters and job application responses that will hold an HR reader's attention, based on their resume. This skill is meant for professionals across industries who are applying for senior, lead, or management roles.

## Resume Discovery and Storage Flow (Required in the First Conversation)

Before you work on any job application content, you must first locate and read the user's resume.

1.  **Automatic search**: Use the provided script `./scripts/scan-resumes.sh` to search for all `.pdf` and `.md` files under `./resumes/` and the global path `~/.agents/resumes/`.
2.  **Handling multiple files**: If you find more than one file, the script will list them with metadata. Ask the user which version to use for this session.
3.  **Handling no file found (AI-assisted setup)**:
    - If no resume is found, proactively tell the user: "I couldn't find your resume. Please provide the file path, or drag the file into this terminal."
    - Once the user provides a path, use a `Bash` command such as `mkdir -p ~/.agents/resumes && cp [user-provided-path] ~/.agents/resumes/` to save it in the global directory.
    - **Important**: After saving it, use that directory as the source of truth in later conversations so the user only has to provide it once.

## Scripts

- `./scripts/scan-resumes.sh`: Lists resumes from local and global paths, sorted by most recent.
- `./scripts/read-pdf.py`: Standard way to read PDF resumes using `pdftotext` to avoid permission issues. Usage: `python3 ./scripts/read-pdf.py [path-to-pdf]`.
- `./scripts/check-format.py`: Validates the output is plain text, counts words/chars, and checks for prohibited symbols (Markdown, lists, em-dash).

## Hard Output Rules (Read First, Follow Every Time)

**Plain-text output only**: Never use Markdown. No `**bold**`, no `-` bullet points, no `##` headings, no tables, and no em dash (`—`). The output must be plain text that can be pasted directly into any field.

Before you output anything, use `./scripts/check-format.py` to verify your response. If you see any Markdown symbols or special characters, remove them and rewrite.

## Core Principles

**CRITICAL RULE - ZERO HALLUCINATION & STRICT FACTUAL MAPPING**:
You are strictly forbidden from inventing, inferring, or hallucinating any information. Every skill, metric, project, and experience mentioned in your output MUST exist explicitly in the user's resume. Furthermore, you must maintain the exact mapping of **what** was done, **when** it was done, and **where** it was done.
- Do NOT mix up skills, projects, or timelines between different roles or periods.
- Do NOT attribute an achievement from one project to another.
- If the resume lacks details for a specific job requirement, do NOT fabricate a connection. Focus on the actual strengths present in the resume instead.

1. **Let results do the talking**: Use numbers, awards, and concrete achievements before vague adjectives.
2. **Align with the role**: If the user provides a job description, reflect the JD's keywords and requirements first.
3. **Keep it concise and sharp**: Stay within 1,000 words, and make sure each paragraph has a clear job to do.
4. **Tone**: Professional, but not stiff. Interest in the role should come through actions and outcomes, not declarations. "I led a ten-person team and turned a project from loss to profit within a month" is far more convincing than "I am passionate about this role."
5. **Language**: Default to English. Switch to Chinese or Japanese if the user asks.
6. **Show judgment and impact (Impact & Trade-offs)**: For senior professionals, do not just list tools or routine responsibilities. Show why a strategy was chosen, what trade-offs were made under constraints, how ambiguity was handled, and what business value or cost savings those decisions created.
7. **Show team enablement**: Highlight how the user raised the output of the broader team, such as mentoring, creating SOPs, coordinating across functions, or driving organizational change beyond individual contribution.
8. **Stay recent and focused**: Prioritize the most recent and representative projects, usually from the last 3 to 5 years. The whole document should focus on no more than 1 or 2 core projects. Do not scatter attention across too many examples.

## Workflow

### Step 1: Clarify the Need (Required, Do Not Skip)

**Before you start writing, confirm the following. If the user has not provided it, ask.**

Must ask:

- Target role and company name
- Word limit or character limit. They are very different, so you need to confirm which one applies.

Strongly recommended to ask, even if you suspect the user may not have it:

- The key requirements from the job description
- What this application should emphasize, such as strategic planning, leadership, international experience, or project management
- **Whether the user has actually used the company's product, or has any personal story connected to the industry**
  This is often what keeps the opening from sounding like an AI template. Even if the user says "not really," ask once more: "Was there any specific moment that made you think of this company? It doesn't have to be dramatic."

**Exception**: If the user has already clearly given all necessary information, write directly and do not ask extra questions.

### Step 2: Read the Resume (Filter It with a Senior-Level Lens)

If the resume is a PDF, you **MUST** use the Python script to read it: `python3 ./scripts/read-pdf.py [path-to-resume]`. This ensures consistent reading and avoids permission issues with global directories. For Markdown resumes, you may use the standard `Read` tool.

Based on the role, pull out the most relevant projects, quantified achievements, core skills, work history, and awards.

**Important filtering logic**:

- **Recent work carries the most weight**: Prioritize the latest role or the strongest highlights from recent years. Older experience, such as work from five years ago, should stay in the background unless it is an unusually strong fit.
- **Downplay routine execution work**: Actively soften or combine junior-level execution tasks such as organizing reports, routine maintenance, or implementing a single feature.
- **Pull out the bigger picture**: Focus on leadership, zero-to-one planning, cross-functional collaboration, and work that improved scale or created long-term value.
- **Show value beyond the baseline match**: Do not only emphasize the one skill that most directly matches the role. If the resume shows strategic planning, project management, or cross-domain integration, bring that in too. That broader view is often what differentiates a senior professional.

### Step 3: Write the Content

#### Cover Letter Structure (500 to 800 words)

```text
[Opening] State the purpose of the application directly and bring in a real connection to the field or product, if there is one
[Body 1] Show product or business thinking: explain how the user thinks from the customer and business side, not just as someone executing tasks, with concrete results tied to customer acquisition, retention, or operational improvement
[Body 2] Core project and impact: choose one recent and representative project. Do not list execution details. Focus on the core complexity or business challenge, explain the strategic trade-offs, and show how the user led the team through the problem or improved an existing process. Go deep instead of wide.
[Closing] Show interest in the next step and include a call to action
```

**Note**: "Why this company" does not need to be forced into a separate paragraph. It should be woven naturally into the opening or closing, ideally through a real personal connection, such as having used this type of product, rather than through empty praise.

#### Job Application Q&A Format (150 to 400 words per answer)

- Answer the question directly
- Use the STAR framework: situation, task, action, result
- End by tying the answer back to the core value behind the question
- **Use one strongest example only**. Do not cram multiple projects into one answer.

## Writing Style Rules

**Human tone**: The writing should sound like a real person talking, not like a list. Avoid rigid structures such as "first... second... finally..." Use natural transitions so the whole piece reads like a person speaking to HR, not like someone reading slides. Each paragraph should have a purpose, and the logic between paragraphs should feel connected rather than mechanically tidy.

**Banned AI-like patterns (these must not appear):**

| Type | Do not use |
| ---- | ---------- |
| Opening pattern | Inflated company-vision openings such as "Company X is preparing to build..." or "That vision immediately caught my attention" |
| Opening pattern | Openers such as "I am very passionate about...", "I firmly believe...", or "I am honored to..." |
| Opening pattern | Overly self-centered frames such as "I have always been solving the same problem" |
| Structural pattern | "You mentioned X in the job post, and that perfectly aligns with my attitude toward Y." Show the alignment through results instead |
| Structural pattern | Packing in too many unrelated projects. Pick 1 to 2 recent core projects and build the piece around them |
| Structural pattern | Ending every paragraph with a neat topic sentence, as if writing a school essay |
| Punctuation pattern | Using em dashes (`—`) to force transitions or add manufactured dramatic pauses. This is also a common AI pattern. Use normal periods, commas, or rewrite the sentence |
| Filler phrase | Phrases such as "Not only that," "In addition," or "It is worth mentioning that" |
| Filler phrase | Empty lines such as "I am passionate about this role," or ending every paragraph with an exclamation mark |
| Senior-level red flag | Learner framing such as "I hope to join your company so I can learn more" or "This would be a great learning opportunity." Senior professionals are there to solve problems as peers |
| Senior-level red flag | Keyword stacking such as "I am proficient in A, B, C, and D..." A tool-heavy list without business context reads as junior |

## Mandatory Self-Check Before Output

**REQUIRED**: Run `python3 ./scripts/check-format.py [output-text]` (or pipe content to it) before finalizing your response.

| Check item | Warning sign |
| ---------- | ------------ |
| Zero Hallucinations? | The output mentions skills, metrics, projects, or experiences not explicitly in the resume, or mixes timelines and technologies between different roles |
| Linter passed? | `./scripts/check-format.py` reports any error |
| Plain text? | Symbols such as `**`, `-`, `##`, or `—` appear |
| No em dash? | The writing uses `—` to create pauses, side notes, or dramatic emphasis |
| Opening works? | It starts with lines like "Company X is preparing..." or "I firmly believe..." |
| Project focus? | It mentions too many different projects (limit to 1-2) |
| No filler? | Phrases like "Not only that" or "It is worth mentioning that" |
| Logical flow? | Paragraphs do not transition naturally |

## Writing Quality Standard

Every achievement should include a concrete and verifiable number or result. The first two sentences should be able to catch the reader's attention. Do not use empty words such as "passionate" or "hardworking" unless they are backed by a specific example. Reflect the actual keywords from the company or role. Stay within the required length, with a default cap of 1,000 words.

## Output Format

First output the finished plain-text content. Then leave one blank line and add a short paragraph explaining what this version emphasizes and how the direction could be adjusted if needed. That explanation must also be plain text, not a bullet list.
ion must also be plain text, not a bullet list.

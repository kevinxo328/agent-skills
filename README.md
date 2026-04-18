# Agent Skills

This repository is a collection of high-quality AI agent skills designed to enhance the capabilities of your AI coding assistants, such as **Gemini CLI**, **Claude Code**, **Cursor**, and **Copilot**.

These skills provide standard operating procedures (SOPs), specialized knowledge, and domain-specific workflows to make your AI agents more effective and consistent.

## Available Skills

Currently, this repository includes the following skills:

*   **`commit-message`**: Write high-quality Git commit messages following the Conventional Commits specification.
*   **`humanizer-tw`**: Remove signs of AI-generated writing from text to make it sound more natural and human-written (Taiwan Traditional Chinese version).
*   **`writing-job-application`**: Help with job application materials, such as cover letters, self-introductions, and recruiter Q&A.

*(More skills will be added soon!)*

## Installation & Usage

You can easily install and manage these skills using the [`skills`](https://skills.sh) CLI tool.

### Prerequisites

Ensure you have Node.js and `npx` installed.

### Installing Skills

#### 1. Project-Level (Recommended)
```bash
# Install all skills
npx skills add kevinxo328/agent-skills

# Install a specific skill
npx skills add kevinxo328/agent-skills --skill commit-message
```

#### 2. Global-Level
```bash
# Install all skills globally
npx skills add kevinxo328/agent-skills -g

# Install a specific skill globally
npx skills add kevinxo328/agent-skills --skill commit-message -g
```

### Updating Skills

Keep your skills up to date with the latest improvements.

```bash
# Update all installed skills
npx skills update -y
```

### More Information

For advanced usage (specifying agents, listing skills, etc.), please refer to the [official skills CLI documentation](https://github.com/vercel-labs/skills).

## Contributing

Feel free to open issues or submit pull requests if you have ideas for new skills or improvements to existing ones!

## License

MIT License

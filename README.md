# Agent Skills

This repository is a collection of high-quality AI agent skills designed to enhance the capabilities of your AI coding assistants, such as **Gemini CLI**, **Claude Code**, **Cursor**, and **Copilot**.

These skills provide standard operating procedures (SOPs), specialized knowledge, and domain-specific workflows to make your AI agents more effective and consistent.

## Available Skills

Currently, this repository includes the following skills:

*   **`commit-message`**: Write high-quality Git commit messages following the Conventional Commits specification.

*(More skills will be added soon!)*

## Installation & Usage

You can easily install and manage these skills using the [`skills`](https://skills.sh) CLI tool. It automatically detects your installed AI agents and places the skills in the correct directories (e.g., `.gemini/`, `.cursor/rules/`, `.claude/skills/`).

### Prerequisites

Ensure you have Node.js and `npx` installed.

### Installing Skills

You can install skills directly from this GitHub repository.

#### 1. Project-Level Installation (Recommended for Teams)
Install the skills into your current project directory. The AI agent will use these skills only when working within this project.

```bash
# Install all skills in this repository to the current project
npx skills add <your-github-username>/agent-skills

# Install a specific skill to the current project
npx skills add <your-github-username>/agent-skills --skill commit-message
```

#### 2. Global Installation (Personal Level)
Install the skills globally on your machine. The AI agent will have access to these skills across all your projects.

```bash
# Install all skills globally
npx skills add <your-github-username>/agent-skills -g

# Install a specific skill globally
npx skills add <your-github-username>/agent-skills --skill commit-message -g
```

### Advanced Usage

**Specify Target Agents:**
If you only want to install the skills for a specific AI agent, use the `--agent` flag:

```bash
# Install only for Gemini CLI
npx skills add <your-github-username>/agent-skills --agent gemini-cli
```

**List Installed Skills:**

```bash
# List project skills
npx skills ls

# List global skills
npx skills ls -g
```

## Contributing

Feel free to open issues or submit pull requests if you have ideas for new skills or improvements to existing ones!

## License

MIT License

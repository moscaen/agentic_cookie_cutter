# agentic-cookie-cutter

A CLI tool to bootstrap agentic workflow configuration for AI coding assistants (Gemini CLI and Claude Code) in any codebase.

## What it does

Running `init` against a project directory generates a ready-to-use `.gemini/` or `.claude/` folder (or both) containing:

- A project context file (`GEMINI.md` / `CLAUDE.md`) with placeholders filled in for project name, description, tech stack, and tooling.
- A set of standard **skills** (Gemini) / **commands** (Claude) that activate specialised agent roles:

| Skill / Command | Role |
| --- | --- |
| `developer` | Implements features, fixes bugs, writes tests following TDD |
| `git-committer` | Generates Conventional Commit messages and PR/MR descriptions |
| `code-reviewer` | Reviews code for quality, architecture, and security |
| `technical-writer` | Creates and maintains technical documentation |
| `qa-reviewer` | Produces structured QA test plans from PRs and diffs |
| `project-manager` | Creates well-structured stories and issues aligned with the roadmap |

## Usage

```bash
# Install (editable) — makes the agentic-cookie-cutter command available
uv sync

# Gemini CLI (default) — analyzes the codebase automatically with the Gemini CLI
uv run agentic-cookie-cutter init /path/to/project \
  --project-name "My API" \
  --description "REST API for managing orders." \
  --tech-stack "Python, FastAPI, PostgreSQL" \
  --package-manager uv \
  --test-runner pytest \
  --linter ruff

# Claude Code — analyzes the codebase automatically with the Claude CLI
uv run agentic-cookie-cutter init /path/to/project --type claude ...

# Both tools at once
uv run agentic-cookie-cutter init /path/to/project --type both ...

# Skip AI analysis; use template substitution only
uv run agentic-cookie-cutter init /path/to/project --no-analyze

# Select a subset of skills
uv run agentic-cookie-cutter init /path/to/project --skills developer,git-committer,code-reviewer

# Overwrite existing files
uv run agentic-cookie-cutter init /path/to/project --overwrite
```

### Codebase analysis

By default, `init` invokes the chosen AI CLI (`gemini -p` or `claude -p`) with a prompt that asks it to read the project and produce a tailored `GEMINI.md` / `CLAUDE.md`. Skill/command files are always copied from the templates unchanged.

If the CLI is not installed or returns an error, the tool falls back to plain template substitution using the values supplied via CLI flags. Pass `--no-analyze` to always use the fallback.

## Template structure

```text
src/agentic_cookie_cutter/templates/
├── .gemini/
│   ├── GEMINI.md               # Project context ({{VARIABLE}} placeholders)
│   ├── .geminiignore
│   └── skills/
│       ├── developer/SKILL.md
│       ├── git-committer/SKILL.md
│       ├── code-reviewer/SKILL.md
│       ├── technical-writer/SKILL.md
│       ├── qa-reviewer/SKILL.md
│       └── project-manager/SKILL.md
└── .claude/
    ├── CLAUDE.md               # Project context ({{VARIABLE}} placeholders)
    └── commands/
        ├── developer.md
        ├── git-committer.md
        ├── code-reviewer.md
        ├── technical-writer.md
        ├── qa-reviewer.md
        └── project-manager.md
```

Template variables substituted at generation time:

| Variable | CLI flag | Default |
| --- | --- | --- |
| `{{PROJECT_NAME}}` | `--project-name` | `My Project` |
| `{{DESCRIPTION}}` | `--description` | `A software project.` |
| `{{TECH_STACK}}` | `--tech-stack` | `Python` |
| `{{PACKAGE_MANAGER}}` | `--package-manager` | `uv` |
| `{{TEST_RUNNER}}` | `--test-runner` | `pytest` |
| `{{LINTER}}` | `--linter` | `ruff` |

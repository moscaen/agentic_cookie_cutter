"""agentic-cookie-cutter: Set up agentic workflow configuration for AI coding tools."""

import argparse
import subprocess
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

AVAILABLE_SKILLS = [
    "developer",
    "git-committer",
    "code-reviewer",
    "technical-writer",
    "qa-reviewer",
    "project-manager",
]


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

def substitute(content: str, variables: dict[str, str]) -> str:
    for key, value in variables.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def strip_code_fences(content: str) -> str:
    """Remove a single surrounding markdown code fence block if present."""
    lines = content.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def copy_file(src: Path, dst: Path, variables: dict[str, str], overwrite: bool) -> bool:
    if dst.exists() and not overwrite:
        print(f"  skipped  {dst} (already exists; use --overwrite)")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    content = substitute(src.read_text(), variables)
    dst.write_text(content)
    print(f"  created  {dst}")
    return True


# ---------------------------------------------------------------------------
# AI codebase analysis
# ---------------------------------------------------------------------------

def _analysis_prompt(filename: str, template: str) -> str:
    return (
        f"Analyze this codebase and generate a {filename} configuration file "
        f"for AI coding assistants.\n\n"
        f"Examine the project structure and configuration files "
        f"(pyproject.toml, package.json, Cargo.toml, go.mod, etc.) to understand:\n"
        f"- What the project does and its main purpose\n"
        f"- The tech stack, frameworks, and key libraries\n"
        f"- The architecture and key components/directories\n"
        f"- Development standards: package manager, test runner, linter/formatter\n"
        f"- Key workflows and entry points\n"
        f"- Important conventions or pitfalls\n\n"
        f"Produce the complete content for {filename} with accurate, project-specific "
        f"information replacing all placeholder sections. "
        f"Output ONLY the file content — no explanations, no surrounding code fences.\n\n"
        f"Use this as your starting template:\n\n{template}"
    )


def _run_cli(cmd: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0 and result.stdout.strip():
            return strip_code_fences(result.stdout)
        if result.stderr.strip():
            print(f"  warning  CLI stderr: {result.stderr.strip()[:200]}")
    except FileNotFoundError:
        print(f"  warning  '{cmd[0]}' not found; falling back to template substitution")
    except subprocess.TimeoutExpired:
        print(f"  warning  '{cmd[0]}' timed out; falling back to template substitution")
    return None


def analyze_with_gemini(target: Path, template: str, filename: str) -> str | None:
    print("  analyzing codebase with Gemini CLI...")
    return _run_cli(["gemini", "-p", _analysis_prompt(filename, template)], target)


def analyze_with_claude(target: Path, template: str, filename: str) -> str | None:
    print("  analyzing codebase with Claude CLI...")
    return _run_cli(["claude", "-p", _analysis_prompt(filename, template)], target)


# ---------------------------------------------------------------------------
# Init routines
# ---------------------------------------------------------------------------

def _write_config(
    src: Path,
    dst: Path,
    variables: dict[str, str],
    overwrite: bool,
    analyzer,  # callable(target, template, filename) -> str | None
    target: Path,
) -> None:
    """Write a main config file, using AI analysis when available."""
    if dst.exists() and not overwrite:
        print(f"  skipped  {dst} (already exists; use --overwrite)")
        return
    template = substitute(src.read_text(), variables)
    content = analyzer(target, template, dst.name) if analyzer else None
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content or template)
    suffix = "(AI-generated)" if content else "(template)"
    print(f"  created  {dst} {suffix}")


def init_gemini(
    target: Path,
    variables: dict[str, str],
    skills: list[str],
    overwrite: bool,
    analyze: bool,
) -> None:
    gemini_dir = target / ".gemini"
    src_base = TEMPLATES_DIR / ".gemini"
    print(f"\nInitializing .gemini/ in {target}")

    analyzer = analyze_with_gemini if analyze else None
    _write_config(
        src_base / "GEMINI.md", gemini_dir / "GEMINI.md",
        variables, overwrite, analyzer, target,
    )
    copy_file(src_base / ".geminiignore", gemini_dir / ".geminiignore", variables, overwrite)

    for skill in skills:
        src = src_base / "skills" / skill / "SKILL.md"
        if not src.exists():
            print(f"  warning  skill '{skill}' not found in templates, skipping")
            continue
        copy_file(src, gemini_dir / "skills" / skill / "SKILL.md", variables, overwrite)


def init_claude(
    target: Path,
    variables: dict[str, str],
    skills: list[str],
    overwrite: bool,
    analyze: bool,
) -> None:
    src_base = TEMPLATES_DIR / ".claude"
    print(f"\nInitializing CLAUDE.md + .claude/commands/ in {target}")

    analyzer = analyze_with_claude if analyze else None
    _write_config(
        src_base / "CLAUDE.md", target / "CLAUDE.md",
        variables, overwrite, analyzer, target,
    )

    for skill in skills:
        src = src_base / "commands" / f"{skill}.md"
        if not src.exists():
            print(f"  warning  command '{skill}' not found in templates, skipping")
            continue
        copy_file(src, target / ".claude" / "commands" / f"{skill}.md", variables, overwrite)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_init(args: argparse.Namespace) -> None:
    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Error: target directory '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"Error: '{target}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    variables = {
        "PROJECT_NAME": args.project_name,
        "DESCRIPTION": args.description,
        "TECH_STACK": args.tech_stack,
        "PACKAGE_MANAGER": args.package_manager,
        "TEST_RUNNER": args.test_runner,
        "LINTER": args.linter,
    }

    skills = AVAILABLE_SKILLS
    if args.skills:
        skills = [s.strip() for s in args.skills.split(",")]
        unknown = [s for s in skills if s not in AVAILABLE_SKILLS]
        if unknown:
            print(f"Error: unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
            print(f"Available skills: {', '.join(AVAILABLE_SKILLS)}", file=sys.stderr)
            sys.exit(1)

    analyze = not args.no_analyze

    if args.type in ("gemini", "both"):
        init_gemini(target, variables, skills, args.overwrite, analyze)
    if args.type in ("claude", "both"):
        init_claude(target, variables, skills, args.overwrite, analyze)

    print("\nDone.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agentic-cookie-cutter",
        description="Set up agentic workflow configuration (.gemini/ or .claude/) for any project.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    init_parser = subparsers.add_parser(
        "init",
        help="Initialize agentic configuration in a project directory.",
    )
    init_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory (default: current directory).",
    )
    init_parser.add_argument(
        "--type",
        choices=["gemini", "claude", "both"],
        default="gemini",
        help="Which tool to configure (default: gemini).",
    )
    init_parser.add_argument(
        "--project-name",
        default="My Project",
        metavar="NAME",
        help="Project name used in the config file (default: 'My Project').",
    )
    init_parser.add_argument(
        "--description",
        default="A software project.",
        metavar="TEXT",
        help="Short project description (default: 'A software project.').",
    )
    init_parser.add_argument(
        "--tech-stack",
        default="Python",
        metavar="TEXT",
        help="Technologies used, e.g. 'Python, FastAPI, PostgreSQL' (default: 'Python').",
    )
    init_parser.add_argument(
        "--package-manager",
        default="uv",
        metavar="TOOL",
        help="Package manager, e.g. uv, pip, npm (default: uv).",
    )
    init_parser.add_argument(
        "--test-runner",
        default="pytest",
        metavar="TOOL",
        help="Test runner, e.g. pytest, jest (default: pytest).",
    )
    init_parser.add_argument(
        "--linter",
        default="ruff",
        metavar="TOOL",
        help="Linter/formatter, e.g. ruff, eslint (default: ruff).",
    )
    init_parser.add_argument(
        "--skills",
        metavar="SKILL[,SKILL...]",
        help=(
            f"Comma-separated list of skills to include "
            f"(default: all). Available: {', '.join(AVAILABLE_SKILLS)}."
        ),
    )
    init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files.",
    )
    init_parser.add_argument(
        "--no-analyze",
        action="store_true",
        help="Skip AI codebase analysis; use template substitution only.",
    )

    args = parser.parse_args()

    if args.command == "init":
        run_init(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

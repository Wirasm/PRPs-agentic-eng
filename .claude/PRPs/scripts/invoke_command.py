#!/usr/bin/env -S uv run --script
"""Invoke a Claude Code slash command from Python.

Usage:
    uv run .claude/PRPs/scripts/invoke_command.py prp-core-create "Add JWT authentication"
    uv run .claude/PRPs/scripts/invoke_command.py prp-core-execute my-feature --interactive
    uv run .claude/PRPs/scripts/invoke_command.py .claude/commands/prp-core/prp-core-pr.md "Add auth feature"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # project root


def resolve_command_path(command: str) -> Path:
    """Resolve command name or path to full .md file path.

    Args:
        command: Either a command name (e.g., "prp-core-create") or full path

    Returns:
        Path to the command .md file
    """
    # If it's already a path, use it
    if command.endswith(".md"):
        path = Path(command)
        if path.is_absolute():
            return path
        return ROOT / path

    # Otherwise, search in .claude/commands/
    commands_dir = ROOT / ".claude" / "commands"

    # Try common locations
    search_paths = [
        commands_dir / f"{command}.md",
        commands_dir / "prp-core" / f"{command}.md",
        commands_dir / "prp-commands" / f"{command}.md",
        commands_dir / "development" / f"{command}.md",
        commands_dir / "code-quality" / f"{command}.md",
    ]

    for path in search_paths:
        if path.exists():
            return path

    # Fallback: search recursively
    for md_file in commands_dir.rglob("*.md"):
        if md_file.stem == command:
            return md_file

    sys.exit(f"Command not found: {command}")


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown content.

    Frontmatter is delimited by --- at the start and end.
    """
    if content.startswith("---\n"):
        # Find the closing ---
        end_marker = content.find("\n---\n", 4)
        if end_marker != -1:
            # Return content after frontmatter
            return content[end_marker + 5:].lstrip()
    return content


def expand_template(template: str, arguments: str) -> str:
    """Expand template with arguments.

    Supports:
    - $ARGUMENTS: all arguments as single string
    - $1, $2, $3, etc.: individual positional arguments
    """
    # Strip frontmatter first
    template = strip_frontmatter(template)

    # Replace $ARGUMENTS with full argument string
    expanded = template.replace("$ARGUMENTS", arguments)

    # Replace positional arguments
    args_list = arguments.split()
    for i, arg in enumerate(args_list, 1):
        expanded = expanded.replace(f"${i}", arg)

    return expanded


def invoke_command(
    command_path: Path,
    arguments: str = "",
    interactive: bool = False,
    output_format: str = "text",
    allowed_tools: str = "Edit,Bash,Write,Read,Glob,Grep,TodoWrite,WebFetch,WebSearch,Task",
) -> None:
    """Invoke a Claude Code slash command.

    Args:
        command_path: Path to command .md file
        arguments: Arguments to pass to command
        interactive: Run in interactive mode
        output_format: Output format for headless mode (text, json, stream-json)
        allowed_tools: Comma-separated list of allowed tools
    """
    # Read and expand template
    template = command_path.read_text()
    prompt = expand_template(template, arguments)

    # Build command
    if interactive:
        # Interactive mode: pipe via stdin
        cmd = [
            "claude",
            "--allowedTools",
            allowed_tools,
        ]
        subprocess.run(cmd, input=prompt.encode(), check=True)
    else:
        # Headless mode: use -p flag
        cmd = [
            "claude",
            "-p",
            prompt,
            "--allowedTools",
            allowed_tools,
            "--output-format",
            output_format,
        ]
        subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Invoke a Claude Code slash command",
        epilog="""
Examples:
  %(prog)s prp-core-create "Add JWT authentication"
  %(prog)s prp-core-execute my-feature --interactive
  %(prog)s .claude/commands/prp-core/prp-core-pr.md "Add auth" --output-format json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        help="Command name (e.g., 'prp-core-create') or path to .md file",
    )
    parser.add_argument(
        "arguments",
        nargs="?",
        default="",
        help="Arguments to pass to the command",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json", "stream-json"],
        default="text",
        help="Output format for headless mode (default: text)",
    )
    parser.add_argument(
        "--allowed-tools",
        default="Edit,Bash,Write,Read,Glob,Grep,TodoWrite,WebFetch,WebSearch,Task",
        help="Comma-separated list of allowed tools",
    )

    args = parser.parse_args()

    # Resolve command path
    command_path = resolve_command_path(args.command)
    print(f"Invoking: {command_path.relative_to(ROOT)}", file=sys.stderr)
    if args.arguments:
        print(f"Arguments: {args.arguments}", file=sys.stderr)
    print(file=sys.stderr)

    # Invoke command
    invoke_command(
        command_path=command_path,
        arguments=args.arguments,
        interactive=args.interactive,
        output_format=args.output_format,
        allowed_tools=args.allowed_tools,
    )


if __name__ == "__main__":
    main()

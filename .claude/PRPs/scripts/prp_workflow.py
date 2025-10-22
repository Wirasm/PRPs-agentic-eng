#!/usr/bin/env -S uv run --script
"""PRP workflow orchestrator - chain create, execute, commit, and PR commands.

Usage:
    # Full workflow
    uv run .claude/PRPs/scripts/prp_workflow.py "Add JWT authentication"

    # With custom PR title
    uv run .claude/PRPs/scripts/prp_workflow.py "Add JWT authentication" --pr-title "feat: add JWT auth"

    # Start from execute (if PRP already exists)
    uv run .claude/PRPs/scripts/prp_workflow.py --prp-path .claude/PRPs/features/my-feature.md --skip-create

    # Execute only (no commit/PR)
    uv run .claude/PRPs/scripts/prp_workflow.py "Add feature" --no-commit --no-pr
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def print_box(title: str, content: str = "", icon: str = "🚀") -> None:
    """Print a nice box for workflow steps."""
    width = 80
    print()
    print("╭" + "─" * (width - 2) + "╮")
    title_line = f"│ {icon} {title}"
    padding = width - len(title_line) - 1
    print(title_line + " " * padding + "│")
    if content:
        for line in content.split("\n"):
            line = f"│ {line}"
            padding = width - len(line) - 1
            print(line + " " * padding + "│")
    print("╰" + "─" * (width - 2) + "╯")
    print()


def run_command(
    command_name: str,
    arguments: str = "",
    output_format: str = "text",
    capture_output: bool = False
) -> tuple[int, str]:
    """Run a slash command using invoke_command.py.

    Returns:
        Tuple of (exit_code, output_text)
    """
    cmd = [
        "uv", "run",
        str(ROOT / ".claude/PRPs/scripts/invoke_command.py"),
        command_name,
        arguments,
        "--output-format", output_format
    ]

    print(f"→ Running: {command_name} {arguments}", file=sys.stderr)

    if capture_output:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout
    else:
        result = subprocess.run(cmd)
        return result.returncode, ""


def extract_prp_path(output: str) -> Optional[str]:
    """Extract PRP file path from prp-core-create output.

    Looks for patterns like:
    - `.claude/PRPs/features/xxx.md`
    - Full path to PRP file
    """
    # Try to find .claude/PRPs/features/*.md pattern
    match = re.search(r'\.claude/PRPs/features/[a-z0-9_-]+\.md', output)
    if match:
        return match.group(0)

    # Try to find quoted path
    match = re.search(r'`([^`]*\.claude/PRPs/features/[^`]+\.md)`', output)
    if match:
        return match.group(1)

    return None


def workflow_create(feature_description: str) -> Optional[str]:
    """Step 1: Create PRP.

    Returns:
        PRP file path if successful, None otherwise
    """
    print_box("Step 1: Creating PRP", feature_description, "📝")

    exit_code, output = run_command(
        "prp-core-create",
        feature_description,
        output_format="text",
        capture_output=True
    )

    # Print output
    print(output)

    if exit_code != 0:
        print("❌ PRP creation failed", file=sys.stderr)
        return None

    # Extract PRP path
    prp_path = extract_prp_path(output)
    if not prp_path:
        print("⚠️  Could not extract PRP file path from output", file=sys.stderr)
        return None

    print(f"✅ PRP created: {prp_path}", file=sys.stderr)
    return prp_path


def workflow_execute(prp_path: str) -> bool:
    """Step 2: Execute PRP.

    Returns:
        True if successful, False otherwise
    """
    print_box("Step 2: Executing PRP", prp_path, "⚙️")

    exit_code, _ = run_command(
        "prp-core-execute",
        prp_path,
        output_format="text",
        capture_output=False
    )

    if exit_code != 0:
        print("❌ PRP execution failed", file=sys.stderr)
        return False

    print("✅ PRP execution completed", file=sys.stderr)
    return True


def workflow_commit() -> bool:
    """Step 3: Commit changes.

    Returns:
        True if successful, False otherwise
    """
    print_box("Step 3: Committing Changes", "", "💾")

    exit_code, _ = run_command(
        "PRP-core-commit",
        "",
        output_format="text",
        capture_output=False
    )

    if exit_code != 0:
        print("❌ Commit failed", file=sys.stderr)
        return False

    print("✅ Changes committed", file=sys.stderr)
    return True


def workflow_pr(pr_title: Optional[str] = None) -> bool:
    """Step 4: Create PR.

    Returns:
        True if successful, False otherwise
    """
    title = pr_title or "PRP Implementation"
    print_box("Step 4: Creating Pull Request", title, "🚀")

    exit_code, _ = run_command(
        "prp-core-pr",
        title,
        output_format="text",
        capture_output=False
    )

    if exit_code != 0:
        print("❌ PR creation failed", file=sys.stderr)
        return False

    print("✅ Pull request created", file=sys.stderr)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRP workflow orchestrator - chain create, execute, commit, and PR commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full workflow
  %(prog)s "Add JWT authentication"

  # With custom PR title
  %(prog)s "Add JWT auth" --pr-title "feat: add JWT authentication system"

  # Start from execute (if PRP already exists)
  %(prog)s --prp-path .claude/PRPs/features/my-feature.md --skip-create

  # Execute only (no commit/PR)
  %(prog)s "Add feature" --no-commit --no-pr

  # Create and execute only
  %(prog)s "Add feature" --no-commit
        """
    )

    parser.add_argument(
        "feature",
        nargs="?",
        help="Feature description for PRP creation"
    )
    parser.add_argument(
        "--prp-path",
        help="Path to existing PRP file (skips create step)"
    )
    parser.add_argument(
        "--skip-create",
        action="store_true",
        help="Skip PRP creation (requires --prp-path)"
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip commit step"
    )
    parser.add_argument(
        "--no-pr",
        action="store_true",
        help="Skip PR creation step"
    )
    parser.add_argument(
        "--pr-title",
        help="Custom PR title (default: 'PRP Implementation')"
    )

    args = parser.parse_args()

    # Validation
    if args.skip_create and not args.prp_path:
        sys.exit("Error: --skip-create requires --prp-path")

    if not args.skip_create and not args.feature:
        sys.exit("Error: Feature description required (unless using --skip-create)")

    print_box("PRP Workflow Started", f"Feature: {args.feature or args.prp_path}", "🚀")

    # Step 1: Create PRP (or use existing)
    if args.skip_create:
        prp_path = args.prp_path
        print(f"ℹ️  Using existing PRP: {prp_path}", file=sys.stderr)
    else:
        prp_path = workflow_create(args.feature)
        if not prp_path:
            sys.exit(1)

    # Verify PRP file exists
    full_prp_path = ROOT / prp_path
    if not full_prp_path.exists():
        sys.exit(f"❌ PRP file not found: {full_prp_path}")

    # Step 2: Execute PRP
    if not workflow_execute(prp_path):
        sys.exit(1)

    # Step 3: Commit (optional)
    if not args.no_commit:
        if not workflow_commit():
            sys.exit(1)
    else:
        print("ℹ️  Skipping commit (--no-commit)", file=sys.stderr)

    # Step 4: Create PR (optional)
    if not args.no_pr:
        if not args.no_commit:
            if not workflow_pr(args.pr_title):
                sys.exit(1)
        else:
            print("ℹ️  Skipping PR (no commit created)", file=sys.stderr)
    else:
        print("ℹ️  Skipping PR (--no-pr)", file=sys.stderr)

    # Success!
    print_box("Workflow Complete! 🎉", "", "✅")


if __name__ == "__main__":
    main()

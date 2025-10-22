#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "rich",
# ]
# ///
"""
PRP Core Workflow Runner

Executes the complete PRP workflow in sequence:
1. Create PRP: /prp-core-create {feature_description}
2. Execute PRP: /prp-core-execute {prp_file}
3. Commit changes: /prp-core-commit

Usage:
    uv run .claude/PRPs/scripts/prp_workflow.py "Add user authentication"
    uv run .claude/PRPs/scripts/prp_workflow.py "Implement search functionality" --model opus

Output:
    Logs saved to: .claude/PRPs/logs/{prp_id}/
    - step1_create.log
    - step2_execute.log
    - step3_commit.log
    - workflow_summary.json
"""

import subprocess
import sys
import os
import json
import re
import uuid
from pathlib import Path
from typing import Optional, Literal
from rich.console import Console
from rich.panel import Panel

console = Console()


def generate_prp_id() -> str:
    """Generate a short 8-character UUID for tracking."""
    return str(uuid.uuid4())[:8]


def setup_log_directory(prp_id: str) -> Path:
    """Create log directory for this workflow run."""
    log_dir = Path(".claude/PRPs/logs") / prp_id
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def run_claude_command(
    command: str,
    args: str,
    step_name: str,
    log_file: Path,
    model: Literal["sonnet", "opus"] = "sonnet",
) -> tuple[bool, str]:
    """Execute a Claude Code command and capture output.

    Args:
        command: Claude slash command (e.g., "/prp-core-create")
        args: Arguments for the command
        step_name: Human-readable step name for display
        log_file: Path to save command output
        model: Claude model to use

    Returns:
        Tuple of (success, output)
    """
    prompt = f"{command} {args}"
    cmd = ["claude", "-p", prompt, "--model", model]

    with console.status(f"[bold yellow]{step_name}...[/bold yellow]"):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=1800,  # 30 minute timeout
            )

            # Save output to log file
            with open(log_file, "w") as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(f"Return Code: {result.returncode}\n")
                f.write(f"\n{'='*80}\nSTDOUT:\n{'='*80}\n")
                f.write(result.stdout)
                if result.stderr:
                    f.write(f"\n{'='*80}\nSTDERR:\n{'='*80}\n")
                    f.write(result.stderr)

            success = result.returncode == 0
            output = result.stdout if success else result.stderr or result.stdout

            return (success, output)

        except subprocess.TimeoutExpired:
            error_msg = "Command timed out after 30 minutes"
            with open(log_file, "w") as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(f"Error: {error_msg}\n")
            return (False, error_msg)

        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            with open(log_file, "w") as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(f"Error: {error_msg}\n")
            return (False, error_msg)


def extract_prp_filename(output: str) -> Optional[str]:
    """Extract PRP filename from prp-core-create output.

    Looks for patterns like:
    - Full path to created PRP file
    - `.claude/PRPs/features/{name}.md`

    Returns:
        PRP filename without .md extension, or None if not found
    """
    # Look for common patterns in create output
    patterns = [
        r"\.claude/PRPs/features/([a-z0-9-]+)\.md",  # Full path
        r"PRPs/features/([a-z0-9-]+)\.md",  # Relative path
        r"Created PRP: ([a-z0-9-]+)\.md",  # Explicit statement
        r"Saved as.*?([a-z0-9-]+)\.md",  # Saved as statement
    ]

    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return match.group(1)

    # If no pattern found, look for any kebab-case name followed by .md
    match = re.search(r"([a-z][a-z0-9-]{5,})\.md", output)
    if match:
        return match.group(1)

    return None


def save_workflow_summary(
    log_dir: Path,
    prp_id: str,
    feature_description: str,
    model: str,
    prp_filename: Optional[str],
    steps: dict,
) -> None:
    """Save workflow execution summary as JSON."""
    summary = {
        "prp_id": prp_id,
        "feature_description": feature_description,
        "model": model,
        "prp_filename": prp_filename,
        "steps": steps,
        "log_directory": str(log_dir),
    }

    summary_file = log_dir / "workflow_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)


def main():
    """Execute the PRP core workflow."""

    # Parse arguments
    if len(sys.argv) < 2:
        console.print(
            Panel(
                "[red]Missing feature description[/red]\n\n"
                "Usage:\n"
                "  uv run .claude/PRPs/scripts/prp_workflow.py \"Feature description\"\n"
                "  uv run .claude/PRPs/scripts/prp_workflow.py \"Add auth\" --model opus",
                title="❌ Error",
                border_style="red",
            )
        )
        sys.exit(1)

    # Extract feature description and model
    args = sys.argv[1:]
    model = "sonnet"  # default

    # Check for --model flag
    if "--model" in args:
        model_idx = args.index("--model")
        if model_idx + 1 < len(args):
            model_value = args[model_idx + 1]
            if model_value in ["sonnet", "opus"]:
                model = model_value
            args = args[:model_idx] + args[model_idx + 2:]  # Remove --model and value

    feature_description = " ".join(args)

    # Generate PRP ID and setup logging
    prp_id = generate_prp_id()
    log_dir = setup_log_directory(prp_id)

    # Display header
    console.print()
    console.print(
        Panel(
            f"[bold cyan]PRP ID:[/bold cyan] {prp_id}\n"
            f"[bold cyan]Feature:[/bold cyan] {feature_description}\n"
            f"[bold cyan]Model:[/bold cyan] {model}\n"
            f"[bold cyan]Logs:[/bold cyan] {log_dir}",
            title="🚀 PRP Workflow Started",
            border_style="blue",
        )
    )
    console.print()

    # Track step results
    steps = {}
    prp_filename = None

    # Step 1: Create PRP
    console.print("[bold]Step 1/3:[/bold] Creating PRP")
    success, output = run_claude_command(
        command="/prp-core-create",
        args=feature_description,
        step_name="Creating PRP",
        log_file=log_dir / "step1_create.log",
        model=model,
    )

    steps["create"] = {"success": success, "output_length": len(output)}

    if not success:
        console.print(
            Panel(
                f"[red]Failed to create PRP[/red]\n\n"
                f"Check logs: {log_dir / 'step1_create.log'}",
                title="❌ Step 1 Failed",
                border_style="red",
            )
        )
        save_workflow_summary(log_dir, prp_id, feature_description, model, None, steps)
        sys.exit(1)

    # Extract PRP filename
    prp_filename = extract_prp_filename(output)

    if not prp_filename:
        console.print(
            Panel(
                "[red]Could not extract PRP filename from output[/red]\n\n"
                f"Check logs: {log_dir / 'step1_create.log'}\n"
                "You may need to run /prp-core-execute manually",
                title="⚠️  Warning",
                border_style="yellow",
            )
        )
        save_workflow_summary(log_dir, prp_id, feature_description, model, None, steps)
        sys.exit(1)

    console.print(f"✅ PRP created: [cyan]{prp_filename}.md[/cyan]")
    console.print()

    # Step 2: Execute PRP
    console.print("[bold]Step 2/3:[/bold] Executing PRP")
    success, output = run_claude_command(
        command="/prp-core-execute",
        args=prp_filename,
        step_name="Executing PRP",
        log_file=log_dir / "step2_execute.log",
        model=model,
    )

    steps["execute"] = {"success": success, "output_length": len(output)}

    if not success:
        console.print(
            Panel(
                f"[red]Failed to execute PRP[/red]\n\n"
                f"Check logs: {log_dir / 'step2_execute.log'}\n"
                f"PRP file: .claude/PRPs/features/{prp_filename}.md",
                title="❌ Step 2 Failed",
                border_style="red",
            )
        )
        save_workflow_summary(log_dir, prp_id, feature_description, model, prp_filename, steps)
        sys.exit(1)

    console.print("✅ PRP executed successfully")
    console.print()

    # Step 3: Commit changes
    console.print("[bold]Step 3/3:[/bold] Committing changes")
    success, output = run_claude_command(
        command="/prp-core-commit",
        args="",
        step_name="Committing changes",
        log_file=log_dir / "step3_commit.log",
        model=model,
    )

    steps["commit"] = {"success": success, "output_length": len(output)}

    if not success:
        console.print(
            Panel(
                f"[yellow]Commit step had issues[/yellow]\n\n"
                f"Check logs: {log_dir / 'step3_commit.log'}\n"
                "You may need to commit manually with: /smart-commit",
                title="⚠️  Step 3 Warning",
                border_style="yellow",
            )
        )
    else:
        console.print("✅ Changes committed")

    console.print()

    # Save summary
    save_workflow_summary(log_dir, prp_id, feature_description, model, prp_filename, steps)

    # Final summary
    all_success = all(step["success"] for step in steps.values())

    if all_success:
        console.print(
            Panel(
                f"[green]All steps completed successfully![/green]\n\n"
                f"[bold]PRP File:[/bold] .claude/PRPs/features/completed/{prp_filename}.md\n"
                f"[bold]Logs:[/bold] {log_dir}\n"
                f"[bold]Summary:[/bold] {log_dir / 'workflow_summary.json'}",
                title="🎉 Workflow Complete",
                border_style="green",
            )
        )
        sys.exit(0)
    else:
        console.print(
            Panel(
                f"[yellow]Workflow completed with warnings[/yellow]\n\n"
                f"[bold]Logs:[/bold] {log_dir}\n"
                f"[bold]Summary:[/bold] {log_dir / 'workflow_summary.json'}",
                title="⚠️  Workflow Complete (with warnings)",
                border_style="yellow",
            )
        )
        sys.exit(0)


if __name__ == "__main__":
    main()

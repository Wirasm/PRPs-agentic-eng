#!/usr/bin/env -S uv run --script
"""Run an AI coding agent against a PRP.

KISS version - no repo-specific assumptions.

Typical usage:
    uv run RUNNERS/claude_runner.py --prp test --interactive
    uv run RUNNERS/claude_runner.py --prp test --output-format json
    uv run RUNNERS/claude_runner.py --prp test --output-format stream-json

Arguments:
    --prp-path       Path to a PRP markdown file (overrides --prp)
    --prp            Feature key; resolves to PRPs/{feature}.md
    --model          CLI executable for the LLM (default: "claude") Only Claude Code is supported for now
    --interactive    Pass through to run the model in chat mode; otherwise headless.
    --output-format  Output format for headless mode: text, json, stream-json (default: text)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterator

ROOT = Path(__file__).resolve().parent.parent  # project root

META_HEADER = """Ingest and understand the Product Requirement Prompt (PRP) below in detail.

    # WORKFLOW GUIDANCE:

    ## Planning Phase
    - Think hard before you code. Create a comprehensive plan addressing all requirements.
    - Break down complex tasks into smaller, manageable steps.
    - Use the TodoWrite tool to create and track your implementation plan.
    - Identify implementation patterns from existing code to follow.

    ## Implementation Phase
    - Follow code conventions and patterns found in existing files.
    - Implement one component at a time and verify it works correctly.
    - Write clear, maintainable code with appropriate comments.
    - Consider error handling, edge cases, and potential security issues.
    - Use type hints to ensure type safety.

    ## Testing Phase
    - Test each component thoroughly as you build it.
    - Use the provided validation gates to verify your implementation.
    - Verify that all requirements have been satisfied.
    - Run the project tests when finished and output "DONE" when they pass.

    ## Example Implementation Approach:
    1. Analyze the PRP requirements in detail
    2. Search for and understand existing patterns in the codebase
    3. Search the Web and gather additional context and examples
    4. Create a step-by-step implementation plan with TodoWrite
    5. Implement core functionality first, then additional features
    6. Test and validate each component
    7. Ensure all validation gates pass

    ***When you are finished, move the completed PRP to the PRPs/completed folder***
    """


def build_prompt(prp_path: Path) -> str:
    return META_HEADER + prp_path.read_text()


def stream_json_output(process: subprocess.Popen) -> Iterator[Dict[str, Any]]:
    """Parse streaming JSON output line by line."""
    for line in process.stdout:
        line = line.strip()
        if line:
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse JSON line: {e}", file=sys.stderr)
                print(f"Line content: {line}", file=sys.stderr)


def handle_json_output(output: str) -> Dict[str, Any]:
    """Parse the JSON output from Claude Code."""
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}", file=sys.stderr)
        return {"error": "Failed to parse JSON output", "raw": output}


def run_model(
    prompt: str,
    model: str = "claude",
    interactive: bool = False,
    output_format: str = "text",
) -> None:
    if interactive:
        # Chat mode: feed prompt via STDIN, no -p flag so the user can continue the session.
        cmd = [
            model,
            "--allowedTools",
            "Edit,Bash,Write,MultiEdit,NotebookEdit,WebFetch,Agent,LS,Grep,Read,NotebookRead,TodoRead,TodoWrite,WebSearch",
        ]
        subprocess.run(cmd, input=prompt.encode(), check=True)
    else:
        # Headless: pass prompt via -p for non-interactive mode
        cmd = [
            model,
            "-p",  # This is the --print flag for non-interactive mode
            prompt,
            "--allowedTools",
            "Edit,Bash,Write,MultiEdit,NotebookEdit,WebFetch,Agent,LS,Grep,Read,NotebookRead,TodoRead,TodoWrite,WebSearch",
            # "--max-turns",
            # "30",  # Safety limit for headless mode uncomment if needed
            "--output-format",
            output_format,
        ]

        if output_format == "stream-json":
            # Handle streaming JSON output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
            )

            try:
                for message in stream_json_output(process):
                    # Process each message as it arrives
                    if (
                        message.get("type") == "system"
                        and message.get("subtype") == "init"
                    ):
                        print(
                            f"Session started: {message.get('session_id')}",
                            file=sys.stderr,
                        )
                    elif message.get("type") == "assistant":
                        print(
                            f"Assistant: {message.get('message', {}).get('content', '')[:100]}...",
                            file=sys.stderr,
                        )
                    elif message.get("type") == "result":
                        print(f"\nFinal result:", file=sys.stderr)
                        print(
                            f"  Success: {message.get('subtype') == 'success'}",
                            file=sys.stderr,
                        )
                        print(
                            f"  Cost: ${message.get('cost_usd', 0):.4f}",
                            file=sys.stderr,
                        )
                        print(
                            f"  Duration: {message.get('duration_ms', 0)}ms",
                            file=sys.stderr,
                        )
                        print(
                            f"  Turns: {message.get('num_turns', 0)}", file=sys.stderr
                        )
                        if message.get("result"):
                            print(
                                f"\nResult text:\n{message.get('result')}",
                                file=sys.stderr,
                            )

                    # Print the full message for downstream processing
                    print(json.dumps(message))

                # Wait for process to complete
                process.wait()
                if process.returncode != 0:
                    stderr = process.stderr.read()
                    print(
                        f"Claude Code failed with exit code {process.returncode}",
                        file=sys.stderr,
                    )
                    print(f"Error: {stderr}", file=sys.stderr)
                    sys.exit(process.returncode)

            except KeyboardInterrupt:
                process.terminate()
                print("\nInterrupted by user", file=sys.stderr)
                sys.exit(1)

        elif output_format == "json":
            # Handle complete JSON output
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(
                    f"Claude Code failed with exit code {result.returncode}",
                    file=sys.stderr,
                )
                print(f"Error: {result.stderr}", file=sys.stderr)
                sys.exit(result.returncode)

            # Parse and pretty print the JSON
            json_data = handle_json_output(result.stdout)
            print(json.dumps(json_data, indent=2))

            # Print summary to stderr for user visibility
            if isinstance(json_data, dict):
                if json_data.get("type") == "result":
                    print(f"\nSummary:", file=sys.stderr)
                    print(
                        f"  Success: {not json_data.get('is_error', False)}",
                        file=sys.stderr,
                    )
                    print(
                        f"  Cost: ${json_data.get('cost_usd', 0):.4f}", file=sys.stderr
                    )
                    print(
                        f"  Duration: {json_data.get('duration_ms', 0)}ms",
                        file=sys.stderr,
                    )
                    print(
                        f"  Session: {json_data.get('session_id', 'unknown')}",
                        file=sys.stderr,
                    )

        else:
            # Default text output
            subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PRP with an LLM agent.")
    parser.add_argument(
        "--prp-path", help="Relative path to PRP file eg: PRPs/feature.md"
    )
    parser.add_argument(
        "--prp", help="The file name of the PRP without the .md extension eg: feature"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Launch interactive chat session"
    )
    parser.add_argument("--model", default="claude", help="Model CLI executable name")
    parser.add_argument(
        "--output-format",
        choices=["text", "json", "stream-json"],
        default="text",
        help="Output format for headless mode (default: text)",
    )
    args = parser.parse_args()

    if not args.prp_path and not args.prp:
        sys.exit("Must supply --prp or --prp-path")

    prp_path = Path(args.prp_path) if args.prp_path else ROOT / f"PRPs/{args.prp}.md"
    if not prp_path.exists():
        sys.exit(f"PRP not found: {prp_path}")

    os.chdir(ROOT)  # ensure relative paths match PRP expectations
    prompt = build_prompt(prp_path)
    run_model(
        prompt,
        model=args.model,
        interactive=args.interactive,
        output_format=args.output_format,
    )


if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
prp_loop.py — autonomous, cyclic PRP pipeline orchestrator.

Pipeline:
    plan -> implement (loop until green) -> pr (create once) -> review
    review clean? -> done
    review dirty? -> fix (loop until green) -> push -> review   (cyclic, bounded)

Design:
- Headless: each stage is one `claude -p "<prompt>"` call in a fresh session.
- State lives in .claude/prp-loop.state.json (resumable: re-run with --resume).
- Fully autonomous (--dangerously-skip-permissions).
- Does NOT use the prp-ralph Stop-hook. This script owns both loops and detects
  "green" from each stage's `VALIDATION: GREEN` sentinel (parsed from the clean
  result text) and/or an optional hard `--validate` command (authoritative).
- Stages are invoked by naming the skill in a natural-language prompt, so the
  agent-invocable PRP skills auto-load. Skills are never modified.
- Bounded by --max-cycles (outer review loop) and --max-implement-iterations (inner).

Usage:
    uv run .claude/PRPs/scripts/prp_loop.py "implement feature X" [--base main]
    uv run .claude/PRPs/scripts/prp_loop.py --resume
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .claude/PRPs/scripts/ -> repo root
STATE_FILE = ROOT / ".claude" / "prp-loop.state.json"
PLANS_DIR = ROOT / ".claude" / "PRPs" / "plans"
REVIEW_DIR = ROOT / ".claude" / "PRPs" / "reviews"

GREEN = "VALIDATION: GREEN"
PROTECTED_BRANCHES = {"main", "master", "development", "develop"}
STAGE_TIMEOUT = 3600  # seconds per claude stage
LOOP_ARTIFACTS = (".claude/prp-loop.state.json", ".claude/prp-loop.run.log")  # never commit these


def log(msg: str) -> None:
    print(f"[prp-loop] {msg}", flush=True)


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------- state ----------
def load_state() -> dict | None:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return None


def save_state(state: dict) -> None:
    state["updated_at"] = now()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def record(state: dict, stage: str, result: str) -> None:
    state.setdefault("history", []).append(
        {"stage": stage, "cycle": state["cycle"], "result": result, "at": now()}
    )


def halt(state: dict, reason: str) -> None:
    state["status"] = "halted"
    state["halt_reason"] = reason
    save_state(state)
    log(f"HALTED: {reason}")
    log(f"State preserved at {STATE_FILE.relative_to(ROOT)}. Fix, then re-run with --resume.")
    sys.exit(1)


# ---------- shells ----------
def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()


def run_claude(prompt: str) -> str:
    """Run one headless Claude stage; return its final result text. Raises on error."""
    cmd = [
        "claude", "-p", prompt,
        "--dangerously-skip-permissions",
        "--output-format", "json",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=STAGE_TIMEOUT)
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr[:500]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.stdout  # tolerate plain text
    if data.get("is_error"):
        raise RuntimeError(f"stage reported an error: {str(data.get('result'))[:500]}")
    return str(data.get("result", ""))


# ---------- helpers ----------
def newest_plan() -> str | None:
    if not PLANS_DIR.exists():
        return None
    plans = list(PLANS_DIR.glob("*.plan.md"))
    if not plans:
        return None
    return str(max(plans, key=lambda p: p.stat().st_mtime).relative_to(ROOT))


def current_pr() -> tuple[int | None, str | None]:
    out = subprocess.run(
        ["gh", "pr", "view", "--json", "number,url"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if out.returncode != 0:
        return None, None
    d = json.loads(out.stdout)
    return d.get("number"), d.get("url")


def _excludes() -> list[str]:
    return [f":(exclude){p}" for p in LOOP_ARTIFACTS]


def _dirty() -> str:
    """Porcelain status, excluding the loop's own artifacts so we never sweep them in."""
    return git("status", "--porcelain", "--", ".", *_excludes())


def ensure_committed(state: dict) -> None:
    """Ensure implement's changes are committed, but NEVER commit the loop's own artifacts
    (state.json / run.log) — even if the target repo doesn't gitignore them."""
    if _dirty():
        log("uncommitted changes remain; committing via prp-commit")
        run_claude("Use the prp-commit skill to commit all current changes.")
    if _dirty():
        subprocess.run(["git", "add", "-A", "--", ".", *_excludes()], cwd=ROOT)
        subprocess.run(["git", "commit", "-m", "chore: prp-loop checkpoint"], cwd=ROOT)


def check_green(state: dict, result: str) -> tuple[bool, str]:
    """Decide whether validations pass. --validate is authoritative if provided."""
    cmd = state.get("validate_cmd")
    if cmd:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=True)
        return proc.returncode == 0, (proc.stdout + proc.stderr)[-2000:]
    if GREEN in result:
        return True, ""
    if "VALIDATION: FAILED" in result:
        return False, result.split("VALIDATION: FAILED", 1)[-1][:2000]
    return False, result[-2000:]


def implement_until_green(state: dict, initial_prompt: str, label: str) -> bool:
    prompt = initial_prompt
    for i in range(1, state["max_implement_iterations"] + 1):
        log(f"{label} iteration {i}/{state['max_implement_iterations']} (cycle {state['cycle']})")
        result = run_claude(prompt)
        green, failures = check_green(state, result)
        if green:
            record(state, label, f"green@{i}")
            save_state(state)
            return True
        prompt = (
            "Continue working on the current branch. The previous attempt's validations "
            f"did not pass:\n{failures}\n\n"
            "Fix the failures, re-run ALL validations, and commit. End your message with "
            f"exactly '{GREEN}' when everything passes, otherwise 'VALIDATION: FAILED' "
            "followed by the failing output."
        )
        save_state(state)
    return False


# ---------- stages ----------
def stage_plan(state: dict) -> None:
    log("STAGE plan")
    run_claude(f"Use the prp-plan skill to create an implementation plan for: {state['feature']}")
    plan = newest_plan()
    if not plan:
        halt(state, "plan stage produced no .plan.md under .claude/PRPs/plans/")
    state["artifacts"]["plan_path"] = plan
    record(state, "plan", "ok")
    state["stage"] = "implement"
    save_state(state)
    log(f"plan -> {plan}")


def stage_implement(state: dict) -> None:
    log("STAGE implement")
    plan = state["artifacts"]["plan_path"]
    base_arg = f" --base {state['base']}" if state.get("base") else ""
    initial = (
        f"Use the prp-implement skill to execute the plan at {plan}{base_arg}. "
        "Run ALL validations and commit your work. End your message with exactly "
        f"'{GREEN}' if every validation passes, otherwise end with 'VALIDATION: FAILED' "
        "followed by the failing output."
    )
    if not implement_until_green(state, initial, "implement"):
        halt(state, f"implement not green after {state['max_implement_iterations']} iterations")
    ensure_committed(state)
    state["stage"] = "pr"
    save_state(state)


def stage_pr(state: dict) -> None:
    log("STAGE pr")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch or branch in PROTECTED_BRANCHES or branch == (state.get("base") or ""):
        halt(state, f"refusing to open a PR from base/protected branch '{branch}'")
    state["artifacts"]["branch"] = branch
    base_arg = f" --base {state['base']}" if state.get("base") else ""
    run_claude(f"Use the prp-pr skill to push the current branch and open a pull request{base_arg}.")
    num, url = current_pr()
    if not num:
        halt(state, "pr stage did not produce a discoverable PR (gh pr view failed)")
    state["artifacts"]["pr_number"] = num
    state["artifacts"]["pr_url"] = url
    record(state, "pr", f"#{num}")
    state["stage"] = "review"
    save_state(state)
    log(f"pr -> #{num} {url}")


def stage_review(state: dict) -> None:
    log("STAGE review")
    num = state["artifacts"]["pr_number"]
    cycle = state["cycle"]
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    verdict_path = REVIEW_DIR / f"pr-{num}-cycle-{cycle}.verdict.json"
    rel = verdict_path.relative_to(ROOT)
    bar = state["clean_bar"]
    prompt = (
        f"Use the prp-review-agents skill to review PR #{num}. "
        "After the review is complete, decide whether the PR is CLEAN, where clean means "
        f"there are zero {bar} issues. Then write a JSON file to {rel} with exactly this "
        'shape and nothing else:\n'
        '{"clean": <true|false>, "blocking": ["<one line per blocking finding>"]}'
    )
    run_claude(prompt)
    if not verdict_path.exists():
        halt(state, f"review stage did not write the verdict file {rel}")
    verdict = json.loads(verdict_path.read_text())
    state["artifacts"].setdefault("review_verdicts", []).append(str(rel))

    if verdict.get("clean"):
        record(state, "review", "clean")
        state["stage"] = "done"
        state["status"] = "done"
        save_state(state)
        log("review CLEAN — pipeline complete")
        return

    blocking = verdict.get("blocking", [])
    record(state, "review", f"dirty:{len(blocking)}")
    if state["cycle"] >= state["max_cycles"]:
        halt(state, f"review still dirty after {state['max_cycles']} cycles; PR #{num} left open for review")
    state["cycle"] += 1
    state["pending_findings"] = blocking
    state["stage"] = "fix"
    save_state(state)
    log(f"review dirty ({len(blocking)} blocking) — entering cycle {state['cycle']}")


def stage_fix(state: dict) -> None:
    log("STAGE fix")
    findings = "\n".join(f"- {f}" for f in state.get("pending_findings", []))
    plan = state["artifacts"]["plan_path"]
    pr_num = state["artifacts"]["pr_number"]
    head_before = git("rev-parse", "HEAD")
    initial = (
        f"Address these blocking review findings on the current branch (PR #{pr_num}):\n"
        f"{findings}\n\n"
        f"Use the prp-implement skill's approach against the plan at {plan}: make the fixes, "
        "run ALL validations, and commit. End your message with exactly "
        f"'{GREEN}' when everything passes, otherwise 'VALIDATION: FAILED' + the output."
    )
    if not implement_until_green(state, initial, "fix"):
        halt(state, f"fix pass not green after {state['max_implement_iterations']} iterations")
    ensure_committed(state)
    if git("rev-parse", "HEAD") == head_before:
        halt(state, "fix pass produced no new commit (no progress) — halting to avoid an infinite loop")
    push = subprocess.run(["git", "push"], cwd=ROOT, capture_output=True, text=True)
    if push.returncode != 0:
        halt(state, f"git push failed: {push.stderr[:300]}")
    record(state, "fix", "pushed")
    state.pop("pending_findings", None)
    state["stage"] = "review"
    save_state(state)


STAGES = {
    "plan": stage_plan,
    "implement": stage_implement,
    "pr": stage_pr,
    "review": stage_review,
    "fix": stage_fix,
}


def main() -> None:
    ap = argparse.ArgumentParser(description="Autonomous cyclic PRP pipeline (plan->implement->pr->review).")
    ap.add_argument("feature", nargs="?", help="Feature description, or path to a PRD/plan.")
    ap.add_argument("--base", help="Base branch (default: auto-detected by the skills).")
    ap.add_argument("--max-cycles", type=int, default=3, help="Max review->fix cycles (default 3).")
    ap.add_argument("--max-implement-iterations", type=int, default=10,
                    help="Max implement/fix iterations per stage (default 10).")
    ap.add_argument("--clean-bar", default="Critical or Important",
                    help="Severity that blocks 'clean' (default: 'Critical or Important').")
    ap.add_argument("--validate", dest="validate_cmd",
                    help="Authoritative shell command for green (exit 0 = pass). "
                         "If omitted, falls back to the VALIDATION: GREEN sentinel.")
    ap.add_argument("--resume", action="store_true", help="Resume from the existing state file.")
    args = ap.parse_args()

    state = load_state()
    if args.resume:
        if not state:
            sys.exit("no state file to resume from")
        state["status"] = "running"
        log(f"resuming at stage={state['stage']} cycle={state['cycle']}")
    else:
        if state and state.get("status") == "running":
            sys.exit(f"a loop is already running ({STATE_FILE.relative_to(ROOT)}); use --resume or delete it")
        if not args.feature:
            sys.exit("a feature description is required to start a new loop")
        state = {
            "loop_id": f"prp-loop-{now()}",
            "feature": args.feature,
            "stage": "plan",
            "cycle": 0,
            "max_cycles": args.max_cycles,
            "max_implement_iterations": args.max_implement_iterations,
            "clean_bar": args.clean_bar,
            "validate_cmd": args.validate_cmd,
            "base": args.base,
            "status": "running",
            "artifacts": {},
            "history": [],
            "started_at": now(),
        }
        save_state(state)

    while state["stage"] != "done":
        stage = state["stage"]
        try:
            STAGES[stage](state)
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001 - top-level guard halts with preserved state
            halt(state, f"stage '{stage}' raised: {e}")

    log(f"DONE. PR: {state['artifacts'].get('pr_url')}")


if __name__ == "__main__":
    main()

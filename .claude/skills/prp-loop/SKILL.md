---
name: prp-loop
description: Run the autonomous cyclic PRP pipeline end to end (plan → implement → pr → review, looping review→fix until the PR is clean). Use when the user wants to "ship feature X end to end", "run the full PRP loop", "auto-implement and open a PR for a feature", or invokes /prp-loop.
argument-hint: "<feature description> [--base <branch>] [--max-cycles N] [--validate \"<cmd>\"] | --resume"
---

# PRP Loop — autonomous cyclic pipeline

Launch the orchestrator that drives `plan → implement → pr → review` and loops `review → fix` until the PR review is clean (or limits are hit). It runs headless `claude -p` once per stage and tracks progress in `.claude/prp-loop.state.json`.

## Run it

Start a new loop with the user's request as the feature argument:

```bash
uv run .claude/PRPs/scripts/prp_loop.py "$ARGUMENTS"
```

Resume a halted or in-progress loop:

```bash
uv run .claude/PRPs/scripts/prp_loop.py --resume
```

Defaults: `--max-cycles 3`, `--max-implement-iterations 10`, base branch auto-detected. Pass `--validate "<cmd>"` to give the loop an authoritative green check (exit 0 = pass).

## What it does

1. **plan** — `prp-plan` writes `.claude/PRPs/plans/<feature>.plan.md`.
2. **implement** — `prp-implement` executes the plan, looping until all validations pass (bounded by `--max-implement-iterations`), then commits.
3. **pr** — `prp-pr` pushes the branch and opens the PR (once).
4. **review** — `prp-review-agents` reviews the PR and writes a `{clean, blocking}` verdict.
5. **cycle** — if not clean, the blocking findings feed back into a fix pass → push → re-review, up to `--max-cycles`. Clean → done.

## Safety

- Fully autonomous (`--dangerously-skip-permissions`). Operates only on the feature branch — it refuses to PR from `main`/`master`/`development`/the base branch.
- Halts with state preserved on: implement/fix not green after the iteration limit, review still dirty after `--max-cycles`, a fix pass with no new commit (no progress), failed push, or any stage error.
- Inspect or resume via `.claude/prp-loop.state.json`.

## Notes

This orchestrator is self-contained and does **not** use the `prp-ralph` Stop-hook. It owns both loops itself and detects "green" from each stage's `VALIDATION: GREEN` sentinel (or the `--validate` command). The PRP skills it calls are invoked verbatim and never modified.

# Feature: Consolidate the PRP skill suite (18 → 12)

## Summary

Reduce skill sprawl in `.claude/skills/` by removing one stale skill, merging two duplicate-capability pairs, folding one lifecycle-maintenance skill into its artifact owner, and deprecating the buggy Ralph in favour of a `prp-loop` mode. Bodies are lifted **verbatim** when merging (fidelity first); refactor/trim is a later, separate step. The plugin is explicitly out of scope here.

## Problem Statement

The suite grew to 18 skills with real overlap: two ways to review a PR, a stale orchestrator replaced by `prp-loop`, a buggy Ralph whose function `prp-loop` already covers, and a plan-maintenance skill that is really a stage of the plan's own lifecycle. The sprawl dilutes trigger precision and creates "which one do I use?" ambiguity.

## Solution Statement

Apply the consolidation rubric from `prp-meta-skill` (bundle same-capability variants and tightly-coupled artifact lifecycles; keep distinct capabilities/verbs separate; merge = one self-contained skill, never cross-linked). End state: 12 skills.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | REFACTOR                                          |
| Complexity       | MEDIUM                                            |
| Systems Affected | `.claude/skills/`, `.claude/PRPs/scripts/prp_loop.py`, `.claude/hooks/`, `.claude/settings.local.json` |
| Dependencies     | none (markdown skills + one python script)        |
| Estimated Tasks  | 6                                                 |

## Lifecycle (append-only)

- **Created:** 2026-06-25
- **Modified:**
- **Commits:**
- **Agent / Session:**
- **Back refs:** [[prp-commands-to-skills-port]] (the port that created these skills)
- **Forward refs:** plugin skill-structure migration (future phase)

> Append-only; never overwrite existing entries.

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `.claude/skills/prp-core-runner/` | DELETE | Stale; replaced by `prp-loop` |
| `.claude/skills/prp-review-agents/` | DELETE | Merged into `prp-review` |
| `.claude/skills/prp-review/SKILL.md` | UPDATE | Absorb fan-out as `--agents`; report format → `templates/` |
| `.claude/skills/prp-update-references/` | DELETE | Folded into `prp-plan` |
| `.claude/skills/prp-plan/` | UPDATE | Add `update-references` workflow (+ `workflows/` dir) |
| `.claude/skills/prp-issue/` | CREATE | Bundle investigate + fix as workflows |
| `.claude/skills/prp-issue-investigate/`, `prp-issue-fix/` | DELETE | Lifted into `prp-issue` |
| `.claude/skills/prp-ralph/`, `prp-ralph-cancel/` | DELETE | Deprecated; covered by `prp-loop` |
| `.claude/PRPs/scripts/prp_loop.py` | UPDATE | Add `--until <stage>` (implement-only = Ralph replacement) |
| `.claude/hooks/prp-ralph-stop.sh` | DELETE | Ralph retired |
| `.claude/settings.local.json` | UPDATE | Remove the Ralph Stop-hook registration |

## NOT Building (scope limits)

- The plugin (`plugins/prp-core/`) — separate migration phase, deliberately untouched here.
- Bundling `prp-prd` into `prp-plan` — they stay separate (distinct capabilities).
- Bundling `prp-commit`/`prp-pr` or the investigation skills — kept separate.
- Removing the plugin's `prp-ralph-loop`/hooks — handled in the plugin phase.

## Step-by-Step Tasks

Status markers: `[ ]` idle · `[wip]` in progress · `[x]` complete · `[f]` failed. Prefix every task. `[f]` → note why in Agent Notes and move on if the rest can proceed.

### `[ ]` Task 1: Remove `prp-core-runner`
- **ACTION**: delete `.claude/skills/prp-core-runner/`
- **VALIDATE**: skill no longer listed; nothing references it

### `[ ]` Task 2: Merge review pair → `prp-review`
- **ACTION**: fold `prp-review-agents`'s multi-agent fan-out into `prp-review` as an `--agents`/`[aspects…]` mode; keep `--approve|--request-changes`
- **IMPLEMENT**: lift the fan-out body verbatim into a workflow/section; move the shared review-summary format to `prp-review/templates/review-report.md` with a mandatory-read pointer
- **THEN**: delete `prp-review-agents/`; update `prp-loop` review stage prompt → "use `prp-review` with `--agents`"
- **GOTCHA**: side-effecting (posts comments / approves) → for the eventual plugin copy, mark `disable-model-invocation`
- **VALIDATE**: `/prp-review` triggers; agents mode runs; prp-loop review stage references resolve

### `[ ]` Task 3: Fold `update-references` into `prp-plan`
- **ACTION**: add an `update-references` workflow to `prp-plan` (introduce `prp-plan/workflows/` if splitting); lift the body verbatim
- **THEN**: delete `prp-update-references/`; update any references (prp-implement maintenance text, memory)
- **VALIDATE**: linking two plans still works end-to-end; prp-plan still triggers for plain planning

### `[ ]` Task 4: Bundle issue pair → `prp-issue`
- **ACTION**: create `.claude/skills/prp-issue/` with `investigate` and `fix` workflows; lift both bodies **verbatim** into `workflows/`
- **IMPLEMENT**: SKILL.md routes on arg (`investigate <issue>` | `fix <issue|artifact>`); preserve each phase's process/output exactly
- **THEN**: delete `prp-issue-investigate/`, `prp-issue-fix/`
- **GOTCHA**: `fix` is side-effecting (commits, opens PR) — note for plugin invocation control
- **VALIDATE**: `/prp-issue` triggers; both workflows reproduce prior behavior

### `[ ]` Task 5: Deprecate Ralph → `prp-loop` mode
- **ACTION**: add `--until <stage>` to `prp_loop.py` (stop after the named stage; `--until implement` = "grind one plan to green, no PR" = the Ralph replacement)
- **THEN**: delete `prp-ralph/`, `prp-ralph-cancel/`, `.claude/hooks/prp-ralph-stop.sh`; remove the Stop-hook block from `.claude/settings.local.json`
- **GOTCHA**: UX change — Ralph was single-session interactive; `prp-loop --until implement` is headless. Document in the loop skill
- **VALIDATE**: `python3 -m py_compile prp_loop.py`; `--until implement` stops after implement; no dangling Ralph references

### `[ ]` Task 6: Verify the consolidated suite
- **ACTION**: confirm 12 skills remain; every surviving skill triggers; `prp-loop` references only existing skills
- **VALIDATE**: see Validation Commands; exercise merged `prp-review` and new `prp-issue` for real (per the meta-skill "exercise end-to-end" gate)

## Validation Commands

🔁 **Validation loop:** not complete until every check passes. On failure, fix and re-run.

- `ls -1d .claude/skills/*/ | wc -l` → **EXPECT 12**
- `python3 -m py_compile .claude/PRPs/scripts/prp_loop.py` → exit 0
- `grep -rl 'prp-review-agents\|prp-update-references\|prp-ralph\|prp-core-runner\|prp-issue-investigate\|prp-issue-fix' .claude/skills .claude/PRPs/scripts` → **EXPECT no stale references** (except intended deprecation notes)
- Trigger test: `/prp-review`, `/prp-issue`, `/prp-plan` (update-references mode), `/prp-loop --until implement` all resolve
- Exercise-for-real: run merged `prp-review` and `prp-issue investigate` against a real target; confirm unchanged behavior

## Acceptance Criteria

- [ ] 12 skills remain; the 6 removed/merged are gone
- [ ] Merged `prp-review` and `prp-issue` reproduce prior process + output (fidelity preserved)
- [ ] `prp-plan` gains `update-references`; `prp-loop` gains `--until`
- [ ] No dangling references to removed skills anywhere
- [ ] Ralph hook + settings registration removed

## Questionables

<details>
<summary>Should the merged `prp-review` default to the fan-out, or single-pass with `--agents` opt-in?</summary>

Assumption taken: **single-pass default, `--agents` opt-in** (cheaper default; fan-out when asked or for large diffs). Revisit if you want fan-out always-on.
</details>

## Agent Notes

_Open canvas._

- Merges follow **fidelity-first**: lift bodies verbatim, prove behavior, trim later. Trimming merged skills into lean references is a *separate* follow-up, not part of this plan.
- "Bundle" here = one self-contained skill with internal `workflows/`; no cross-skill reference links (one-source-of-truth).
- Plugin migration is the natural next phase — it will mirror these same merges into `plugins/prp-core/` and decide the source-of-truth model.
- `--until <stage>` is independently useful (it's the guarded-run control we wanted during the loop's first run).

## Amendments

_Append-only; populated by the build/update steps._

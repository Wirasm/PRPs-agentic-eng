---
description: Generate implementation plans for multiple PRD phases or a list of features in batch
argument-hint: <path/to/prd.md | comma-separated feature list>
---

# Batch Plan Generator

**Input**: $ARGUMENTS

---

## Your Mission

Generate implementation plans for multiple features or PRD phases by invoking the `/prp-plan` workflow for each.

---

## Phase 1: ANALYZE — Determine What to Plan

### If input is a PRD file path:

Read the PRD and extract ALL pending phases from the Implementation Phases table:

```bash
cat "$ARGUMENTS"
```

Parse the phases table. Collect all phases with `Status: pending`.

**Respect dependencies**: Only plan phases whose dependencies are `complete` or are being planned in this batch (sequential execution handles ordering).

### If input is a feature list:

Split the input into individual features. Each becomes a standalone plan.

### Determine batch size:

| Scenario | Count |
|----------|-------|
| PRD with N pending phases | Plan all phases with met dependencies |
| Comma-separated features | One plan per feature |
| Single complex feature | 1 (redirect to `/prp-plan` directly) |

---

## Phase 2: PROPOSE — Present Plan to User

```markdown
## Batch Plan Generation

**Source**: {PRD file or feature list}

I'll generate **{N}** implementation plans:

| # | Plan | Source | Dependencies Met? | Can Parallelize? |
|---|------|--------|--------------------|------------------|
| 1 | {phase/feature name} | Phase 1 of PRD | Yes | - |
| 2 | {phase/feature name} | Phase 2 of PRD | Yes (depends on 1) | - |
| 3 | {phase/feature name} | Phase 3 of PRD | Yes | with 4 |
| 4 | {phase/feature name} | Phase 4 of PRD | Yes | with 3 |

**Generation order**: {sequence accounting for dependencies}

Proceed?
```

**GATE**: Wait for user approval.

---

## Phase 3: GENERATE — Create Each Plan

For each approved item, invoke the full `/prp-plan` workflow:

1. Process plans **sequentially** in dependency order
2. For each plan:
   - If from a PRD: pass the PRD path and specify the target phase
   - If from a feature list: pass the feature description directly
   - Follow ALL phases of `/prp-plan` (Parse → Explore → Research → Design → Architect → Generate)
   - The generated plan goes to `.claude/PRPs/plans/{name}.plan.md`
   - If sourced from a PRD, update the PRD's Implementation Phases table (set status to `in-progress`, add PRP Plan link)
3. Brief confirmation after each plan before proceeding

### Cross-Plan Consistency

- Reference shared interfaces or contracts defined in earlier plans
- Use consistent naming for shared concepts
- Note cross-plan integration points explicitly in each plan

---

## Phase 4: SUMMARIZE — Batch Report

```markdown
## Batch Plan Generation Complete

**Source**: {input}
**Plans Generated**: {N}

| # | Plan | File | Tasks | Parallel? |
|---|------|------|-------|-----------|
| 1 | {name} | `.claude/PRPs/plans/{file}.plan.md` | {N} | - |
| 2 | {name} | `.claude/PRPs/plans/{file}.plan.md` | {N} | - |
| 3 | {name} | `.claude/PRPs/plans/{file}.plan.md` | {N} | with 4 |
| 4 | {name} | `.claude/PRPs/plans/{file}.plan.md` | {N} | with 3 |

### Execution Strategy

**Sequential plans** (have dependencies):
{List in order}

**Parallelizable plans** (independent):
{List groups that can run in separate worktrees}

### Next Steps

- **Implement first**: `/prp-implement .claude/PRPs/plans/{first-plan}.plan.md`
- **Ralph loop**: `/prp-ralph .claude/PRPs/plans/{first-plan}.plan.md --max-iterations 20`
- **Parallel worktrees** (for independent plans):
  ```bash
  git worktree add -b {branch} ../{dir}
  cd ../{dir} && claude "/prp-implement .claude/PRPs/plans/{plan}.plan.md"
  ```
```

---

## Examples

```
# All pending phases from a PRD
/prp-plan-batch .claude/PRPs/prds/user-auth.prd.md

# List of independent features
/prp-plan-batch "pagination API, search filters, CSV export"
```

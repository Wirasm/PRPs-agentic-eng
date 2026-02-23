---
description: Generate multiple PRDs from a broad initiative, product vision, or feature list
argument-hint: <initiative description or comma-separated feature list>
---

# Batch PRD Generator

**Input**: $ARGUMENTS

---

## Your Mission

Decompose a broad initiative or feature list into the optimal number of independent PRDs, then generate each one by invoking the `/prp-prd` workflow.

---

## Phase 1: ANALYZE — Determine Optimal Decomposition

Read and understand the input. Determine whether it's:

| Input Type | Example | Action |
|------------|---------|--------|
| Broad initiative | "Build a multi-tenant SaaS platform" | Decompose into logical product areas |
| Feature list | "auth, billing, admin dashboard, notifications" | Validate separation, merge or split as needed |
| Single complex feature | "User management with RBAC, SSO, and audit logging" | Split into bounded deliverables |

### Decomposition Criteria

Each PRD should be:
- **Independent**: Can be built, deployed, and validated without other PRDs being complete (or has minimal, explicit dependencies)
- **Bounded**: Completable in 1-5 implementation phases
- **Cohesive**: Covers a single product area or domain
- **Valuable**: Delivers user-visible value on its own

### Anti-patterns to avoid:
- Too granular (e.g., one PRD per API endpoint) — merge related items
- Too broad (e.g., "the entire backend") — split by domain
- Overlapping scope between PRDs — draw clear boundaries
- Circular dependencies — reorder or merge

---

## Phase 2: PROPOSE — Present Plan to User

Present the decomposition for approval:

```markdown
## Batch PRD Plan

**Initiative**: {restated input}

I recommend generating **{N}** PRDs:

| # | PRD Name | Scope | Dependencies | Est. Phases |
|---|----------|-------|--------------|-------------|
| 1 | {name} | {1-2 sentence scope} | None | {N} |
| 2 | {name} | {1-2 sentence scope} | PRD 1 | {N} |
| 3 | {name} | {1-2 sentence scope} | None | {N} |

**Dependency graph**:
{Simple ASCII showing which PRDs depend on others, or "All independent" if none}

**Suggested order**: {execution order accounting for dependencies}

Should I proceed? You can also:
- Merge/split any items
- Adjust scope boundaries
- Change the count
```

**GATE**: Wait for user approval or adjustments before proceeding.

---

## Phase 3: GENERATE — Create Each PRD

For each approved PRD, invoke the full `/prp-prd` workflow:

### Execution Strategy

1. Process PRDs **sequentially** (each builds context for the next)
2. For each PRD:
   - Pass the scoped description as input to the `/prp-prd` process
   - Follow ALL phases of `/prp-prd` (Foundation questions → Grounding → Deep Dive → etc.)
   - **IMPORTANT**: For batch mode, answer Foundation/Deep Dive/Scope questions using context from the initiative description and previously generated PRDs. Only pause for user input when genuinely ambiguous.
   - Generate the PRD file to `.claude/PRPs/prds/{kebab-case-name}.prd.md`
3. After each PRD, briefly confirm completion before moving to the next

### Cross-PRD Consistency

Maintain consistency across generated PRDs:
- **Shared terminology**: Use same terms for same concepts across all PRDs
- **Dependency references**: When PRD B depends on PRD A, reference the specific file and phase
- **Non-overlapping scope**: Ensure no capability appears in multiple PRDs
- **Aligned technical approach**: Consistent architecture decisions

---

## Phase 4: SUMMARIZE — Batch Report

After all PRDs are generated:

```markdown
## Batch PRD Generation Complete

**Initiative**: {input}
**PRDs Generated**: {N}

| # | PRD | File | Phases | Dependencies |
|---|-----|------|--------|--------------|
| 1 | {name} | `.claude/PRPs/prds/{file}.prd.md` | {N} | - |
| 2 | {name} | `.claude/PRPs/prds/{file}.prd.md` | {N} | PRD 1 |
| 3 | {name} | `.claude/PRPs/prds/{file}.prd.md` | {N} | - |

### Dependency Order

{Recommended execution sequence, noting which can run in parallel}

### Open Questions Across PRDs

{Aggregated open questions that span multiple PRDs}

### Next Steps

- **Sequential**: Run `/prp-plan .claude/PRPs/prds/{first-prd}.prd.md` to start
- **Parallel (independent PRDs)**: Use git worktrees for PRDs with no dependencies
- **Batch plan**: Run `/prp-plan-batch` to generate plans for all pending phases
```

---

## Examples

```
# Broad initiative
/prp-prd-batch "Build an e-commerce platform with product catalog, cart, checkout, and order management"

# Explicit feature list
/prp-prd-batch "user authentication with SSO, role-based access control, audit logging, user profile management"

# Single complex feature that needs splitting
/prp-prd-batch "Real-time collaboration system: presence indicators, cursor tracking, conflict resolution, change history"
```

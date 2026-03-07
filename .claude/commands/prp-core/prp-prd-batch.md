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

## Phase 1: ANALYZE — Determine Optimal PRD Count & Decomposition

Read and understand the input. Classify it:

| Input Type | Example | Action |
|------------|---------|--------|
| Milestone / epic | "Q3 platform launch: auth, billing, marketplace, analytics" | Identify distinct project areas, determine optimal count |
| Broad initiative | "Build a multi-tenant SaaS platform" | Decompose into logical product areas |
| Feature list | "auth, billing, admin dashboard, notifications" | Validate separation, merge or split as needed |
| Single complex feature | "User management with RBAC, SSO, and audit logging" | Split into bounded deliverables |

### Step 1: Determine Optimal Number of PRDs

Before decomposing, explicitly analyze the scope to determine how many PRDs are needed:

1. **Extract distinct deliverables** — List every capability, project, or feature area mentioned or implied in the description
2. **Cluster by domain** — Group related deliverables into cohesive product domains (e.g., "login + SSO + password reset" → single "Authentication" PRD)
3. **Apply sizing heuristics**:
   - Each PRD should map to **1-5 implementation phases** (roughly 1-4 weeks of work per phase)
   - If a cluster exceeds ~5 phases, split it further
   - If a cluster has only 1 trivial phase, merge it into an adjacent domain
4. **Count and justify** — Arrive at the optimal N with explicit reasoning:
   ```
   Scope analysis:
   - Identified {X} distinct capabilities in the description
   - Clustered into {Y} domains after merging related items
   - Split {Z} oversized domains → final count: {N} PRDs
   - Rationale: {why N is the right number, not N-1 or N+1}
   ```

**For milestone-type inputs** (roadmap items, epics, quarterly goals), pay special attention to:
- Each milestone may contain **multiple independent projects** — each project typically warrants its own PRD
- Shared infrastructure across projects should be its own PRD if non-trivial
- Identify which projects are truly independent vs. which share foundations

### Step 2: Validate Decomposition Quality

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
- Milestone with N items ≠ N PRDs — cluster by domain, not by bullet point

---

## Phase 2: PROPOSE — Present Plan to User

Present the decomposition for approval, including the count rationale from Phase 1:

```markdown
## Batch PRD Plan

**Initiative**: {restated input}
**Input type**: {Milestone / Broad initiative / Feature list / Complex feature}

### Optimal Count Analysis

- Identified **{X}** distinct capabilities in the description
- Clustered into **{Y}** domains after merging related items
- {Split/merged adjustments if any}
- **Optimal count: {N} PRDs** — {one-sentence rationale}

### Proposed PRDs

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
# Milestone with multiple projects
/prp-prd-batch "Q3 Milestone: launch self-serve onboarding, migrate billing to Stripe, add team workspaces, build analytics dashboard, implement webhook system"

# Broad initiative
/prp-prd-batch "Build an e-commerce platform with product catalog, cart, checkout, and order management"

# Explicit feature list
/prp-prd-batch "user authentication with SSO, role-based access control, audit logging, user profile management"

# Single complex feature that needs splitting
/prp-prd-batch "Real-time collaboration system: presence indicators, cursor tracking, conflict resolution, change history"
```

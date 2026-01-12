---
name: prp-ralph-loop
description: "Autonomous iteration execution guide for PRP Ralph loops. Use when .claude/prp-ralph.state.md exists, when continuing Ralph iterations, or when executing plans autonomously until all validations pass. Provides iteration behavior, completion protocol, validation requirements, and progress logging."
user-invocable: false
---

# PRP Ralph Loop Execution Guide

This skill provides the knowledge needed to correctly execute Ralph loop iterations. Ralph is an autonomous loop system that executes PRP plans iteratively until all tasks are complete and all validations pass.

---

## 1. Context Detection

### How to Know You're in a Ralph Loop

Check for the state file: `.claude/prp-ralph.state.md`

If this file exists, you are in an active Ralph loop. Read it first to understand:
- Current iteration number
- Maximum iterations allowed
- Path to the plan being executed
- Progress from previous iterations

### State File Location

```
.claude/prp-ralph.state.md
```

---

## 2. State File Format

The state file uses YAML frontmatter followed by a progress log:

```markdown
---
iteration: 3
max_iterations: 10
plan_path: ".claude/PRPs/plans/add-feature.md"
started_at: "2024-01-12T10:00:00Z"
---

# Ralph Progress Log

## Codebase Patterns
[Consolidated learnings that apply across iterations]

## Iteration 1 - 2024-01-12T10:05:00Z
- Implemented X
- Files changed: a.ts, b.ts
- Learnings: Found that Y pattern is used for Z
- Still failing: type-check (3 errors)

## Iteration 2 - 2024-01-12T10:15:00Z
- Fixed type errors
- Added missing imports
- Learnings: Always import types from @/types
- Still failing: tests (1 failure in auth.test.ts)

---
```

### Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `iteration` | number | Current iteration (1-indexed) |
| `max_iterations` | number | Maximum allowed iterations (0 = unlimited) |
| `plan_path` | string | Path to the plan file being executed |
| `started_at` | string | ISO timestamp when loop started |

---

## 3. Iteration Behavior Protocol

### Each Iteration Must Follow This Sequence

#### Step 1: Read Context
1. Read the state file to understand current iteration and history
2. Read the plan file (from `plan_path`) to understand all tasks
3. Check the "Codebase Patterns" section for learnings from previous iterations
4. Review git status to see current state of changes

#### Step 2: Assess Current State
1. What tasks in the plan are already complete?
2. What validations are currently passing/failing?
3. What did the previous iteration accomplish?
4. What's blocking completion?

#### Step 3: Implement Next Piece
1. Pick the next logical task (respect dependencies)
2. Implement it fully
3. Keep changes focused and minimal
4. Follow existing code patterns

#### Step 4: Run ALL Validations
Run every validation command. Do not skip any.

**TypeScript/JavaScript:**
```bash
bun run type-check || npm run type-check || npx tsc --noEmit
bun run lint || npm run lint
bun test || npm test
bun run build || npm run build
```

**Python:**
```bash
uv run ruff check --fix
uv run mypy .
uv run pytest
```

**General:**
```bash
git status  # Check for uncommitted changes
```

#### Step 5: Update Progress
Append to the state file's progress log (see Section 6).

#### Step 6: Decide Continue or Complete
- If ALL validations pass AND all tasks done → Output completion signal
- If ANY validation failing OR tasks remain → End response normally

---

## 4. Validation Requirements (Critical)

### The Golden Rules

1. **NEVER skip validations** - Run them every iteration
2. **NEVER complete if ANY validation fails** - Even one error means continue
3. **Log what's failing** - Next iteration needs to know
4. **Fix before adding** - Don't add new features while tests fail

### Validation Priority

1. **Type-check** - Must pass (catches most issues early)
2. **Lint** - Must pass (code quality)
3. **Tests** - Must pass (functionality verification)
4. **Build** - Must pass (deployment readiness)

### What Counts as "Passing"

- Exit code 0
- No errors in output
- Warnings are acceptable (but note them)

### Common Validation Failures and Fixes

| Failure | Common Cause | Fix |
|---------|--------------|-----|
| Type error | Missing import, wrong type | Add import, fix type annotation |
| Lint error | Formatting, unused var | Run auto-fix, remove unused code |
| Test failure | Logic bug, missing mock | Fix logic, add proper mocks |
| Build error | Missing dependency | Install dependency, fix imports |

---

## 5. Completion Protocol

### The Completion Signal

```
<promise>COMPLETE</promise>
```

This exact string signals that the Ralph loop should end.

### When to Output the Completion Signal

Output `<promise>COMPLETE</promise>` ONLY when ALL of these are true:

1. **All tasks in the plan are done** - Every checkbox checked, every requirement met
2. **Type-check passes** - Zero type errors
3. **Lint passes** - Zero lint errors
4. **Tests pass** - All tests green
5. **Build passes** - Successful build (if applicable)
6. **Changes committed** - All work committed to git

### When NOT to Output the Completion Signal

NEVER output the completion signal if:

- Any validation is failing
- Tasks remain incomplete
- You're unsure if everything works
- There are uncommitted changes that should be committed

### What Happens After Completion

When you output `<promise>COMPLETE</promise>`:
1. The stop hook detects it
2. State file is cleaned up
3. Loop exits successfully
4. User sees completion message

### What Happens If You Don't Complete

If you end your response without the completion signal:
1. The stop hook detects incomplete state
2. Hook blocks exit and feeds continuation prompt
3. Next iteration begins with fresh context
4. Progress is preserved in state file

---

## 6. Progress Logging

### Why Progress Logging Matters

Each iteration has limited context. Progress logs are how you communicate with future iterations (including yourself). Good logs = faster completion.

### Progress Entry Format

After each iteration, APPEND to the state file:

```markdown
## Iteration N - [ISO timestamp]
Thread: [conversation reference if available]

### Completed
- [What was implemented this iteration]
- [Files changed: list them]

### Validation Status
- Type-check: [PASS/FAIL - details if failing]
- Lint: [PASS/FAIL - details if failing]
- Tests: [PASS/FAIL - details if failing]
- Build: [PASS/FAIL - details if failing]

### Learnings
- [Pattern discovered: "this codebase uses X for Y"]
- [Gotcha found: "don't forget to Z when doing W"]
- [Context: "the settings panel is in component X"]

### Next Steps
- [What the next iteration should focus on]
- [Specific files or functions to look at]

---
```

### Consolidating Patterns

If you discover a **reusable pattern** that future iterations should know, add it to the `## Codebase Patterns` section at the TOP of the progress log:

```markdown
## Codebase Patterns
- Use `sql<number>` template for type-safe SQL aggregations
- Always use `IF NOT EXISTS` in migrations
- Export types from actions.ts for UI components
- Form validation uses zod schemas in /lib/validations
```

Only add patterns that are **general and reusable**, not iteration-specific details.

---

## 7. Feeding Learnings Back to the System

### Updating CLAUDE.md

If you discover patterns that should be permanent project knowledge, update the project's CLAUDE.md:

**Good additions:**
- API patterns specific to this codebase
- Testing approaches that work well
- Configuration requirements
- Dependencies between modules

**Bad additions:**
- Temporary debugging notes
- Iteration-specific implementation details
- Information already in the plan

### Updating AGENTS.md Files

Check if edited directories have AGENTS.md files. Add learnings that help future work:

```markdown
## Patterns
- When modifying X, also update Y
- This module uses pattern Z for all API calls

## Gotchas
- Tests require dev server on port 3000
- Field names must match template exactly
```

### Creating Progress Archive

When a Ralph loop completes successfully, the learnings should be:

1. **Consolidated** - Important patterns extracted
2. **Archived** - Full progress log saved to `.claude/PRPs/ralph-archives/`
3. **Integrated** - Key learnings added to CLAUDE.md or AGENTS.md

Archive format:
```
.claude/PRPs/ralph-archives/
└── YYYY-MM-DD-feature-name/
    ├── state.md        # Final state file
    ├── plan.md         # The executed plan
    └── learnings.md    # Consolidated patterns
```

---

## 8. Common Mistakes to Avoid

### Mistake 1: Outputting Completion Too Early
**Wrong:** "Tests are probably passing, <promise>COMPLETE</promise>"
**Right:** Run tests, verify they pass, THEN output completion

### Mistake 2: Not Reading Previous Progress
**Wrong:** Start implementing without checking what's done
**Right:** Read state file first, understand current state

### Mistake 3: Ignoring Codebase Patterns
**Wrong:** Invent new patterns for common operations
**Right:** Check patterns section, follow existing conventions

### Mistake 4: Skipping Validations
**Wrong:** "I'm confident this works, no need to run tests"
**Right:** ALWAYS run ALL validations, every iteration

### Mistake 5: Not Logging Learnings
**Wrong:** Fix a tricky issue without documenting it
**Right:** Log the gotcha so future iterations don't repeat it

### Mistake 6: Too Much in One Iteration
**Wrong:** Try to complete 5 tasks in one iteration
**Right:** Focus on one task, do it well, validate, commit

---

## 9. Integration with Commands

### Starting a Ralph Loop

User invokes: `/prp-ralph [plan.md] --max-iterations N`

The command:
1. Creates the state file
2. Sets initial iteration to 1
3. Provides initial execution prompt

### Canceling a Ralph Loop

User invokes: `/prp-ralph-cancel`

This:
1. Removes the state file
2. Stops the loop
3. Preserves git history

### This Skill's Role

This skill is **not user-invoked**. It provides the knowledge Claude needs during loop execution. The command starts the loop, the hook maintains it, and this skill guides correct behavior.

---

## 10. Quick Reference

### State File Path
```
.claude/prp-ralph.state.md
```

### Completion Signal
```
<promise>COMPLETE</promise>
```

### Iteration Checklist
- [ ] Read state file and plan
- [ ] Check codebase patterns section
- [ ] Implement next task
- [ ] Run type-check
- [ ] Run lint
- [ ] Run tests
- [ ] Run build (if applicable)
- [ ] Commit changes
- [ ] Update progress log
- [ ] Decide: complete or continue

### Validation Commands (Common)
```bash
# TypeScript/JavaScript
npm run type-check && npm run lint && npm test && npm run build

# Python
uv run ruff check && uv run mypy . && uv run pytest
```

### Progress Log Template
```markdown
## Iteration N - YYYY-MM-DDTHH:MM:SSZ

### Completed
- [What was done]

### Validation Status
- Type-check: PASS/FAIL
- Lint: PASS/FAIL
- Tests: PASS/FAIL
- Build: PASS/FAIL

### Learnings
- [Patterns, gotchas, context]

### Next Steps
- [What to do next]

---
```

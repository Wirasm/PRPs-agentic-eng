---
description: Split working tree changes into multiple logical commits with smart grouping
argument-hint: [grouping strategy] (blank = auto-detect logical groups)
---

# Batch Commit

**Strategy**: $ARGUMENTS

---

## Your Mission

Analyze all uncommitted changes, determine the optimal number of logical commits, then create each commit using the `/prp-commit` workflow.

---

## Phase 1: ASSESS — Survey All Changes

```bash
git status --short
git diff --stat
git diff --cached --stat
```

If nothing to commit, stop.

---

## Phase 2: ANALYZE — Determine Logical Groups

Examine the changes and group them by logical unit. Consider:

### Grouping Strategies

| Strategy Input | Behavior |
|---------------|----------|
| (blank / auto) | Group by logical change unit (feature, fix, refactor, etc.) |
| `by-type` | Group by change type: feat, fix, refactor, docs, test, chore |
| `by-directory` | Group by top-level directory |
| `by-feature` | Group by feature/domain area |
| `atomic` | One commit per file |

### Auto-Detection Heuristic

When no strategy is specified, analyze the diff to identify:

1. **Distinct features**: New files + their tests + config changes = one group
2. **Refactors**: Renamed/moved files + import updates = one group
3. **Fixes**: Bug fix changes separate from feature work
4. **Docs**: Documentation-only changes
5. **Chore**: Config, dependency, tooling changes

**CRITICAL**: Each commit must leave the codebase in a valid state (compiles, passes lint).

---

## Phase 3: PROPOSE — Present Commit Plan

```markdown
## Batch Commit Plan

**Total changes**: {N} files ({additions}+ / {deletions}-)

I recommend **{N}** commits:

| # | Type | Message | Files | +/- |
|---|------|---------|-------|-----|
| 1 | feat | {message} | {file list or pattern} | +{N}/-{N} |
| 2 | fix | {message} | {file list or pattern} | +{N}/-{N} |
| 3 | refactor | {message} | {file list or pattern} | +{N}/-{N} |

**Order**: {explanation of commit order — dependencies first, features before tests, etc.}

Proceed? You can adjust grouping, merge, or split any items.
```

**GATE**: Wait for user approval or adjustments.

---

## Phase 4: EXECUTE — Create Each Commit

For each approved commit group:

1. **Reset staging area** (if needed):
   ```bash
   git reset HEAD
   ```

2. **Stage only the files for this commit**:
   ```bash
   git add {specific files}
   ```

3. **Verify staging is correct**:
   ```bash
   git diff --cached --name-only
   ```

4. **Commit** with conventional message:
   ```bash
   git commit -m "{type}: {description}"
   ```

5. **Confirm** before moving to next group

Repeat for each commit group in order.

---

## Phase 5: SUMMARIZE

```markdown
## Batch Commit Complete

**Commits created**: {N}

| # | Hash | Message | Files |
|---|------|---------|-------|
| 1 | {short-hash} | {type}: {message} | {N} files |
| 2 | {short-hash} | {type}: {message} | {N} files |
| 3 | {short-hash} | {type}: {message} | {N} files |

**Total**: {files} files changed, {insertions} insertions, {deletions} deletions

Next: `git push` or `/prp-pr`
```

---

## Examples

```
/prp-commit-batch                    # Auto-detect logical groups
/prp-commit-batch by-type            # Group by conventional commit type
/prp-commit-batch by-directory       # Group by directory
/prp-commit-batch by-feature         # Group by feature domain
/prp-commit-batch atomic             # One commit per file
```

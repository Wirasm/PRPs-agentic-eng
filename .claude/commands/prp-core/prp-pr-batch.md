---
description: Create PRs for multiple feature branches at once
argument-hint: [base-branch] (default: main)
---

# Batch PR Creator

**Base branch**: $ARGUMENTS (default: main)

---

## Your Mission

Identify all branches with unpushed/un-PR'd work, then create a PR for each using the `/prp-pr` workflow.

---

## Phase 1: DISCOVER — Find Branches Needing PRs

```bash
# List all local branches except main/master
git branch --list | grep -v -E '^\*?\s*(main|master)$'

# For each branch, check if it has a PR already
for branch in $(git branch --list --format='%(refname:short)' | grep -v -E '^(main|master)$'); do
  echo "=== $branch ==="
  # Check commits ahead of base
  git log origin/${base:-main}..$branch --oneline 2>/dev/null | head -5
  # Check for existing PR
  gh pr list --head "$branch" --json number,url --jq '.[0].url // "no PR"' 2>/dev/null
done
```

Filter to branches that:
- Have commits ahead of base branch
- Do NOT already have an open PR

---

## Phase 2: PROPOSE — Present PR Plan

```markdown
## Batch PR Plan

**Base branch**: {base}

I found **{N}** branches ready for PRs:

| # | Branch | Commits | Summary | Existing PR? |
|---|--------|---------|---------|--------------|
| 1 | {branch} | {N} commits | {1-line summary from commits} | None |
| 2 | {branch} | {N} commits | {1-line summary from commits} | None |
| 3 | {branch} | {N} commits | {1-line summary from commits} | None |

**Skipped** (already have PRs):
{List of branches with existing PRs, or "None"}

Proceed with creating PRs for all {N} branches?
```

**GATE**: Wait for user approval. User can exclude specific branches.

---

## Phase 3: CREATE — Generate Each PR

For each approved branch:

1. **Switch to the branch**:
   ```bash
   git checkout {branch}
   ```

2. **Invoke the `/prp-pr` workflow**:
   - Follow ALL phases of `/prp-pr` (Validate → Discover template → Analyze → Push → Create)
   - Pass the base branch argument
   - Let it handle template detection, commit analysis, and PR creation

3. **Record the PR URL** for the summary

4. **Brief confirmation** before moving to next branch

### Cross-PR Awareness

When creating multiple PRs:
- Note related PRs in each PR body (e.g., "Related: #123, #124")
- If branches have dependency ordering, mention it in PR descriptions
- Use consistent labeling if the project uses labels

---

## Phase 4: SUMMARIZE

```markdown
## Batch PR Creation Complete

**PRs Created**: {N}

| # | Branch | PR | Title | Status |
|---|--------|----|-------|--------|
| 1 | {branch} | #{number} | {title} | Created |
| 2 | {branch} | #{number} | {title} | Created |
| 3 | {branch} | #{number} | {title} | Created |

### Review Order

{Suggested review/merge order based on dependencies, or "Any order — all independent"}

### Next Steps

- Review PRs: `/prp-review {pr-number}`
- Multi-agent review: `/prp-review-agents {pr-number}`
```

---

## Phase 5: RESTORE — Return to Original Branch

```bash
git checkout {original-branch}
```

---

## Examples

```
/prp-pr-batch                # PRs for all branches, base = main
/prp-pr-batch develop        # PRs for all branches, base = develop
```

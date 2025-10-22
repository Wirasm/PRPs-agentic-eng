# Create PR for PRP Implementation

Create a pull request for completed PRP implementation with validation, proper commit, and comprehensive PR description.

## PR Title (if provided)
$ARGUMENTS

## Workflow

This command handles the complete flow from validation through PR creation for PRP-based implementations.

### Phase 1: Pre-Commit Validation

**Run Project Validation:**

```bash
# Level 1: Syntax & Style
uv run ruff check --fix
uv run mypy .

# Level 2: Unit Tests (if applicable)
uv run pytest tests/ -v
```

**Stop if validation fails.** Report failures and exit.

### Phase 2: Review Changes

**Analyze Current State:**

```bash
# Check current branch
git branch --show-current

# If on main/development, stop and warn user to create feature branch first

# Review what will be committed
git status
git diff HEAD

# Review all commits in feature branch
git log main..HEAD --oneline
```

### Phase 3: Create Commit (if needed)

**Only if there are uncommitted changes:**

- Stage all changes: `git add -A`
- Create atomic commit following conventional commits
- Use format: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **NEVER** mention Claude Code, Anthropic, AI, or co-authorship
- Keep subject line ≤50 characters, lowercase, no period
- Present tense verbs (add, fix, update)

**Example Commit Messages:**
- `feat: add user authentication with JWT tokens`
- `fix: resolve race condition in async task handler`
- `refactor: simplify database query logic`
- `test: add integration tests for api endpoints`

### Phase 4: Push to Remote

**Push Changes:**

```bash
# Push current branch to remote with tracking
git push -u origin HEAD
```

### Phase 5: Create Pull Request

**Generate PR Description:**

Analyze all commits and changes in the branch since diverging from main:

```bash
# Get full context of changes
git diff main...HEAD

# Review commit history
git log main..HEAD
```

**Create PR with gh CLI:**

```bash
gh pr create --title "$ARGUMENTS" --body "$(cat <<'EOF'
## Summary

[Concise 2-3 sentence overview of what this PR accomplishes and why]

## Implementation Details

### Key Changes

- [Specific change with file references]
- [Another specific change]
- [Additional changes]

### Architecture/Design Decisions

[If applicable: explain significant architectural choices, trade-offs, or patterns used]

## Type of Change

- [ ] New feature (non-breaking change adding functionality)
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Refactoring (code restructuring without behavior change)
- [ ] Documentation update
- [ ] Configuration/infrastructure change

## Testing

### Validation Completed

- [x] Syntax & style checks pass (`ruff check`, `mypy`)
- [x] Unit tests pass (if applicable)
- [x] Integration tests pass (if applicable)
- [x] Manual testing completed

### Test Coverage

[Describe what was tested and how]

### Edge Cases Considered

[List any edge cases that were specifically handled or tested]

## Validation Commands

Commands executed to verify implementation:

```bash
# Run these to validate the changes
uv run ruff check --fix
uv run mypy .
uv run pytest tests/ -v  # if applicable
```

## Checklist

- [ ] Code follows project style and conventions
- [ ] Self-reviewed the changes
- [ ] Updated documentation (if needed)
- [ ] All validation commands pass
- [ ] No debug code or console logs
- [ ] Backward compatibility maintained (or breaking changes documented)
- [ ] Performance implications considered

## Related Context

**PRP Reference:** [If executed from PRP, reference the PRP file]

**Related Issues:** [Link any related GitHub issues]

**Dependencies:** [Note any dependency changes or requirements]

## Reviewer Notes

[Any specific areas you want reviewers to focus on or context they should have]

EOF
)"
```

### Phase 6: Post-Creation Actions

**Add Metadata:**

```bash
# Add appropriate labels
gh pr edit --add-label "prp-implementation,needs-review"

# Add additional labels based on change type
# Examples: "feature", "bugfix", "breaking-change", "documentation"

# Request reviewers (if known)
# gh pr edit --add-reviewer username
```

**Report PR URL:**

```bash
# Get PR URL
gh pr view --web
```

## Success Criteria

- ✅ All validation commands pass before commit
- ✅ Changes committed with proper conventional commit format
- ✅ Branch pushed to remote successfully
- ✅ PR created with comprehensive description
- ✅ PR includes validation commands and testing details
- ✅ Labels and metadata applied appropriately
- ✅ PR URL returned for user review

## Important Notes

**Branch Requirements:**
- Must be on feature branch (not main/development)
- Branch should have meaningful name related to feature

**Commit Requirements:**
- No references to AI, Claude, Anthropic, or similar
- Follow conventional commit format strictly
- Keep commits atomic and focused

**PR Requirements:**
- Comprehensive description with all sections filled
- Include validation commands that reviewers can run
- Reference related PRPs, issues, or documentation
- Explain architectural decisions if significant

**Validation First:**
- ALWAYS run validation before committing
- Stop immediately if validation fails
- Fix issues before proceeding

## Error Handling

**If validation fails:**
1. Report specific failures with file/line numbers
2. Stop process - do not create commit or PR
3. Prompt user to fix issues first

**If on wrong branch:**
1. Warn user they're on main/development
2. Stop process
3. Suggest creating feature branch first

**If no changes to commit:**
1. Check if already committed
2. If yes, skip to push/PR creation
3. If no changes at all, report and exit

## Output Format

Provide clear step-by-step report:

1. ✅ Validation results (all checks passed)
2. ✅ Commit created: `<commit hash>` - "<commit message>"
3. ✅ Branch pushed: `<branch-name>`
4. ✅ PR created: `<PR number>` - "<PR title>"
5. 🔗 PR URL: `<github-url>`

---

Remember: This is the final step in PRP execution. Ensure all implementation is complete and validated before running this command.

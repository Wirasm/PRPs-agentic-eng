---
description: Comprehensive PR review using specialized agents - comments, tests, errors, types, code quality, docs, and simplification
argument-hint: "<pr-number> [aspects: comments|tests|errors|types|code|docs|simplify|all]"
---

# Comprehensive PR Review with Specialized Agents

Run a multi-agent review on a pull request, with each agent focusing on a specific aspect of code quality.

**Target**: $ARGUMENTS

## Pre-Review Setup

Before running reviews:

1. **Identify the PR**
   - If PR number provided: `gh pr view <number>`
   - If no number: `gh pr view` (current branch's PR)
   - Get PR branch name and changed files

2. **Check PR State**
   - Is rebase needed? Check if behind base branch
   - Are there conflicts? Resolve intelligently if needed
   - Never push to main without explicit user approval

3. **Get Changed Files**
   ```bash
   gh pr diff <number> --name-only
   ```

## Review Aspects

| Aspect | Agent | When to Run |
|--------|-------|-------------|
| `code` | code-reviewer | Always - general quality and guidelines |
| `docs` | docs-impact-agent | Almost always - updates stale docs |
| `tests` | pr-test-analyzer | When test files or tested code changed |
| `comments` | comment-analyzer | When comments/docstrings added |
| `errors` | silent-failure-hunter | When error handling changed |
| `types` | type-design-analyzer | When types added/modified |
| `simplify` | code-simplifier | After passing review - polish |
| `all` | All applicable | Default if no aspects specified |

## Aspect Selection Logic

**Always run**:
- `code-reviewer` - Core quality check

**Almost always run** (skip only for trivial PRs):
- `docs-impact-agent` - Updates project docs

**Skip docs-impact-agent only when**:
- Typo-only fixes (comments, strings)
- Test-only changes (no production code)
- Documentation-only changes
- Config tweaks (CI, linting)

**Run based on changes**:
- Test files changed → `pr-test-analyzer`
- Comments/docstrings added → `comment-analyzer`
- Try-catch or error handling → `silent-failure-hunter`
- New types or type modifications → `type-design-analyzer`

**Run last**:
- `code-simplifier` - After other reviews pass

## Execution

### Sequential (Default)

Run agents one at a time for clear, actionable feedback:

1. `code-reviewer` - Guidelines and bugs
2. `docs-impact-agent` - Fix stale docs (commits to PR branch)
3. Applicable specialist agents based on changes
4. `code-simplifier` - Final polish (if requested or all reviews pass)

### Parallel (When Requested)

If user specifies "parallel", launch all applicable agents simultaneously using multiple Task tool calls in one message.

## Agent Instructions

When launching each agent via Task tool:

**code-reviewer**:
> Review PR #<number> for project guideline compliance, bugs, and quality issues. Focus on the diff. Report only high-confidence issues (80+).

**docs-impact-agent**:
> Review PR #<number> and update any documentation that's affected by these changes. Fix stale docs in CLAUDE.md, README.md, and docs/. If you make updates, commit and push them to the PR branch `<branch-name>`.

**pr-test-analyzer**:
> Analyze test coverage for PR #<number>. Focus on behavioral coverage, identify critical gaps, rate recommendations by criticality.

**comment-analyzer**:
> Analyze code comments in PR #<number> for accuracy, completeness, and long-term value. Verify comments match actual code behavior.

**silent-failure-hunter**:
> Hunt for silent failures in PR #<number>. Check all error handling for proper logging, user feedback, and specific catch blocks.

**type-design-analyzer**:
> Analyze type design in PR #<number>. Rate encapsulation, invariant expression, usefulness, and enforcement. Focus on new or modified types.

**code-simplifier**:
> Simplify code in PR #<number> for clarity while preserving functionality. No nested ternaries, prefer explicit over clever. Commit and push improvements to PR branch `<branch-name>`.

## Result Aggregation

After all agents complete, aggregate findings:

### Categories

| Category | Description | Action |
|----------|-------------|--------|
| **Critical** | Must fix before merge | Block merge |
| **Important** | Should fix | Address before merge |
| **Suggestions** | Nice to have | Consider |
| **Strengths** | What's good | Acknowledge |

### Summary Format

```markdown
## PR Review Summary

### Critical Issues (X found)
| Agent | Issue | Location |
|-------|-------|----------|
| code-reviewer | Description | `file.ts:line` |

### Important Issues (X found)
| Agent | Issue | Location |
|-------|-------|----------|
| silent-failure-hunter | Description | `file.ts:line` |

### Suggestions (X found)
| Agent | Suggestion | Location |
|-------|------------|----------|
| type-design-analyzer | Description | `file.ts:line` |

### Strengths
- Well-structured error handling
- Good test coverage for critical paths

### Documentation Updates
- `CLAUDE.md` - Added new command reference
- `README.md` - Updated configuration section

### Verdict
[READY TO MERGE / NEEDS FIXES / CRITICAL ISSUES]

### Recommended Actions
1. Fix critical issues first
2. Address important issues
3. Consider suggestions
4. Re-run review after fixes
```

## Post to GitHub

**Always post the summary to the PR when a PR number is provided**:

```bash
gh pr comment <PR_NUMBER> --body "<summary>"
```

## Usage Examples

```bash
# Full review of specific PR
/prp-review-agents 163

# Review only specific aspects
/prp-review-agents 163 tests errors

# Review current branch's PR
/prp-review-agents

# Only code and docs review
/prp-review-agents 42 code docs

# All reviews in parallel
/prp-review-agents 42 all parallel

# Just simplify after passing review
/prp-review-agents 42 simplify
```

## Workflow Integration

**Before creating PR**:
1. Run `/prp-review-agents` on current branch
2. Fix critical and important issues
3. Re-run to verify
4. Create PR

**During PR review**:
1. Run `/prp-review-agents <pr-number>`
2. Review posts summary to GitHub
3. Address feedback
4. Re-run targeted aspects

**After making changes**:
1. Run specific aspects: `/prp-review-agents <pr-number> tests code`
2. Verify issues resolved
3. Push updates

## Notes

- Agents analyze git diff by default (changed files only)
- Each agent returns detailed report with file:line references
- docs-impact-agent commits and pushes doc updates to PR branch
- code-simplifier commits and pushes improvements to PR branch
- Summary always posted as PR comment when PR number provided

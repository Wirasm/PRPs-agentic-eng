---
description: "Execute a feature PRP until fully complete"
---

# Execute Feature PRP

## PRP File: $ARGUMENTS

## Instructions

- Ingest the PRP file completely
- Think hard about the implementation approach
- Execute every task in the STEP-BY-STEP TASKS section sequentially
- Validate after each task using the task's validation command
- If validation fails, fix and re-validate before proceeding
- Run full validation suite from the PRP when all tasks complete
- **Critical**: Don't stop until the entire plan is fulfilled and all validation passes
- Use TodoWrite to track progress through tasks
- Trust the PRP's strategic direction, but verify tactical details (imports, paths, names)
- If the PRP has errors in details, fix them and note in report

## Success Criteria

- ✓ Every task completed
- ✓ All validation commands pass
- ✓ Acceptance criteria met

## Completion

Once all validation passes:

```bash
mkdir -p .claude/PRPs/features/completed
mv .claude/PRPs/features/{prp-file}.md .claude/PRPs/features/completed/
```

## Report

After completion:

**Summary:**
- Feature: {name}
- Tasks completed: {count}
- Files created/modified: {list}

**Validation:**
```bash
✓ Linting: Passed
✓ Type checking: Passed
✓ Tests: X/X passed
```

**Adjustments** (if any):
- Note any PRP details that were incorrect and how you fixed them

**Files Changed:**
```bash
git diff --stat
```

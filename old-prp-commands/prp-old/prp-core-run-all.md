---
description: Run all prp core commands in sequence from feature request to pr
---

Feature: $ARGUMENTS

## Instructions

Execute in sequence:
1. `/prp-core-new-branch $ARGUMENTS`
2. `/prp-core-create $ARGUMENTS`
3. `/prp-core-execute` (use PRP from step 2)
4. `/prp-core-commit`
5. `/prp-core-pr` (generate title from feature)

Stop if any fails.

## Report

Output summary of completed workflow including:
- Branch name created
- PRP file path
- Commit hash
- PR URL

name: "Bun PRP Template - Context-Rich with Validation Loops"
description: |

## Purpose

Template optimized for AI agents to implement Bun features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

## Core Principles

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal

[What needs to be built - be specific about the end state and desires]

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)

```yaml
# MUST READ - Include these in your context window
- url: [Official Bun docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example.ts]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Library documentation URL]
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [prp/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash

```

### Desired Codebase tree with files to be added and responsibility of file

```bash

```

### Known Gotchas of our codebase & Library Quirks

```typescript
// CRITICAL: [Library name] requires [specific setup]
// Example: Bun's native HTTP server has different API than Node.js
// Example: Bun's built-in SQLite differs from node-sqlite3
// Example: We use Bun 1.0+ native APIs and TypeScript strict mode
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```typescript
Examples:
 - TypeScript interfaces/types
 - Zod schemas for validation
 - Database schema types
 - API response types
 - Component prop types

```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.ts:
  - FIND pattern: "export class OldImplementation"
  - INJECT after line containing "constructor"
  - PRESERVE existing method signatures

CREATE src/new_feature.ts:
  - MIRROR pattern from: src/similar_feature.ts
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

### Per task pseudocode as needed added to each task

```typescript

// Task 1
// Pseudocode with CRITICAL details don't write entire code
export async function newFeature(param: string): Promise<Response> {
    // PATTERN: Always validate input first (see src/validators.ts)
    const validated = validateInput(param);  // throws ValidationError

    // GOTCHA: Bun's native fetch is different from Node.js
    const response = await fetch('https://api.example.com', {
        method: 'POST',
        body: JSON.stringify({ data: validated }),
        headers: { 'Content-Type': 'application/json' }
    });
    
    // PATTERN: Use existing retry mechanism
    const result = await retryWithBackoff(3, async () => {
        // CRITICAL: API returns 429 if >10 req/sec
        await rateLimiter.acquire();
        return await response.json();
    });

    // PATTERN: Standardized response format
    return formatResponse(result);  // see src/utils/responses.ts
}
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - client: "Use Bun's native SQLite or external DB client"

CONFIG:
  - add to: src/config.ts
  - pattern: "export const FEATURE_TIMEOUT = Number(Bun.env.FEATURE_TIMEOUT) || 30000"

ROUTES:
  - add to: src/server.ts
  - pattern: "Bun.serve({ fetch: router, port: 3000 })"
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
bun run lint                        # ESLint checks
bun run typecheck                   # TypeScript type checking
bun run format                      # Prettier formatting

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns

```typescript
// CREATE src/__tests__/new_feature.test.ts with these test cases:
import { describe, it, expect, beforeEach } from "bun:test";
import { newFeature } from "../new_feature";

describe("newFeature", () => {
  it("should return success for valid input", async () => {
    const result = await newFeature("valid_input");
    expect(result.status).toBe("success");
  });

  it("should throw validation error for invalid input", async () => {
    expect(async () => {
      await newFeature("");
    }).toThrow();
  });

  it("should handle external API timeout gracefully", async () => {
    // Mock external API to timeout
    const result = await newFeature("valid");
    expect(result.status).toBe("error");
    expect(result.message).toContain("timeout");
  });
});
```

```bash
# Run and iterate until passing:
bun test src/__tests__/new_feature.test.ts
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test

```bash
# Start the dev server
bun run dev

# Test the endpoint
curl -X POST http://localhost:3000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check Bun console for error messages
```

### Level 4: Deployment & Creative Validation

```bash
# Production build check
bun run build

# Expected: Successful build with no errors
# Common issues:
# - Import/export errors → Check module resolution
# - Type errors → Run bun run typecheck
# - Runtime errors → Check Bun-specific APIs

# Test production build
bun run start

# Performance validation
bun run benchmark                   # If available
bun --hot src/server.ts            # Hot reload testing

# Custom validation specific to the feature
# [Add creative validation methods here]
```

## Final validation Checklist

- [ ] All tests pass: `bun test`
- [ ] No linting errors: `bun run lint`
- [ ] No type errors: `bun run typecheck`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't mix Bun APIs with Node.js APIs unnecessarily
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
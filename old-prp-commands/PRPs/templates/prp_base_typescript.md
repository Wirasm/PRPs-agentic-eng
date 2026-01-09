name: "TypeScript PRP Template v3 - Implementation-Focused with Precision Standards"
description: |

---

## Goal

**Feature Goal**: [Specific, measurable end state of what needs to be built]

**Deliverable**: [Concrete artifact - React component, API route, integration, etc.]

**Success Definition**: [How you'll know this is complete and working]

## User Persona (if applicable)

**Target User**: [Specific user type - developer, end user, admin, etc.]

**Use Case**: [Primary scenario when this feature will be used]

**User Journey**: [Step-by-step flow of how user interacts with this feature]

**Pain Points Addressed**: [Specific user frustrations this feature solves]

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] [Specific measurable outcomes]

## All Needed Context

### Context Completeness Check

_Before writing this PRP, validate: "If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: [Complete URL with section anchor]
  why: [Specific methods/concepts needed for implementation]
  critical: [Key insights that prevent common implementation errors]

- file: [exact/path/to/pattern/file.tsx]
  why: [Specific pattern to follow - component structure, hook usage, etc.]
  pattern: [Brief description of what pattern to extract]
  gotcha: [Known constraints or limitations to avoid]

- docfile: [PRPs/ai_docs/typescript_specific.md]
  why: [Custom documentation for complex TypeScript/Next.js patterns]
  section: [Specific section if document is large]
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
// Example: Next.js 15 App Router - Route handlers must export named functions
// Example: 'use client' directive must be at top of file, affects entire component tree
// Example: Server Components can't use browser APIs or event handlers
// Example: We use TypeScript strict mode and require proper typing
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```typescript
Examples:
 - Zod schemas for validation
 - TypeScript interfaces/types
 - Database schema types
 - API response types
 - Component prop types

```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE lib/types/{domain}.types.ts
  - IMPLEMENT: TypeScript interfaces and types for domain models
  - FOLLOW pattern: lib/types/existing.types.ts (interface structure, export patterns)
  - NAMING: PascalCase for interfaces, camelCase for properties
  - PLACEMENT: Type definitions in lib/types/

Task 2: CREATE components/{domain}/{ComponentName}.tsx
  - IMPLEMENT: React component with proper TypeScript props interface
  - FOLLOW pattern: components/existing/ExistingComponent.tsx (component structure, props typing)
  - NAMING: PascalCase for components, camelCase for props, kebab-case for CSS classes
  - DEPENDENCIES: Import types from Task 1
  - PLACEMENT: Component layer in components/{domain}/

Task 3: CREATE app/api/{resource}/route.ts
  - IMPLEMENT: Next.js API route handlers (GET, POST, etc.)
  - FOLLOW pattern: app/api/existing/route.ts (request/response handling, error patterns)
  - NAMING: Named exports (GET, POST, PUT, DELETE), proper TypeScript typing
  - DEPENDENCIES: Import types and components from previous tasks
  - PLACEMENT: API routes in app/api/{resource}/

Task 4: CREATE app/{feature}/page.tsx
  - IMPLEMENT: Next.js page component using domain components
  - FOLLOW pattern: app/existing-page/page.tsx (page structure, metadata, error boundaries)
  - NAMING: Default export, proper metadata export, TypeScript page props
  - DEPENDENCIES: Import components from Task 2, types from Task 1
  - PLACEMENT: Page routes in app/{feature}/

Task 5: CREATE hooks/use{DomainAction}.ts
  - IMPLEMENT: Custom React hooks for state management and API calls
  - FOLLOW pattern: hooks/useExisting.ts (hook structure, TypeScript generics, error handling)
  - NAMING: use{ActionName} with proper TypeScript return types
  - DEPENDENCIES: Import types from Task 1, API endpoints from Task 3
  - PLACEMENT: Custom hooks in hooks/

Task 6: CREATE __tests__/{component}.test.tsx
  - IMPLEMENT: Jest/Testing Library tests for components and hooks
  - FOLLOW pattern: __tests__/existing.test.tsx (test structure, mocking patterns)
  - NAMING: describe blocks, test naming conventions, TypeScript test typing
  - COVERAGE: All components and hooks with positive and negative test cases
  - PLACEMENT: Tests alongside the code they test
```

### Implementation Patterns & Key Details

```typescript
// Show critical patterns and gotchas - keep concise, focus on non-obvious details

// Example: Component pattern
interface {Domain}Props {
  // PATTERN: Strict TypeScript interfaces (follow lib/types/existing.types.ts)
  data: {Domain}Data;
  onAction?: (id: string) => void;
}

export function {Domain}Component({ data, onAction }: {Domain}Props) {
  // PATTERN: Client/Server component patterns (check existing components)
  // GOTCHA: 'use client' needed for event handlers, useState, useEffect
  // CRITICAL: Server Components for data fetching, Client Components for interactivity

  return (
    // PATTERN: Consistent styling approach (see components/ui/)
    <div className="existing-class-pattern">
      {/* Follow existing component composition patterns */}
    </div>
  );
}

// Example: API route pattern
export async function GET(request: Request): Promise<Response> {
  // PATTERN: Request validation and error handling (see app/api/existing/route.ts)
  // GOTCHA: [TypeScript-specific constraint or Next.js requirement]
  // RETURN: Response object with proper TypeScript typing
}

// Example: Custom hook pattern
export function use{Domain}Action(): {Domain}ActionResult {
  // PATTERN: Hook structure with TypeScript generics (see hooks/useExisting.ts)
  // GOTCHA: [React hook rules and TypeScript typing requirements]
}
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add table 'feature_data' with proper indexes"
  - client: "@/lib/database/client"
  - pattern: "createClient() for client components, createServerClient() for server components"

CONFIG:
  - add to: .env.local
  - pattern: "NEXT_PUBLIC_* for client-side env vars"
  - pattern: "FEATURE_TIMEOUT = process.env.FEATURE_TIMEOUT || '30000'"

ROUTES:
  - file structure: app/feature-name/page.tsx
  - api routes: app/api/feature-name/route.ts
  - middleware: middleware.ts (root level)
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation - fix before proceeding
npm run lint                    # ESLint checks with TypeScript rules
npx tsc --noEmit               # TypeScript type checking (no JS output)
npm run format                 # Prettier formatting

# Project-wide validation
npm run lint:fix               # Auto-fix linting issues
npm run type-check             # Full TypeScript validation

# Expected: Zero errors. If errors exist, READ output and fix before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component/hook as it's created
npm test -- __tests__/{domain}.test.tsx
npm test -- __tests__/use{Hook}.test.ts

# Full test suite for affected areas
npm test -- components/{domain}/
npm test -- hooks/

# Coverage validation (if available)
npm test -- --coverage --watchAll=false

# Expected: All tests pass. If failing, debug root cause and fix implementation.
```

### Level 3: Integration Testing (System Validation)

```bash
# Development server validation
npm run dev &
sleep 5  # Allow Next.js startup time

# Page load validation
curl -I http://localhost:3000/{feature-page}
# Expected: 200 OK response

# API endpoint validation
curl -X POST http://localhost:3000/api/{resource} \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}' \
  | jq .  # Pretty print JSON response

# Production build validation
npm run build
# Expected: Successful build with no TypeScript errors or warnings

# Component rendering validation (if SSR/SSG)
curl http://localhost:3000/{page} | grep -q "expected-content"

# Expected: All integrations working, proper responses, no hydration errors
```

### Level 4: Creative & Domain-Specific Validation

```bash
# TypeScript/Next.js Specific Validation:

# Production build performance
npm run build && npm run analyze  # Bundle analyzer if available

# Type safety validation
npx tsc --noEmit --strict        # Strict TypeScript checking

# Next.js specific checks
npm run lint:next                # Next.js linting rules if available

# MCP Server Validation Examples:
# Playwright MCP (for E2E testing)
playwright-mcp --test-user-flows --browser chromium

# Performance MCP (for Lighthouse audits)
lighthouse-mcp --url http://localhost:3000 --audit performance

# Accessibility MCP (for a11y testing)
axe-mcp --scan http://localhost:3000/{pages}

# Custom TypeScript/React Validation
# React Testing Library integration tests
# Storybook visual regression tests (if available)
# TypeScript strict mode compliance

# Expected: All creative validations pass, performance/accessibility standards met
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `npm test`
- [ ] No linting errors: `npm run lint`
- [ ] No type errors: `npx tsc --noEmit`
- [ ] No formatting issues: `npm run format --check`
- [ ] Production build succeeds: `npm run build`

### Feature Validation

- [ ] All success criteria from "What" section met
- [ ] Manual testing successful: [specific commands from Level 3]
- [ ] Error cases handled gracefully with proper TypeScript error types
- [ ] Integration points work as specified
- [ ] User persona requirements satisfied (if applicable)

### Code Quality Validation

- [ ] Follows existing TypeScript/React patterns and naming conventions
- [ ] File placement matches desired codebase tree structure
- [ ] Anti-patterns avoided (check against Anti-Patterns section)
- [ ] Dependencies properly managed with correct TypeScript typings
- [ ] Configuration changes properly integrated

### TypeScript/Next.js Specific

- [ ] Proper TypeScript interfaces and types defined
- [ ] Server/Client component patterns followed correctly
- [ ] 'use client' directives used appropriately
- [ ] API routes follow Next.js App Router patterns
- [ ] No hydration mismatches between server/client rendering

### Documentation & Deployment

- [ ] Code is self-documenting with clear TypeScript types
- [ ] Props interfaces properly documented
- [ ] Environment variables documented if new ones added

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use 'use client' unnecessarily - embrace Server Components
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific

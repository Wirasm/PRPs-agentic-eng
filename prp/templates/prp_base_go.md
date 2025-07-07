name: "Go PRP Template - Context-Rich with Validation Loops"
description: |

## Purpose

Template optimized for AI agents to implement Go features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

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
- url: [Official Go docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example.go]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Package documentation URL]
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

```go
// CRITICAL: [Package name] requires [specific setup]
// Example: gorilla/mux requires explicit route handling setup
// Example: database/sql requires proper connection pooling
// Example: We use Go 1.21+ and context.Context patterns
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```go
Examples:
 - struct definitions
 - interface declarations
 - custom error types
 - validation functions

```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY internal/existing/module.go:
  - FIND pattern: "type OldImplementation struct"
  - INJECT after line containing "func NewOldImplementation"
  - PRESERVE existing method signatures

CREATE internal/feature/new_feature.go:
  - MIRROR pattern from: internal/similar/feature.go
  - MODIFY struct name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

### Per task pseudocode as needed added to each task

```go

// Task 1
// Pseudocode with CRITICAL details don't write entire code
func NewFeature(ctx context.Context, param string) (*Response, error) {
    // PATTERN: Always validate input first (see internal/validators/validate.go)
    if err := validateInput(param); err != nil {
        return nil, fmt.Errorf("validation failed: %w", err)
    }

    // GOTCHA: This package requires connection pooling
    db, err := getConnectionPool(ctx)  // see internal/db/pool.go
    if err != nil {
        return nil, fmt.Errorf("db connection failed: %w", err)
    }
    
    // PATTERN: Use existing retry mechanism
    result, err := retryWithBackoff(ctx, 3, func() (*ExternalResult, error) {
        // CRITICAL: API returns 429 if >10 req/sec
        if err := rateLimiter.Wait(ctx); err != nil {
            return nil, err
        }
        return externalAPI.Call(ctx, param)
    })
    if err != nil {
        return nil, fmt.Errorf("external call failed: %w", err)
    }

    // PATTERN: Standardized response format
    return formatResponse(result), nil  // see internal/utils/responses.go
}
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - schema: "Update models/schema.go with new fields"

CONFIG:
  - add to: internal/config/config.go
  - pattern: "FeatureTimeout time.Duration `env:'FEATURE_TIMEOUT' envDefault:'30s'`"

ROUTES:
  - add to: internal/handlers/routes.go
  - pattern: "r.HandleFunc('/feature', featureHandler).Methods('POST')"
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
go fmt ./...                        # Format code
go vet ./...                        # Static analysis
golangci-lint run                   # Comprehensive linting

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns

```go
// CREATE internal/feature/new_feature_test.go with these test cases:
func TestNewFeature_HappyPath(t *testing.T) {
    ctx := context.Background()
    
    result, err := NewFeature(ctx, "valid_input")
    
    assert.NoError(t, err)
    assert.NotNil(t, result)
    assert.Equal(t, "success", result.Status)
}

func TestNewFeature_ValidationError(t *testing.T) {
    ctx := context.Background()
    
    result, err := NewFeature(ctx, "")
    
    assert.Error(t, err)
    assert.Nil(t, result)
    assert.Contains(t, err.Error(), "validation failed")
}

func TestNewFeature_ExternalAPITimeout(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Millisecond)
    defer cancel()
    
    result, err := NewFeature(ctx, "valid")
    
    assert.Error(t, err)
    assert.Nil(t, result)
}
```

```bash
# Run and iterate until passing:
go test ./internal/feature -v
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test

```bash
# Start the service
go run cmd/server/main.go

# Test the endpoint
curl -X POST http://localhost:8080/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs for stack trace
```

### Level 4: Deployment & Creative Validation

```bash
# Performance and security validation
go test -bench=. ./...              # Run benchmarks
go test -race ./...                 # Race condition detection
gosec ./...                         # Security audit

# Build validation
go build -o bin/server cmd/server/main.go

# Custom validation specific to the feature
# [Add creative validation methods here]
```

## Final validation Checklist

- [ ] All tests pass: `go test ./...`
- [ ] No linting errors: `golangci-lint run`
- [ ] No race conditions: `go test -race ./...`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't ignore context.Context - always pass it through
- ❌ Don't forget to handle errors - Go requires explicit error handling
- ❌ Don't use global variables - pass dependencies explicitly
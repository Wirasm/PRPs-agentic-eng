name: "Rust PRP Template - Context-Rich with Validation Loops"
description: |

## Purpose

Template optimized for AI agents to implement Rust features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

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
- url: [Official Rust docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example.rs]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Crate documentation URL]
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

```rust
// CRITICAL: [Crate name] requires [specific setup]
// Example: tokio requires async runtime for async functions
// Example: serde requires derive feature for automatic serialization
// Example: We use tokio 1.0 and async/await patterns
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```rust
Examples:
 - struct definitions
 - enum variants
 - trait implementations
 - error types

```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.rs:
  - FIND pattern: "struct OldImplementation"
  - INJECT after line containing "impl Default"
  - PRESERVE existing method signatures

CREATE src/new_feature.rs:
  - MIRROR pattern from: src/similar_feature.rs
  - MODIFY struct name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

### Per task pseudocode as needed added to each task

```rust

// Task 1
// Pseudocode with CRITICAL details don't write entire code
pub async fn new_feature(param: String) -> Result<Response, FeatureError> {
    // PATTERN: Always validate input first (see src/validators.rs)
    let validated = validate_input(&param)?;  // returns FeatureError

    // GOTCHA: This crate requires connection pooling
    let pool = get_connection_pool().await?;  // see src/db/pool.rs
    
    // PATTERN: Use existing retry mechanism
    retry_with_backoff(3, || async {
        // CRITICAL: API returns 429 if >10 req/sec
        rate_limiter.acquire().await?;
        external_api::call(&validated).await
    }).await?;

    // PATTERN: Standardized response format
    Ok(format_response(result))  // see src/utils/responses.rs
}
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - schema: "Update schema.rs with new fields"

CONFIG:
  - add to: src/config.rs
  - pattern: "feature_timeout: u64 = env::var('FEATURE_TIMEOUT').unwrap_or(30)"

ROUTES:
  - add to: src/routes.rs
  - pattern: "router.route('/feature', post(feature_handler))"
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
cargo fmt                           # Format code
cargo clippy -- -D warnings         # Linting with strict warnings

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns

```rust
// CREATE tests/new_feature_test.rs with these test cases:
#[tokio::test]
async fn test_happy_path() {
    // Basic functionality works
    let result = new_feature("valid_input".to_string()).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_validation_error() {
    // Invalid input returns error
    let result = new_feature("".to_string()).await;
    assert!(result.is_err());
    assert!(matches!(result.unwrap_err(), FeatureError::Validation(_)));
}

#[tokio::test]
async fn test_external_api_timeout() {
    // Handles timeouts gracefully
    // Mock external API to return timeout
    let result = new_feature("valid".to_string()).await;
    assert!(result.is_err());
}
```

```bash
# Run and iterate until passing:
cargo test new_feature -- --nocapture
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test

```bash
# Start the service
cargo run --bin server -- --dev

# Test the endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs for stack trace
```

### Level 4: Deployment & Creative Validation

```bash
# Performance and safety validation
cargo bench                         # Run benchmarks
cargo audit                         # Security audit
cargo check --release               # Release build check

# Custom validation specific to the feature
# [Add creative validation methods here]
```

## Final validation Checklist

- [ ] All tests pass: `cargo test`
- [ ] No linting errors: `cargo clippy -- -D warnings`
- [ ] No format issues: `cargo fmt --check`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use unwrap() in production code - handle errors properly
- ❌ Don't clone unnecessarily - use references when possible
- ❌ Don't ignore compiler warnings - they often indicate real issues
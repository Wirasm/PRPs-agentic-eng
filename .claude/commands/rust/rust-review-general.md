# Rust Code Review

## Target: $ARGUMENTS

Perform comprehensive Rust code review focusing on safety, performance, and maintainability.

## Review Areas

### 1. Memory Safety & Ownership
- Check borrow checker compliance
- Verify proper lifetime annotations
- Review reference usage patterns
- Ensure no memory leaks or unsafe blocks

### 2. Error Handling
- Verify proper use of Result<T, E> types
- Check error propagation with `?` operator
- Review custom error types and implementations
- Ensure no unwrap() or expect() in production code

### 3. Performance & Efficiency
- Review allocations and cloning patterns
- Check for unnecessary Vec reallocations
- Verify efficient iterator usage
- Look for opportunities to use references over owned values

### 4. Code Quality
- Check adherence to Rust naming conventions
- Verify proper module organization
- Review trait implementations and bounds
- Ensure appropriate visibility modifiers

### 5. Testing & Documentation
- Verify comprehensive test coverage
- Check for proper documentation comments
- Review example code in documentation
- Ensure integration tests cover key workflows

## Validation Commands

```bash
# Format check
cargo fmt --check

# Linting
cargo clippy -- -D warnings

# Tests
cargo test

# Documentation
cargo doc --no-deps

# Security audit
cargo audit
```

## Review Checklist

- [ ] No compiler warnings
- [ ] All tests pass
- [ ] Error handling is comprehensive
- [ ] No unsafe code without justification
- [ ] Performance considerations addressed
- [ ] Documentation is complete and accurate

Provide specific feedback on code quality, safety, and performance improvements.
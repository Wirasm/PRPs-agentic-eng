# Go Code Review

## Target: $ARGUMENTS

Perform comprehensive Go code review focusing on idiomatic patterns, performance, and maintainability.

## Review Areas

### 1. Go Idioms & Best Practices
- Check adherence to Go naming conventions
- Verify proper package organization
- Review interface usage and implementation
- Ensure proper use of channels and goroutines

### 2. Error Handling
- Verify proper error checking patterns
- Check for appropriate error wrapping
- Review custom error types and implementations
- Ensure errors provide sufficient context

### 3. Concurrency & Safety
- Review goroutine usage and lifecycle
- Check for proper channel usage patterns
- Verify context usage for cancellation
- Look for race conditions and data races

### 4. Performance & Efficiency
- Review memory allocation patterns
- Check for efficient string handling
- Verify proper slice and map usage
- Look for unnecessary copying

### 5. Testing & Documentation
- Verify comprehensive test coverage
- Check for proper benchmarks
- Review example tests and documentation
- Ensure integration tests cover key workflows

## Validation Commands

```bash
# Format check
go fmt ./...

# Static analysis
go vet ./...

# Tests with race detection
go test -race ./...

# Benchmarks
go test -bench=. ./...

# Coverage
go test -cover ./...
```

## Review Checklist

- [ ] No go vet warnings
- [ ] All tests pass
- [ ] Error handling follows Go conventions
- [ ] Proper context usage
- [ ] No race conditions detected
- [ ] Documentation is complete and accurate

Provide specific feedback on code quality, performance, and Go best practices.
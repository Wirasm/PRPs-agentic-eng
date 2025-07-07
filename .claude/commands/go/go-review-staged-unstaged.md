# Go Staged/Unstaged Changes Review

Review staged and unstaged Go code changes with focus on idioms and best practices.

## Review Process

### 1. Analyze Changes
- Review git diff for staged changes
- Check unstaged modifications
- Identify new files and deletions
- Note any breaking changes to APIs

### 2. Go-Specific Checks
- Verify Go formatting and conventions
- Check for proper error handling patterns
- Review concurrency and goroutine usage
- Ensure context usage is appropriate

### 3. Quality Assessment
- Check formatting with go fmt
- Run go vet for static analysis
- Verify tests cover new functionality
- Review documentation updates

## Validation Commands

```bash
# Check staged changes
git diff --cached

# Check unstaged changes  
git diff

# Format and vet
go fmt ./...
go vet ./...

# Run tests with race detection
go test -race ./...

# Check for compilation issues
go build ./...
```

## Review Focus Areas

### Idioms & Conventions
- Naming conventions (camelCase, proper exports)
- Package structure and imports
- Interface design and usage
- Proper Go error handling patterns

### Concurrency
- Goroutine lifecycle management
- Channel usage patterns
- Context propagation
- Synchronization primitives

### Performance
- Memory allocation efficiency
- String concatenation patterns
- Slice and map operations
- Unnecessary type conversions

## Checklist

- [ ] All changes compile without errors
- [ ] Tests pass for modified code
- [ ] Error handling follows Go conventions
- [ ] Proper context usage
- [ ] No race conditions detected
- [ ] Documentation updated where needed

Provide detailed feedback on the changes with specific improvement suggestions.
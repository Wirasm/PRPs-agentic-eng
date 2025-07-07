# Rust Staged/Unstaged Changes Review

Review staged and unstaged Rust code changes with focus on safety and best practices.

## Review Process

### 1. Analyze Changes
- Review git diff for staged changes
- Check unstaged modifications
- Identify new files and deletions
- Note any breaking changes

### 2. Rust-Specific Checks
- Verify borrow checker compliance in changes
- Check for proper error handling patterns
- Review any new unsafe blocks
- Ensure thread safety considerations

### 3. Quality Assessment
- Check formatting with cargo fmt
- Run clippy for linting issues
- Verify tests cover new functionality
- Review documentation updates

## Validation Commands

```bash
# Check staged changes
git diff --cached

# Check unstaged changes  
git diff

# Format and lint
cargo fmt
cargo clippy -- -D warnings

# Run tests
cargo test

# Check for compilation issues
cargo check
```

## Review Focus Areas

### Safety & Correctness
- Memory safety and ownership
- Proper error handling
- Thread safety considerations
- Panic safety

### Performance
- Unnecessary allocations
- Inefficient algorithms
- Missing optimizations
- Resource usage

### Maintainability
- Code clarity and documentation
- Test coverage
- API design consistency
- Module organization

## Checklist

- [ ] All changes compile without warnings
- [ ] Tests pass for modified code
- [ ] Error handling follows project patterns
- [ ] No unnecessary unsafe code
- [ ] Documentation updated where needed
- [ ] Performance impact considered

Provide detailed feedback on the changes with specific improvement suggestions.
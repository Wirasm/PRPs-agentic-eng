# Bun Staged/Unstaged Changes Review

Review staged and unstaged Bun code changes with focus on performance and TypeScript best practices.

## Review Process

### 1. Analyze Changes
- Review git diff for staged changes
- Check unstaged modifications
- Identify new files and deletions
- Note any breaking changes to APIs

### 2. Bun-Specific Checks
- Verify proper Bun API usage in changes
- Check for performance optimizations
- Review TypeScript type safety
- Ensure proper bundling considerations

### 3. Quality Assessment
- Check TypeScript compilation
- Run linting for code quality
- Verify tests cover new functionality
- Review build impact

## Validation Commands

```bash
# Check staged changes
git diff --cached

# Check unstaged changes  
git diff

# Type checking and linting
bun run typecheck
bun run lint

# Run tests
bun test

# Check build impact
bun run build
```

## Review Focus Areas

### Performance & Optimization
- Bundle size impact
- Runtime performance
- Memory usage patterns
- Network request efficiency

### Type Safety
- Proper TypeScript usage
- Type definitions accuracy
- Generic implementations
- Interface design

### Bun Integration
- Native API usage
- Server/client patterns
- Build tool integration
- Development workflow

## Checklist

- [ ] All changes compile without errors
- [ ] Tests pass for modified code
- [ ] TypeScript types are accurate
- [ ] Performance impact considered
- [ ] Build process remains efficient
- [ ] Documentation updated where needed

Provide detailed feedback on the changes with specific improvement suggestions.
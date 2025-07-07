# Bun Code Review

## Target: $ARGUMENTS

Perform comprehensive Bun code review focusing on performance, TypeScript patterns, and Bun-specific optimizations.

## Review Areas

### 1. Bun-Specific Patterns
- Check proper use of Bun APIs vs Node.js APIs
- Verify native Bun features are utilized
- Review Bun.serve usage and patterns
- Ensure proper use of Bun's built-in modules

### 2. TypeScript & Type Safety
- Verify proper TypeScript usage
- Check for type assertions and any usage
- Review interface and type definitions
- Ensure proper generic usage

### 3. Performance & Efficiency
- Review bundle size and optimization
- Check for unnecessary polyfills
- Verify efficient import/export patterns
- Look for Bun-specific performance optimizations

### 4. Testing & Quality
- Verify proper use of bun:test
- Check test coverage and patterns
- Review mock implementations
- Ensure integration tests are comprehensive

### 5. Build & Development
- Review build configuration
- Check development workflow efficiency
- Verify proper environment handling
- Ensure proper bundling strategies

## Validation Commands

```bash
# Type checking
bun run typecheck

# Linting
bun run lint

# Tests
bun test

# Build check
bun run build

# Bundle analysis (if available)
bun run analyze
```

## Review Checklist

- [ ] No TypeScript errors
- [ ] All tests pass
- [ ] Proper Bun API usage
- [ ] Performance considerations addressed
- [ ] Build process is optimized
- [ ] Documentation is complete and accurate

Provide specific feedback on code quality, performance, and Bun best practices.
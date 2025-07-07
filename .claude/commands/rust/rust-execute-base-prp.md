# Execute BASE PRP

## PRP File: $ARGUMENTS

Execute the specified Rust PRP with comprehensive implementation and validation.

## Execution Process

1. **Load PRP Context**
   - Read the complete PRP file
   - Understand all requirements, context, and constraints
   - Note the validation gates and success criteria

2. **Implementation**
   - Follow the implementation blueprint exactly
   - Use existing patterns identified in the PRP
   - Implement all tasks in the specified order
   - Apply Rust best practices and idioms

3. **Validation Loop**
   - Run each validation gate in sequence
   - Fix any errors or warnings before proceeding
   - Ensure all tests pass
   - Verify manual testing scenarios

## Validation Commands

```bash
# Level 1: Format and Lint
cargo fmt
cargo clippy -- -D warnings

# Level 2: Unit Tests
cargo test

# Level 3: Build Validation
cargo build --release

# Level 4: Integration Tests
cargo test --test integration
```

## Success Criteria

- [ ] All validation commands pass without errors
- [ ] All PRP requirements implemented
- [ ] Code follows existing project patterns
- [ ] Error handling is comprehensive
- [ ] Documentation is updated if needed

## Output

Implement the feature according to the PRP specifications, ensuring all validation gates pass.
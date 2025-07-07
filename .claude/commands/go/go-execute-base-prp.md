# Execute BASE PRP

## PRP File: $ARGUMENTS

Execute the specified Go PRP with comprehensive implementation and validation.

## Execution Process

1. **Load PRP Context**
   - Read the complete PRP file
   - Understand all requirements, context, and constraints
   - Note the validation gates and success criteria

2. **Implementation**
   - Follow the implementation blueprint exactly
   - Use existing patterns identified in the PRP
   - Implement all tasks in the specified order
   - Apply Go best practices and idioms

3. **Validation Loop**
   - Run each validation gate in sequence
   - Fix any errors or warnings before proceeding
   - Ensure all tests pass
   - Verify manual testing scenarios

## Validation Commands

```bash
# Level 1: Format and Vet
go fmt ./...
go vet ./...

# Level 2: Unit Tests
go test ./...

# Level 3: Build Validation
go build ./...

# Level 4: Race Condition Check
go test -race ./...
```

## Success Criteria

- [ ] All validation commands pass without errors
- [ ] All PRP requirements implemented
- [ ] Code follows existing project patterns
- [ ] Error handling is comprehensive
- [ ] Documentation is updated if needed

## Output

Implement the feature according to the PRP specifications, ensuring all validation gates pass.
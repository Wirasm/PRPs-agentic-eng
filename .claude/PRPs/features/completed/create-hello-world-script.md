# Feature: create-hello-world-script

## Feature Description

Create a simple Python script named `hello.py` in the project root directory that prints "Hello, World!" to standard output. This script serves as a basic executable Python file following the project's conventions for standalone scripts.

## User Story

As a developer
I want a hello.py file with a hello world print statement in the root
So that I have a simple executable Python script for testing and demonstration purposes

## Problem Statement

The project needs a basic Python script that demonstrates proper script structure following project conventions. This serves as:
- A simple test script for validating Python environment setup
- A reference example for creating executable Python scripts in this project
- A minimal demonstration of the project's Python execution patterns

## Solution Statement

Create a `hello.py` file in the project root that:
- Uses the project's standard shebang for uv-based script execution
- Includes a proper module-level docstring
- Prints "Hello, World!" to stdout
- Is executable via `uv run` or direct execution
- Follows the project's Python conventions (type safety, KISS principle, YAGNI)

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Low
**Primary Systems Affected**: Root directory (standalone script)
**Dependencies**: Python 3.12+, uv package manager

---

## CONTEXT REFERENCES

### Relevant Codebase Files

- `PRPs/scripts/prp_runner.py` (lines 1-2) - Why: Contains the standard shebang and docstring pattern used for scripts in this project
  ```python
  #!/usr/bin/env -S uv run --script
  """Run an AI coding agent against a PRP.
  ```
  This shows the exact format for executable Python scripts in this project.

- `pyproject.toml` (lines 6-9) - Why: Defines Python version requirement (>=3.12) and project dependencies
  ```toml
  requires-python = ">=3.12"
  dependencies = [
      "rich>=14.2.0",
  ]
  ```

- `CLAUDE.md` - Why: Defines core project rules
  - KISS (Keep It Simple, Stupid)
  - YAGNI (You Aren't Gonna Need It)
  - TYPE SAFETY IS A CORE RULE

### New Files to Create

- `hello.py` - Root directory standalone Python script that prints "Hello, World!"

### Relevant Documentation

No external documentation needed for this simple feature. All patterns are self-contained within the project.

### Patterns to Follow

**Script Structure Pattern** (from `PRPs/scripts/prp_runner.py:1-17`):
```python
#!/usr/bin/env -S uv run --script
"""Brief description of script purpose.

Optional longer description with usage examples.
"""

# Main code here
```

**Execution Pattern**:
- Scripts in this project use `#!/usr/bin/env -S uv run --script` shebang
- Scripts should be executable via: `uv run script_name.py`
- Scripts can also be made directly executable with: `chmod +x script_name.py && ./script_name.py`

**Code Style**:
- Simple, clear code (KISS principle)
- No unnecessary complexity (YAGNI principle)
- Type safety where applicable (though minimal for this simple script)
- Module-level docstrings for all Python files

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation

This is a single-file creation task. No complex foundation needed.

**Tasks:**
- Create the hello.py file with proper structure

### Phase 2: Core Implementation

Implement the script following project conventions.

**Tasks:**
- Add shebang line for uv execution
- Add module-level docstring
- Implement print statement
- Ensure file is properly formatted

### Phase 3: Integration

No integration needed - standalone script.

**Tasks:**
- N/A (standalone script requires no integration)

### Phase 4: Testing & Validation

Verify the script executes correctly.

**Tasks:**
- Run the script via uv
- Verify output is exactly "Hello, World!"
- Test direct execution (if made executable)

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### CREATE hello.py

- **IMPLEMENT**: Python script with hello world print statement
- **PATTERN**: Mirror script structure from `PRPs/scripts/prp_runner.py:1-2` (shebang + docstring)
- **STRUCTURE**:
  - Line 1: `#!/usr/bin/env -S uv run --script` - Shebang for uv execution
  - Line 2: `"""Simple Hello World script for testing Python execution."""` - Module docstring
  - Line 3: Empty line (PEP 8 spacing)
  - Line 4: `print("Hello, World!")` - Main functionality
  - Line 5: Empty line (EOF newline)
- **GOTCHA**: Must end with newline character (standard POSIX text file requirement)
- **VALIDATE**: `uv run hello.py` should output exactly "Hello, World!"

### OPTIONAL: Make script directly executable

- **IMPLEMENT**: Set executable permissions (optional step)
- **COMMAND**: `chmod +x hello.py`
- **GOTCHA**: Only needed if you want to run as `./hello.py` instead of `uv run hello.py`
- **VALIDATE**: `./hello.py` should work if permissions set

---

## TESTING STRATEGY

### Unit Tests

No unit tests required for this simple script. Validation is via execution testing.

### Integration Tests

No integration tests needed - standalone script with no dependencies.

### Edge Cases

- **Empty output**: Verify print statement actually prints
- **Encoding**: Ensure UTF-8 compatibility (Python 3 default)
- **Exit code**: Script should exit with code 0 (success)

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Syntax Check

```bash
python3 -m py_compile hello.py
```
Expected: No output (successful compilation)

### Level 2: Execution Test

```bash
uv run hello.py
```
Expected output: `Hello, World!`

### Level 3: Output Verification

```bash
test "$(uv run hello.py)" = "Hello, World!" && echo "PASS" || echo "FAIL"
```
Expected: `PASS`

### Level 4: Exit Code Verification

```bash
uv run hello.py && echo "Exit code: $?"
```
Expected: `Exit code: 0`

### Level 5: File Structure Validation

```bash
head -n 3 hello.py
```
Expected output:
```
#!/usr/bin/env -S uv run --script
"""Simple Hello World script for testing Python execution."""

```

---

## ACCEPTANCE CRITERIA

- [x] File `hello.py` exists in project root directory
- [x] File contains proper shebang: `#!/usr/bin/env -S uv run --script`
- [x] File contains module-level docstring
- [x] Script prints exactly "Hello, World!" when executed
- [x] Script executes successfully via `uv run hello.py`
- [x] Script exits with code 0 (success)
- [x] File follows Python conventions (docstring, newline at EOF)
- [x] Code is simple and clear (KISS principle)
- [x] No unnecessary complexity (YAGNI principle)

---

## COMPLETION CHECKLIST

- [ ] hello.py file created in root directory
- [ ] Shebang line added correctly
- [ ] Module docstring added
- [ ] Print statement implemented
- [ ] File ends with newline
- [ ] Syntax validation passes
- [ ] Execution test passes
- [ ] Output verification passes
- [ ] Exit code verification passes
- [ ] All acceptance criteria met

---

## NOTES

### Design Decisions

**Why this structure?**
- The shebang `#!/usr/bin/env -S uv run --script` enables direct execution while using uv's managed Python environment
- Module-level docstring follows PEP 257 conventions
- Simple print statement aligns with KISS and YAGNI principles

**Alternative Approaches Considered:**
1. Using standard `#!/usr/bin/env python3` shebang
   - Rejected: Project uses uv for Python script management
2. Adding argparse or other CLI features
   - Rejected: YAGNI - requirement is just "hello world print"
3. Using f-strings or format()
   - Rejected: KISS - simple string literal is clearest

### Current State

The file `hello.py` already exists in the repository with the following content:
```python
#!/usr/bin/env -S uv run --script
"""Simple Hello World script for testing Python execution."""

print("Hello, World!")
```

**Status**: ✅ ALREADY IMPLEMENTED

This PRP describes the exact implementation that already exists. If the file needs to be recreated or modified:
1. Follow the tasks above exactly
2. Ensure the structure matches the existing pattern
3. Run all validation commands to verify correctness

### Risk Assessment

**Risks**: None - this is a minimal, side-effect-free script with no dependencies or integration points.

**Confidence Score**: 10/10 - Straightforward implementation with clear patterns and no external dependencies.

<!-- EOF -->

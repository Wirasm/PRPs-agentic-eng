# PRP Workflow Scripts

Automated workflows for PRP Core operations.

## prp_workflow.py

Executes the complete PRP workflow in sequence:

1. **Create PRP**: `/prp-core-create {feature_description}`
2. **Execute PRP**: `/prp-core-execute {prp_file}`
3. **Commit**: `/prp-core-commit`

### Usage

```bash
# Basic usage with sonnet (default)
uv run .claude/PRPs/scripts/prp_workflow.py "Add user authentication"

# Use opus model
uv run .claude/PRPs/scripts/prp_workflow.py "Implement search functionality" --model opus

# Complex feature description
uv run .claude/PRPs/scripts/prp_workflow.py "Refactor database layer to use async patterns"
```

### What It Does

**Step 1: Create PRP**
- Runs `/prp-core-create` with your feature description
- Performs deep codebase analysis
- Generates comprehensive implementation plan
- Saves to `.claude/PRPs/features/{kebab-case-name}.md`

**Step 2: Execute PRP**
- Automatically extracts PRP filename from step 1 output
- Runs `/prp-core-execute {prp_file}`
- Implements all tasks sequentially
- Validates after each task
- Moves completed PRP to `.claude/PRPs/features/completed/`

**Step 3: Commit**
- Runs `/prp-core-commit` to commit changes
- Creates smart commit message
- (Optional step - can be done manually with `/smart-commit`)

### Output

All execution logs saved to: `.claude/PRPs/logs/{prp_id}/`

**Files created:**
- `step1_create.log` - PRP creation output
- `step2_execute.log` - PRP execution output
- `step3_commit.log` - Commit output
- `workflow_summary.json` - Metadata and status

**Summary JSON structure:**
```json
{
  "prp_id": "abc12345",
  "feature_description": "Add user authentication",
  "model": "sonnet",
  "prp_filename": "add-user-authentication",
  "steps": {
    "create": {"success": true, "output_length": 15000},
    "execute": {"success": true, "output_length": 8000},
    "commit": {"success": true, "output_length": 500}
  },
  "log_directory": ".claude/PRPs/logs/abc12345"
}
```

### Examples

**Simple feature:**
```bash
uv run .claude/PRPs/scripts/prp_workflow.py "Add dark mode toggle"
```

**Complex feature with opus:**
```bash
uv run .claude/PRPs/scripts/prp_workflow.py \
  "Implement real-time collaboration with WebSockets and conflict resolution" \
  --model opus
```

**Bug fix:**
```bash
uv run .claude/PRPs/scripts/prp_workflow.py "Fix memory leak in data processing pipeline"
```

### Error Handling

If any step fails:
- Workflow stops at that step
- Error details saved to log file
- Exit with non-zero status code
- Summary JSON shows which step failed

**Example failure output:**
```
❌ Step 2 Failed

Failed to execute PRP

Check logs: .claude/PRPs/logs/abc12345/step2_execute.log
PRP file: .claude/PRPs/features/add-auth.md
```

You can then:
1. Check the log file to see what went wrong
2. Fix any issues
3. Manually run `/prp-core-execute add-auth` to continue

### Tips

- **Use descriptive feature names**: The script uses your description for the PRP
- **Check logs on failure**: Logs contain full Claude Code output
- **Model selection**: Use `opus` for complex features, `sonnet` for most tasks
- **Manual override**: If step 3 fails, use `/smart-commit` manually
- **Tracking**: Each run gets a unique `prp_id` for tracking multiple workflows

### Requirements

- Claude Code CLI installed and configured
- `uv` package manager
- Python 3.10+
- Dependencies: `rich` (auto-installed by uv)

### Architecture

Inspired by the `adw_slash_command.py` pattern but simplified:
- Uses `prp_id` for tracking (8-char UUID)
- Direct Claude CLI execution via subprocess
- Rich terminal output for better UX
- Structured logging to `.claude/PRPs/logs/`
- Automatic PRP filename extraction via regex
- Sequential execution with error handling

### Integration

This workflow script integrates with:
- **PRP Core Commands**: `/prp-core-create`, `/prp-core-execute`, `/prp-core-commit`
- **PRP Storage**: `.claude/PRPs/features/` directory
- **Git Operations**: Automatic commit via `/prp-core-commit`
- **Claude Code**: Direct CLI integration

### Future Enhancements

Possible improvements:
- Parallel execution option
- Resume from specific step
- Custom step selection (skip commit, etc.)
- Webhook notifications on completion
- CI/CD integration examples

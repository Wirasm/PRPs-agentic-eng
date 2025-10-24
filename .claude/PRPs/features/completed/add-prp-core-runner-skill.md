# Feature: Add Agent Skill for PRP Core Workflow Runner

## Feature Description

Create an Agent Skill that orchestrates the complete PRP core workflow, automating the end-to-end process from feature request to pull request. This skill will execute the sequence: create branch → create PRP → execute PRP → commit → create PR, streamlining the development workflow for implementing new features using the PRP methodology.

## User Story

As a developer using the PRP framework
I want to run the complete PRP core workflow with a single invocation
So that I can quickly go from feature idea to pull request without manually executing each command

## Problem Statement

Currently, developers must manually execute 5 separate slash commands to complete the full PRP workflow:
1. `/prp-core-new-branch` - Create feature branch
2. `/prp-core-create` - Generate comprehensive PRP
3. `/prp-core-execute` - Implement the feature
4. `/prp-core-commit` - Commit changes
5. `/prp-core-pr` - Create pull request

This manual orchestration is:
- Time-consuming and error-prone
- Requires remembering the correct sequence
- Interrupts developer flow
- Not discoverable to new team members

## Solution Statement

Create an Agent Skill that Claude can autonomously invoke when a developer requests to implement a feature using the PRP workflow. The skill will:
- Automatically orchestrate all 5 PRP core commands in sequence
- Stop execution if any step fails
- Provide clear progress tracking
- Be discoverable through natural language requests
- Follow the existing command patterns and validation requirements

Additionally, create two supporting slash commands:
- `/prp-core-run-all` - Manually invoke the complete workflow
- `/prp-core-new-branch` - Create a conventional git branch (currently missing)

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Medium
**Primary Systems Affected**:
- `.claude/skills/` - New Agent Skills system
- `.claude/commands/prp-core/` - Additional workflow commands
**Dependencies**:
- Claude Code Agent Skills feature (v1.0+)
- Existing prp-core commands (create, execute, commit, pr)
- SlashCommand tool for command invocation

---

## CONTEXT REFERENCES

### Relevant Codebase Files

- `.claude/commands/prp-core/prp-core-create.md` (lines 1-409) - Why: Template for creating comprehensive PRPs with validation
- `.claude/commands/prp-core/prp-core-execute.md` (lines 1-60) - Why: Execution pattern for PRPs with validation gates
- `.claude/commands/prp-core/PRP-core-commit.md` (lines 1-56) - Why: Atomic commit pattern with conventional commits
- `.claude/commands/prp-core/prp-core-pr.md` (lines 1-85) - Why: PR creation pattern with proper formatting
- `.claude/commands/development/new-dev-branch.md` (lines 1-8) - Why: Simple branch creation pattern to enhance
- `CLAUDE.md` (lines 68-101) - Why: Project validation requirements and PRP methodology

### New Files to Create

- `.claude/skills/prp-core-runner/SKILL.md` - Agent Skill for automated PRP workflow
- `.claude/commands/prp-core/prp-core-run-all.md` - Slash command wrapper for the workflow
- `.claude/commands/prp-core/prp-core-new-branch.md` - Conventional branch naming command

### Relevant Documentation

- [Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
  - Specific section: SKILL.md structure and frontmatter requirements
  - Why: Required for proper skill creation with correct metadata
- [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
  - Specific section: Writing clear descriptions for discoverability
  - Why: Ensures Claude can discover and invoke the skill appropriately
- [Agent Skills in Claude Code](https://docs.claude.com/en/docs/claude-code/agent-skills)
  - Specific section: Project Skills in `.claude/skills/`
  - Why: Shows proper directory structure and team sharing via git

### Patterns to Follow

**Slash Command Structure** (from existing prp-core commands):
```markdown
---
description: "Brief description of what this command does"
---

# Command Title

## Instructions

Step-by-step execution instructions...

## Report

Expected output format...
```

**SKILL.md Structure** (from Agent Skills documentation):
```yaml
---
name: skill-name-kebab-case
description: What the skill does and when to use it (max 1024 chars)
---

# Skill Name

## Instructions
Clear, step-by-step guidance for Claude

## Examples
Concrete usage examples
```

**Conventional Branch Naming** (standard practice):
- Prefixes: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`, `perf/`
- Format: `{prefix}/{kebab-case-description}`
- Max 50 characters
- Examples: `feat/add-user-auth`, `fix/login-redirect`

**Commit Message Format** (from PRP-core-commit.md):
```
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
Present tense, lowercase, 50 chars max, no period
NEVER mention Claude Code, Anthropic, or co-authoring
```

**Error Handling Pattern**:
- Stop execution if command fails
- Report which step failed clearly
- Provide actionable error message
- Don't proceed to next step on failure

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation

Create the directory structure and supporting commands that the skill will orchestrate.

**Tasks:**
- Create `.claude/skills/prp-core-runner/` directory
- Create `/prp-core-new-branch` command for conventional branch creation
- Create `/prp-core-run-all` orchestrator command

### Phase 2: Core Skill Implementation

Implement the main Agent Skill with proper metadata and instructions.

**Tasks:**
- Write SKILL.md with correct YAML frontmatter
- Define clear, step-by-step instructions for workflow orchestration
- Add error handling and validation requirements
- Include usage examples

### Phase 3: Integration

Ensure the skill integrates properly with existing PRP core commands.

**Tasks:**
- Verify skill can invoke SlashCommand tool
- Test error propagation from failed commands
- Validate command sequence execution
- Ensure proper reporting at each step

### Phase 4: Testing & Validation

Test the complete workflow end-to-end.

**Tasks:**
- Manual test: Invoke skill with feature request
- Verify branch creation with conventional naming
- Confirm PRP creation and execution
- Validate commit and PR creation
- Test failure scenarios (e.g., test failures, validation errors)

---

## STEP-BY-STEP TASKS

### Task 1: CREATE .claude/skills/prp-core-runner/ directory

- **IMPLEMENT**: Create directory structure for Agent Skills
- **PATTERN**: Standard directory creation for project skills
- **GOTCHA**: Directory must be in `.claude/skills/` for Claude Code to discover it
- **VALIDATE**: `test -d .claude/skills/prp-core-runner && echo "Directory created successfully"`

### Task 2: CREATE .claude/commands/prp-core/prp-core-new-branch.md

- **IMPLEMENT**: Conventional git branch creation command
- **PATTERN**: Mirror `.claude/commands/development/new-dev-branch.md` structure
- **IMPORTS**: None required
- **GOTCHA**: Branch names must be kebab-case, max 50 chars, use conventional prefixes
- **DETAILS**:
  - Check current branch and warn if not on main/develop
  - Generate conventional branch name from feature description
  - Prefixes: feat/, fix/, chore/, docs/, refactor/, test/, perf/
  - Validate branch doesn't already exist
  - If exists, append -v2, -v3, etc.
  - Create and checkout new branch
  - Report branch name created
- **VALIDATE**: `test -f .claude/commands/prp-core/prp-core-new-branch.md && echo "Command file created"`

### Task 3: CREATE .claude/commands/prp-core/prp-core-run-all.md

- **IMPLEMENT**: Orchestrator slash command that runs all PRP core commands in sequence
- **PATTERN**: Mirror structure of other prp-core commands with clear steps
- **IMPORTS**: None required
- **GOTCHA**: Must use SlashCommand tool for each step, stop on any failure
- **DETAILS**:
  - Accept feature description as $ARGUMENTS
  - Execute in sequence:
    1. `/prp-core-new-branch {feature}`
    2. `/prp-core-create {feature}`
    3. `/prp-core-execute` (using PRP from step 2)
    4. `/prp-core-commit`
    5. `/prp-core-pr` (generate title from feature)
  - Stop if any command fails
  - Report progress at each step
  - Final report with summary of all actions
- **VALIDATE**: `test -f .claude/commands/prp-core/prp-core-run-all.md && echo "Orchestrator created"`

### Task 4: CREATE .claude/skills/prp-core-runner/SKILL.md

- **IMPLEMENT**: Agent Skill for autonomous PRP workflow execution
- **PATTERN**: Follow Agent Skills documentation structure exactly
- **IMPORTS**: None required
- **GOTCHA**: YAML frontmatter must be valid, name must be kebab-case, description max 1024 chars
- **DETAILS**:
  - **YAML Frontmatter**:
    ```yaml
    ---
    name: prp-core-runner
    description: Orchestrate complete PRP workflow from feature request to pull request. Run create branch, create PRP, execute implementation, commit changes, and create PR in sequence. Use when implementing features using PRP methodology or when user requests full PRP workflow.
    ---
    ```
  - **Instructions Section**:
    - Use SlashCommand tool to invoke `/prp-core-run-all`
    - Pass user's feature description as argument
    - Monitor each step for failures
    - Report progress clearly
    - Stop on any validation failures
  - **Examples Section**:
    - Example 1: "Implement user authentication using JWT"
    - Example 2: "Add search API with Elasticsearch integration"
    - Example 3: "Refactor database layer for better performance"
  - **When to Use**:
    - User requests to "implement a feature using PRP"
    - User asks to "run the full PRP workflow"
    - User wants end-to-end automation from idea to PR
  - **Error Handling**:
    - If any step fails, report which step and why
    - Don't proceed to next steps
    - Provide actionable guidance for fixing the issue
- **VALIDATE**: `test -f .claude/skills/prp-core-runner/SKILL.md && grep -q "^name: prp-core-runner$" .claude/skills/prp-core-runner/SKILL.md && echo "Skill created with valid frontmatter"`

### Task 5: VALIDATE YAML frontmatter syntax

- **IMPLEMENT**: Verify SKILL.md has valid YAML frontmatter
- **PATTERN**: Use head and basic parsing to validate structure
- **GOTCHA**: YAML must have opening ---, closing ---, and valid key: value pairs
- **VALIDATE**: `head -n 5 .claude/skills/prp-core-runner/SKILL.md | grep -E "^(---|name:|description:)" | wc -l | grep -q "4" && echo "YAML frontmatter valid"`

### Task 6: VALIDATE skill name follows conventions

- **IMPLEMENT**: Verify skill name is kebab-case, lowercase, max 64 chars
- **PATTERN**: Regex validation for naming conventions
- **GOTCHA**: Only lowercase letters, numbers, and hyphens allowed
- **VALIDATE**: `grep "^name: prp-core-runner$" .claude/skills/prp-core-runner/SKILL.md && echo "Skill name valid"`

### Task 7: VALIDATE description field exists and is appropriate length

- **IMPLEMENT**: Check description is present and under 1024 characters
- **PATTERN**: Extract description field and measure length
- **GOTCHA**: Description must be on one line (or properly quoted if multi-line)
- **VALIDATE**: `grep "^description:" .claude/skills/prp-core-runner/SKILL.md | wc -c | awk '{if ($1 < 1024 && $1 > 50) print "Description length valid"}'`

### Task 8: VALIDATE all command files have proper markdown structure

- **IMPLEMENT**: Verify markdown files have headers and required sections
- **PATTERN**: Check for ## Instructions and ## Report sections
- **GOTCHA**: Commands should follow existing prp-core command structure
- **VALIDATE**: `grep -l "## Instructions" .claude/commands/prp-core/prp-core-new-branch.md .claude/commands/prp-core/prp-core-run-all.md | wc -l | grep -q "2" && echo "Command structure valid"`

### Task 9: VALIDATE directory structure is correct

- **IMPLEMENT**: Ensure all files are in correct locations
- **PATTERN**: Test each file path exists
- **VALIDATE**:
```bash
test -f .claude/skills/prp-core-runner/SKILL.md && \
test -f .claude/commands/prp-core/prp-core-new-branch.md && \
test -f .claude/commands/prp-core/prp-core-run-all.md && \
echo "All files in correct locations"
```

### Task 10: UPDATE CLAUDE.md to document new skill and commands

- **IMPLEMENT**: Add new skill and commands to project documentation
- **PATTERN**: Add to "Key Claude Commands" section
- **IMPORTS**: None required
- **GOTCHA**: Maintain existing formatting and organization
- **DETAILS**:
  - Add to "Core PRP Workflow (Recommended)" section:
    - `/prp-core-new-branch` - Create conventional git branch for feature
    - `/prp-core-run-all` - Run complete PRP workflow from feature to PR
  - Add note about prp-core-runner skill being available for autonomous workflow execution
- **VALIDATE**: `grep -q "prp-core-run-all" CLAUDE.md && grep -q "prp-core-new-branch" CLAUDE.md && echo "Documentation updated"`

---

## TESTING STRATEGY

### Unit Tests

No unit tests required - this feature consists of configuration files and markdown templates.

### Integration Tests

Manual integration testing required to verify the complete workflow.

**Test Scenarios:**

1. **Happy Path - Feature Implementation**
   - Invoke skill with feature request
   - Verify branch created with conventional name
   - Verify PRP created in `.claude/PRPs/features/`
   - Verify feature implementation completes
   - Verify commit created with conventional message
   - Verify PR created with proper description

2. **Failure Handling - Validation Error**
   - Trigger validation failure (e.g., introduce syntax error)
   - Verify workflow stops at failed step
   - Verify clear error message provided
   - Verify subsequent steps don't execute

3. **Skill Discovery**
   - Ask Claude "What skills are available?"
   - Verify prp-core-runner appears in list
   - Ask "Can you implement a feature using PRP?"
   - Verify Claude invokes the skill autonomously

### Edge Cases

1. **Branch Already Exists**: Verify -v2, -v3 suffixes work correctly
2. **Long Feature Names**: Verify truncation to 50 chars for branch names
3. **Special Characters in Feature**: Verify proper sanitization to kebab-case
4. **Existing Changes**: Verify behavior when working directory isn't clean
5. **Network Issues**: Verify proper error handling if PR creation fails

---

## VALIDATION COMMANDS

### Level 1: File Structure & Syntax

```bash
# Verify directory structure
test -d .claude/skills/prp-core-runner && echo "✓ Skills directory exists"

# Verify all files exist
test -f .claude/skills/prp-core-runner/SKILL.md && echo "✓ SKILL.md exists"
test -f .claude/commands/prp-core/prp-core-new-branch.md && echo "✓ new-branch command exists"
test -f .claude/commands/prp-core/prp-core-run-all.md && echo "✓ run-all command exists"

# Verify YAML frontmatter
head -n 10 .claude/skills/prp-core-runner/SKILL.md | grep -E "^---$" | wc -l | grep -q "2" && echo "✓ Valid YAML delimiters"
grep -q "^name: prp-core-runner$" .claude/skills/prp-core-runner/SKILL.md && echo "✓ Valid skill name"
grep -q "^description:" .claude/skills/prp-core-runner/SKILL.md && echo "✓ Description present"

# Verify markdown structure
grep -q "## Instructions" .claude/skills/prp-core-runner/SKILL.md && echo "✓ Instructions section exists"
grep -q "## Examples" .claude/skills/prp-core-runner/SKILL.md && echo "✓ Examples section exists"
```

### Level 2: Content Validation

```bash
# Verify skill description is discoverable
grep "^description:" .claude/skills/prp-core-runner/SKILL.md | grep -q -i "prp workflow" && echo "✓ Description mentions PRP workflow"

# Verify new-branch command has conventional naming logic
grep -q "feat/" .claude/commands/prp-core/prp-core-new-branch.md && echo "✓ Branch command includes conventional prefixes"

# Verify run-all command sequences all steps
grep -q "prp-core-new-branch" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Includes branch creation"
grep -q "prp-core-create" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Includes PRP creation"
grep -q "prp-core-execute" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Includes execution"
grep -q "prp-core-commit" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Includes commit"
grep -q "prp-core-pr" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Includes PR creation"

# Verify error handling mentioned
grep -q -i "fail\|error\|stop" .claude/commands/prp-core/prp-core-run-all.md && echo "✓ Error handling documented"
```

### Level 3: Integration Testing

```bash
# List skills to verify it's discoverable
ls -la .claude/skills/*/SKILL.md

# Verify command files are readable
cat .claude/commands/prp-core/prp-core-new-branch.md | head -20
cat .claude/commands/prp-core/prp-core-run-all.md | head -20

# Verify SKILL.md is properly formatted
cat .claude/skills/prp-core-runner/SKILL.md
```

### Level 4: Manual Validation

**Test 1: Skill Discovery**
1. Start fresh Claude Code session
2. Ask: "What skills are available?"
3. Verify prp-core-runner appears in response

**Test 2: Autonomous Invocation**
1. Request: "Can you implement a new feature for user notifications using the PRP workflow?"
2. Verify Claude invokes prp-core-runner skill autonomously
3. Verify skill executes all workflow steps

**Test 3: Manual Command Invocation**
1. Run: `/prp-core-run-all Add logging to API endpoints`
2. Verify branch created with name like `feat/add-logging-to-api-endpoints`
3. Verify PRP created in `.claude/PRPs/features/add-logging-to-api-endpoints.md`
4. Verify subsequent steps execute in order

**Test 4: Branch Naming**
1. Run: `/prp-core-new-branch Fix authentication redirect bug`
2. Verify branch name: `fix/authentication-redirect-bug`
3. Run again with same name
4. Verify new branch: `fix/authentication-redirect-bug-v2`

---

## ACCEPTANCE CRITERIA

- [ ] `.claude/skills/prp-core-runner/SKILL.md` created with valid YAML frontmatter
- [ ] Skill name follows kebab-case convention: `prp-core-runner`
- [ ] Skill description is clear, specific, and under 1024 characters
- [ ] Skill description includes when to use it (PRP workflow, feature implementation)
- [ ] `.claude/commands/prp-core/prp-core-new-branch.md` created
- [ ] new-branch command implements conventional branch naming (feat/, fix/, etc.)
- [ ] new-branch command handles name conflicts with version suffixes
- [ ] `.claude/commands/prp-core/prp-core-run-all.md` created
- [ ] run-all command sequences all 5 workflow steps correctly
- [ ] run-all command stops execution on any step failure
- [ ] All files have proper markdown structure with required sections
- [ ] CLAUDE.md updated with new commands and skill documentation
- [ ] All Level 1 & 2 validation commands pass
- [ ] Manual testing confirms skill is discoverable by Claude
- [ ] Manual testing confirms autonomous invocation works
- [ ] Manual testing confirms complete workflow executes successfully

---

## COMPLETION CHECKLIST

- [ ] All tasks (1-10) completed in order
- [ ] Each task validation command passed
- [ ] All validation commands executed successfully (Levels 1-4)
- [ ] File structure validated
- [ ] YAML frontmatter syntax verified
- [ ] Skill naming conventions followed
- [ ] Command structure validated
- [ ] Documentation updated
- [ ] Manual testing confirms functionality
- [ ] Acceptance criteria all met
- [ ] No markdown syntax errors
- [ ] Skill is discoverable by Claude
- [ ] Workflow executes end-to-end successfully

---

## NOTES

### Design Decisions

**Why Agent Skill + Slash Commands?**
- Agent Skill provides autonomous invocation when Claude detects the user wants the full workflow
- Slash commands provide manual control for developers who want to run specific steps or the full sequence
- This dual approach supports both autonomous and manual workflows

**Why Separate new-branch Command?**
- Branch creation with conventional naming is reusable beyond PRP workflow
- Developers might want to create a branch without running the full workflow
- Follows single responsibility principle

**Branch Naming Convention Choices:**
- Used standard prefixes (feat/, fix/, etc.) for consistency with conventional commits
- Max 50 characters keeps branch names readable in terminal and git UIs
- Kebab-case is most common in git workflows and avoids URL encoding issues

**Error Handling Strategy:**
- Fail-fast approach: stop on first error to prevent cascading failures
- Clear error messages guide user to fix issues
- Don't try to auto-fix complex issues; report and let user decide

### Trade-offs

**Complexity vs. Flexibility:**
- Current design runs all 5 steps in sequence
- Alternative: Could allow running subset of steps
- Decision: Keep it simple - users can still run individual commands manually

**Discoverability vs. Specificity:**
- Skill description mentions "PRP workflow" specifically
- Alternative: More generic description like "automate feature development"
- Decision: Be specific so Claude knows exactly when to use it

**Validation Strictness:**
- Current design stops on any validation failure
- Alternative: Could try to continue with warnings
- Decision: Strict validation prevents shipping broken code

### Future Enhancements

Potential improvements for future iterations:

1. **Parallel PRP Creation**: Integrate with `/parallel-prp-creation` for exploring multiple approaches
2. **Review Integration**: Add optional `/prp-core-review` step before commit
3. **Configuration**: Allow customizing workflow steps via config file
4. **Rollback**: Add ability to undo workflow if late-stage validation fails
5. **Metrics**: Track workflow success rate and common failure points
6. **Templates**: Support different workflow templates for different project types

<!-- EOF -->

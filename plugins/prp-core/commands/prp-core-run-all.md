---
description: Run all prp core commands in sequence from feature request to pr
---

# PRP Core Complete Workflow

Feature: $ARGUMENTS

## Instructions

Execute the complete PRP workflow from feature idea to GitHub PR. This workflow uses a mix of subagent delegation (via Task tool) and main agent execution to optimize context usage and performance.

**CRITICAL**: Follow the delegation strategy exactly as specified. Some steps MUST run in subagents, others MUST run in the main conversation.

---

### Step 1: Create Branch (SUBAGENT) 🌿

**Delegation Strategy**: Use Task tool to delegate to subagent.

**Why subagent**: Branch creation is a simple, isolated task that doesn't require conversation context.

**Task Tool Invocation**:
```
description: "Create conventional git branch"
prompt: "You must execute the slash command /prp-core:prp-core-new-branch with the argument: '$ARGUMENTS'

Follow ALL instructions in that command exactly:
1. Check current branch
2. Generate conventional branch name (feat/, fix/, chore/, etc.)
3. Handle conflicts with version suffixes if needed
4. Create and checkout the new branch
5. Verify creation

After completion, report ONLY the branch name that was created (no additional text).

Example output: feat/add-user-auth"
subagent_type: "general-purpose"
```

**Wait for completion**. Capture the branch name from subagent output.

**Validation**: Verify branch name follows conventional format (prefix/description).

---

### Step 2: Create PRP (SUBAGENT) 📝

**Delegation Strategy**: Use Task tool to delegate to subagent.

**Why subagent**: PRP creation is research-heavy and benefits from isolated context window for codebase analysis.

**Task Tool Invocation**:
```
description: "Generate comprehensive feature PRP"
prompt: "You must execute the slash command /prp-core:prp-core-create with the argument: '$ARGUMENTS'

This command will guide you through creating a comprehensive Product Requirement Prompt. Follow ALL phases:

Phase 1: Feature Understanding
- Analyze the feature request thoroughly
- Create user story format
- Assess complexity

Phase 2: Codebase Intelligence Gathering
- Use specialized agents for pattern recognition
- Analyze project structure
- Identify dependencies and integration points

Phase 3: External Research & Documentation
- Research relevant libraries and best practices
- Gather documentation with specific anchors
- Identify gotchas and known issues

Phase 4: Deep Strategic Thinking
- Consider edge cases and design decisions
- Plan for extensibility and maintainability

Phase 5: PRP Generation
- Output comprehensive PRP file to .claude/PRPs/features/

After completion, report the EXACT file path of the created PRP.

Example output: .claude/PRPs/features/add-user-authentication.md"
subagent_type: "general-purpose"
```

**Wait for completion**. Capture the PRP file path from subagent output.

**Validation**:
1. Verify PRP file exists at reported path
2. Verify file is not empty
3. Verify it contains required sections (STEP-BY-STEP TASKS, VALIDATION COMMANDS)

---

### Step 3: Execute PRP (MAIN AGENT) ⚙️

**Delegation Strategy**: DO NOT delegate. Execute directly in main conversation using SlashCommand tool.

**Why main agent**:
- PRP execution is complex and long-running (10-50+ tasks)
- Requires full conversation context and memory
- Needs user interaction capability for clarifications
- Must manage state across many sequential operations
- Benefits from conversation history and continuity

**Direct Execution**:

Use the SlashCommand tool to invoke:
```
/prp-core:prp-core-execute [PRP-file-path-from-step-2]
```

This will:
1. Ingest the complete PRP file
2. Execute every task in STEP-BY-STEP TASKS sequentially
3. Validate after each task
4. Fix failures and re-validate before proceeding
5. Run full validation suite on completion
6. Move completed PRP to .claude/PRPs/features/completed/

**IMPORTANT**:
- Execute this step YOURSELF in the main conversation
- DO NOT use Task tool for this step
- Track progress with TodoWrite
- Don't stop until entire PRP is complete and validated

**Wait for execution to fully complete** before proceeding to Step 4.

**Validation**:
1. All tasks completed
2. PRP moved to completed/ directory
3. All validation commands passed

---

### Step 4: Commit Changes (SUBAGENT) 💾

**Delegation Strategy**: Use Task tool to delegate to subagent.

**Why subagent**: Commit creation is isolated and only needs current git state.

**Task Tool Invocation**:
```
description: "Create conventional commit"
prompt: "You must execute the slash command /prp-core:prp-core-commit

Follow ALL instructions in that command:
1. Review uncommitted changes with git diff
2. Check git status
3. Stage all changes with git add -A
4. Create commit with conventional format: <type>: <description>
   - Types: feat, fix, docs, style, refactor, test, chore
   - Present tense, lowercase, ≤50 chars, no period
   - NEVER mention Claude Code, Anthropic, or AI

After completion, report the commit hash and commit message.

Example output:
Commit: a1b2c3d
Message: feat: add user authentication system"
subagent_type: "general-purpose"
```

**Wait for completion**. Capture commit hash and message.

**Validation**: Verify commit exists with `git log -1 --oneline`.

---

### Step 5: Create PR (SUBAGENT) 🚀

**Delegation Strategy**: Use Task tool to delegate to subagent.

**Why subagent**: PR creation is isolated and only needs git history.

**Task Tool Invocation**:
```
description: "Push and create GitHub PR"
prompt: "You must execute the slash command /prp-core:prp-core-pr with the title generated from the feature: '$ARGUMENTS'

Follow ALL instructions in that command:
1. Check current branch
2. Review changes with git status and git diff
3. Push to remote with git push -u origin HEAD
4. Create GitHub PR using gh pr create with:
   - Title: Generated from feature request
   - Body: Comprehensive description with summary, changes, type, testing, checklist

After completion, report the PR URL.

Example output: https://github.com/Wirasm/PRPs-agentic-eng/pull/15"
subagent_type: "general-purpose"
```

**Wait for completion**. Capture PR URL.

**Validation**: Verify PR URL is accessible.

---

## Completion Report

After all 5 steps complete successfully, provide a comprehensive summary:

```
✅ PRP Core Workflow Complete

Branch: [branch-name-from-step-1]
PRP: [prp-file-path-from-step-2] → completed/
Commit: [commit-hash-from-step-4] - [commit-message]
PR: [pr-url-from-step-5]

Summary:
- Created conventional git branch
- Generated comprehensive PRP with deep codebase analysis
- Executed all [X] tasks with validation
- Committed changes with conventional format
- Pushed and created GitHub pull request

The feature is now ready for review!
```

---

## Error Handling

If any step fails:
1. **STOP immediately** - do not proceed to next step
2. Report which step failed and the error message
3. Provide actionable guidance for fixing the issue
4. Do NOT attempt automatic retry without user confirmation

---

## Design Rationale

**Subagent Delegation (Steps 1, 2, 4, 5)**:
- Simple, isolated tasks
- Don't need conversation context
- Benefit from fresh context windows
- Can run independently

**Main Agent Execution (Step 3)**:
- Complex, multi-task execution
- Requires conversation continuity
- Needs full context and state management
- May require user interaction
- Long-running operation (10-50+ sequential tasks)

This hybrid approach optimizes:
- **Context window usage**: Subagents for simple tasks don't pollute main context
- **Performance**: Isolated tasks complete faster in dedicated contexts
- **Reliability**: Complex execution stays in main agent with full capabilities
- **User experience**: Main agent maintains conversation for complex work

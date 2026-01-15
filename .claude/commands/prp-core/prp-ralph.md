---
description: Start autonomous Ralph loop to execute PRP plan until all validations pass
argument-hint: <plan.md|prd.md> [--max-iterations N]
---

# PRP Ralph Loop

**Input**: $ARGUMENTS

---

## Your Mission

Start an autonomous Ralph loop that executes a PRP plan iteratively until all validations pass.

**Core Philosophy**: Self-referential feedback loop. Each iteration, you see your previous work in files and git history. You implement, validate, fix, repeat - until complete.

**Skill Reference**: The `prp-ralph-loop` skill provides detailed execution guidance. It will be automatically available during loop iterations.

---

## Phase 1: PARSE - Validate Input

### 1.1 Parse Arguments

Extract from input:
- **File path**: Must end in `.plan.md` or `.prd.md`
- **Max iterations**: `--max-iterations N` (default: 20)

### 1.2 Validate Input Type

| Input | Action |
|-------|--------|
| Ends with `.plan.md` | Valid - use as plan file |
| Ends with `.prd.md` | Valid - will select next phase |
| Free-form text | STOP with message below |
| No input | STOP with message below |

**If invalid input:**
```
Ralph requires a PRP plan or PRD file.

Create one first:
  /prp-plan "your feature description"   # Creates plan from description
  /prp-prd "your product idea"           # Creates PRD with phases

Then run:
  /prp-ralph .claude/PRPs/plans/your-feature.plan.md --max-iterations 20
```

### 1.3 Verify File Exists

```bash
test -f "{file_path}" && echo "EXISTS" || echo "NOT_FOUND"
```

**If NOT_FOUND**: Stop with error message.

### 1.4 If PRD File - Select Next Phase

If input is a `.prd.md` file:
1. Read the PRD
2. Parse Implementation Phases table
3. Find first phase with `Status: pending` where dependencies are `complete`
4. Report which phase will be executed
5. Note: The loop will create and execute a plan for this phase

**PHASE_1_CHECKPOINT:**
- [ ] Input parsed (file path + max iterations)
- [ ] File exists and is valid type
- [ ] If PRD: next phase identified

---

## Phase 2: SETUP - Initialize Ralph Loop

### 2.1 Create State File

Create `.claude/prp-ralph.state.md`:

```bash
mkdir -p .claude
mkdir -p .claude/PRPs/ralph-archives
```

Write state file with this structure:

```markdown
---
iteration: 1
max_iterations: {N}
plan_path: "{file_path}"
input_type: "{plan|prd}"
started_at: "{ISO timestamp}"
---

# PRP Ralph Loop State

## Codebase Patterns
(Consolidate reusable patterns here - future iterations read this first)

## Current Task
Execute PRP plan and iterate until all validations pass.

## Plan Reference
{file_path}

## Instructions
1. Read the plan file
2. Implement all incomplete tasks
3. Run ALL validation commands from the plan
4. If any validation fails: fix and re-validate
5. Update plan file: mark completed tasks, add notes
6. When ALL validations pass: output <promise>COMPLETE</promise>

## Progress Log
(Append learnings after each iteration)

---
```

### 2.2 Display Startup Message

```markdown
## PRP Ralph Loop Activated

**Plan**: {file_path}
**Iteration**: 1
**Max iterations**: {N}

The stop hook is now active. When you try to exit:
- If validations incomplete → same prompt fed back
- If all validations pass → loop exits

To monitor: `cat .claude/prp-ralph.state.md`
To cancel: `/prp-ralph-cancel`

---

CRITICAL REQUIREMENTS:
- Work through ALL tasks in the plan
- Run ALL validation commands
- Fix failures before proceeding
- Only output <promise>COMPLETE</promise> when ALL validations pass
- Do NOT lie to exit - the loop continues until genuinely complete

---

Starting iteration 1...
```

### 2.3 Initialize Memory System

Create complete memory directory structure (5 layers, 9 files):

```bash
# Create all memory directories
mkdir -p .claude/prp-memory/working
mkdir -p .claude/prp-memory/episodic
mkdir -p .claude/prp-memory/semantic
mkdir -p .claude/prp-memory/procedural
mkdir -p .claude/prp-memory/learned

# Working memory (rebuilt each session)
echo '{"version":3,"computedAt":null,"sessionId":null,"activeFeature":null,"relevantMemory":{"recentDecisions":[],"projectPatterns":[],"avoidApproaches":[],"learnedRules":[]},"currentTask":null,"compilationLog":[]}' > .claude/prp-memory/working/context.json

# Episodic memory (rolling window)
if [ ! -f .claude/prp-memory/episodic/decisions.json ]; then
  echo '{"version":3,"maxEntries":50,"entries":[]}' > .claude/prp-memory/episodic/decisions.json
fi

# Semantic memory (project knowledge)
if [ ! -f .claude/prp-memory/semantic/architecture.json ]; then
  echo '{"version":3,"projectType":null,"techStack":{},"structure":{},"patterns":{},"discoveredAt":null,"lastUpdated":null}' > .claude/prp-memory/semantic/architecture.json
fi

if [ ! -f .claude/prp-memory/semantic/entities.json ]; then
  echo '{"version":3,"entities":[]}' > .claude/prp-memory/semantic/entities.json
fi

if [ ! -f .claude/prp-memory/semantic/constraints.json ]; then
  echo '{"version":3,"constraints":[],"rules":[]}' > .claude/prp-memory/semantic/constraints.json
fi

# Procedural memory (failures, successes, patterns)
if [ ! -f .claude/prp-memory/procedural/failures.json ]; then
  echo '{"version":3,"entries":[]}' > .claude/prp-memory/procedural/failures.json
fi

if [ ! -f .claude/prp-memory/procedural/successes.json ]; then
  echo '{"version":3,"entries":[]}' > .claude/prp-memory/procedural/successes.json
fi

if [ ! -f .claude/prp-memory/procedural/patterns.json ]; then
  echo '{"version":3,"patterns":{"codePatterns":[],"namingConventions":{},"projectSpecificRules":[]}}' > .claude/prp-memory/procedural/patterns.json
fi

# Learned rules
if [ ! -f .claude/prp-memory/learned/rules.json ]; then
  echo '{"version":3,"lastUpdated":null,"metadata":{"totalRules":0,"projectSpecific":0,"general":0,"lastReflection":null},"rules":[]}' > .claude/prp-memory/learned/rules.json
fi
```

### 2.4 Compile Working Context

Build fresh, relevant context from all memory layers:

1. **Generate session ID:**
   ```
   sessionId = "ralph-{plan-name}-{ISO-timestamp}"
   ```

2. **Read plan file to extract:**
   - Task description
   - Related files
   - Acceptance criteria

3. **Query procedural memory for failures to AVOID:**
   ```bash
   cat .claude/prp-memory/procedural/failures.json
   ```
   - Filter entries where `files` overlap with plan's related files
   - Filter entries where `approach` contains similar keywords
   - Take top 5 most recent relevant failures
   - Add to `relevantMemory.avoidApproaches`

4. **Query procedural memory for successful patterns:**
   ```bash
   cat .claude/prp-memory/procedural/successes.json
   ```
   - Filter for similar file patterns or task types
   - Take top 5 most relevant successes
   - Add to `relevantMemory.projectPatterns`

5. **Query episodic memory for recent decisions:**
   ```bash
   cat .claude/prp-memory/episodic/decisions.json
   ```
   - Get entries from last 7 days OR last 20 entries (whichever is smaller)
   - Add to `relevantMemory.recentDecisions`

6. **Load applicable learned rules:**
   ```bash
   cat .claude/prp-memory/learned/rules.json
   ```
   - Filter rules where `active: true`
   - Filter rules where `applicability.always: true` OR file patterns match
   - Add to `relevantMemory.learnedRules`

7. **Write compiled context to working/context.json**

8. **Display memory summary:**
   ```
   ┌─────────────────────────────────────────────────────────────────┐
   │  MEMORY CONTEXT COMPILED                                        │
   ├─────────────────────────────────────────────────────────────────┤
   │  Recent decisions: {N} loaded                                   │
   │  Success patterns: {N} loaded                                   │
   │  Approaches to AVOID: {N} loaded                                │
   │  Learned rules: {N} applied                                     │
   └─────────────────────────────────────────────────────────────────┘
   ```

   If `avoidApproaches` has entries, display prominently:
   ```
   ⚠️  APPROACHES TO AVOID (from past failures):
   - {failure.approach} → {failure.rootCause}
   ```

### 2.5 Discover Semantic Memory (First Run Only)

Auto-detect project architecture on first run:

1. **Check if semantic memory is populated:**
   ```bash
   cat .claude/prp-memory/semantic/architecture.json
   ```
   If `projectType` is null, run discovery.

2. **Detect project type:**
   ```bash
   # Check for package.json
   if [ -f "package.json" ]; then
     # Check for Next.js
     grep -q '"next"' package.json && echo "nextjs"
     # Check for React
     grep -q '"react"' package.json && echo "react"
   elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
     echo "python"
   elif [ -f "Cargo.toml" ]; then
     echo "rust"
   elif [ -f "go.mod" ]; then
     echo "go"
   fi
   ```

3. **Extract tech stack from config files:**
   - Framework from package.json/requirements.txt
   - Language (TypeScript/JavaScript/Python)
   - Database from dependencies
   - Test framework from devDependencies

4. **Discover project structure:**
   - Entry points (src/app/, src/index.ts, main.py)
   - Component directories
   - API routes
   - Test directories

5. **Write to semantic/architecture.json**

6. **Log discovery:**
   ```
   Discovered project architecture:
   - Type: {projectType}
   - Framework: {framework}
   - Language: {language}
   ```

**PHASE_2_CHECKPOINT:**
- [ ] State file created
- [ ] Archive directory exists
- [ ] Startup message displayed
- [ ] All memory directories exist (5 layers)
- [ ] All JSON files initialized (9 files)
- [ ] Working context compiled
- [ ] Semantic memory discovered (first run only)

---

## Phase 3: EXECUTE - Work on Plan

### 3.0 Failure Prevention Check (Memory System)

**BEFORE implementing anything:**

1. **Read failures.json:**
   ```bash
   cat .claude/prp-memory/procedural/failures.json
   ```

2. **Read patterns.json for known patterns:**
   ```bash
   cat .claude/prp-memory/procedural/patterns.json
   ```

3. **Check for similar patterns:**
   - Compare planned approach with documented failures
   - Check if similar files are affected
   - Check if similar error messages occurred in the past
   - Check `patterns.codePatterns` for applicable patterns

4. **If failure match found - WARN:**
   ```
   ⚠️  SIMILAR APPROACH FAILED BEFORE

   Failure ID: {id}
   When: {timestamp}
   Approach: {approach}
   Files: {files}
   Error: {errors}
   Root Cause: {rootCause}

   Prevention Tip: {prevention}
   ```

5. **Check successes.json for alternatives:**
   ```bash
   cat .claude/prp-memory/procedural/successes.json
   ```

   If a successful approach exists for a similar problem:
   ```
   ✅ SUCCESSFUL ALTERNATIVE EXISTS

   Approach: {approach}
   Why it worked: {whyItWorked}
   Pattern: {pattern}
   ```

6. **Display applicable code patterns:**
   If `patterns.codePatterns` has relevant entries:
   ```
   📋 KNOWN PATTERNS TO APPLY:
   - {pattern.name}: {pattern.description}
   ```

### 3.0.5 Load Learned Rules

Display applicable learned rules before implementation:

1. **Read learned rules:**
   ```bash
   cat .claude/prp-memory/learned/rules.json
   ```

2. **Filter applicable rules:**
   - Include rules where `active: true` (or no active field)
   - Include rules where `applicability.always: true`
   - Include rules where `applicability.filePatterns` overlap with current task files

3. **Display if rules found:**
   ```
   ┌─────────────────────────────────────────────────────────────────┐
   │  LEARNED RULES (from user corrections)                          │
   ├─────────────────────────────────────────────────────────────────┤
   │  Rule: {rule.rule}                                              │
   │  Example: {rule.example}                                        │
   └─────────────────────────────────────────────────────────────────┘
   ```

4. **Apply rules during implementation:**
   - Reference rules when making relevant decisions
   - Note rule application in progress log

### 3.1 Read Context First

Before implementing anything:
1. Read the state file - check "Codebase Patterns" section
2. Read the plan file - understand all tasks
3. Check git status - what's already changed?
4. Review progress log - what did previous iterations do?

### 3.2 Identify Work

From the plan, identify:
- Tasks not yet completed
- Validation commands to run
- Acceptance criteria to meet

### 3.3 Implement

For each incomplete task:
1. Read the task requirements
2. Read any MIRROR/pattern references
3. Implement the change
4. Run task-specific validation if specified

### 3.4 Validate

Run ALL validation commands from the plan:

```bash
# Typical validation levels (adapt to plan)
bun run type-check || npm run type-check
bun run lint || npm run lint
bun test || npm test
bun run build || npm run build
```

### 3.5 Track Results

| Check | Result | Notes |
|-------|--------|-------|
| Type check | PASS/FAIL | {details} |
| Lint | PASS/FAIL | {details} |
| Tests | PASS/FAIL | {details} |
| Build | PASS/FAIL | {details} |

### 3.6 If Any Validation Fails

1. Analyze the failure
2. Fix the issue
3. Re-run validation
4. Repeat until passing

### 3.7 Update Plan File

After each significant change:
- Mark completed tasks with checkboxes
- Add notes about what was done
- Document any deviations

### 3.8 Update State File Progress Log

Append to Progress Log section using this format:

```markdown
## Iteration {N} - {ISO timestamp}

### Completed
- {Task 1 summary}
- {Task 2 summary}

### Validation Status
- Type-check: PASS/FAIL ({error count if failing})
- Lint: PASS/FAIL
- Tests: PASS/FAIL ({X/Y passing})
- Build: PASS/FAIL

### Learnings
- {Pattern discovered: "this codebase uses X for Y"}
- {Gotcha found: "don't forget to Z when doing W"}
- {Context: "the component X is in directory Y"}

### Next Steps
- {What still needs to be done}
- {Specific blockers to address}

---
```

### 3.9 Consolidate Codebase Patterns

If you discover a **reusable pattern**, add it to the "Codebase Patterns" section at the TOP of the state file:

```markdown
## Codebase Patterns
- Use `sql<number>` template for type-safe SQL aggregations
- Always use `IF NOT EXISTS` in migrations
- Export types from actions.ts for UI components
- Form validation uses zod schemas in /lib/validations
```

Only add patterns that are **general and reusable**, not iteration-specific.

### 3.10 Record to Memory (After Validation)

After EVERY validation (whether successful or not):

#### On FAILED Validation:

1. **Append to failures.json:**
   ```json
   {
     "id": "fail-{YYYYMMDD}-{SEQ}",
     "timestamp": "{ISO-TIMESTAMP}",
     "plan": "{plan_path}",
     "iteration": {iteration_number},
     "approach": "{What was attempted - 1-2 sentences}",
     "files": ["{Affected files}"],
     "errors": ["{Exact error messages}"],
     "rootCause": "{Analysis of WHY it failed}",
     "prevention": "{How to avoid this in the future}",
     "category": "{ssr-hydration|type-error|import|test|build|lint|other}"
   }
   ```

2. **Record decision to episodic memory (decisions.json):**
   ```json
   {
     "id": "dec-{YYYYMMDD}-{SEQ}",
     "timestamp": "{ISO-TIMESTAMP}",
     "feature": "{plan_path}",
     "decision": "Attempted {approach}",
     "rationale": "Based on {reasoning}",
     "alternatives": [],
     "impact": "{files}"
   }
   ```

**IMPORTANT:**
- `rootCause` must be a REAL analysis, not just repeating the error message
- `prevention` must be ACTIONABLE
- `category` helps with future pattern matching

#### On SUCCESSFUL Validation:

1. **Append to successes.json:**
   ```json
   {
     "id": "suc-{YYYYMMDD}-{SEQ}",
     "timestamp": "{ISO-TIMESTAMP}",
     "plan": "{plan_path}",
     "approach": "{What worked - 1-2 sentences}",
     "files": ["{Affected files}"],
     "whyItWorked": "{Why this approach was successful}",
     "pattern": "{Reusable pattern for similar problems}",
     "verificationResults": {
       "build": "PASS|FAIL",
       "tests": "PASS|FAIL ({X}/{Y})",
       "lint": "PASS|FAIL",
       "typecheck": "PASS|FAIL"
     },
     "lessons": ["{Key takeaways}"]
   }
   ```

2. **Record decision to episodic memory (decisions.json):**
   ```json
   {
     "id": "dec-{YYYYMMDD}-{SEQ}",
     "timestamp": "{ISO-TIMESTAMP}",
     "feature": "{plan_path}",
     "decision": "Successfully used {approach}",
     "rationale": "{Why this worked}",
     "alternatives": ["{What was tried before}"],
     "impact": "{files}"
   }
   ```

3. **Prune episodic memory if > 50 entries:**
   - Remove oldest entries (FIFO)
   - Keep max 50 entries

**IMPORTANT:**
- Only document SIGNIFICANT successes (not every small fix)
- `pattern` should be generalizable
- `lessons` capture key insights for future reference

### 3.11 Extract Patterns

After successful validation, analyze for generalizable patterns:

1. **Check if pattern already exists:**
   ```bash
   cat .claude/prp-memory/procedural/patterns.json
   ```

2. **Identify new patterns from success:**
   - Code structures that can be reused
   - Naming conventions discovered
   - Project-specific rules observed

3. **If new pattern detected, add to patterns.json:**
   ```json
   {
     "id": "pattern-{YYYYMMDD}-{SEQ}",
     "name": "{Pattern name}",
     "description": "{What the pattern does}",
     "example": "{Code example}",
     "extractedFrom": "{success-id}",
     "applicability": ["{keywords for matching}"]
   }
   ```

4. **Update naming conventions if new convention detected:**
   - Add to `patterns.namingConventions`

5. **Update project-specific rules if applicable:**
   - Add to `patterns.projectSpecificRules`

**PHASE_3_CHECKPOINT:**
- [ ] Context read (patterns, previous progress)
- [ ] All tasks attempted
- [ ] All validations run
- [ ] Plan file updated
- [ ] State file progress log updated
- [ ] Patterns consolidated if discovered
- [ ] Memory updated (failures or successes recorded)
- [ ] Episodic decisions recorded
- [ ] Patterns extracted (if successful)

---

## Phase 4: COMPLETION CHECK

### 4.1 Verify All Validations Pass

ALL of these must be true:
- [ ] All tasks in plan completed
- [ ] Type check passes
- [ ] Lint passes (0 errors)
- [ ] Tests pass
- [ ] Build succeeds
- [ ] All acceptance criteria met

### 4.2 If ALL Pass - Complete the Loop

1. **Generate Implementation Report**

   Create `.claude/PRPs/reports/{plan-name}-report.md`:

   ```markdown
   # Implementation Report

   **Plan**: {plan_path}
   **Completed**: {timestamp}
   **Iterations**: {N}

   ## Summary
   {What was implemented}

   ## Tasks Completed
   {List from plan}

   ## Validation Results
   | Check | Result |
   |-------|--------|
   | Type check | PASS |
   | Lint | PASS |
   | Tests | PASS |
   | Build | PASS |

   ## Codebase Patterns Discovered
   {From state file Codebase Patterns section}

   ## Learnings
   {Consolidated from state file progress log}

   ## Deviations from Plan
   {Any changes made}
   ```

2. **Archive the Ralph Run**

   ```bash
   # Create archive directory
   DATE=$(date +%Y-%m-%d)
   PLAN_NAME=$(basename {plan_path} .plan.md)
   ARCHIVE_DIR=".claude/PRPs/ralph-archives/${DATE}-${PLAN_NAME}"
   mkdir -p "$ARCHIVE_DIR"

   # Copy state file (with all learnings)
   cp .claude/prp-ralph.state.md "$ARCHIVE_DIR/state.md"

   # Copy the plan
   cp {plan_path} "$ARCHIVE_DIR/plan.md"

   # Extract consolidated learnings
   # (The report serves as learnings.md)
   cp .claude/PRPs/reports/{plan-name}-report.md "$ARCHIVE_DIR/learnings.md"
   ```

3. **Update CLAUDE.md with Permanent Patterns (if applicable)**

   If any patterns from "Codebase Patterns" section are significant enough to be permanent project knowledge:

   - Read the project's CLAUDE.md
   - Add new patterns to appropriate section
   - Avoid duplicating existing patterns

   Example addition:
   ```markdown
   ## Patterns Discovered via Ralph
   - {Pattern that should be permanent}
   ```

4. **Archive Plan to Completed**

   ```bash
   mkdir -p .claude/PRPs/plans/completed
   mv {plan_path} .claude/PRPs/plans/completed/
   ```

5. **Clean Up State**

   ```bash
   rm .claude/prp-ralph.state.md
   ```

6. **Output Completion Promise**

   ```
   <promise>COMPLETE</promise>
   ```

### 4.3 If NOT All Pass - End Iteration

If validations are not all passing:
- Document current state in progress log
- End your response normally
- The stop hook will feed the prompt back for next iteration

**Do NOT output the completion promise if validations are failing.**

### 4.4 Extract Learned Rules (Optional)

If the user made corrections during the loop:

1. **Identify the correction:**
   - What did the user say?
   - What was wrong with the original approach?

2. **Generalize to a rule:**
   - Not project-specific, but generally applicable
   - Include a concrete example

3. **Append to learned/rules.json:**
   ```json
   {
     "id": "rule-{YYYYMMDD}-{SEQ}",
     "timestamp": "{ISO-TIMESTAMP}",
     "trigger": "{What triggered the correction}",
     "rule": "{Generalized rule}",
     "example": "{Concrete example: WRONG vs RIGHT}",
     "source": "user-correction",
     "confidence": "high|medium|low",
     "active": true,
     "applicability": {
       "always": false,
       "features": [],
       "filePatterns": ["{patterns where rule applies}"]
     }
   }
   ```

4. **Update rules.json metadata:**
   ```json
   {
     "lastUpdated": "{ISO-TIMESTAMP}",
     "metadata": {
       "totalRules": {N+1},
       "projectSpecific": {count},
       "general": {count},
       "lastReflection": "{ISO-TIMESTAMP}"
     }
   }
   ```

**Detection triggers for user corrections:**
- User says "Korrektur:", "Correction:", "Wrong:", "Falsch:"
- User explicitly corrects an approach
- User provides alternative that worked

**Confidence levels:**
- `high`: User explicitly stated the rule
- `medium`: Rule inferred from correction
- `low`: Pattern observed but not confirmed

### 4.5 Update Semantic Memory

After successful completion, update semantic memory with new discoveries:

1. **Identify new entities created/modified:**
   - Components, services, hooks, API routes
   - Read files that were created during the loop

2. **Update entities.json with new entities:**
   ```json
   {
     "id": "entity-{YYYYMMDD}-{SEQ}",
     "name": "{EntityName}",
     "type": "{component|service|hook|api|test}",
     "file": "{file path}",
     "description": "{What it does}",
     "dependencies": ["{imports}"],
     "dependents": [],
     "discoveredAt": "{ISO-TIMESTAMP}"
   }
   ```

3. **Update architecture.json structure:**
   - Add new entry points if discovered
   - Add new component paths
   - Add new API routes
   - Add new test patterns

4. **Update constraints.json if new constraints discovered:**
   - Technical constraints (e.g., "must use edge runtime")
   - Convention rules (e.g., "use server actions for forms")

5. **Update lastUpdated timestamp in architecture.json**

---

## Handling Edge Cases

### Max Iterations Reached

If iteration count reaches max_iterations:
- Document what's incomplete
- Document what's blocking
- Archive current state (even if incomplete)
- Suggest next steps
- Loop will exit automatically (stop hook handles this)

### Stuck on Same Issue

If you notice you're stuck (same error multiple iterations):
1. Document the blocker clearly in progress log
2. Check "Codebase Patterns" - maybe there's a hint
3. Try alternative approaches
4. If truly stuck, document for human review

### Plan Has Errors

If the plan itself has issues:
- Document the problems in progress log
- Suggest corrections
- Continue with what's executable

---

## Learnings Feedback System

The Ralph loop captures learnings that can improve the system:

### During Loop
- **Codebase Patterns**: Added to state file, read by future iterations
- **Progress Log**: Detailed notes on what worked/failed

### After Completion
- **Archive**: Full state preserved in `.claude/PRPs/ralph-archives/`
- **Report**: Consolidated learnings in report file
- **CLAUDE.md Updates**: Permanent patterns added to project config

### Using Archives for Improvement

Archives can be used to:
1. Train better PRP plan generation
2. Identify common failure patterns
3. Improve validation command suggestions
4. Update skill documentation with real examples

```bash
# List all Ralph archives
ls -la .claude/PRPs/ralph-archives/

# Review learnings from a specific run
cat .claude/PRPs/ralph-archives/2024-01-12-feature-name/learnings.md
```

---

## Success Criteria

- **PLAN_EXECUTED**: All tasks from plan completed
- **VALIDATIONS_PASS**: All validation commands succeed
- **REPORT_GENERATED**: Implementation report created
- **LEARNINGS_CAPTURED**: Progress log has useful insights
- **PATTERNS_CONSOLIDATED**: Reusable patterns extracted
- **ARCHIVE_CREATED**: Full run archived for future reference
- **CLEAN_EXIT**: Completion promise output only when genuinely complete

# PRP Commands for Dummies

## What is PRP?

**PRP = PRD + codebase intelligence + validation loop**

You give the AI a detailed plan with context and validation commands. The AI implements, tests, and self-corrects until everything passes.

---

## The Commands (New Simplified Flow)

### Core Workflow

| Command          | What it does                                    |
| ---------------- | ----------------------------------------------- |
| `/prp-prd`       | Create a PRD with implementation phases         |
| `/prp-plan`      | Create an implementation plan                   |
| `/prp-implement` | Execute a plan with validation loops            |
| `/prp-ralph`     | Autonomous loop until all validations pass      |

### Issue & Debug Workflow

| Command                  | What it does                          |
| ------------------------ | ------------------------------------- |
| `/prp-issue-investigate` | Analyze a GitHub issue, create a plan |
| `/prp-issue-fix`         | Implement the fix                     |
| `/prp-debug`             | Deep root cause analysis (5 Whys)     |

### Git & Review

| Command       | What it does                              |
| ------------- | ----------------------------------------- |
| `/prp-commit` | Smart commit with natural language targeting |
| `/prp-pr`     | Create a pull request                     |
| `/prp-review` | Review a pull request                     |

---

## The Basic Flow

### For Big Features

```
/prp-prd "user authentication system"
    ↓
Creates PRD with phases (stored in .claude/PRPs/prds/)
    ↓
/prp-plan .claude/PRPs/prds/user-auth.prd.md
    ↓
Creates implementation plan for next phase
    ↓
/prp-implement .claude/PRPs/plans/user-auth-phase-1.plan.md
    ↓
Executes plan, runs validations, fixes failures
    ↓
Repeat /prp-plan for next phase
```

### For Medium Features

Skip the PRD. Go straight to a plan:

```
/prp-plan "add pagination to the API"
    ↓
/prp-implement .claude/PRPs/plans/add-pagination.plan.md
```

### For Bug Fixes (GitHub Issues)

```
/prp-issue-investigate 123
    ↓
/prp-issue-fix 123
```

### For Debugging (Errors, Stack Traces)

```
/prp-debug "TypeError: Cannot read property 'x' of undefined"
    ↓
Creates RCA report with root cause and fix specification
```

---

## The Ralph Loop (Autonomous Mode)

Instead of `/prp-implement`, use `/prp-ralph` for fully autonomous execution:

```
/prp-ralph .claude/PRPs/plans/my-feature.plan.md --max-iterations 20
```

This runs in a loop:
1. Implements the plan
2. Runs all validations
3. If something fails → fixes it → re-validates
4. Keeps going until everything passes
5. Exits when done

Go make coffee. Come back to working code (or a progress log).

**Cancel with:** `/prp-ralph-cancel`

---

## The Git Flow

After implementation:

```
/prp-commit                    # Stage and commit with smart message
/prp-pr                        # Create pull request
/prp-review 123                # Review someone else's PR
```

---

## Where Stuff Gets Saved

```
.claude/PRPs/
├── prds/              # PRD documents
├── plans/             # Implementation plans
│   └── completed/     # Archived plans
├── reports/           # Implementation reports
├── issues/            # Issue investigations
└── reviews/           # PR reviews
```

---

## Quick Examples

### "I have a rough idea"

```bash
/prp-prd "I want users to be able to like posts"
```

This asks you clarifying questions, does research, and creates a structured PRD with phases.

### "I know what I want to build"

```bash
/prp-plan "add a like button to posts with real-time count updates"
```

Creates a detailed implementation plan with tasks and validation commands.

### "Just build it"

```bash
/prp-ralph .claude/PRPs/plans/like-button.plan.md --max-iterations 15
```

Autonomous execution until done.

### "There's a bug"

```bash
/prp-issue-investigate 456
/prp-issue-fix 456
```

### "I'm done, let's commit"

```bash
/prp-commit typescript files except tests
/prp-pr
```

---

## Tips

1. **Context is king** - The more context in your plan, the better the output
2. **Validation matters** - Plans with test commands work better than plans without
3. **Use Ralph for big stuff** - Let it iterate instead of babysitting
4. **Max iterations** - Always set `--max-iterations` on Ralph loops
5. **Start specific** - "Add OAuth2 with Google" beats "add authentication"

---

## The Old Commands

Previous commands like `/prp-base-create`, `/prp-spec-create`, `/api-contract-define`, etc. are preserved in `old-prp-commands/` for reference. The new streamlined flow replaces all of them.

---

## That's It

1. Big feature? → `/prp-prd` → `/prp-plan` → `/prp-ralph`
2. Medium feature? → `/prp-plan` → `/prp-implement`
3. GitHub issue? → `/prp-issue-investigate` → `/prp-issue-fix`
4. Weird bug? → `/prp-debug "error message"`
5. Done? → `/prp-commit` → `/prp-pr`

Happy building.

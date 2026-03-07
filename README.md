# PRP (Product Requirement Prompts)

A collection of prompts for AI-assisted development with Claude Code.

## Video Walkthrough

https://www.youtube.com/watch?v=KVOZ9s1S9Gk&lc=UgzfwxvFjo6pKEyPo1R4AaABAg

### Support This Work

**Found value in these resources?**

**Buy me a coffee:** https://coff.ee/wirasm

I spent a considerable amount of time creating these resources and prompts. If you find value in this project, please consider buying me a coffee to support my work.

---

### Transform Your Team with AI Engineering Workshops

**Ready to move beyond toy demos to production-ready AI systems?**

**Book a workshop:** https://www.rasmuswiding.com/

**What you'll get:**

- Put your team on a path to become AI power users
- Learn the exact PRP methodology used by top engineering teams
- Hands-on training with Claude Code, PRPs, and real codebases
- From beginner to advanced AI engineering workshops for teams and individuals

**Perfect for:** Engineering teams, Product teams, and developers who want AI that actually works in production

Contact me directly at hello@rasmuswiding.com

---

## What is PRP?

**Product Requirement Prompt (PRP)** = PRD + curated codebase intelligence + agent/runbook

The minimum viable packet an AI needs to ship production-ready code on the first pass.

A PRP keeps the goal and justification sections of a traditional PRD yet adds AI-critical layers:

- **Context**: Precise file paths, library versions, code snippet examples
- **Patterns**: Existing codebase conventions to follow
- **Validation**: Executable commands the AI can run to verify its work

---

## Quick Start

```bash
# Copy commands into your project
cp -r /path/to/PRPs-agentic-eng/.claude/commands/prp-core .claude/commands/

# Or clone the repo
git clone https://github.com/Wirasm/PRPs-agentic-eng.git
```

---

## Commands Reference

All commands live in `.claude/commands/prp-core/` and are invoked with `/` in Claude Code.

### Core Workflow

| Command | Args | Description |
|---------|------|-------------|
| `/prp-prd` | `[feature idea]` | Interactive PRD generator — problem-first, hypothesis-driven, with phased implementation table |
| `/prp-plan` | `<description \| path/to/prd.md>` | Create implementation plan (auto-selects next PRD phase if given a PRD) |
| `/prp-implement` | `<path/to/plan.md>` | Execute plan with validation loops (type-check, lint, test, build) |

### Issue & Debug

| Command | Args | Description |
|---------|------|-------------|
| `/prp-issue-investigate` | `<issue-number \| url \| "description">` | Analyze issue with parallel codebase agents + 5 Whys RCA |
| `/prp-issue-fix` | `<issue-number \| artifact-path>` | Implement fix from investigation, create PR, self-review |
| `/prp-debug` | `<error \| stacktrace> [--quick]` | Deep root cause analysis (5 Whys, or 2-3 with `--quick`) |

### Git & Review

| Command | Args | Description |
|---------|------|-------------|
| `/prp-commit` | `[target]` | Smart commit with natural language targeting (`"typescript files"`, `"except tests"`, `"staged"`) |
| `/prp-pr` | `[base-branch]` | Push & create PR with template support |
| `/prp-review` | `<pr-number> [--approve \| --request-changes]` | Single-agent comprehensive PR review |
| `/prp-review-agents` | `<pr-number> [aspects]` | Multi-agent review (7 specialists: code, tests, types, docs, errors, comments, simplify) |

### Research

| Command | Args | Description |
|---------|------|-------------|
| `/prp-codebase-question` | `<question> [--web] [--follow-up]` | Research-only codebase exploration with parallel agents |

### Autonomous Loop (Ralph)

| Command | Args | Description |
|---------|------|-------------|
| `/prp-ralph` | `<plan.md \| prd.md> [--max-iterations N]` | Implement → validate → fix → repeat until all checks pass |
| `/prp-ralph-cancel` | — | Cancel active Ralph loop |

### Batch Commands

Run multiple operations in a single session. The agent analyzes your input, determines the optimal number of items to generate, then invokes the corresponding single command for each.

| Command | Args | Description |
|---------|------|-------------|
| `/prp-prd-batch` | `<initiative or feature list>` | Generate multiple PRDs from a broad initiative or feature list |
| `/prp-plan-batch` | `<prd-path \| list of features>` | Generate plans for all pending PRD phases or a list of features |
| `/prp-commit-batch` | `[grouping strategy]` | Split working tree changes into logical commits |
| `/prp-pr-batch` | `[base-branch]` | Create PRs for multiple feature branches |

---

## Workflow Patterns

### 1. Large Feature: PRD → Plan → Implement

```
/prp-prd "user authentication system"
    → .claude/PRPs/prds/user-auth.prd.md  (with phased implementation table)

/prp-plan .claude/PRPs/prds/user-auth.prd.md
    → auto-selects next pending phase, creates plan

/prp-implement .claude/PRPs/plans/user-auth-phase-1.plan.md
    → executes, validates, archives plan, updates PRD status

Repeat /prp-plan for next phase.
```

### 2. Medium Feature: Direct to Plan

```
/prp-plan "add pagination to the API"
/prp-implement .claude/PRPs/plans/add-pagination.plan.md
```

### 3. Bug Fix: Issue Workflow

```
/prp-issue-investigate 123
/prp-issue-fix 123          → creates PR with self-review
```

### 4. Autonomous: Ralph Loop

```
/prp-plan "add JWT authentication"
/prp-ralph .claude/PRPs/plans/add-jwt-auth.plan.md --max-iterations 20
```

Ralph iterates (implement → validate → fix) until all checks pass, then exits.

### 5. Batch: Multiple PRDs from Initiative

```
/prp-prd-batch "Build a multi-tenant SaaS platform with auth, billing, and admin dashboard"
    → agent determines 3 PRDs needed, generates each using /prp-prd
```

### 6. Parallel Development with Worktrees

When PRD phases are marked parallel:

```bash
git worktree add -b phase-3-ui ../project-phase-3
git worktree add -b phase-4-tests ../project-phase-4
# Run Claude in each worktree independently
```

---

## Architecture: Agents & Patterns

Commands use specialized subagents for intelligence gathering:

| Agent | Purpose |
|-------|---------|
| `codebase-explorer` | Finds WHERE code lives — files, patterns, conventions |
| `codebase-analyst` | Understands HOW code works — data flow, integration points |
| `web-researcher` | External docs, APIs, best practices, market research |
| `code-reviewer` | Guideline compliance, bugs, quality (high-confidence only) |
| `code-simplifier` | Simplifies code while preserving behavior (can push to PR) |
| `docs-impact-agent` | Updates docs affected by code changes (can push to PR) |
| `pr-test-analyzer` | Behavioral test coverage analysis |
| `silent-failure-hunter` | Finds swallowed errors, empty catches, silent fallbacks |
| `type-design-analyzer` | Type design quality (encapsulation, invariants, enforcement) |
| `comment-analyzer` | Verifies comments match actual behavior |

**Common dispatch patterns:**
- **Parallel dual-agent**: `codebase-explorer` + `codebase-analyst` (used by `prp-plan`, `prp-prd`, `prp-issue-investigate`)
- **Sequential triple**: codebase agents first → `web-researcher` second
- **Multi-agent review**: 7 specialists dispatched by `prp-review-agents`

---

## Artifacts Structure

```
.claude/PRPs/
├── prds/              # Product requirement documents
├── plans/             # Implementation plans
│   └── completed/     # Archived completed plans
├── reports/           # Implementation reports
├── issues/            # Issue investigation artifacts
│   └── completed/     # Archived completed investigations
├── reviews/           # PR review reports
├── research/          # Codebase question outputs
├── debug/             # Root cause analysis reports
└── ralph-archives/    # Completed Ralph loop artifacts
```

---

## Ralph Loop Setup

Add the stop hook to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/prp-ralph-stop.sh"
          }
        ]
      }
    ]
  }
}
```

---

## PRD Phase Tracking

PRDs include an Implementation Phases table:

```markdown
| # | Phase | Description | Status      | Parallel | Depends | PRP Plan |
|---|-------|-------------|-------------|----------|---------|----------|
| 1 | Auth  | User login  | complete    | -        | -       | [link]   |
| 2 | API   | Endpoints   | in-progress | -        | 1       | [link]   |
| 3 | UI    | Frontend    | pending     | with 4   | 2       | -        |
| 4 | Tests | Test suite  | pending     | with 3   | 2       | -        |
```

Status: `pending` → `in-progress` → `complete`. Phases marked parallel can run in separate worktrees.

---

## Best Practices

1. **Context is King** — Include ALL necessary docs, examples, and caveats in PRPs
2. **Validation Loops** — Provide executable tests the AI can run and fix
3. **Bounded Scope** — Each plan should be completable in one AI loop
4. **Codebase First** — Explore existing patterns before introducing new ones

---

## Project Structure

```
your-project/
├── .claude/
│   ├── commands/prp-core/   # PRP commands (copy these)
│   ├── agents/              # Specialized subagents
│   ├── hooks/               # Ralph stop hook
│   ├── skills/              # Autonomous skill definitions
│   └── PRPs/                # Generated artifacts (gitignored or committed per preference)
├── CLAUDE.md                # Project-specific AI guidelines
└── src/                     # Your source code
```

---

## Resources

- **Templates**: `PRPs/templates/` — PRP base, story/task, planning templates
- **AI Docs**: `PRPs/ai_docs/` — Curated Claude Code documentation for context injection
- **Legacy Commands**: `old-prp-commands/` — Previous command versions for reference

---

## License

MIT License

---

## Support

I spent a considerable amount of time creating these resources and prompts. If you find value in this project, please consider buying me a coffee to support my work.

**Buy me a coffee:** https://coff.ee/wirasm

---

**The goal is one-pass implementation success through comprehensive context.**

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Nature

This is a **PRP (Product Requirement Prompt) Framework** repository, not a traditional software project. The core concept: **"PRP = PRD + curated codebase intelligence + agent/runbook"** - designed to enable AI agents to ship production-ready code on the first pass.

## Core Architecture

### Command-Driven System

- **35+ pre-configured Claude Code commands** in `.claude/commands/`
- Commands organized by function:
  - `prp/` - PRP creation and execution workflows (language-agnostic)
  - `dev/` - Core development utilities (prime-core, onboarding, debug)
  - `quality/` - Review and refactoring commands
  - `lab/experimental/` - Parallel PRP creation and hackathon tools
  - `git/` - Conflict resolution and smart git operations
  - `rust/` - Rust-specific PRP and review commands
  - `go/` - Go-specific PRP and review commands  
  - `bun/` - Bun-specific PRP and review commands
  - `typescript/` - TypeScript-specific commands (legacy)

### Multi-Language Template System

- **Language-Specific PRP Templates** in `prp/templates/`:
  - `prp_base.md` - Python (default)
  - `prp_base_typescript.md` - TypeScript/JavaScript
  - `prp_base_rust.md` - Rust with cargo validation
  - `prp_base_go.md` - Go with go test validation
  - `prp_base_bun.md` - Bun with native APIs
- **Context-Rich Approach**: Every PRP must include comprehensive documentation, examples, and gotchas
- **Validation-First Design**: Each PRP contains executable validation gates specific to the language

### AI Documentation Curation

- `prp/ai_docs/` contains curated Claude Code documentation for context injection
- `claude_md_files/` provides comprehensive language-specific CLAUDE.md examples:
  - `CLAUDE-RUST.md` - Rust best practices and patterns
  - `CLAUDE-GO.md` - Go idioms and conventions
  - `CLAUDE-BUN.md` - Bun performance and TypeScript patterns
  - `CLAUDE-NODE.md` - Node.js development guidelines

## Development Commands

### PRP Execution

```bash
# Interactive mode (recommended for development)
uv run prp/scripts/prp_runner.py --prp [prp-name] --interactive

# Headless mode (for CI/CD)
uv run prp/scripts/prp_runner.py --prp [prp-name] --output-format json

# Streaming JSON (for real-time monitoring)
uv run prp/scripts/prp_runner.py --prp [prp-name] --output-format stream-json
```

### Key Claude Commands

#### Universal Commands (Language-Agnostic)
- `/prp-base-create` - Generate comprehensive PRPs with automatic language detection
- `/prp-base-execute` - Execute PRPs against codebase with language-specific validation
- `/prp-planning-create` - Create planning documents with diagrams
- `/prime-core` - Prime Claude with project context and language detection
- `/review-staged-unstaged` - Review git changes using PRP methodology

#### Language-Specific Commands
- `/rust-create-base-prp` - Rust PRP creation with cargo patterns
- `/rust-execute-base-prp` - Execute Rust PRPs with cargo validation
- `/rust-review-general` - Rust code review focusing on safety and performance
- `/go-create-base-prp` - Go PRP creation with go test patterns
- `/go-execute-base-prp` - Execute Go PRPs with go toolchain validation
- `/go-review-general` - Go code review focusing on idioms and concurrency
- `/bun-create-base-prp` - Bun PRP creation with native API patterns
- `/bun-execute-base-prp` - Execute Bun PRPs with bun test validation
- `/bun-review-general` - Bun code review focusing on performance and TypeScript

## Critical Success Patterns

### The PRP Methodology

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

### PRP Structure Requirements

- **Goal**: Specific end state and desires
- **Why**: Business value and user impact
- **What**: User-visible behavior and technical requirements
- **All Needed Context**: Documentation URLs, code examples, gotchas, patterns
- **Implementation Blueprint**: Pseudocode with critical details and task lists
- **Validation Loop**: Executable commands for syntax, tests, integration

### Validation Gates (Must be Executable)

```bash
# Level 1: Syntax & Style
ruff check --fix && mypy .

# Level 2: Unit Tests
uv run pytest tests/ -v

# Level 3: Integration
uv run uvicorn main:app --reload
curl -X POST http://localhost:8000/endpoint -H "Content-Type: application/json" -d '{...}'

# Level 4: Deployment
# mcp servers, or other creative ways to self validate
```

## Anti-Patterns to Avoid

- L Don't create minimal context prompts - context is everything - the PRP must be comprehensive and self-contained, reference relevant documentation and examples.
- L Don't skip validation steps - they're critical for one-pass success - The better The AI is at running the validation loop, the more likely it is to succeed.
- L Don't ignore the structured PRP format - it's battle-tested
- L Don't create new patterns when existing templates work
- L Don't hardcode values that should be config
- L Don't catch all exceptions - be specific

## Working with This Framework

### When Creating new PRPs

1. **Context Process**: New PRPs must consist of context sections, Context is King!
2.

### When Executing PRPs

1. **Load PRP**: Read and understand all context and requirements
2. **ULTRATHINK**: Create comprehensive plan, break down into todos, use subagents, batch tool etc check prps/ai_docs/
3. **Execute**: Implement following the blueprint
4. **Validate**: Run each validation command, fix failures
5. **Complete**: Ensure all checklist items done

### Command Usage

- Read the .claude/commands directory
- Access via `/` prefix in Claude Code
- Commands are self-documenting with argument placeholders
- Use parallel creation commands for rapid development
- Leverage existing review and refactoring commands

## Project Structure Understanding

```
PRPs-agentic-eng/
.claude/
  commands/           # 28+ Claude Code commands
  settings.local.json # Tool permissions
PRPs/
  templates/          # PRP templates with validation
  scripts/           # PRP runner and utilities
  ai_docs/           # Curated Claude Code documentation
   *.md               # Active and example PRPs
 claude_md_files/        # Framework-specific CLAUDE.md examples
 pyproject.toml         # Python package configuration
```

Remember: This framework is about **one-pass implementation success through comprehensive context and validation**. Every PRP should contain the exact context for an AI agent to successfully implement working code in a single pass.

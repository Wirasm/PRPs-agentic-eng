### ☕ Support This Work

**Found value in these resources?**

👉 **Buy me a coffee:** https://coff.ee/wirasm

I spent a considerable amount of time creating these resources and prompts. If you find value in this project, please consider buying me a coffee to support my work.

That will help me maintain and improve the resources available for free

---

### 🎯 Transform Your Team with AI Engineering Workshops

**Ready to move beyond toy demos to production-ready AI systems?**

👉 **Book a workshop:** https://www.rasmuswiding.com/

✅ **What you'll get:**

- Put your team on a path to become AI power users
- Learn the exact PRP methodology used by top engineering teams
- Hands-on training with Claude Code, PRPs, and real codebases
- From beginner to advanced AI engineering workshops for teams and individuals

💡 **Perfect for:** Engineering teams, Product teams, and developers who want AI that actually works in production

Let's talk!
Contact me directly at rasmus@widinglabs.com

# AI Engineering Resources for Claude Code

A comprehensive library of assets and context engineering for Agentic Engineering, optimized for Claude Code. This repository provides the Product Requirement Prompt (PRP) methodology, pre-configured commands, and extensive documentation to enable AI-assisted development that delivers production-ready code on the first pass.

## What is PRP?

Product Requirement Prompt (PRP) is a structured prompt methodology first established in summer 2024 with context engineering at heart. A PRP supplies an AI coding agent with everything it needs to deliver a vertical slice of working software—no more, no less.

> "Over-specifying what to build while under-specifying the context, and how to build it, is why so many AI-driven coding attempts stall at 80%."

### How PRP Differs from Traditional PRD

A traditional PRD clarifies what the product must do and why customers need it, but deliberately avoids how it will be built.

A PRP keeps the goal and justification sections of a PRD yet adds three AI-critical layers:

### Context

Precise file paths and content, library versions and library context, code snippets examples. LLMs generate higher-quality code when given direct, in-prompt references instead of broad descriptions. Usage of a ai_docs/ directory to pipe in library and other docs.

### Implementation Details and Strategy

In contrast to a traditional PRD, a PRP explicitly states how the product will be built. This includes the use of API endpoints, test runners, or agent patterns (ReAct, Plan-and-Execute) to use. Usage of typehints, dependencies, architectural patterns and other tools to ensure the code is built correctly.

### Validation Gates

Deterministic checks such as pytest, ruff, or static type passes. "Shift-left" quality controls catch defects early and are cheaper than late re-work. Example: Each new function should be individually tested, Validation gate = all tests pass.

### Why Context is Non-Negotiable

Large-language-model outputs are bounded by their context window; irrelevant or missing context literally squeezes out useful tokens.

The industry mantra "Garbage In → Garbage Out" applies doubly to prompt engineering and especially in agentic engineering: sloppy input yields brittle code.

### In Short

A PRP is **PRD + curated codebase intelligence + agent/runbook**—the minimum viable packet an AI needs to ship production-ready code on the first pass.

The PRP can be small and focusing on a single task or large and covering multiple tasks. The true power of PRP is in the ability to chain tasks together in a PRP to build, self-validate and ship complex features.

## Getting Started

### Option 1: Copy Resources to Your Existing Project (PRPs/scripts/getting_started_option1.sh)

1. **Copy the Claude commands** to your project:

   ```bash
   # From your project root
   cp -r /path/to/PRPs-agentic-eng/.claude/commands .claude/
   ```

2. **Copy the PRP templates and runner**:

   ```bash
   cp -r /path/to/PRPs-agentic-eng/PRPs/templates PRPs/
   cp -r /path/to/PRPs-agentic-eng/PRPs/scripts PRPs/
   cp /path/to/PRPs-agentic-eng/PRPs/README.md PRPs/
   ```

3. **Copy AI documentation** (optional but recommended):
   ```bash
   cp -r /path/to/PRPs-agentic-eng/PRPs/ai_docs PRPs/
   ```

### Option 2: Clone and Start a New Project

1. **Clone this repository**:

   ```bash
   git clone https://github.com/Wirasm/PRPs-agentic-eng.git
   cd PRPs-agentic-eng
   ```

2. **Create your project structure**:

   ```bash
   # Example for a Python project
   mkdir -p src/tests
   touch src/__init__.py
   touch pyproject.toml
   touch CLAUDE.md
   ```

3. **Initialize with UV** (for Python projects):
   ```bash
   uv venv
   uv sync
   ```

## Using Claude Commands

The `.claude/commands/` directory contains 12 pre-configured commands that appear as slash commands in Claude Code.

### Available Commands

1. **PRP Creation & Execution**:
   - `/create-base-prp` - Generate comprehensive PRPs with research
   - `/execute-base-prp` - Execute PRPs against codebase
   - `/planning-create` - Create planning documents with diagrams
   - `/spec-create-adv` - Advanced specification creation
   - `/spec-execute` - Execute specifications

2. **Code Review & Refactoring**:
   - `/review-general` - General code review
   - `/review-staged-unstaged` - Review git changes
   - `/refactor-simple` - Simple refactoring tasks

3. **Git & GitHub**:
   - `/create-pr` - Create pull requests

4. **Utilities**:
   - `/prime-core` - Prime Claude with project context
   - `/onboarding` - Onboarding process for new team members
   - `/debug` - Debugging workflow

### How to Use Commands

1. **In Claude Code**, type `/` to see available commands
2. **Select a command** and provide arguments when prompted
3. **Example usage**:
   ```
   /create-base-prp user authentication system with OAuth2
   ```

## Using PRPs

### Creating a PRP

1. **Use the template** as a starting point:

   ```bash
   cp PRPs/templates/prp_base.md PRPs/my-feature.md
   ```

2. **Fill in the sections**:
   - Goal: What needs to be built
   - Why: Business value and user impact
   - Context: Documentation, code examples, gotchas
   - Implementation Blueprint: Tasks and pseudocode
   - Validation Loop: Executable tests

3. **Or use Claude to generate one**:
   ```
   /create-base-prp implement user authentication with JWT tokens
   ```

### Executing a PRP

1. **Using the runner script**:

   ```bash
   # Interactive mode (recommended for development)
   uv run PRPs/scripts/prp_runner.py --prp my-feature --interactive

   # Headless mode (for CI/CD)
   uv run PRPs/scripts/prp_runner.py --prp my-feature --output-format json

   # Streaming JSON (for real-time monitoring)
   uv run PRPs/scripts/prp_runner.py --prp my-feature --output-format stream-json
   ```

2. **Using Claude commands**:
   ```
   /execute-base-prp PRPs/my-feature.md
   ```

### PRP Best Practices

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

### Example PRP Structure

```markdown
## Goal

Implement user authentication with JWT tokens

## Why

- Enable secure user sessions
- Support API authentication
- Replace basic auth with industry standard

## What

JWT-based authentication system with login, logout, and token refresh

### Success Criteria

- [ ] Users can login with email/password
- [ ] JWT tokens expire after 24 hours
- [ ] Refresh tokens work correctly
- [ ] All endpoints properly secured

## All Needed Context

### Documentation & References

- url: https://jwt.io/introduction/
  why: JWT structure and best practices

- file: src/auth/basic_auth.py
  why: Current auth pattern to replace

- doc: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
  section: OAuth2 with Password and JWT

### Known Gotchas

# CRITICAL: Use RS256 algorithm for production

# CRITICAL: Store refresh tokens in httpOnly cookies

# CRITICAL: Implement token blacklist for logout

## Implementation Blueprint

[... detailed implementation plan ...]

## Validation Loop

### Level 1: Syntax & Style

ruff check src/ --fix
mypy src/

### Level 2: Unit Tests

uv run pytest tests/test_auth.py -v

### Level 3: Integration Test

curl -X POST http://localhost:8000/auth/login \
 -H "Content-Type: application/json" \
 -d '{"email": "test@example.com", "password": "testpass"}'
```

## Project Structure Recommendations

```
your-project/
|-- .claude/
|   |-- commands/          # Claude Code commands
|   `-- settings.json      # Tool permissions
|-- PRPs/
|   |-- templates/         # PRP templates
|   |-- scrips/           # PRP runner
|   |-- ai_docs/          # Library documentation
|   |-- completed/        # Finished PRPs
|   `-- *.md              # Active PRPs
|-- CLAUDE.md             # Project-specific guidelines
|-- src/                  # Your source code
`-- tests/                # Your tests
```

## Setting Up CLAUDE.md

Create a `CLAUDE.md` file in your project root with:

1. **Core Principles**: KISS, YAGNI, etc.
2. **Code Structure**: File size limits, function length
3. **Architecture**: How your project is organized
4. **Testing**: Test patterns and requirements
5. **Style Conventions**: Language-specific guidelines
6. **Development Commands**: How to run tests, lint, etc.

See the example CLAUDE.md in this repository for a comprehensive template.

## Advanced Usage

### Running Multiple Claude Sessions

Use Git worktrees for parallel development:

```bash
git worktree add -b feature-auth ../project-auth
git worktree add -b feature-api ../project-api

# Run Claude in each worktree
cd ../project-auth && claude
cd ../project-api && claude
```

### CI/CD Integration

Use the PRP runner in headless mode:

```yaml
# GitHub Actions example
- name: Execute PRP
  run: |
    uv run PRPs/scripts/prp_runner.py \
      --prp implement-feature \
      --output-format json > result.json
```

### Custom Commands

Create your own commands in `.claude/commands/`:

```markdown
# .claude/commands/my-command.md

# My Custom Command

Do something specific to my project.

## Arguments: $ARGUMENTS

[Your command implementation]
```

## Resources Included

### Documentation (PRPs/ai_docs/)

- `cc_base.md` - Core Claude Code documentation
- `cc_actions_sdk.md` - GitHub Actions and SDK integration
- `cc_best_practices.md` - Best practices guide
- `cc_settings.md` - Configuration and security
- `cc_tutorials.md` - Step-by-step tutorials

### Templates (PRPs/templates/)

- `prp_base.md` - Comprehensive PRP template with validation
- `prp_spec.md` - Specification template
- `prp_planning_base.md` - Planning template with diagrams

### Example PRP

- `example-from-workshop-mcp-crawl4ai-refactor-1.md` - Real-world refactoring example

## License

MIT License

## Support

I spent a considerable amount of time creating these resources and prompts. If you find value in this project, please consider buying me a coffee to support my work.

👉 **Buy me a coffee:** https://coff.ee/wirasm

---

Remember: The goal is one-pass implementation success through comprehensive context. Happy coding with Claude Code!

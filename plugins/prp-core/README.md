# PRP Core Plugin

Complete PRP (Product Requirement Prompt) workflow automation for Claude Code.

## Overview

This plugin provides a comprehensive workflow for creating, executing, and shipping features using the PRP methodology - where **PRP = PRD + curated codebase intelligence + agent/runbook** designed to enable AI agents to ship production-ready code on the first pass.

## Features

### 4 Core Commands

#### 1. `/prp-core-create`

Create comprehensive feature PRPs with deep codebase analysis.

```bash
/prp-core-create "Add JWT authentication"
```

**What it does:**
- Analyzes your codebase for patterns and conventions
- Researches relevant documentation and best practices
- Creates a detailed, context-rich implementation plan
- Generates executable validation gates
- Outputs a complete PRP file ready for execution

**Output:** `.claude/PRPs/features/{feature-name}.md`

#### 2. `/prp-core-execute`

Execute a PRP file until fully complete with validation.

```bash
/prp-core-execute .claude/PRPs/features/my-feature.md
```

**What it does:**
- Ingests and analyzes the complete PRP
- Executes every task sequentially
- Validates after each step
- Runs full validation suite on completion
- Moves completed PRP to `completed/` directory

**Success Criteria:**
- ✓ Every task completed
- ✓ All validation commands pass
- ✓ Acceptance criteria met

#### 3. `/prp-core-commit`

Create atomic git commit with proper formatting and validation.

```bash
/prp-core-commit
```

**What it does:**
- Reviews uncommitted changes
- Runs lint checks and unit tests
- Stops if validation fails
- Creates conventional commit with proper format
- Never mentions Claude Code or AI in commit messages

**Commit Format:** `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Present tense, lowercase, ≤50 characters

#### 4. `/prp-core-pr`

Push changes and create pull request with comprehensive description.

```bash
/prp-core-pr "Add JWT authentication"
```

**What it does:**
- Validates all changes (lint, tests)
- Ensures you're on a feature branch
- Commits any uncommitted changes (if needed)
- Pushes to remote with tracking
- Creates GitHub PR with detailed description
- Adds appropriate labels and metadata

**PR includes:**
- Summary of changes
- Implementation details
- Testing validation
- Checklist for reviewers

## Workflow

The plugin provides a complete end-to-end workflow:

1. **Create PRP** (`/prp-core-create`) - Generates comprehensive implementation plan
2. **Execute PRP** (`/prp-core-execute`) - Implements the feature
3. **Commit** (`/prp-core-commit`) - Creates atomic commit with validation
4. **PR** (`/prp-core-pr`) - Pushes and creates pull request

Execute commands sequentially, or let Claude orchestrate the workflow based on your needs.

## Installation

### Option 1: From GitHub (Recommended)

Once the plugin is pushed to GitHub:

```bash
# Add marketplace from GitHub
/plugin marketplace add Wirasm/PRPs-agentic-eng

# Install plugin
/plugin install prp-core@prp-marketplace
```

### Option 2: Local Development/Testing

For testing the plugin locally:

```bash
# Navigate to the repository root
cd /path/to/PRPs-agentic-eng

# Start Claude Code
claude

# Add local marketplace (use absolute path)
/plugin marketplace add /absolute/path/to/PRPs-agentic-eng

# Install plugin
/plugin install prp-core@prp-marketplace

# Restart Claude Code (required)
# Exit (Ctrl+C) and run 'claude' again

# Verify installation
/help
```

**Important Notes:**
- Use **absolute path** when adding local marketplace
- **Restart Claude Code** after installation for commands to load
- Verify commands appear in `/help` output

### Option 3: Team Automatic Installation

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "prp-marketplace": {
      "source": "Wirasm/PRPs-agentic-eng"
    }
  },
  "enabledPlugins": [
    "prp-core@prp-marketplace"
  ]
}
```

Team members who trust the repository will automatically have the plugin installed.

## Usage

### Quick Start

```bash
# 1. Create a feature PRP
/prp-core-create "Add user authentication with JWT tokens"

# 2. Execute the generated PRP
/prp-core-execute .claude/PRPs/features/add-user-authentication.md

# 3. Commit changes
/prp-core-commit

# 4. Create PR
/prp-core-pr "feat: add JWT authentication"
```

### Complete Workflow

Execute commands in sequence for the full workflow:

```bash
# 1. Create PRP
/prp-core-create "Add user authentication with JWT tokens"

# 2. Execute the PRP (wait for completion)
/prp-core-execute .claude/PRPs/features/add-user-authentication.md

# 3. Commit changes
/prp-core-commit

# 4. Create PR
/prp-core-pr "feat: add JWT authentication system"
```

This workflow:
- ✅ Creates comprehensive PRP with deep analysis
- ✅ Executes implementation with validation
- ✅ Commits changes with proper formatting
- ✅ Pushes and creates pull request

## PRP Methodology

### What is a PRP?

**PRP = PRD + curated codebase intelligence + agent/runbook**

A PRP is a comprehensive implementation document that contains:
1. **Context** - All necessary patterns, documentation, and examples
2. **Plan** - Step-by-step tasks with validation gates
3. **Validation** - Executable commands to verify correctness

### Core Principles

1. **Context is King** - Include ALL necessary information
2. **Validation Loops** - Provide executable tests the AI can run and fix
3. **Information Dense** - Use keywords and patterns from codebase
4. **Progressive Success** - Start simple, validate, enhance

### PRP Structure

Every PRP includes:
- **Feature Description** - What we're building and why
- **Context References** - Files, patterns, documentation
- **Implementation Plan** - Phased approach with tasks
- **Step-by-Step Tasks** - Atomic, ordered, independently testable
- **Testing Strategy** - Unit, integration, edge cases
- **Validation Commands** - Executable verification (syntax, tests, manual)
- **Acceptance Criteria** - Measurable completion requirements

## Requirements

- Claude Code installed
- Git configured
- GitHub CLI (`gh`) for PR creation
- Python environment with linters (ruff, mypy) for validation

## Configuration

### Project Structure

The plugin expects this structure in your project:

```
your-project/
├── .claude/
│   ├── PRPs/
│   │   ├── features/           # Active PRPs
│   │   └── completed/          # Completed PRPs
│   └── settings.json           # Optional: team config
├── tests/                      # For validation
└── pyproject.toml             # Or package.json, etc.
```

### Validation Commands

The plugin uses these standard validation commands:

```bash
# Syntax & Style
ruff check --fix
mypy .

# Unit Tests
pytest tests/ -v

# Or for JavaScript/TypeScript
npm run lint
npm run type-check
npm test
```

Customize validation commands in your PRPs as needed.

## Troubleshooting

### Plugin Not Loading

```bash
# Check plugin status
/plugin

# Reinstall plugin
/plugin uninstall prp-core@marketplace
/plugin install prp-core@marketplace

# Restart Claude Code
```

### Commands Not Found

Ensure Claude Code restarted after installation. Check available commands:

```bash
/help
```

### Validation Issues

If validation commands fail, ensure your environment has the required tools:

```bash
# Install Python linters
pip install ruff mypy

# Or with uv
uv pip install ruff mypy
```

## Development

### Plugin Structure

```
plugins/prp-core/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/                  # Slash commands
│   ├── PRP-core-commit.md
│   ├── prp-core-create.md
│   ├── prp-core-execute.md
│   └── prp-core-pr.md
└── README.md                  # This file
```

### Testing Changes

1. Make changes to plugin files
2. Uninstall plugin: `/plugin uninstall prp-core@marketplace`
3. Reinstall plugin: `/plugin install prp-core@marketplace`
4. Test commands

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - See repository for details

## Support

- **Issues**: https://github.com/Wirasm/PRPs-agentic-eng/issues
- **Documentation**: https://github.com/Wirasm/PRPs-agentic-eng
- **Examples**: See `.claude/PRPs/features/` in the repository

## Version History

### 1.0.0 (2025-10-22)
- Initial release
- 4 core commands (create, execute, commit, pr)
- 2 utility scripts (invoke_command, prp_workflow)
- Complete PRP workflow automation
- Team marketplace distribution

## See Also

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [PRP Methodology](https://github.com/Wirasm/PRPs-agentic-eng/blob/main/CLAUDE.md)

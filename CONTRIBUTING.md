# Contributing to PRP Extended

Thank you for your interest in contributing to PRP Extended!

## This is a Fork

This repository is a fork of [Wirasm/PRPs-agentic-eng](https://github.com/Wirasm/PRPs-agentic-eng) with added memory system features.

### Where to Contribute

| Type of Change | Where to Contribute |
|----------------|---------------------|
| Core PRP methodology improvements | [Upstream repo](https://github.com/Wirasm/PRPs-agentic-eng) |
| Memory system features | This fork |
| Bug fixes in memory system | This fork |
| Documentation for memory features | This fork |

## Getting Started

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test with a real PRP plan using `/prp-ralph`
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/YOUR-USERNAME/PRPs-agentic-eng.git
cd PRPs-agentic-eng
git checkout development
```

## Memory System Guidelines

When contributing to the memory system:

### JSON Schema

Maintain backward compatibility with the existing JSON schemas:

**failures.json entries must include:**
- `id` - Unique identifier (format: `fail-XXX`)
- `timestamp` - ISO 8601 format
- `plan` - Path to the plan file
- `iteration` - Loop iteration number
- `approach` - What was attempted
- `files` - Affected files array
- `errors` - Error messages array
- `rootCause` - Analysis of why it failed
- `prevention` - How to prevent in future

**successes.json entries must include:**
- `id` - Unique identifier (format: `success-XXX`)
- `timestamp` - ISO 8601 format
- `plan` - Path to the plan file
- `approach` - What worked
- `files` - Affected files array
- `whyItWorked` - Why this approach succeeded
- `pattern` - Reusable pattern

**rules.json entries must include:**
- `id` - Unique identifier (format: `rule-XXX`)
- `timestamp` - ISO 8601 format
- `trigger` - What triggered the rule creation
- `rule` - The generalized rule
- `example` - Concrete example (WRONG vs RIGHT)
- `source` - Origin (`user-correction`, `pattern-extraction`, etc.)

### Testing

Before submitting:

1. Test the full Ralph loop with your changes
2. Verify memory files are created/updated correctly
3. Check that warnings appear when similar failures exist
4. Ensure JSON files remain valid

## Code Style

- Keep prompts in English
- Use clear, descriptive phase names
- Document new phases in README.md
- Update CHANGELOG.md for notable changes

## Pull Request Process

1. Update README.md with any new features
2. Update CHANGELOG.md under `[Unreleased]`
3. Ensure all tests pass
4. Request review from maintainers

## Questions?

Open an issue for discussion before making major changes.

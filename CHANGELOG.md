# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-15

### Added

- **Memory System Integration** - Persistent failure prevention and success pattern tracking
  - `.claude/prp-memory/procedural/failures.json` - Records failed approaches with root cause analysis
  - `.claude/prp-memory/procedural/successes.json` - Records successful patterns for reuse
  - `.claude/prp-memory/learned/rules.json` - Captures user corrections as reusable rules

- **New Ralph Loop Phases**
  - Phase 2.3: Initialize Memory System - Creates memory directories and JSON files on startup
  - Phase 3.0: Failure Prevention Check - Checks past failures before implementing
  - Phase 3.10: Record to Memory - Saves failures/successes after each validation
  - Phase 4.4: Extract Learned Rules - Captures user corrections as generalizable rules

- **Warning System** - Displays warnings when similar approaches have failed before, suggests successful alternatives

### Changed

- Updated README with Memory System documentation
- Updated project structure documentation to include memory directories
- Added installation instructions for the fork

### Credits

- Original PRP by [Wirasm](https://github.com/Wirasm/PRPs-agentic-eng)
- Memory architecture inspired by [claude-harness](https://github.com/panayiotism/claude-harness)

---

## Fork History

This changelog tracks changes made in the [Milofax/PRPs-agentic-eng](https://github.com/Milofax/PRPs-agentic-eng) fork.

For the original PRP changelog, see the [upstream repository](https://github.com/Wirasm/PRPs-agentic-eng).

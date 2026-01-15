# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-15

### Added

- **Graphiti Long-Term Memory Integration** (optional, cross-project)
  - Phase 2.4.1: Bootstrap from Graphiti - Loads relevant learnings from knowledge graph
  - Phase 4.6: Graduate to Graphiti - Promotes high-value learnings after success
  - Tech-stack based `group_id` strategy (`typescript-nextjs`, `python-fastapi`, etc.)
  - Graceful degradation when Graphiti unavailable

- **New Configuration File**
  - `.claude/prp-memory/config.json` - Graphiti settings and graduation criteria
  - Configurable confidence thresholds, lesson requirements, failure thresholds
  - Bootstrap limits for facts and nodes

- **Graduation System**
  - Learned rules (high/medium confidence) → Graphiti episodes
  - Success patterns (with lessons) → Graphiti episodes
  - Recurring failure patterns → Graphiti episodes (AVOID markers)
  - Code patterns → Graphiti episodes
  - Deduplication via content hashing (`graphitiHash` field)

### Changed

- Updated Phase 2 checkpoint to include Graphiti bootstrap status
- Updated Success Criteria to include `GRAPHITI_GRADUATED`
- Memory entries now track graduation status with `graphitiHash` and `graduatedAt`

### Notes

- Graphiti integration is **completely optional** - works without it
- Uses MCP tool discovery for detection (works with mcp-funnel)
- Cross-project learnings filtered by tech stack to avoid contamination

## [1.1.0] - 2026-01-15

### Added

- **Full 5-Layer Memory Architecture** (claude-harness compatible)
  - **Working Memory** (`working/context.json`) - Session context, rebuilt each run
  - **Episodic Memory** (`episodic/decisions.json`) - Rolling window of decisions (max 50, FIFO)
  - **Semantic Memory** - Project knowledge layer
    - `semantic/architecture.json` - Project type, tech stack, structure
    - `semantic/entities.json` - Components, services, hooks, API routes
    - `semantic/constraints.json` - Project rules and conventions
  - **Procedural Memory** - Now includes `patterns.json` for extracted patterns
  - **Learned Rules** - Enhanced with confidence levels and applicability filters

- **New Ralph Loop Phases**
  - Phase 2.4: Compile Working Context - Builds session context from all memory layers
  - Phase 2.5: Discover Semantic Memory - Auto-detects project architecture (first run)
  - Phase 3.0.5: Load Learned Rules - Displays applicable rules before implementation
  - Phase 3.11: Extract Patterns - Generalizes successes into reusable patterns
  - Phase 4.5: Update Semantic Memory - Records new entities after completion

- **Enhanced Schemas**
  - Failures now include `category` field for pattern matching
  - Successes now include `verificationResults` and `lessons`
  - Rules now include `confidence`, `active`, and `applicability` fields
  - All files now include `version: 3` for schema tracking

### Changed

- Phase 2.3 now creates all 5 memory layers (9 files total)
- Phase 3.0 now also reads `patterns.json` for known patterns
- Phase 3.10 now records decisions to episodic memory
- Phase 4.4 enhanced with confidence scoring and applicability filtering
- Updated README with 5-layer memory architecture documentation
- Updated memory structure diagram in documentation

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

# Story PRP Workflow Guide

## Overview

The Story PRP workflow is a streamlined approach for converting user stories/tasks from Jira, Linear, or other project management tools into executable implementation plans. Unlike the comprehensive Base PRP flow, Story PRPs focus on tactical, task-oriented implementation.

## Key Differences from Base PRPs

| Aspect | Base PRP | Story PRP |
|--------|----------|-----------|
| **Scope** | Full feature/product | Single story/task |
| **Context** | Extensive documentation | Focused references |
| **Format** | Detailed blueprint | Task checklist |
| **Validation** | 4-level comprehensive | Inline per-task |
| **Use Case** | New features, major changes | Sprint tasks, bug fixes |

## Workflow Components

### 1. Template: `PRPs/templates/prp_story.md`
- Simplified structure focused on implementation tasks
- Each task has inline validation
- No extensive blueprint sections
- Direct, actionable format

### 2. Commands

#### `/prp-story-create {story description}`
Creates a Story PRP by:
- Analyzing codebase for patterns and conventions
- Breaking down story into concrete tasks
- Generating validation commands
- Leveraging specialized subagents for parallel analysis

#### `/prp-story-execute {prp_file}`
Executes a Story PRP by:
- Implementing tasks sequentially
- Validating each task immediately
- Following discovered patterns exactly
- Ensuring all acceptance criteria are met

### 3. Specialized Subagents

#### `@codebase-analyst`
- Deep pattern analysis
- Convention discovery
- Architecture understanding
- Testing pattern extraction

#### `@library-researcher`
- External documentation fetching
- Implementation example finding
- Best practices research
- Known issues identification

## Usage Examples

### Creating a Story PRP

```bash
# From a user story
/prp-story-create As a user, I want to add pagination to the product list API so that large result sets load faster

# From a bug report
/prp-story-create BUG: Email notifications are not being sent when users reset their password

# From a technical task
/prp-story-create Refactor database connection pool to use async context managers
```

### Executing a Story PRP

```bash
# Execute the generated PRP
/prp-story-execute PRPs/story_add_pagination.md

# Or use the runner script
uv run PRPs/scripts/prp_runner.py --prp story_add_pagination --interactive
```

## Task Format Examples

### CREATE Task
```markdown
### CREATE services/pagination_service.py:
- IMPLEMENT: PaginationService with calculate_offset() method
- PATTERN: Follow services/filter_service.py structure
- IMPORTS: from typing import Tuple; from math import ceil
- GOTCHA: Handle negative page numbers gracefully
- **VALIDATE**: `python -c "from services.pagination_service import PaginationService; print('✓')"`
```

### UPDATE Task
```markdown
### UPDATE api/products.py:
- ADD: pagination parameters to list_products endpoint
- FIND: `async def list_products(request: Request):`
- INSERT: `page: int = Query(1, ge=1), per_page: int = Query(20, le=100)`
- **VALIDATE**: `grep -q "page.*Query" api/products.py && echo "✓ Params added"`
```

## Best Practices

### When Creating Story PRPs

1. **Provide Clear Context**: Include acceptance criteria and any constraints
2. **Let Agents Analyze**: Don't pre-specify implementation details
3. **Trust the Process**: The system will discover patterns and conventions

### When Executing Story PRPs

1. **Sequential Execution**: Complete tasks in order
2. **Validate Immediately**: Run validation after each task
3. **Follow Patterns**: Don't create new patterns, use existing ones
4. **Fix Forward**: If validation fails, fix and continue

## Typical Story Types

- **Feature Addition**: New endpoints, services, or components
- **Bug Fixes**: Targeted fixes with test coverage
- **Refactoring**: Code improvements maintaining behavior
- **Integration**: Adding third-party services or libraries
- **Performance**: Optimization tasks with benchmarks
- **Security**: Adding auth, validation, or hardening

## Advanced Usage

### Parallel Analysis
The create command spawns multiple subagents to analyze:
- Project structure
- Similar implementations
- External documentation
- Testing patterns

### Custom Validation
Each task can have custom validation beyond standard commands:
- API endpoint testing with curl
- Database verification queries
- Performance benchmarks
- Integration tests

### Context References
The system automatically discovers and includes:
- Relevant codebase patterns
- External documentation
- Configuration examples
- Test patterns

## When to Use Story PRPs vs Base PRPs

**Use Story PRPs for:**
- Sprint tasks and user stories
- Bug fixes and small features
- Refactoring and optimization
- Tasks with clear scope

**Use Base PRPs for:**
- New products or major features
- Complex architectural changes
- Multi-system integrations
- Features requiring extensive context

## Troubleshooting

**Issue**: Tasks seem too high-level
**Solution**: Provide more specific acceptance criteria in the story

**Issue**: Wrong patterns detected
**Solution**: Include hints about which part of codebase to reference

**Issue**: Validation commands fail
**Solution**: Check project setup, ensure dependencies installed

## Example Output

See `PRPs/story_add_rate_limiting_example.md` for a complete example of a generated Story PRP from a user story about adding rate limiting to an API.
name: "PRP Creation Agent using PydanticAI - Context-Rich Implementation"
description: |
Comprehensive PRP for building an automated PRP creation agent using PydanticAI framework,
leveraging parallel research capabilities and existing codebase patterns for maximum efficiency.

## Goal

Build a production-ready PRP creation agent using PydanticAI that can automatically generate comprehensive PRPs by:

- Analyzing user requirements and context
- Conducting parallel research (codebase analysis, external documentation, testing patterns)
- Generating structured PRPs following established templates
- Validating output quality and completeness
- Integrating with existing Claude Code infrastructure

**End State**: A Python agent that takes a feature description as input and outputs a complete, validated PRP file ready for implementation.

## Why

- **Efficiency**: Reduce PRP creation time from manual hours to automated minutes
- **Consistency**: Ensure all PRPs follow established patterns and include necessary context
- **Quality**: Leverage AI capabilities for comprehensive research and validation
- **Scalability**: Enable rapid prototyping and feature development across teams
- **Integration**: Work seamlessly with existing Claude Code workflows and validation gates

## What

### Core Functionality

- **Input Processing**: Parse natural language feature descriptions into structured requirements
- **Parallel Research**: Simultaneously analyze codebase patterns, external documentation, and testing strategies
- **PRP Generation**: Create comprehensive PRPs using established templates and discovered patterns
- **Quality Validation**: Score and validate generated PRPs against quality metrics
- **File Management**: Handle PRP file creation, organization, and versioning

### User Experience

```bash
# Command-line interface
uv run python -m prp_agent "Create a user authentication system with OAuth2 and JWT tokens"

# Python API
from prp_agent import PRPCreationAgent
agent = PRPCreationAgent()
prp = await agent.create_prp("Feature description here")
```

### Success Criteria

- [ ] Generate PRPs with 8+ quality score on all metrics (Context, Clarity, Validation, Success Probability)
- [ ] Complete PRP generation in under 2 minutes
- [ ] 90%+ first-pass implementation success rate
- [ ] Full integration with existing validation gates
- [ ] Support for both interactive and headless modes

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://ai.pydantic.dev/
  why: Core PydanticAI framework documentation and API reference

- url: https://ai.pydantic.dev/agents/
  why: Agent creation patterns and best practices

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and usage patterns

- url: https://ai.pydantic.dev/examples/
  why: Real-world implementation examples and patterns

- url: https://github.com/pydantic/pydantic-ai
  why: Source code examples and issue tracking

- url: https://ai.pydantic.dev/troubleshooting/
  why: Common issues and solutions for production deployment

- file: /Users/rasmus/Projects/prp-spaces/dynamo-share/PRPs/templates/prp_base.md
  why: Established PRP template structure and validation patterns

- file: /Users/rasmus/Projects/prp-spaces/dynamo-share/PRPs/scripts/prp_runner.py
  why: Existing PRP execution patterns and Claude Code integration

- file: /Users/rasmus/Projects/prp-spaces/dynamo-share/.claude/commands/create-base-prp-parallel.md
  why: Parallel research agent patterns and coordination strategies

- file: /Users/rasmus/Projects/prp-spaces/dynamo-share/CLAUDE.md
  why: Project conventions, architecture patterns, and development standards

- docfile: /Users/rasmus/Projects/prp-spaces/dynamo-share/PRPs/ai_docs/build_with_claude_code.md
  why: Claude Code SDK integration patterns and async operations

- docfile: /Users/rasmus/Projects/prp-spaces/dynamo-share/PRPs/ai_docs/cc_mcp.md
  why: MCP server configuration and tool extension patterns
```

### Current Codebase Tree

```bash
.
├── CLAUDE.md                    # Project conventions and architecture
├── PRPs/
│   ├── ai_docs/                 # AI agent documentation
│   │   ├── build_with_claude_code.md
│   │   ├── cc_mcp.md
│   │   └── cc_overview.md
│   ├── templates/               # PRP templates
│   │   ├── prp_base.md
│   │   └── prp_planning_base.md
│   └── scripts/
│       └── prp_runner.py        # Existing PRP execution script
├── .claude/
│   └── commands/                # Claude Code custom commands
│       ├── create-base-prp.md
│       └── create-base-prp-parallel.md
├── pyproject.toml               # Project configuration
└── uv.lock                      # UV lock file
```

### Desired Codebase Tree

```bash
src/
├── prp_agent/
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── agent.py                 # Core PydanticAI agent
│   ├── tests/
│   │   ├── test_agent.py
│   │   ├── test_models.py
│   │   └── conftest.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── prp_models.py        # Pydantic models for PRP structure
│   │   ├── request_models.py    # Input validation models
│   │   └── tests/
│   │       └── test_models.py
│   ├── features/
│   │   ├── research_coordinator/
│   │   │   ├── __init__.py
│   │   │   ├── coordinator.py   # Parallel research orchestration
│   │   │   └── tests/
│   │   │       └── test_coordinator.py
│   │   ├── prp_generator/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py     # PRP content generation
│   │   │   └── tests/
│   │   │       └── test_generator.py
│   │   └── quality_validator/
│   │       ├── __init__.py
│   │       ├── validator.py     # Quality scoring and validation
│   │       └── tests/
│   │           └── test_validator.py
│   └── tools/
│       ├── __init__.py
│       ├── codebase_analyzer.py # Codebase pattern analysis
│       ├── documentation_fetcher.py # External documentation research
│       ├── file_manager.py      # PRP file operations
│       └── tests/
│           └── test_tools.py
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: PydanticAI requires Python 3.9+
# CRITICAL: Set ALLOW_MODEL_REQUESTS = False in tests to prevent real API calls
# CRITICAL: Use TestModel() for fast testing without LLM calls
# CRITICAL: Async functions required for run() method
# CRITICAL: Tool functions must be decorated with @agent.tool
# CRITICAL: Event loop conflicts in Jupyter - use nest_asyncio.apply()
# CRITICAL: UV package management - always use 'uv run' for commands
# CRITICAL: Pydantic v2 syntax - use Field() for validation
# CRITICAL: Claude Code tool allowlists - specify exact tools needed
# CRITICAL: File operations must use absolute paths
# CRITICAL: Tests must be co-located with code (per CLAUDE.md)
# CRITICAL: Functions max 50 lines, files max 500 lines (per CLAUDE.md)
```

## Implementation Blueprint

### Data Models and Structure

```python
# Core Pydantic models for type safety and validation
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum

class ResearchType(str, Enum):
    CODEBASE = "codebase"
    EXTERNAL = "external"
    TESTING = "testing"
    DOCUMENTATION = "documentation"

class PRPRequest(BaseModel):
    """Input validation for PRP creation requests"""
    feature_description: str = Field(..., min_length=10, max_length=1000)
    context_requirements: List[str] = Field(default_factory=list)
    validation_level: str = Field(default="comprehensive", pattern="^(basic|standard|comprehensive)$")
    research_depth: str = Field(default="parallel", pattern="^(minimal|standard|parallel)$")
    output_format: str = Field(default="markdown", pattern="^(markdown|json|yaml)$")

class ResearchResult(BaseModel):
    """Structured research findings"""
    research_type: ResearchType
    findings: List[str]
    file_references: List[str] = Field(default_factory=list)
    url_references: List[HttpUrl] = Field(default_factory=list)
    patterns_discovered: List[str] = Field(default_factory=list)
    gotchas: List[str] = Field(default_factory=list)
    quality_score: int = Field(ge=1, le=10)

class PRPSection(BaseModel):
    """Individual PRP section structure"""
    title: str
    content: str
    validation_commands: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class PRPResult(BaseModel):
    """Complete PRP output structure"""
    title: str
    sections: List[PRPSection]
    quality_scores: Dict[str, int] = Field(default_factory=dict)
    validation_gates: List[str] = Field(default_factory=list)
    file_path: Optional[str] = None
    generated_at: str
    research_summary: List[ResearchResult] = Field(default_factory=list)

    def overall_quality_score(self) -> float:
        """Calculate overall quality score"""
        if not self.quality_scores:
            return 0.0
        return sum(self.quality_scores.values()) / len(self.quality_scores)
```

### Task List (in order of completion)

```yaml
Task 1: Setup Project Structure
CREATE src/prp_agent/__init__.py:
  - ESTABLISH package structure
  - EXPORT main classes and functions
  - FOLLOW vertical slice architecture pattern

CREATE src/prp_agent/models/prp_models.py:
  - IMPLEMENT Pydantic models from blueprint above
  - INCLUDE comprehensive field validation
  - MIRROR existing validation patterns from codebase

CREATE src/prp_agent/models/tests/test_models.py:
  - FOLLOW pytest patterns from CLAUDE.md
  - TEST all validation scenarios
  - ENSURE type safety verification

Task 2: Core Agent Implementation
CREATE src/prp_agent/agent.py:
  - IMPLEMENT PydanticAI agent with tools
  - CONFIGURE model providers (OpenAI, Anthropic)
  - PATTERN: Use structured outputs with Pydantic models
  - INCLUDE proper error handling and logging

CREATE src/prp_agent/tools/codebase_analyzer.py:
  - IMPLEMENT @agent.tool decorated functions
  - ANALYZE file patterns and existing implementations
  - MIRROR search patterns from existing .claude/commands/

CREATE src/prp_agent/tools/documentation_fetcher.py:
  - IMPLEMENT web search and documentation parsing
  - INTEGRATE with WebFetch tool patterns
  - HANDLE rate limiting and error cases

Task 3: Parallel Research Coordination
CREATE src/prp_agent/features/research_coordinator/coordinator.py:
  - IMPLEMENT parallel agent execution pattern
  - COORDINATE 4 research agents simultaneously
  - PATTERN: Follow create-base-prp-parallel.md approach
  - HANDLE agent failures and partial results

Task 4: PRP Generation Engine
CREATE src/prp_agent/features/prp_generator/generator.py:
  - IMPLEMENT PRP content generation
  - USE prp_base.md template as foundation
  - INTEGRATE research findings into structured output
  - ENSURE template compliance and quality

Task 5: Quality Validation System
CREATE src/prp_agent/features/quality_validator/validator.py:
  - IMPLEMENT 4-metric quality scoring system
  - VALIDATE PRP structure and completeness
  - SCORE: Context richness, Implementation clarity, Validation completeness, Success probability
  - PROVIDE actionable feedback for improvements

Task 6: CLI Interface
CREATE src/prp_agent/main.py:
  - IMPLEMENT command-line interface
  - SUPPORT both interactive and headless modes
  - PATTERN: Follow prp_runner.py structure
  - INCLUDE progress indicators and streaming output

Task 7: Integration with Claude Code
MODIFY src/prp_agent/agent.py:
  - INTEGRATE with Claude Code SDK
  - SUPPORT tool allowlists and permissions
  - ENABLE MCP server integration if needed
  - ENSURE compatibility with existing workflows

Task 8: Testing and Validation
CREATE comprehensive test suite:
  - UNIT tests for all components
  - INTEGRATION tests with real PRP generation
  - PERFORMANCE benchmarks
  - QUALITY validation against known good PRPs
```

### Pseudocode for Core Components

```python
# Core Agent Implementation
async def create_prp_agent() -> Agent:
    """Create and configure PydanticAI agent"""

    # PATTERN: Follow existing model configuration patterns use proper prompting follow the /commands and prp templates for real examples
    agent = Agent(
        model='openai:gpt-4o-mini',  # Default model
        output_type=PRPResult,       # Structured output with Pydantic
        instructions="""
        You are a PRP creation agent. Generate comprehensive PRPs by:
        1. Analyzing user requirements thoroughly
        2. Conducting parallel research across multiple dimensions
        3. Creating structured, actionable implementation plans
        4. Ensuring quality and completeness validation
        """,
        tools=[
            codebase_analyzer_tool,
            documentation_fetcher_tool,
            file_manager_tool,
            quality_validator_tool
        ]
    )

    return agent

# Parallel Research Coordination
async def coordinate_research(request: PRPRequest) -> List[ResearchResult]:
    """Coordinate parallel research agents"""

    # CRITICAL: Launch all agents simultaneously for efficiency
    research_tasks = [
        analyze_codebase_patterns(request.feature_description),
        fetch_external_documentation(request.feature_description),
        analyze_testing_strategies(request.feature_description),
        gather_project_documentation(request.feature_description)
    ]

    # PATTERN: Use asyncio.gather for parallel execution
    results = await asyncio.gather(*research_tasks, return_exceptions=True)

    # GOTCHA: Handle partial failures gracefully
    validated_results = []
    for result in results:
        if isinstance(result, Exception):
            logger.warning(f"Research task failed: {result}")
            continue
        validated_results.append(result)

    return validated_results

# PRP Generation with Quality Validation
async def generate_prp(request: PRPRequest, research: List[ResearchResult]) -> PRPResult:
    """Generate complete PRP with quality validation"""

    # PATTERN: Use structured prompts with research context
    context = synthesize_research_context(research)

    # CRITICAL: Use existing template structure
    template = load_prp_template("prp_base.md")

    # Generate sections iteratively with validation
    sections = []
    for section_name in template.sections:
        section = await generate_section(
            section_name=section_name,
            context=context,
            request=request
        )

        # VALIDATION: Check section quality before proceeding
        quality_score = validate_section_quality(section)
        if quality_score < 7:
            # PATTERN: Iterative refinement
            section = await refine_section(section, quality_score)

        sections.append(section)

    # FINAL: Comprehensive quality validation
    prp_result = PRPResult(
        title=f"PRP: {request.feature_description}",
        sections=sections,
        research_summary=research,
        generated_at=datetime.now().isoformat()
    )

    # QUALITY GATES: Score all dimensions
    prp_result.quality_scores = {
        "context_richness": score_context_richness(prp_result),
        "implementation_clarity": score_implementation_clarity(prp_result),
        "validation_completeness": score_validation_completeness(prp_result),
        "success_probability": score_success_probability(prp_result)
    }

    return prp_result

# Tool Integration Examples
@agent.tool
async def analyze_codebase_patterns(feature_description: str) -> ResearchResult:
    """Analyze codebase for relevant patterns"""

    # PATTERN: Use existing search tools
    relevant_files = await search_codebase_patterns(feature_description)
    patterns = await extract_implementation_patterns(relevant_files)

    return ResearchResult(
        research_type=ResearchType.CODEBASE,
        findings=patterns,
        file_references=relevant_files,
        quality_score=calculate_research_quality(patterns)
    )

@agent.tool
async def fetch_external_documentation(feature_description: str) -> ResearchResult:
    """Fetch and analyze external documentation"""

    # PATTERN: Use WebFetch tool patterns
    search_results = await web_search(f"{feature_description} documentation")
    documentation = await fetch_documentation_urls(search_results)

    return ResearchResult(
        research_type=ResearchType.EXTERNAL,
        findings=documentation,
        url_references=search_results,
        quality_score=calculate_documentation_quality(documentation)
    )
```

### Integration Points

```yaml
DATABASE:
  - table: "prp_generations"
  - fields: "id, request_data, result_data, quality_scores, created_at"
  - index: "CREATE INDEX idx_prp_quality ON prp_generations(quality_scores)"

CONFIG:
  - add to: src/prp_agent/config.py
  - pattern: "OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')"
  - pattern: "ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')"
  - pattern: "PRP_OUTPUT_DIR = Path(os.getenv('PRP_OUTPUT_DIR', 'PRPs/generated'))"

CLAUDE_CODE:
  - integration: Claude Code SDK for tool access
  - pattern: "from claude_code import Client"
  - tools: "Agent,WebFetch,Read,Write,Glob,Grep,Bash"
  - allowlist: Specific tools for PRP generation workflow

CLI:
  - add to: pyproject.toml
  - pattern: "[project.scripts]"
  - pattern: "prp-agent = 'prp_agent.main:main'"

MCP_SERVER:
  - optional: Create MCP server for external tool integration
  - pattern: Follow cc_mcp.md for server configuration
  - tools: Custom tools for specialized PRP operations
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
uv run ruff check src/prp_agent/ --fix
uv run ruff format src/prp_agent/
uv run mypy src/prp_agent/

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests

```python
# CREATE comprehensive test suite following pytest patterns
def test_prp_request_validation():
    """Test input validation for PRP requests"""
    # Valid request
    request = PRPRequest(
        feature_description="Create user authentication system",
        validation_level="comprehensive"
    )
    assert request.feature_description == "Create user authentication system"

    # Invalid request - too short
    with pytest.raises(ValidationError):
        PRPRequest(feature_description="")

async def test_parallel_research_coordination():
    """Test parallel research agent coordination"""
    request = PRPRequest(feature_description="Test feature")

    with Agent.override(model=TestModel()):
        results = await coordinate_research(request)

        assert len(results) == 4  # All research types
        assert all(isinstance(r, ResearchResult) for r in results)
        assert all(r.quality_score >= 1 for r in results)

async def test_prp_generation_quality():
    """Test PRP generation meets quality standards"""
    request = PRPRequest(feature_description="User authentication system")
    research = [create_mock_research_result()]

    with Agent.override(model=TestModel()):
        prp = await generate_prp(request, research)

        assert prp.overall_quality_score() >= 8.0
        assert len(prp.sections) >= 5  # Minimum sections
        assert "Goal" in [s.title for s in prp.sections]
        assert "Implementation Blueprint" in [s.title for s in prp.sections]

def test_quality_validation_metrics():
    """Test quality validation scoring"""
    prp = create_mock_prp_result()

    context_score = score_context_richness(prp)
    clarity_score = score_implementation_clarity(prp)
    validation_score = score_validation_completeness(prp)
    success_score = score_success_probability(prp)

    assert all(1 <= score <= 10 for score in [context_score, clarity_score, validation_score, success_score])
```

```bash
# Run and iterate until passing:
uv run pytest src/prp_agent/tests/ -v --cov=prp_agent
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Tests

```bash
# Test CLI interface
uv run python -m prp_agent "Create a simple REST API with FastAPI"

# Expected output: Complete PRP file generated
# Location: PRPs/generated/create-a-simple-rest-api-with-fastapi.md
# Quality: Overall score >= 8.0

# Test with different models use the actual keys in the .env file and test real requests
OPENAI_API_KEY="test-key" uv run python -m prp_agent "User authentication" --model="openai:gpt-4o-mini"
ANTHROPIC_API_KEY="test-key" uv run python -m prp_agent "User authentication" --model="anthropic:claude-3-haiku-20240307"

# Test error handling
uv run python -m prp_agent ""  # Should fail with validation error
uv run python -m prp_agent "x" * 2000  # Should fail with length validation
```

### Level 4: Quality Validation

```bash
# Generate test PRP and validate
uv run python -m prp_agent "Create a user dashboard with charts" --output-dir="test_output"

# Validate generated PRP structure
uv run python -c "
from prp_agent.features.quality_validator import validate_prp_file
result = validate_prp_file('test_output/create-a-user-dashboard-with-charts.md')
print(f'Quality Score: {result.overall_quality_score():.1f}/10')
assert result.overall_quality_score() >= 8.0
"

# Test implementation success probability
uv run python -c "
from prp_agent.features.quality_validator import predict_implementation_success
prp_content = open('test_output/create-a-user-dashboard-with-charts.md').read()
probability = predict_implementation_success(prp_content)
print(f'Implementation Success Probability: {probability:.1f}%')
assert probability >= 80.0
"
```

## Final Validation Checklist

- [ ] All tests pass: `uv run pytest src/prp_agent/tests/ -v --cov=prp_agent`
- [ ] No linting errors: `uv run ruff check src/prp_agent/`
- [ ] No type errors: `uv run mypy src/prp_agent/`
- [ ] CLI interface works: `uv run python -m prp_agent "Test feature"`
- [ ] Generated PRPs score >= 8.0 on all quality metrics
- [ ] Integration with Claude Code SDK successful
- [ ] Performance benchmark: PRP generation < 2 minutes
- [ ] Error cases handled gracefully with informative messages
- [ ] Documentation generated and complete
- [ ] MCP server integration (if implemented) works correctly
- [ ] Test coverage >= 90%
- [ ] Memory usage stable (no leaks during extended use)
- [ ] Support for multiple model providers verified

---

## Success Metrics Scoring

### Context Richness (1-10)

- **8-10**: Comprehensive research findings, specific file references, external documentation
- **6-7**: Good research coverage, some missing context areas
- **4-5**: Basic research, limited context
- **1-3**: Minimal research, insufficient context

### Implementation Clarity (1-10)

- **8-10**: Clear step-by-step implementation, specific pseudocode, integration points
- **6-7**: Good implementation guidance, some ambiguity
- **4-5**: Basic implementation outline, missing details
- **1-3**: Unclear implementation path, significant gaps

### Validation Completeness (1-10)

- **8-10**: Comprehensive validation gates, executable commands, quality checks
- **6-7**: Good validation coverage, some missing tests
- **4-5**: Basic validation, limited testing
- **1-3**: Minimal validation, insufficient quality gates

### One-Pass Success Probability (1-10)

- **8-10**: High confidence in successful implementation without iterations
- **6-7**: Good probability, may need minor adjustments
- **4-5**: Moderate probability, some iterations expected
- **1-3**: Low probability, significant iterations likely

**Target**: 8+ on all metrics through comprehensive parallel research and validation

## Time Efficiency Benefits

This PydanticAI-based approach provides:

- **10x faster PRP creation**: Automated vs manual research and writing
- **Parallel research**: 4x faster than sequential research
- **Quality consistency**: Standardized validation across all PRPs
- **Reduced iterations**: Comprehensive upfront context reduces implementation cycles
- **Scalable automation**: Handle multiple PRP requests simultaneously

**Expected ROI**: 40+ hours saved per week for active development teams

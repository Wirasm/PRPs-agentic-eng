name: "MCP Crawl4AI RAG Refactor - Phase 1: Foundation First"
description: |

## Purpose
Transform the monolithic mcp-crawl4ai-rag codebase into a maintainable vertical slice architecture with proper separation of concerns, type safety, and comprehensive testing.

## Core Principles
1. **Foundation First**: Build core structure before moving functionality
2. **Type Safety**: Use Pydantic models for all data validation
3. **Test as You Go**: Add pytest tests for each component
4. **Progressive Validation**: Verify each phase before proceeding
5. **Zero Regression**: All existing functionality must continue working

---

## Goal
Refactor the current monolithic codebase (src/crawl4ai_mcp.py: 1054 lines, src/utils.py: 738 lines) into a well-structured vertical slice architecture with proper separation of concerns, comprehensive type safety, and unit tests for all components.

## Why
- Current files exceed 500-line limit (CLAUDE.md requirement)
- Business logic mixed with MCP tool definitions
- No type safety or request/response validation
- Missing unit tests make changes risky
- Difficult to maintain and extend current structure

## What
Transform the codebase into a vertical slice architecture where:
- Each tool is a thin wrapper calling service methods
- Services contain all business logic
- Models provide type safety via Pydantic
- Tests live next to the code they test
- Configuration is centralized and validated

### Success Criteria
- [ ] All files under 500 lines
- [ ] 100% type coverage with Pydantic models
- [ ] Pytest tests for all new components
- [ ] All existing functionality working
- [ ] UV package management properly configured
- [ ] Ruff linting passing

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- file: PRPs/ai_docs/uv_practices.md
  why: Complete UV package management guide - read sections on pyproject.toml setup and pytest integration
  
- file: PRPs/ai_docs/uv_tools.md
  why: UV tools documentation for running tests and linting
  
- file: CLAUDE.md
  why: Project coding standards - especially file size limits and testing requirements
  
- url: https://docs.pydantic.dev/latest/concepts/models/
  why: Pydantic v2 model creation and validation patterns
  
- url: https://docs.pytest.org/en/stable/how-to/fixtures.html
  why: Pytest fixture patterns for test setup
  
- docfile: PRPs/ai_docs/refactor_plan.md
  why: Complete refactor requirements and target structure
```

### Current Codebase tree
```bash
mcp-crawl4ai-rag/
├── src/
│   ├── crawl4ai_mcp.py    # 1054 lines - MCP server + all tool logic
│   └── utils.py           # 738 lines - database, embeddings, search
├── pyproject.toml         # Missing pytest configuration
├── crawled_pages.sql      # Database schema
├── Dockerfile
├── README.md
└── QUICKSTART.md
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
mcp-crawl4ai-rag/
├── main.py                    # Entry point (minimal - just runs src.mcp_server)
├── pyproject.toml            # Updated with pytest config and src layout
├── src/
│   ├── __init__.py
│   ├── config.py             # Pydantic settings & environment validation
│   ├── models.py             # All Pydantic models for requests/responses
│   ├── mcp_server.py         # FastMCP server setup & lifespan management
│   ├── conftest.py           # Shared pytest fixtures
│   │
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── crawling.py       # All crawling logic (from crawl4ai_mcp.py)
│   │   ├── search.py         # Search/RAG logic (from utils.py)
│   │   ├── database.py       # Database operations (from utils.py)
│   │   ├── embeddings.py     # Embedding operations (from utils.py)
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_crawling.py
│   │       ├── test_search.py
│   │       ├── test_database.py
│   │       └── test_embeddings.py
│   │
│   ├── tools/                # MCP tool definitions (thin wrappers)
│   │   ├── __init__.py
│   │   ├── crawl_single_page.py
│   │   ├── smart_crawl_url.py
│   │   ├── get_available_sources.py
│   │   ├── perform_rag_query.py
│   │   ├── search_code_examples.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_crawl_single_page.py
│   │       ├── test_smart_crawl_url.py
│   │       ├── test_get_available_sources.py
│   │       ├── test_perform_rag_query.py
│   │       └── test_search_code_examples.py
│   │
│   └── utils/                # Shared utilities
│       ├── __init__.py
│       ├── text_processing.py  # Text chunking & extraction
│       ├── reranking.py        # Cross-encoder reranking
│       └── tests/
│           ├── __init__.py
│           ├── test_text_processing.py
│           └── test_reranking.py
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: FastMCP requires async functions for all tools
# CRITICAL: Pydantic v2 is used - use model_dump() not dict()
# CRITICAL: UV requires src/ layout for editable installs
# CRITICAL: Supabase client is synchronous but used in async context
# CRITICAL: Environment variables must be loaded with override=True
# CRITICAL: Cross-encoder model loading can fail - needs try/except
# CRITICAL: Crawl4AI crawler needs proper lifecycle management
```

## Implementation Blueprint

### Data models and structure

Create the core data models for type safety and consistency:
```python
# src/models.py examples:
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class CrawlType(str, Enum):
    SINGLE_PAGE = "single_page"
    SITEMAP = "sitemap"
    TXT_FILE = "txt_file"
    RECURSIVE = "recursive"

class CrawlRequest(BaseModel):
    url: HttpUrl
    max_depth: int = Field(default=3, ge=1, le=10)
    max_concurrent: int = Field(default=10, ge=1, le=50)
    chunk_size: int = Field(default=5000, ge=100, le=10000)

class CrawlResult(BaseModel):
    success: bool
    url: str
    crawl_type: CrawlType
    pages_crawled: int = 0
    chunks_stored: int = 0
    code_examples_stored: int = 0
    error: Optional[str] = None

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    source: Optional[str] = None
    num_results: int = Field(default=5, ge=1, le=20)
    semantic_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

class RAGResponse(BaseModel):
    success: bool
    answer: str
    sources: List[Dict[str, Any]]
    error: Optional[str] = None
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1 - Setup UV and pytest:
DONT pyproject.toml:
  - ADD pytest and pytest-asyncio by running uv add pytest pytest-asyncio
  - ADD [tool.pytest.ini_options] section
  - ENSURE src/ layout configuration
  - ADD development dependencies group

Task 2 - Create foundation structure:
CREATE src/__init__.py:
  - Empty file to make src a package
CREATE main.py:
  - MINIMAL entry point that imports and runs src.mcp_server
CREATE src/conftest.py:
  - Shared pytest fixtures for all tests

Task 3 - Create config module:
CREATE src/config.py:
  - MOVE all os.getenv() calls from existing files
  - USE pydantic_settings.BaseSettings
  - VALIDATE all configuration values
  - PATTERN from: PRPs/ai_docs/refactor_plan.md lines 249-274

Task 4 - Create models module:
CREATE src/models.py:
  - CONVERT Crawl4AIContext dataclass to Pydantic model
  - ADD all request/response models shown above
  - ENSURE all fields have proper validation

Task 5 - Create MCP server module:
CREATE src/mcp_server.py:
  - MOVE FastMCP initialization from crawl4ai_mcp.py
  - MOVE crawl4ai_lifespan function
  - IMPORT tools from tools package (will error until Phase 3)
  - NO business logic - just server setup

Task 6 - Create services structure:
CREATE src/services/__init__.py:
  - Empty file
CREATE src/services/database.py:
  - MOVE get_supabase_client from utils.py
  - MOVE add_documents_to_supabase from utils.py
  - MOVE update_source_info from utils.py
  - MOVE add_code_examples_to_supabase from utils.py
CREATE src/services/tests/test_database.py:
  - Unit tests for database operations

Task 7 - Create embeddings service:
CREATE src/services/embeddings.py:
  - MOVE create_embedding from utils.py
  - MOVE create_embeddings_batch from utils.py
  - MOVE generate_contextual_embedding from utils.py
  - MOVE process_chunk_with_context from utils.py
CREATE src/services/tests/test_embeddings.py:
  - Unit tests for embedding operations

Task 8 - Create search service:
CREATE src/services/search.py:
  - MOVE search_documents from utils.py
  - MOVE search_code_examples from utils.py
  - INTEGRATE with reranking if enabled
CREATE src/services/tests/test_search.py:
  - Unit tests for search operations

Task 9 - Create crawling service:
CREATE src/services/crawling.py:
  - MOVE all crawling logic from crawl4ai_mcp.py
  - MOVE is_sitemap, is_txt, parse_sitemap functions
  - MOVE crawl_batch, crawl_recursive_internal_links
  - MOVE extract_code_blocks, generate_code_example_summary from utils.py
CREATE src/services/tests/test_crawling.py:
  - Unit tests for crawling operations

Task 10 - Create utilities:
CREATE src/utils/__init__.py:
  - Empty file
CREATE src/utils/text_processing.py:
  - MOVE smart_chunk_markdown from crawl4ai_mcp.py
  - MOVE extract_section_info from crawl4ai_mcp.py
CREATE src/utils/reranking.py:
  - MOVE rerank_results from crawl4ai_mcp.py
CREATE src/utils/tests/:
  - Unit tests for utilities

Task 11 - Create tools (Phase 3):
CREATE src/tools/ structure:
  - One file per tool
  - Each tool is a thin wrapper calling services
  - Include tests for each tool

Task 12 - Final cleanup:
UPDATE imports throughout codebase
DELETE src/crawl4ai_mcp.py
DELETE src/utils.py
RUN full test suite
```

### Per task pseudocode as needed

```python
# Task 1 - uv add pytest pytest-asyncio

uv add pytest pytest-asyncio

# Task 2 - uv add ruff mypy ipython

uv add ruff mypy ipython

# Task 2.5 - morify pyproject.toml

morify pyproject.toml

[tool.pytest.ini_options]
testpaths = ["src"]
pythonpath = ["src"]
asyncio_mode = "auto"
addopts = "-v --tb=short"

# Task 3 - config.py structure
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    # MCP Server
    host: str = "0.0.0.0"
    port: int = 8051
    
    # OpenAI - REQUIRED
    openai_api_key: str
    model_choice: str = "gpt-4o-mini"
    
    # Supabase - REQUIRED
    supabase_url: str
    supabase_service_key: str
    
    # Feature flags
    use_contextual_embeddings: bool = False
    use_hybrid_search: bool = False
    use_reranking: bool = False
    
    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        extra = "ignore"

# Task 6 - Service pattern example
# src/services/database.py
from typing import List, Dict, Any
from supabase import Client
from src.config import Settings
from src.models import Document, CodeExample

class DatabaseService:
    def __init__(self, client: Client, settings: Settings):
        self.client = client
        self.settings = settings
    
    async def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        # PATTERN: Validate input with Pydantic first
        # PATTERN: Use existing retry patterns
        # PATTERN: Return structured response
        pass

# Task 11 - Tool wrapper pattern
# src/tools/crawl_single_page.py
from src.mcp_server import mcp
from src.services.crawling import CrawlingService
from src.models import CrawlRequest, CrawlResult
from mcp.server.fastmcp import Context

@mcp.tool()
async def crawl_single_page(ctx: Context, url: str) -> str:
    """Crawl a single web page and store its content."""
    # PATTERN: Tool is just a thin wrapper
    service = CrawlingService(ctx.crawler, ctx.supabase_client)
    request = CrawlRequest(url=url)
    result: CrawlResult = await service.crawl_single_page(request)
    return result.model_dump_json(indent=2)
```

### Integration Points
```yaml
DATABASE:
  - No schema changes needed
  - Existing crawled_pages.sql remains valid
  
CONFIG:
  - move to: src/config.py
  - pattern: Use BaseSettings with validation
  - load .env from project root
  
IMPORTS:
  - Update all imports to use new structure
  - main.py imports from src.mcp_server
  - services import from src.models and src.config
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# After each file creation, run:
uv run ruff check src/new_file.py --fix
uv run mypy src/new_file.py

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests for each component
```python
# Example: src/services/tests/test_database.py
import pytest
from unittest.mock import Mock, AsyncMock
from src.services.database import DatabaseService
from src.models import Document

@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    client = Mock()
    client.table = Mock(return_value=Mock(
        insert=Mock(return_value=Mock(execute=AsyncMock()))
    ))
    return client

@pytest.fixture
def database_service(mock_supabase_client, test_settings):
    """Create DatabaseService with mocked dependencies."""
    return DatabaseService(mock_supabase_client, test_settings)

async def test_add_documents_success(database_service):
    """Test successful document addition."""
    docs = [Document(content="test", url="http://example.com")]
    result = await database_service.add_documents(docs)
    assert result["success"] is True

async def test_add_documents_empty_list(database_service):
    """Test handling of empty document list."""
    result = await database_service.add_documents([])
    assert result["success"] is True
    assert result["count"] == 0
```

```bash
# Run tests after creating each service:
uv run pytest src/services/tests/test_database.py -v
# If failing: Read error, fix code, re-run
```

### Level 3: Integration Test
```bash
# After Phase 5 completion:
# Start the refactored service
uv run python main.py
```

Ensure it runs

## Final Validation Checklist
- [ ] UV properly configured: `uv sync` works
- [ ] All tests pass: `uv run pytest src/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] All files under 500 lines
- [ ] Each component has tests
- [ ] Original functionality preserved
- [ ] Can run with: `uv run python main.py`

---

## Anti-Patterns to Avoid
- ❌ Don't move code without understanding dependencies
- ❌ Don't create circular imports between modules
- ❌ Don't put business logic in tool files
- ❌ Don't skip writing tests "to save time"
- ❌ Don't use synchronous Supabase calls in async functions without proper handling
- ❌ Don't forget to validate all inputs with Pydantic models

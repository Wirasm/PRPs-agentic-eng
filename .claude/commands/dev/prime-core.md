> Command for priming Claude Code with core knowledge about your project

# Prime Context for Claude Code

## Auto-detect project type and language

First, analyze the project structure to determine the technology stack:

```bash
# Check for language-specific files and package managers
ls -la | grep -E "\.(py|ts|js|rs|go|json|toml|mod)$"
ls -la | grep -E "(package\.json|pyproject\.toml|Cargo\.toml|go\.mod|bun\.lockb)"
```

Based on detection results:

**Python Projects**: Look for `pyproject.toml`, `requirements.txt`, `setup.py`, `.py` files
- Read pyproject.toml, setup.py, or requirements.txt
- Focus on src/ or main package directory

**TypeScript/JavaScript Projects**: Look for `package.json`, `tsconfig.json`, `.ts/.js` files  
- Read package.json, tsconfig.json
- Focus on src/, app/, or lib/ directories

**Rust Projects**: Look for `Cargo.toml`, `src/main.rs`, `.rs` files
- Read Cargo.toml, src/main.rs
- Focus on src/ directory and crate structure

**Go Projects**: Look for `go.mod`, `main.go`, `.go` files
- Read go.mod, main.go
- Focus on package structure

**Bun Projects**: Look for `bun.lockb`, `package.json` with bun scripts
- Similar to Node.js but note Bun-specific patterns

## Project Analysis

Use the command `tree` to get an understanding of the project structure.

Start with reading the CLAUDE.md file if it exists to get an understanding of the project.

Read the README.md file to get an understanding of the project.

Read key files based on detected language:
- **Python**: Read key files in src/ or main package directory
- **TypeScript/JS/Bun**: Read key files in src/, app/, or components/
- **Rust**: Read src/main.rs, src/lib.rs, and key modules
- **Go**: Read main.go, cmd/, internal/, and pkg/ directories

> List any additional files that are important to understand the project.

Explain back to me:
- **Detected Language/Technology**: What language was detected and key indicators
- **Project Structure**: Overall organization and important directories
- **Project Purpose and Goals**: What the project does and its objectives
- **Key Files and Their Purposes**: Important files for the detected language
- **Dependencies**: Language-specific dependencies and their purposes
- **Configuration Files**: Build tools, linters, formatters, and deployment configs
- **Development Workflow**: How to run, test, and build the project
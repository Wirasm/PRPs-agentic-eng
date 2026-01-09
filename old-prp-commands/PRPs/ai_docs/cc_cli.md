# CLI reference

> Complete reference for Claude Code command-line interface, including commands and flags.

## CLI commands

| Command                            | Description                                    | Example                                                            |
| :--------------------------------- | :--------------------------------------------- | :----------------------------------------------------------------- |
| `claude`                           | Start interactive REPL                         | `claude`                                                           |
| `claude "query"`                   | Start REPL with initial prompt                 | `claude "explain this project"`                                    |
| `claude -p "query"`                | Query via SDK, then exit                       | `claude -p "explain this function"`                                |
| `cat file \| claude -p "query"`    | Process piped content                          | `cat logs.txt \| claude -p "explain"`                              |
| `claude -c`                        | Continue most recent conversation              | `claude -c`                                                        |
| `claude -c -p "query"`             | Continue via SDK                               | `claude -c -p "Check for type errors"`                             |
| `claude -r "<session-id>" "query"` | Resume session by ID                           | `claude -r "abc123" "Finish this PR"`                              |
| `claude update`                    | Update to latest version                       | `claude update`                                                    |
| `claude mcp`                       | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](/en/docs/claude-code/mcp). |

## CLI flags

Customize Claude Code's behavior with these command-line flags:

| Flag                             | Description                                                                                                                                              | Example                                                     |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `--add-dir`                      | Add additional working directories for Claude to access (validates each path exists as a directory)                                                      | `claude --add-dir ../apps ../lib`                           |
| `--allowedTools`                 | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`               |
| `--disallowedTools`              | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`               |
| `--print`, `-p`                  | Print response without interactive mode (see [SDK documentation](/en/docs/claude-code/sdk) for programmatic usage details)                               | `claude -p "query"`                                         |
| `--output-format`                | Specify output format for print mode (options: `text`, `json`, `stream-json`)                                                                            | `claude -p "query" --output-format json`                    |
| `--input-format`                 | Specify input format for print mode (options: `text`, `stream-json`)                                                                                     | `claude -p --output-format json --input-format stream-json` |
| `--verbose`                      | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)                                       | `claude --verbose`                                          |
| `--max-turns`                    | Limit the number of agentic turns in non-interactive mode                                                                                                | `claude -p --max-turns 3 "query"`                           |
| `--model`                        | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model's full name                                    | `claude --model claude-sonnet-4-20250514`                   |
| `--permission-mode`              | Begin in a specified [permission mode](iam#permission-modes)                                                                                             | `claude --permission-mode plan`                             |
| `--permission-prompt-tool`       | Specify an MCP tool to handle permission prompts in non-interactive mode                                                                                 | `claude -p --permission-prompt-tool mcp_auth_tool "query"`  |
| `--resume`                       | Resume a specific session by ID, or by choosing in interactive mode                                                                                      | `claude --resume abc123 "query"`                            |
| `--continue`                     | Load the most recent conversation in the current directory                                                                                               | `claude --continue`                                         |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution)                                                                                                               | `claude --dangerously-skip-permissions`                     |

<Tip>
  The `--output-format json` flag is particularly useful for scripting and
  automation, allowing you to parse Claude's responses programmatically.
</Tip>

For detailed information about print mode (`-p`) including output formats,
streaming, verbose logging, and programmatic usage, see the
[SDK documentation](/en/docs/claude-code/sdk).

## See also

- [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
- [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
- [Quickstart guide](/en/docs/claude-code/quickstart) - Getting started with Claude Code
- [Common workflows](/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
- [Settings](/en/docs/claude-code/settings) - Configuration options
- [SDK documentation](/en/docs/claude-code/sdk) - Programmatic usage and integrations

# Interactive mode

> Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.

## Keyboard shortcuts

### General controls

| Shortcut         | Description                        | Context                    |
| :--------------- | :--------------------------------- | :------------------------- |
| `Ctrl+C`         | Cancel current input or generation | Standard interrupt         |
| `Ctrl+D`         | Exit Claude Code session           | EOF signal                 |
| `Ctrl+L`         | Clear terminal screen              | Keeps conversation history |
| `Up/Down arrows` | Navigate command history           | Recall previous inputs     |
| `Esc` + `Esc`    | Edit previous message              | Double-escape to modify    |

### Multiline input

| Method         | Shortcut       | Context                 |
| :------------- | :------------- | :---------------------- |
| Quick escape   | `\` + `Enter`  | Works in all terminals  |
| macOS default  | `Option+Enter` | Default on macOS        |
| Terminal setup | `Shift+Enter`  | After `/terminal-setup` |
| Paste mode     | Paste directly | For code blocks, logs   |

### Quick commands

| Shortcut     | Description                        | Notes                                                     |
| :----------- | :--------------------------------- | :-------------------------------------------------------- |
| `#` at start | Memory shortcut - add to CLAUDE.md | Prompts for file selection                                |
| `/` at start | Slash command                      | See [slash commands](/en/docs/claude-code/slash-commands) |

## Vim mode

Enable vim-style editing with `/vim` command or configure permanently via `/config`.

### Mode switching

| Command | Action                      | From mode |
| :------ | :-------------------------- | :-------- |
| `Esc`   | Enter NORMAL mode           | INSERT    |
| `i`     | Insert before cursor        | NORMAL    |
| `I`     | Insert at beginning of line | NORMAL    |
| `a`     | Insert after cursor         | NORMAL    |
| `A`     | Insert at end of line       | NORMAL    |
| `o`     | Open line below             | NORMAL    |
| `O`     | Open line above             | NORMAL    |

### Navigation (NORMAL mode)

| Command         | Action                    |
| :-------------- | :------------------------ |
| `h`/`j`/`k`/`l` | Move left/down/up/right   |
| `w`             | Next word                 |
| `e`             | End of word               |
| `b`             | Previous word             |
| `0`             | Beginning of line         |
| `$`             | End of line               |
| `^`             | First non-blank character |
| `gg`            | Beginning of input        |
| `G`             | End of input              |

### Editing (NORMAL mode)

| Command        | Action                  |
| :------------- | :---------------------- |
| `x`            | Delete character        |
| `dd`           | Delete line             |
| `D`            | Delete to end of line   |
| `dw`/`de`/`db` | Delete word/to end/back |
| `cc`           | Change line             |
| `C`            | Change to end of line   |
| `cw`/`ce`/`cb` | Change word/to end/back |
| `.`            | Repeat last change      |

<Tip>
  Configure your preferred line break behavior in terminal settings. Run `/terminal-setup` to install Shift+Enter binding for iTerm2 and VS Code terminals.
</Tip>

## Command history

Claude Code maintains command history for the current session:

- History is stored per working directory
- Cleared with `/clear` command
- Use Up/Down arrows to navigate (see keyboard shortcuts above)
- **Ctrl+R**: Reverse search through history (if supported by terminal)
- **Note**: History expansion (`!`) is disabled by default

## See also

- [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
- [CLI reference](/en/docs/claude-code/cli-reference) - Command-line flags and options
- [Settings](/en/docs/claude-code/settings) - Configuration options
- [Memory management](/en/docs/claude-code/memory) - Managing CLAUDE.md files

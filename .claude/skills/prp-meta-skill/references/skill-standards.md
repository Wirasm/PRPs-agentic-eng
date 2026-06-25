# Skill Standards

The rules every skill obeys, whether being created or refactored. This is the shared "curated context" — keep it here, not duplicated into the workflow files.

## Anatomy

```
skill-name/
├── SKILL.md          # required: YAML frontmatter + markdown body
├── references/       # docs the agent READS on demand (schemas, patterns, edge cases)
├── templates/        # files reused in OUTPUT (report skeletons, output formats)
├── assets/           # non-text output resources (images, boilerplate projects, fonts)
└── scripts/          # executable code, RUN without loading source into context
```

- **references/** = "read this to inform the work."
- **templates/** = "fill this in / follow this shape when producing output."
- **assets/** = "copy or embed this into the result."
- **scripts/** = "execute this for deterministic, token-free work."

## Context sources

Context is King, but it need not all be bundled. A skill draws context from four places — use the cheapest that fits, and curate rather than dump:

1. **Inline** — in `SKILL.md`. The essentials needed every run. Always loaded, so keep it to the spine.
2. **Bundled** — `references/`, `templates/`, `assets/`, `scripts/`. Detail disclosed on demand (see Progressive disclosure).
3. **External pointers** — repo file paths and URLs (optionally with `#anchors`). The agent reads or fetches them when a step needs them; nothing is copied into the skill. Use for docs you do not own or content that would go stale if duplicated.
4. **Runtime-gathered** — the skill instructs the agent to obtain context when it runs: ask the user (interactive skills like a PRD generator), or inspect the environment (read git state, scan the codebase, call a tool or API).

Choose by ownership and volatility: bundle what you own and want versioned; point to what you do not own or what changes upstream; gather at runtime what only exists in the moment (the user's intent, current repo state).

## Frontmatter spec

| Field | Required | Constraint | Notes |
|-------|----------|------------|-------|
| `name` | yes | ≤64 chars, lowercase + hyphens; match the directory | The **directory name** is what becomes `/the-command`; keep `name` equal to it |
| `description` | yes | ≤1024 chars, third person, non-empty | The trigger. Include WHAT it does + WHEN to use it + literal user phrases |
| `argument-hint` | no | string | Autocomplete hint, e.g. `<path/to/plan.md> [--base <branch>]` |
| `allowed-tools` | no | string/list | Tools usable without prompts while active |
| `model` / `effort` | no | model name / level | Override per-skill execution |
| `disable-model-invocation` | no | bool | `true` = user-only (no auto-invoke). **Leave off for prp skills** |
| `user-invocable` | no | bool | `false` = agent-only, hidden from `/`. **Leave off for prp skills** |

For the PRP skill family the default is **both** invocation paths: omit `user-invocable` and `disable-model-invocation`.

The table covers the common fields, not all of them. Other optional fields exist (`when_to_use`, `disallowed-tools`, `paths`, `hooks`, `context: fork` with `agent`, `shell`); reach for them only when a skill actually needs one, and confirm against the current Claude Code skills docs.

## Progressive disclosure (the core mechanic)

Three load levels — design every skill around them:

1. **Metadata** (`name` + `description`) — always in context. ~100 words. This is the trigger budget.
2. **Body** (`SKILL.md`) — loaded when the skill triggers. Target **1,500–2,000 words**, hard ceiling ~5k. Everything here is paid for on every use.
3. **Resources** (`references/`, `templates/`, `scripts/`) — loaded only when the agent reaches for them. Effectively unlimited; scripts cost zero context because only their output enters the conversation.

**Implication:** put the decision spine and workflow in the body; put bulky, occasionally-needed, or output-shaped detail in resources.

## Writing style — two distinct voices

- **`description` → third person, with literal trigger phrases.**
  - Good: `Extract text and tables from PDFs, fill forms, merge documents. Use when the user mentions PDFs, forms, or document extraction.`
  - Bad: `Helps with documents.` (vague) / `Use this when you...` (wrong voice, no triggers)
- **Body → imperative / infinitive, NOT second person.**
  - Good: `To extract fields, run scripts/analyze.py.` / `Validate the output before reporting.`
  - Bad: `You should run the script.` / `Claude will validate the output.`

## No duplication

A fact lives in exactly one place — body OR a reference, never both. Prefer references for detail; keep only the spine and pointers in the body. Duplication is how skills rot (the two copies drift).

## Wiring references

Every bundled file must be linked from SKILL.md, or the agent will not know it exists. End the body with a "Resources" section listing each file and one line on when to read it. Keep references one level deep (linked directly from SKILL.md), not nested chains. External pointers (file paths, URLs) are cited inline at the point of use rather than in Resources, but must resolve — a dead pointer is a broken skill.

## Cross-provider portability

- The portable core is `name` + `description` + body + bundled files. Other tools (Cursor, Gemini CLI, agentskills.io) ignore unknown Claude-only fields (`allowed-tools`, `user-invocable`, etc.) rather than erroring.
- Keep the body's *core value* provider-agnostic. Claude-only mechanics (subagent fan-out, Stop-hook loops, `${CLAUDE_PLUGIN_ROOT}`) still belong in the body when porting verbatim, but note that they degrade or no-op on other providers.
- Make `scripts/` self-contained. For Python, use PEP 723 inline dependencies so they run under `uv` with no setup:
  ```python
  # /// script
  # requires-python = ">=3.10"
  # dependencies = ["pandas"]
  # ///
  ```
- `$ARGUMENTS` / `$1` substitution is a Claude convenience. Write bodies so they still make sense when args are absent (agent-invoked) — fall back to "infer the target from the conversation."

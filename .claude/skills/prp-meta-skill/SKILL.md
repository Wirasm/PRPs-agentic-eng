---
name: prp-meta-skill
description: Author new Claude Code skills PRP-style, and refactor existing fat skills into a lean SKILL.md plus references/. Use when the user wants to "create a skill", "write a new skill", "turn a command into a skill", "split a skill into references", "trim a SKILL.md", "extract output templates from a skill", "make a skill leaner", or invokes /prp-meta-skill.
argument-hint: [create <name> | refactor <path/to/SKILL.md>] (blank = ask which)
---

# PRP Meta-Skill — Author & Refactor Skills

A PRP-style runbook for two jobs:

- **Create** a new skill from scratch (or from an existing command/prompt).
- **Refactor** an existing skill — split detail into `references/`, move output formats into `templates/`, and trim `SKILL.md` to a lean spine of pointers.

This skill is built the way it teaches: a lean body that defers detail to `references/`. Follow that example.

## The PRP lens on skills

Apply the four PRP principles to every skill:

1. **Context is King** — a skill must give the consuming agent ALL the context it needs (patterns, gotchas, schemas, examples), via whichever source fits: carried inline, bundled in `references/`/`templates/` and disclosed on demand, pointed to by file path or URL, or gathered from the user at runtime when the skill is interactive by design. Curate it — don't dump it. (See `references/skill-standards.md` → Context sources.)
2. **Validation loops** — every skill ships verifiable gates. This meta-skill validates with a checklist, the `plugin-dev:skill-reviewer` agent, and a real trigger test (`references/validation.md`).
3. **Information dense** — real trigger phrases, real templates, real `file:line`. No filler, no restating what the model already knows.
4. **Progressive success** — ship a minimal SKILL.md that triggers correctly first, validate, then enrich with references. Do not build all the references before the spine works.

## Step 0 — Pick the mode

- **Creating** a new skill → follow `references/creating-skills.md`.
- **Refactoring / trimming** an existing skill → follow `references/refactoring-skills.md`.
- Both modes obey the same rules (frontmatter spec, writing style, progressive disclosure, no-duplication, invocation control) → read `references/skill-standards.md` first.

If the argument is blank, ask which mode and what the skill/target is. Do not guess.

## Create — quick spine (full detail in references/creating-skills.md)

1. **Gather context (PRP):** collect the concrete phrases that should trigger the skill, the task it performs, the gotchas, and existing patterns to mirror.
2. **Plan resources:** what repeats → a `scripts/` script; what informs thinking → a `references/` doc; what is reused in the output → a `templates/`/`assets/` file.
3. **Scaffold:** copy `templates/SKILL.template.md` into `.claude/skills/<name>/SKILL.md`; create `references/`, `templates/` only as needed.
4. **Write the spine:** third-person trigger-rich `description`; imperative, lean body; push detail to references.
5. **Validate & iterate** (`references/validation.md`): checklist → skill-reviewer → trigger test.

## Refactor — quick spine (full detail in references/refactoring-skills.md)

1. **Inventory** the target SKILL.md. Classify each block: _spine_ (keep) vs _extractable_ (output-format templates, schemas, long worked examples, exhaustive pattern catalogs, troubleshooting, edge-case lists).
2. **Extract verbatim** into the TARGET skill's own `references/` (or `templates/` for output formats). Do not reword anything that affects behavior.
3. **Replace with a pointer.** For **always-needed** content (e.g. an output format the agent must always follow), add a _mandatory-read_ instruction: "Before producing output, read `templates/<x>.md`." For **sometimes-needed** content, a lazy pointer ("For edge cases, see `references/<x>.md`").
4. **Behavior-preservation check** — the trimmed skill + references must drive the SAME process and SAME output as before. Nothing lost, nothing duplicated.
5. **Validate** (`references/validation.md`).

> The single biggest refactor risk: moving an _always-needed_ output format into a lazily-loaded reference, so the agent forgets to read it and the output silently changes. Always pair such extractions with a mandatory-read instruction. See `references/refactoring-skills.md`.

## Resources

- `references/skill-standards.md` — frontmatter spec, progressive disclosure, writing style, no-duplication, invocation control, cross-provider notes
- `references/creating-skills.md` — full PRP-style create runbook
- `references/refactoring-skills.md` — full split-and-trim runbook with a before/after example
- `references/validation.md` — validation gates, checklist, skill-reviewer, trigger test
- `templates/SKILL.template.md` — lean SKILL.md skeleton
- `templates/reference.template.md` — skeleton for an extracted reference/template file

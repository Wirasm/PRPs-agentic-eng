---
name: prp-core-runner
description: Orchestrate complete PRP workflow from feature request to pull request. Run create branch, create PRP, execute implementation, commit changes, and create PR in sequence. Use when implementing features using PRP methodology or when user requests full PRP workflow.
---

# PRP Core Workflow Runner

## Instructions

When the user requests to implement a feature using the PRP workflow or wants end-to-end automation from idea to PR, use the SlashCommand tool to invoke `/prp-core-run-all` with the user's feature description as the argument.

**Step-by-step execution:**

1. **Invoke the workflow**: Use SlashCommand tool with `/prp-core-run-all {feature-description}`
2. **Monitor progress**: The workflow will execute 5 steps in sequence:
   - Create a conventional git branch
   - Generate comprehensive PRP document
   - Execute the PRP implementation
   - Create atomic git commit
   - Create pull request
3. **Handle failures**: If any step fails:
   - Report which step failed and why
   - Do NOT proceed to subsequent steps
   - Provide actionable guidance for fixing the issue
4. **Report completion**: When all steps succeed, confirm the workflow completed and provide the PR URL

**Error Handling:**

- Stop execution immediately if any validation fails
- Report the specific error clearly
- Guide the user on how to resolve the issue
- Do not attempt to auto-fix complex validation failures

## Examples

**Example 1: Autonomous invocation**
```
User: "Can you implement user authentication using JWT with the PRP workflow?"
Assistant: I'll use the prp-core-runner skill to execute the complete PRP workflow for implementing JWT authentication.
[Invokes: /prp-core-run-all Implement user authentication using JWT]
```

**Example 2: Feature request**
```
User: "I need to add a search API with Elasticsearch integration using PRP"
Assistant: I'll run the full PRP workflow to implement the search API with Elasticsearch.
[Invokes: /prp-core-run-all Add search API with Elasticsearch integration]
```

**Example 3: Refactoring with PRP**
```
User: "Use the PRP methodology to refactor the database layer for better performance"
Assistant: I'll execute the PRP workflow for refactoring the database layer.
[Invokes: /prp-core-run-all Refactor database layer for better performance]
```

## When to Use

Use this skill when:
- User explicitly requests to "implement a feature using PRP"
- User asks to "run the full PRP workflow"
- User wants end-to-end automation from feature idea to pull request
- User mentions both "PRP" and a feature to implement
- User requests a complete workflow including branch, implementation, and PR

Do NOT use this skill when:
- User only wants to run a single PRP command (e.g., just create a PRP)
- User is asking about PRP methodology (provide information instead)
- User wants to implement something without mentioning PRP workflow

# Create a Custom Agent in GitHub Copilot

## What Is a Custom Agent?

A **custom agent** (also called a *Copilot coding agent* or *custom Copilot extension*) is a specialized AI assistant built on top of GitHub Copilot that you configure to perform specific, domain-focused tasks within your development workflow. Rather than relying solely on Copilot's general-purpose behavior, a custom agent lets you define its persona, capabilities, context, and tool access so it acts as a purpose-built assistant for your team or project.

---

## Purpose

| Goal | Description |
|---|---|
| **Domain specialization** | Focus the agent on a particular codebase, tech stack, or business domain (e.g., "only help with our internal TypeScript SDK"). |
| **Workflow automation** | Give the agent access to external tools—ticket trackers, CI systems, APIs—so it can complete multi-step tasks end-to-end. |
| **Consistency** | Encode organization-specific conventions, style guides, and patterns into the agent's instructions so all developers get uniform guidance. |
| **Reduced hallucination** | Narrow the agent's scope so it answers from verified internal knowledge rather than general training data. |

---

## When to Use a Custom Agent

- Your project has unique coding standards or architectural patterns not covered by default Copilot.
- Your team uses internal tools (custom CI, proprietary APIs, internal wikis) that a generic agent does not know about.
- You need the agent to execute real actions—opening pull requests, filing tickets, running tests—not just suggest code.
- You want to restrict the agent to a specific set of repositories or languages for security or compliance reasons.
- You are building a developer product and want to surface AI assistance inside your own GitHub App or Copilot Extension.

---

## How It Differs from the Default Copilot Agent

| Aspect | Default Copilot Agent | Custom Agent |
|---|---|---|
| **Scope** | General-purpose; knows most languages and frameworks | Narrowed to whatever you configure |
| **Context** | Uses the currently open file and workspace | Can load your custom knowledge base, docs, and code snippets |
| **Tools** | Built-in GitHub tools (code search, PR actions, etc.) | You choose which tools are enabled and can add new ones via MCP or function calling |
| **Instructions** | GitHub's default system prompt | Your own system prompt / agent instructions file |
| **Identity** | "GitHub Copilot" | A named agent (e.g., "AcmeCorp Bot") |
| **Availability** | Enabled by default in supported editors | Must be authored, configured, and published (optionally listed in the GitHub Marketplace) |

---

## Configuration Options

Custom agents are primarily configured through a **Copilot agent instructions file** (`.github/copilot-instructions.md`) and, for full Copilot Extensions, through a GitHub App manifest.

### 1. Repository Instructions (`.github/copilot-instructions.md`)

The simplest form of customization. Drop this file into any repository and Copilot will prepend its contents to every conversation in that repo.

```markdown
# Copilot Instructions

- Always use TypeScript strict mode.
- Prefer `pnpm` over `npm` or `yarn`.
- Do not suggest any library that is not already in `package.json`.
- Follow the patterns in `src/core/` when adding new services.
```

### 2. Agent Mode System Prompt (`.github/agents/` directory)

For richer multi-step automation, place agent configuration files under `.github/agents/`. Each file defines an agent with its own name, description, and system prompt.

```yaml
# .github/agents/my-agent.yml
name: AcmeBot
description: Handles issue triage and PR reviews for the Acme monorepo
model: gpt-4o
instructions: |
  You are AcmeBot, an expert in the Acme platform.
  When triaging issues, always check for duplicates first.
  When reviewing PRs, enforce the style guide at docs/STYLE.md.
tools:
  - name: github
    enabled: true
  - name: web_search
    enabled: false
```

### 3. Full Copilot Extension (GitHub App)

For the most powerful customization, create a GitHub App that implements the Copilot Extensions API:

- **Skillset extensions** – add new tools the agent can call (REST endpoints you host).
- **Agent extensions** – fully replace Copilot's reasoning loop with your own logic.

Key configuration fields in the GitHub App:

| Field | Purpose |
|---|---|
| `Copilot` → `App type` | Choose *Skillset* or *Agent* |
| `Callback URL` | Your server that handles Copilot chat events (SSE stream) |
| `Permissions` | Scopes granted to the extension (contents, pull requests, issues, etc.) |
| `Where can this GitHub App be installed` | Only this account, or any account |

---

## Permissions and Security Considerations

### Principle of Least Privilege
Grant only the GitHub permissions the agent truly needs. If it only reads code, do not give it `write` access to pull requests or issues.

### Secrets and Sensitive Data
- Never put API keys or passwords in agent instruction files—these files are committed to source control.
- Use GitHub Actions secrets or a secrets manager and inject them at runtime.

### User Confirmation for Destructive Actions
Design any custom tool that performs irreversible actions (deleting files, merging PRs, deploying) to require explicit human confirmation before proceeding.

### Extension Trust Level
- **Private extensions** – available only within your organization; subject to your internal review.
- **Public extensions** – published to the Copilot Marketplace; require GitHub's review and approval before they become available to all users.

### Data Handling
Understand that conversation context (file contents, prompts, tool outputs) may be sent to the LLM provider. Review GitHub's data privacy documentation and your organization's data handling policies before enabling extensions on sensitive repositories.

### Audit Logging
GitHub logs which Copilot extensions are invoked and by whom. Review these logs regularly to detect unexpected usage.

---

## Examples

### Example 1: Repository-Level Instructions

Add `.github/copilot-instructions.md` to enforce project conventions:

```markdown
# Copilot Instructions for MyProject

- All functions must have JSDoc comments.
- Use `const` by default; only use `let` when reassignment is required.
- Test files live in `__tests__/` and follow the `*.test.ts` naming pattern.
```

### Example 2: Custom Triage Agent (Agent Mode)

A Copilot coding agent that automatically labels new issues:

```
User: @AcmeBot triage the new issues opened today

AcmeBot:
1. Fetching issues opened in the last 24 hours... found 5.
2. Analyzing issue #42: "Login button broken on Safari" → label: bug, priority: high
3. Analyzing issue #43: "Add dark mode" → label: enhancement, priority: low
...
Labels applied. Summary posted to #dev-triage Slack channel.
```

### Example 3: Copilot Extension Skillset (Custom Tool)

Expose an internal knowledge base as a Copilot tool:

```json
{
  "type": "function",
  "function": {
    "name": "search_internal_docs",
    "description": "Search Acme's internal engineering wiki",
    "parameters": {
      "type": "object",
      "properties": {
        "query": { "type": "string", "description": "Search terms" }
      },
      "required": ["query"]
    }
  }
}
```

When a developer asks Copilot a question, Copilot calls `search_internal_docs`, your server queries the wiki, and the result is woven back into the answer—grounding the response in real internal knowledge.

---

## Further Reading

- [GitHub Docs: Creating a Copilot Extension](https://docs.github.com/en/copilot/building-copilot-extensions/creating-a-copilot-extension)
- [GitHub Docs: About Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)
- [GitHub Docs: Adding repository custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- [GitHub Marketplace: Copilot Extensions](https://github.com/marketplace?type=apps&copilot_app=true)

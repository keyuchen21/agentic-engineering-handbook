# v1: Model as Agent

**~200 lines. 4 tools. The essence of every coding agent.**

The secret of Claude Code? **There is no secret.**

Strip away the CLI polish, the progress bars, the permission systems. What remains is surprisingly simple: a loop that lets the model call tools until the task is done.

## The Core Insight

Traditional assistants:
```
User -> Model -> Text Response
```

Agent systems:
```
User -> Model -> [Tool -> Result]* -> Response
                      ^___________|
```

The asterisk matters. The model calls tools **repeatedly** until it decides the task is complete. This transforms a chatbot into an autonomous agent.

**Key insight**: The model is the decision-maker. Code just provides tools and runs the loop.

## The Four Essential Tools

Claude Code has ~20 tools. But 4 cover 90% of use cases:

| Tool | Purpose | Example |
|------|---------|---------|
| `bash` | Run commands | `npm install`, `git status` |
| `read_file` | Read contents | View `src/index.ts` |
| `write_file` | Create/overwrite | Create `README.md` |
| `edit_file` | Precise changes | Replace a function |

With these 4 tools, the model can:
- Explore codebases (`bash: find, grep, ls`)
- Understand code (`read_file`)
- Make changes (`write_file`, `edit_file`)
- Run anything (`bash: python, npm, make`)

## The Agent Loop

The entire agent in one function:

```python
def agent_loop(messages):
    while True:
        # 1. Ask the model
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS
        )

        # 2. Print text output
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)

        # 3. If no tool calls, done
        if response.stop_reason != "tool_use":
            return messages

        # 4. Execute tools, continue
        results = []
        for tc in response.tool_calls:
            output = execute_tool(tc.name, tc.input)
            results.append({"type": "tool_result", "tool_use_id": tc.id, "content": output})

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})
```

**Why this works:**
1. Model controls the loop (keeps calling tools until `stop_reason != "tool_use"`)
2. Results become context (fed back as "user" messages)
3. Memory is automatic (messages list accumulates history)

## System Prompt

The only "configuration" needed:

```python
SYSTEM = f"""You are a coding agent at {WORKDIR}.

Loop: think briefly -> use tools -> report results.

Rules:
- Prefer tools over prose. Act, don't just explain.
- Never invent file paths. Use ls/find first if unsure.
- Make minimal changes. Don't over-engineer.
- After finishing, summarize what changed."""
```

No complex logic. Just clear instructions.

## Why This Design Works

**1. Simplicity**
No state machines. No planning modules. No frameworks.

**2. Model does the thinking**
The model decides which tools, in what order, when to stop.

**3. Transparency**
Every tool call visible. Every result in conversation.

**4. Extensibility**
Add a tool = one function + one JSON schema.

## What's Missing

| Feature | Why omitted | Added in |
|---------|-------------|----------|
| Todo tracking | Not essential | v2 |
| Subagents | Complexity | v3 |
| Permissions | Trust model for learning | Production |

The point: **the core is tiny**. Everything else is refinement.

## The Bigger Picture

Claude Code, Cursor Agent, Codex CLI, Devin—all share this pattern:

```python
while not done:
    response = model(conversation, tools)
    results = execute(response.tool_calls)
    conversation.append(results)
```

Differences are in tools, display, safety. But the essence is always: **give the model tools and let it work**.

---

**Model as Agent. That's the whole secret.**

[← Back to README](../README.md) | [Next: v2 →](./v2-structured-planning.md)

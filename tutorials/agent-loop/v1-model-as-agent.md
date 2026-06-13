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

## Study Notes

> Core idea: Agents are not magic. An agent is fundamentally **LLM + Tools + Loop**.

---

### 1. From Chatbot to Agent

Traditional assistant:

```text
User -> Model -> Response
```

Agent:

```text
User -> Model -> [Tool -> Result]* -> Response
                  ^______________|
```

The key difference:

- A chatbot can only respond.
- An agent can take actions.
- The model can repeatedly call tools until the task is complete.

---

### 2. The Essence of an Agent

```python
while True:
    response = model(messages, tools)

    if no_tool_calls:
        break

    result = execute_tool(...)
    messages.append(result)
```

Core loop:

```text
Observe
↓
Think
↓
Act
↓
Observe
```

Or:

```text
Model
↓
Tool
↓
Result
↓
Model
```

---

### 3. The Four Essential Tools

#### bash

Run arbitrary commands.

```bash
ls
find .
git status
pytest
npm install
```

Purpose:

- Explore projects
- Run tests
- Use Git
- Use Docker
- Execute scripts

In many cases:

```text
Agent ≈ LLM + Bash
```

---

#### read_file

Read file contents.

```python
read_file("src/main.py")
```

Purpose:

- Understand code
- Inspect configuration
- Read logs

---

#### write_file

Create or overwrite files.

```python
write_file("README.md", content)
```

Purpose:

- Generate code
- Create documentation
- Create configuration files

---

#### edit_file

Make precise edits.

```python
edit_file(
    path="app.py",
    old_text="foo",
    new_text="bar"
)
```

Purpose:

- Small modifications
- Bug fixes
- Refactoring

---

### 4. The Model IS the Agent

Traditional software:

```python
if A:
    tool1()

if B:
    tool2()
```

The programmer controls the workflow.

Agent systems:

```text
The model controls the workflow.
```

The application only provides tools.

Example:

User:

```text
Fix the failing tests.
```

Possible execution plan:

```text
1. ls
2. pytest
3. read error output
4. read file
5. edit file
6. pytest
7. repeat...
```

The model creates this workflow dynamically.

---

### 5. Why Memory Works

Most simple agents use:

```python
messages = []
```

Continuously append:

```python
messages.append(user)
messages.append(model)
messages.append(tool_result)
```

Resulting history:

```text
User
Assistant
Tool Result
Assistant
Tool Result
...
```

The entire history is sent back to the model.

That history becomes memory.

---

### 6. Reactive Agents

The simplest agents have no long-term planning.

```text
Observe
↓
Act
↓
Observe
↓
Act
```

Example:

```text
ls
↓
read_file
↓
edit_file
↓
pytest
↓
edit_file
↓
pytest
```

A large portion of Claude Code behaves this way.

---

### 7. Planning

Complex tasks benefit from planning.

Example:

```text
Migrate a Flask application to FastAPI.
```

Generate a todo list:

```text
1. Analyze project structure
2. Understand APIs
3. Create FastAPI skeleton
4. Migrate routes
5. Update tests
6. Verify execution
```

Execution flow:

```text
Plan
↓
Execute
↓
Update Plan
↓
Execute
```

Conceptually:

```python
todo_list = [...]
```

---

### 8. Observation Is Critical

Agents are not:

```text
Think -> Act
```

They are:

```text
Think
↓
Act
↓
Observe
↓
Think Again
```

Example:

```bash
pytest
```

Output:

```text
FAILED: test_login
```

That failure is an observation.

The next action depends on it.

---

### 9. Tool Results Must Return to Context

Incorrect:

```python
result = tool()
print(result)
```

Correct:

```python
messages.append(tool_result)
```

Otherwise the model does not know what happened.

Agents require a closed feedback loop:

```text
Model
↓
Tool
↓
Result
↓
Model
```

---

### 10. Where Self-Healing Comes From

The model writes:

```python
foo()
```

Run tests:

```bash
pytest
```

Error:

```text
NameError: foo not defined
```

The error enters context.

The model sees:

```text
foo does not exist
```

It updates the code:

```python
bar()
```

Runs tests again.

Success.

Self-healing is fundamentally:

```text
Observation
↓
Next Prediction
```

---

### 11. Why Bash Is So Powerful

One Bash tool covers:

```text
Git
Docker
Python
Node
Search
Build
Deploy
```

Examples:

Search code:

```bash
grep -r login .
```

Find files:

```bash
find . -name "*.py"
```

Run tests:

```bash
pytest
```

Commit changes:

```bash
git commit
```

Therefore:

```text
bash ≈ many specialized tools combined
```

---

### 12. The Reality of Agent Frameworks

Many frameworks look like:

```text
Planner Agent
↓
Research Agent
↓
Coding Agent
↓
Review Agent
↓
Testing Agent
```

But underneath:

```python
while not done:
    think()
    use_tools()
    observe()
```

The packaging differs.

The core pattern remains.

---

### 13. Evolution Path

#### V1

```text
LLM
+ Tools
+ Loop
```

#### V2

```text
LLM
+ Tools
+ Loop
+ Planning
```

#### V3

```text
LLM
+ Tools
+ Loop
+ Subagents
```

#### Claude Code / Codex CLI

```text
LLM
+ Tools
+ Loop
+ Planning
+ Memory
+ Permissions
+ Git Integration
+ Parallel Agents
```

The core never changes:

```text
Observe
→ Think
→ Act
→ Observe
```

---

### What to Study Next

The next major topic is:

#### Context Engineering

Key question:

```text
Why is the biggest bottleneck in agent systems
often the context window rather than the model?
```

Recommended roadmap:

1. Context Windows
2. Context Engineering
3. RAG
4. Tool Use
5. Planning Systems
6. Memory Systems
7. Multi-Agent Architectures
8. Claude Code Architecture
9. OpenHands Architecture
10. Codex CLI Architecture
11. Long-Running Agents

---

### One-Sentence Summary

```text
Agent = LLM + Tools + Loop

Advanced Agent = LLM + Tools + Loop + Context Engineering
```

The Model Is The Agent.

**Model as Agent. That's the whole secret.**

[← Back to README](../README.md) | [Next: v2 →](./v2-structured-planning.md)

# v3: Subagent Mechanism

**~450 lines. +1 tool. Divide and conquer.**

v2 adds planning. But for large tasks like "explore the codebase then refactor auth", a single agent hits context limits. Exploration dumps 20 files into history. Refactoring loses focus.

v3 adds the **Task tool**: spawn child agents with isolated context.

## The Problem

Single-agent context pollution:

```
Main Agent History:
  [exploring...] cat file1.py -> 500 lines
  [exploring...] cat file2.py -> 300 lines
  ... 15 more files ...
  [now refactoring...] "wait, what did file1 contain?"
```

The solution: **delegate exploration to a subagent**:

```
Main Agent History:
  [Task: explore codebase]
    -> Subagent explores 20 files
    -> Returns: "Auth in src/auth/, DB in src/models/"
  [now refactoring with clean context]
```

## Agent Type Registry

Each agent type defines capabilities:

```python
AGENT_TYPES = {
    "explore": {
        "description": "Read-only for searching and analyzing",
        "tools": ["bash", "read_file"],  # No write
        "prompt": "Search and analyze. Never modify. Return concise summary."
    },
    "code": {
        "description": "Full agent for implementation",
        "tools": "*",  # All tools
        "prompt": "Implement changes efficiently."
    },
    "plan": {
        "description": "Planning and analysis",
        "tools": ["bash", "read_file"],  # Read-only
        "prompt": "Analyze and output numbered plan. Don't change files."
    }
}
```

## The Task Tool

```python
{
    "name": "Task",
    "description": "Spawn a subagent for focused subtask",
    "input_schema": {
        "description": "Short task name (3-5 words)",
        "prompt": "Detailed instructions",
        "agent_type": "explore | code | plan"
    }
}
```

Main agent calls Task → child agent runs → returns summary.

## Subagent Execution

The heart of Task tool:

```python
def run_task(description, prompt, agent_type):
    config = AGENT_TYPES[agent_type]

    # 1. Agent-specific system prompt
    sub_system = f"You are a {agent_type} subagent.\n{config['prompt']}"

    # 2. Filtered tools
    sub_tools = get_tools_for_agent(agent_type)

    # 3. Isolated history (KEY: no parent context)
    sub_messages = [{"role": "user", "content": prompt}]

    # 4. Same query loop
    while True:
        response = client.messages.create(
            model=MODEL, system=sub_system,
            messages=sub_messages, tools=sub_tools
        )
        if response.stop_reason != "tool_use":
            break
        # Execute tools, append results...

    # 5. Return only final text
    return extract_final_text(response)
```

**Key concepts:**

| Concept | Implementation |
|---------|---------------|
| Context isolation | Fresh `sub_messages = []` |
| Tool filtering | `get_tools_for_agent()` |
| Specialized behavior | Agent-specific system prompt |
| Result abstraction | Only final text returned |

## Tool Filtering

```python
def get_tools_for_agent(agent_type):
    allowed = AGENT_TYPES[agent_type]["tools"]
    if allowed == "*":
        return BASE_TOOLS  # No Task (no recursion in demo)
    return [t for t in BASE_TOOLS if t["name"] in allowed]
```

- `explore`: bash + read_file only
- `code`: all tools
- `plan`: bash + read_file only

Subagents don't get Task tool (prevents infinite recursion in this demo).

## Progress Display

Subagent output doesn't pollute main chat:

```
You: explore the codebase
> Task: explore codebase
  [explore] explore codebase ... 5 tools, 3.2s
  [explore] explore codebase - done (8 tools, 5.1s)

Here's what I found: ...
```

Real-time progress, clean final output.

## Typical Flow

```
User: "Refactor auth to use JWT"

Main Agent:
  1. Task(explore): "Find all auth-related files"
     -> Subagent reads 10 files
     -> Returns: "Auth in src/auth/login.py, session in..."

  2. Task(plan): "Design JWT migration"
     -> Subagent analyzes structure
     -> Returns: "1. Add jwt lib 2. Create token utils..."

  3. Task(code): "Implement JWT tokens"
     -> Subagent writes code
     -> Returns: "Created jwt_utils.py, updated login.py"

  4. Summarize changes
```

Each subagent has clean context. Main agent stays focused.

## Comparison

| Aspect | v2 | v3 |
|--------|----|----|
| Context | Single, growing | Isolated per task |
| Exploration | Pollutes history | Contained in subagent |
| Parallelism | No | Possible (not in demo) |
| Code added | ~300 lines | ~450 lines |

## The Pattern

```
Complex Task
  └─ Main Agent (coordinator)
       ├─ Subagent A (explore) -> summary
       ├─ Subagent B (plan) -> plan
       └─ Subagent C (code) -> result
```

Same agent loop, different contexts. That's the whole trick.

---

## Study Notes

### Read the Source in This Order

Open [`v3_subagent.py`](./v3_subagent.py) and read these pieces first:

1. `AGENT_TYPES`
2. `get_agent_descriptions`
3. `TASK_TOOL`
4. `get_tools_for_agent`
5. `run_task`
6. `execute_tool`
7. `agent_loop`

v3 is easiest to understand if you treat it as v2 plus one new capability:

```text
Task(description, prompt, agent_type)
```

Everything else is support code around that one tool.

### The Agent Registry Is the Control Plane

The source defines subagent behavior in `AGENT_TYPES`:

```python
AGENT_TYPES = {
    "explore": {
        "tools": ["bash", "read_file"],
        "prompt": "Search and analyze, but never modify files..."
    },
    "code": {
        "tools": "*",
        "prompt": "Implement the requested changes efficiently."
    },
    "plan": {
        "tools": ["bash", "read_file"],
        "prompt": "Analyze and output a numbered implementation plan..."
    },
}
```

This registry controls three things:

| Field | What it controls |
|-------|------------------|
| `description` | How the main model chooses the right subagent |
| `tools` | What the child is allowed to do |
| `prompt` | How the child should behave |

That is the core idea: subagents are not special magic objects. They are the
same loop with different instructions, different tools, and different context.

### Task Is a Tool That Starts Another Loop

The main agent sees `Task` as a normal tool:

```python
TASK_TOOL = {
    "name": "Task",
    "description": "Spawn a subagent for a focused subtask.",
    ...
}
```

When the model calls `Task`, `execute_tool` dispatches to:

```python
return run_task(args["description"], args["prompt"], args["agent_type"])
```

That means v3 is still the same agent loop. The only twist is that one tool
starts a nested loop.

```text
main agent loop
  -> Task tool
      -> subagent loop
          -> tools
          -> final summary
  -> tool_result back to main agent
```

### Context Isolation Happens in One Line

The most important line in `run_task` is:

```python
sub_messages = [{"role": "user", "content": prompt}]
```

The child does not receive the parent's full conversation. It starts with a
fresh history and only the task prompt.

That gives you:

- cleaner parent context
- cheaper main conversation
- less accidental carryover
- a natural boundary between exploration and implementation

The parent receives only the returned summary, not every intermediate file read.

### Tool Filtering Is Safety and Focus

The function `get_tools_for_agent` decides what each subagent can use:

```python
allowed = AGENT_TYPES[agent_type]["tools"]
if allowed == "*":
    return BASE_TOOLS
return [t for t in BASE_TOOLS if t["name"] in allowed]
```

This is why `explore` and `plan` are read-only:

```text
explore -> bash + read_file
plan    -> bash + read_file
code    -> all base tools
```

Tool filtering does two jobs:

1. It reduces risk. A research agent cannot edit files.
2. It improves behavior. A planning agent is pushed toward analysis, not action.

### Why Subagents Do Not Get Task

In this demo, subagents receive `BASE_TOOLS`, not `ALL_TOOLS`.

That means child agents do not receive the `Task` tool. This avoids recursive
subagent spawning in the learning version.

Production systems may allow deeper trees, but the beginner version keeps the
tree one level deep:

```text
main agent
 ├── explore subagent
 ├── plan subagent
 └── code subagent
```

### What the Parent Actually Sees

Inside `run_task`, the child can make many tool calls. But at the end:

```python
for block in response.content:
    if hasattr(block, "text"):
        return block.text
```

The parent gets the child final text as a single tool result.

This is the whole value of v3:

```text
many child observations -> one parent summary
```

### Good Subagent Boundaries

Use subagents for tasks that are:

- focused
- independently checkable
- context-heavy
- easy to summarize

Good examples:

```text
Find all auth-related files.
Design a migration plan.
Inspect test failures and summarize likely causes.
```

Weak examples:

```text
Fix everything.
Understand the whole repo.
Do the project.
```

If the prompt is too broad, the subagent will return a vague summary.

### Learning Check

After reading the code, make sure you can answer:

- Where are subagent types defined?
- Which line creates isolated child context?
- Why do `explore` and `plan` have read-only tools?
- Why does the demo avoid giving `Task` to subagents?
- What exactly becomes the `tool_result` returned to the parent?

---

**Divide and conquer. Context isolation.**

[← v2](./v2-structured-planning.md) | [Back to README](../README.md) | [v0 →](./v0-bash-is-all-you-need.md)

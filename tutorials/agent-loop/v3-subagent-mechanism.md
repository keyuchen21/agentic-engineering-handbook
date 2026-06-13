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

**Divide and conquer. Context isolation.**

[← v2](./v2-structured-planning.md) | [Back to README](../README.md) | [v0 →](./v0-bash-is-all-you-need.md)

# v0: Bash is All You Need

**The ultimate simplification: ~50 lines, 1 tool, full agent capability.**

After building v1, v2, and v3, a question emerges: what is the *essence* of an agent?

v0 answers this by going backwards—stripping away everything until only the core remains.

## The Core Insight

Unix philosophy: everything is a file, everything can be piped. Bash is the gateway to this world:

| You need | Bash command |
|----------|--------------|
| Read files | `cat`, `head`, `grep` |
| Write files | `echo '...' > file` |
| Search | `find`, `grep`, `rg` |
| Execute | `python`, `npm`, `make` |
| **Subagent** | `python v0_bash_agent.py "task"` |

The last line is the key insight: **calling itself via bash implements subagents**. No Task tool, no Agent Registry—just recursion.

## The Complete Code

```python
#!/usr/bin/env python
from anthropic import Anthropic
import subprocess, sys, os

client = Anthropic(api_key="your-key", base_url="...")
TOOL = [{
    "name": "bash",
    "description": """Execute shell command. Patterns:
- Read: cat/grep/find/ls
- Write: echo '...' > file
- Subagent: python v0_bash_agent.py 'task description'""",
    "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}
}]
SYSTEM = f"CLI agent at {os.getcwd()}. Use bash. Spawn subagent for complex tasks."

def chat(prompt, history=[]):
    history.append({"role": "user", "content": prompt})
    while True:
        r = client.messages.create(model="...", system=SYSTEM, messages=history, tools=TOOL, max_tokens=8000)
        history.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            return "".join(b.text for b in r.content if hasattr(b, "text"))
        results = []
        for b in r.content:
            if b.type == "tool_use":
                out = subprocess.run(b.input["command"], shell=True, capture_output=True, text=True, timeout=300)
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": out.stdout + out.stderr})
        history.append({"role": "user", "content": results})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(chat(sys.argv[1]))  # Subagent mode
    else:
        h = []
        while (q := input(">> ")) not in ("q", ""):
            print(chat(q, h))
```

That's the entire agent. ~50 lines.

## How Subagents Work

```
Main Agent
  └─ bash: python v0_bash_agent.py "analyze architecture"
       └─ Subagent (isolated process, fresh history)
            ├─ bash: find . -name "*.py"
            ├─ bash: cat src/main.py
            └─ Returns summary via stdout
```

**Process isolation = Context isolation**
- Child process has its own `history=[]`
- Parent captures stdout as tool result
- Recursive calls enable unlimited nesting

## What v0 Sacrifices

| Feature | v0 | v3 |
|---------|----|----|
| Agent types | None | explore/code/plan |
| Tool filtering | None | Whitelists |
| Progress display | Plain stdout | Inline updates |
| Code complexity | ~50 lines | ~450 lines |

## What v0 Proves

**Complex capabilities emerge from simple rules:**

1. **One tool is enough** — Bash is the gateway to everything
2. **Recursion = hierarchy** — Self-calls implement subagents
3. **Process = isolation** — OS provides context separation
4. **Prompt = constraint** — Instructions shape behavior

The core pattern never changes:

```python
while True:
    response = model(messages, tools)
    if response.stop_reason != "tool_use":
        return response.text
    results = execute(response.tool_calls)
    messages.append(results)
```

Everything else—todos, subagents, permissions—is refinement around this loop.

---


## Study Notes

### What to Focus On

Read [`v0_bash_agent.py`](./v0_bash_agent.py) as a tiny working model of a
coding agent. The file is small, but it already contains the core architecture:

```text
LLM + one tool + feedback loop = agent
```

Do not start by memorizing every line. First understand the five moving parts:

1. `client` and `MODEL`
2. `TOOL`
3. `SYSTEM`
4. `chat()`
5. the `__main__` block

Those five pieces are enough to explain the whole file.

### 1. The Client and Model

At the top, the program loads environment variables and creates an Anthropic
client:

```python
load_dotenv()
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)
MODEL = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
```

This is not the agent yet. It is only the connection to the model API.

The agent behavior comes from what the host program sends to the model:

```text
system prompt + messages + tools
```

### 2. The One Tool: bash

v0 exposes exactly one tool:

```python
TOOL = [{
    "name": "bash",
    "description": """Execute shell command. Common patterns:
- Read: cat/head/tail, grep/find/rg/ls, wc -l
- Write: echo 'content' > file, sed -i 's/old/new/g' file
- Subagent: python v0_bash_agent.py 'task description' ...""",
    ...
}]
```

The tool schema tells the model:

- the tool name is `bash`
- the input must contain a `command` string
- common command patterns are allowed
- the agent can launch itself as a subagent

The model does **not** execute shell commands. It only asks for a tool call.
The Python host executes the command.

```text
model: please run {"command": "find . -name '*.py'"}
host: runs subprocess.run(...)
host: returns stdout/stderr as tool_result
```

### 3. The System Prompt Teaches Operating Rules

`SYSTEM` tells the model how to behave inside this CLI environment:

```python
SYSTEM = f"""You are a CLI agent at {os.getcwd()}. Solve problems using bash commands.

Rules:
- Prefer tools over prose. Act first, explain briefly after.
- Read files: cat, grep, find, rg, ls, head, tail
- Write files: echo '...' > file, sed -i, or cat << 'EOF' > file
- Subagent: For complex subtasks, spawn a subagent ...
"""
```

This is important because bash is very broad. The prompt narrows that broad tool
into useful coding-agent behavior.

Think of it this way:

```text
TOOL says what the model can call.
SYSTEM says how and when to use it.
```

### 4. The Whole Agent Is `chat()`

The `chat()` function is the agent loop:

```python
def chat(prompt, history=None):
    history.append({"role": "user", "content": prompt})

    while True:
        response = client.messages.create(...)
        history.append({"role": "assistant", "content": content})

        if response.stop_reason != "tool_use":
            return final_text

        results = execute_tool_calls(...)
        history.append({"role": "user", "content": results})
```

The loop has one job: keep giving the model observations until the model stops
requesting tools.

### 5. Why Tool Results Must Go Back Into `history`

This line is the feedback loop:

```python
history.append({"role": "user", "content": results})
```

If the program only printed command output to the terminal, the human would see
it, but the model would not.

For an agent, every action needs an observation:

```text
Thought -> Tool Call -> Tool Result -> Next Thought
```

That is why tool results are appended to `history` and sent back to the model.

### 6. Interactive Mode vs Subagent Mode

At the bottom, the file has two modes:

```python
if len(sys.argv) > 1:
    print(chat(sys.argv[1]))
else:
    history = []
    while True:
        query = input(">> ")
        print(chat(query, history))
```

Interactive mode keeps one shared history:

```text
human -> agent -> human -> agent
```

Subagent mode runs one task and exits:

```bash
python v0_bash_agent.py "explore src/ and summarize"
```

That makes recursion possible.

### 7. How Subagents Work in v0

v0 has no `Task` tool and no agent registry. Subagents work because the only tool
is powerful enough to launch another process:

```bash
python v0_bash_agent.py "analyze architecture"
```

That child process has a fresh `history`. The parent only receives the child's
stdout as a bash tool result.

```text
Parent history
  -> bash: python v0_bash_agent.py "analyze architecture"
       -> Child history starts empty
       -> Child explores with bash
       -> Child prints final summary
  -> Parent receives summary as tool_result
```

This gives context isolation almost for free:

```text
process isolation = context isolation
```

### 8. Why Bash Is Enough for v0

Bash is a gateway to many capabilities:

| Need | Bash pattern |
|------|--------------|
| list files | `find`, `ls`, `rg --files` |
| read files | `cat`, `head`, `sed -n` |
| search | `grep`, `rg` |
| run tests | `pytest`, `npm test`, `make test` |
| edit files | shell redirection, `sed`, heredocs |
| spawn subagents | `python v0_bash_agent.py "task"` |

That is the lesson of v0: a single general tool can create surprisingly capable
agent behavior.

### 9. What v0 Is Not Teaching Yet

v0 is intentionally unsafe and minimal. Do not mistake it for a production
harness.

Missing pieces include:

- command approvals
- filesystem sandboxing
- network restrictions
- structured file edit tools
- todo tracking
- typed subagents
- skill loading
- robust error handling

Those are added later because the point of v0 is to see the smallest possible
agent loop.

### 10. Safety Boundary

The risky line is:

```python
subprocess.run(cmd, shell=True, ...)
```

With unrestricted shell access, a model can request destructive commands. Real
coding agents add sandboxes, approval gates, command policies, and audit logs.

For studying, the key takeaway is not "give agents shell access." The takeaway
is:

```text
agent = model decisions + host-executed tools + returned observations
```

### Learning Check

After reading the code, make sure you can answer:

- Where is the single tool defined?
- What does the tool schema require as input?
- Where does the program call the model?
- Where are tool results appended back into history?
- Why does `stop_reason != "tool_use"` end the loop?
- How does `python v0_bash_agent.py "task"` create a subagent?
- What safety controls are missing from v0?

---

## Full Source

````python
#!/usr/bin/env python
"""
v0_bash_agent.py - Mini Claude Code: Bash is All You Need (~50 lines core)

Core Philosophy: "Bash is All You Need"
======================================
This is the ULTIMATE simplification of a coding agent. After building v1-v3,
we ask: what is the ESSENCE of an agent?

The answer: ONE tool (bash) + ONE loop = FULL agent capability.

Why Bash is Enough:
------------------
Unix philosophy says everything is a file, everything can be piped.
Bash is the gateway to this world:

    | You need      | Bash command                           |
    |---------------|----------------------------------------|
    | Read files    | cat, head, tail, grep                  |
    | Write files   | echo '...' > file, cat << 'EOF' > file |
    | Search        | find, grep, rg, ls                     |
    | Execute       | python, npm, make, any command         |
    | **Subagent**  | python v0_bash_agent.py "task"         |

The last line is the KEY INSIGHT: calling itself via bash implements subagents!
No Task tool, no Agent Registry - just recursion through process spawning.

How Subagents Work:
------------------
    Main Agent
      |-- bash: python v0_bash_agent.py "analyze architecture"
           |-- Subagent (isolated process, fresh history)
                |-- bash: find . -name "*.py"
                |-- bash: cat src/main.py
                |-- Returns summary via stdout

Process isolation = Context isolation:
- Child process has its own history=[]
- Parent captures stdout as tool result
- Recursive calls enable unlimited nesting

Usage:
    # Interactive mode
    python v0_bash_agent.py

    # Subagent mode (called by parent agent or directly)
    python v0_bash_agent.py "explore src/ and summarize"
"""

from anthropic import Anthropic
from dotenv import load_dotenv
import subprocess
import sys
import os

# Load environment variables from .env file
load_dotenv()

# Initialize API client with credentials from environment
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)
MODEL = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")

# The ONE tool that does everything
# Notice how the description teaches the model common patterns AND how to spawn subagents
TOOL = [{
    "name": "bash",
    "description": """Execute shell command. Common patterns:
- Read: cat/head/tail, grep/find/rg/ls, wc -l
- Write: echo 'content' > file, sed -i 's/old/new/g' file
- Subagent: python v0_bash_agent.py 'task description' (spawns isolated agent, returns summary)""",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"]
    }
}]

# System prompt teaches the model HOW to use bash effectively
# Notice the subagent guidance - this is how we get hierarchical task decomposition
SYSTEM = f"""You are a CLI agent at {os.getcwd()}. Solve problems using bash commands.

Rules:
- Prefer tools over prose. Act first, explain briefly after.
- Read files: cat, grep, find, rg, ls, head, tail
- Write files: echo '...' > file, sed -i, or cat << 'EOF' > file
- Subagent: For complex subtasks, spawn a subagent to keep context clean:
  python v0_bash_agent.py "explore src/ and summarize the architecture"

When to use subagent:
- Task requires reading many files (isolate the exploration)
- Task is independent and self-contained
- You want to avoid polluting current conversation with intermediate details

The subagent runs in isolation and returns only its final summary."""


def chat(prompt, history=None):
    """
    The complete agent loop in ONE function.

    This is the core pattern that ALL coding agents share:
        while not done:
            response = model(messages, tools)
            if no tool calls: return
            execute tools, append results

    Args:
        prompt: User's request
        history: Conversation history (mutable, shared across calls in interactive mode)

    Returns:
        Final text response from the model
    """
    if history is None:
        history = []

    history.append({"role": "user", "content": prompt})

    while True:
        # 1. Call the model with tools
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=history,
            tools=TOOL,
            max_tokens=8000
        )

        # 2. Build assistant message content (preserve both text and tool_use blocks)
        content = []
        for block in response.content:
            if hasattr(block, "text"):
                content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
        history.append({"role": "assistant", "content": content})

        # 3. If model didn't call tools, we're done
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if hasattr(b, "text"))

        # 4. Execute each tool call and collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                cmd = block.input["command"]
                print(f"\033[33m$ {cmd}\033[0m")  # Yellow color for commands

                try:
                    out = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300,
                        cwd=os.getcwd()
                    )
                    output = out.stdout + out.stderr
                except subprocess.TimeoutExpired:
                    output = "(timeout after 300s)"

                print(output or "(empty)")
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output[:50000]  # Truncate very long outputs
                })

        # 5. Append results and continue the loop
        history.append({"role": "user", "content": results})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Subagent mode: execute task and print result
        # This is how parent agents spawn children via bash
        print(chat(sys.argv[1]))
    else:
        # Interactive REPL mode
        history = []
        while True:
            try:
                query = input("\033[36m>> \033[0m")  # Cyan prompt
            except (EOFError, KeyboardInterrupt):
                break
            if query in ("q", "exit", ""):
                break
            print(chat(query, history))
````

---

**Bash is All You Need.**

[← Back to README](../README.md)

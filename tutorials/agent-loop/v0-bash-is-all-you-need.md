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

### Building a Minimal CLI Agent with Tool Calling

This example demonstrates the core architecture behind modern AI agents such as Claude Code, Codex CLI, OpenHands, Cursor Agent, and Devin.

The implementation is surprisingly small, but it contains the fundamental agent loop:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Environment
 ↓
Tool Result
 ↓
LLM
 ↓
...
 ↓
Final Answer
```

---

### The Complete Code

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
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {"type": "string"}
        },
        "required": ["command"]
    }
}]

SYSTEM = f"""
CLI agent at {os.getcwd()}.
Use bash.
Spawn subagent for complex tasks.
"""

def chat(prompt, history=[]):
    history.append({"role": "user", "content": prompt})

    while True:
        r = client.messages.create(
            model="...",
            system=SYSTEM,
            messages=history,
            tools=TOOL,
            max_tokens=8000
        )

        history.append({
            "role": "assistant",
            "content": r.content
        })

        if r.stop_reason != "tool_use":
            return "".join(
                b.text for b in r.content
                if hasattr(b, "text")
            )

        results = []

        for b in r.content:
            if b.type == "tool_use":
                out = subprocess.run(
                    b.input["command"],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                results.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": out.stdout + out.stderr
                })

        history.append({
            "role": "user",
            "content": results
        })

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(chat(sys.argv[1]))  # Subagent mode
    else:
        h = []
        while (q := input(">> ")) not in ("q", ""):
            print(chat(q, h))
```

---

### Step 1: Define Tools

The first step is to tell the model which tools it can use.

```python
TOOL = [{
    "name": "bash",
    "description": "...",
    "input_schema": {
        ...
    }
}]
```

This exposes a single tool called `bash`.

The model learns that it can generate tool calls like:

```json
{
  "type": "tool_use",
  "name": "bash",
  "input": {
    "command": "ls -la"
  }
}
```

The LLM itself does not execute commands.

It only requests tool execution.

The host application executes the command.

---

### Step 2: System Prompt

```python
SYSTEM = f"""
CLI agent at {os.getcwd()}.
Use bash.
Spawn subagent for complex tasks.
"""
```

This gives the model information about its environment.

Example:

```text
CLI agent at /home/project

Use bash.

Spawn subagent for complex tasks.
```

The model now understands:

- Current working directory
- Available tool
- Existence of subagents

The system prompt effectively defines the agent's operating environment.

---

### Step 3: User Sends a Task

Example:

```text
Find all Python files larger than 1MB.
```

The prompt is appended to conversation history:

```python
history.append({
    "role": "user",
    "content": prompt
})
```

Then the entire conversation is sent to the model.

---

### Step 4: Model Requests a Tool Call

The model might respond with:

```json
[
  {
    "type": "tool_use",
    "name": "bash",
    "input": {
      "command": "find . -name '*.py' -size +1M"
    }
  }
]
```

At this point:

```python
r.stop_reason == "tool_use"
```

This indicates that the model wants the host application to execute a tool.

The model is not finished reasoning.

It is waiting for observations.

---

### Step 5: Execute the Tool

The application executes:

```python
subprocess.run(
    command,
    shell=True,
    capture_output=True,
    text=True
)
```

Example:

```bash
find . -name '*.py' -size +1M
```

Output:

```text
./models/train.py
./legacy/big_script.py
```

The environment has now produced an observation.

---

### Step 6: Return Tool Results

The result is packaged as:

```json
{
  "type": "tool_result",
  "tool_use_id": "...",
  "content": "./models/train.py\n./legacy/big_script.py"
}
```

This is added back into the conversation:

```python
history.append({
    "role": "user",
    "content": results
})
```

Then the conversation is sent back to the model.

---

### Step 7: The Model Continues Reasoning

Now the model receives:

```text
Tool Result:

./models/train.py
./legacy/big_script.py
```

The model may decide:

```bash
wc -l ./models/train.py
```

or

```bash
head -50 ./legacy/big_script.py
```

Another tool call is generated.

Another observation is returned.

The loop continues.

---

### The Agent Loop

This process repeats until the model no longer requests tools.

```text
LLM
 ↓
Tool Call
 ↓
Environment
 ↓
Observation
 ↓
LLM
 ↓
Tool Call
 ↓
Environment
 ↓
Observation
```

Eventually:

```python
r.stop_reason != "tool_use"
```

The model finally responds:

```text
I found two Python files larger than 1MB:

- models/train.py
- legacy/big_script.py
```

At this point the task is complete.

---

### What Is a Subagent?

Notice the tool description:

```text
Subagent:
python v0_bash_agent.py 'task description'
```

The agent itself can be launched as a command.

This means the model can create another agent instance.

Example:

```bash
python v0_bash_agent.py \
"Analyze all Python files and summarize architecture"
```

Now we have:

```text
Parent Agent
    ↓
Child Agent
    ↓
LLM
    ↓
Tools
```

The child agent operates independently and returns a summarized result.

---

### Hierarchical Agent Architecture

Instead of one giant agent:

```text
Agent
```

We can create:

```text
Agent
 ├── Subagent A
 ├── Subagent B
 └── Subagent C
```

For example:

```text
Main Agent
 ├── Backend Agent
 ├── Frontend Agent
 └── Infrastructure Agent
```

Each agent has:

- Its own context window
- Its own reasoning process
- Its own tool usage

The parent agent only sees summarized outputs.

This greatly improves scalability.

---

### Why Subagents Matter

Suppose a repository contains:

```text
10,000 files
```

One agent cannot effectively inspect everything.

Instead:

```text
Main Agent
 ├── Agent A analyzes backend
 ├── Agent B analyzes frontend
 └── Agent C analyzes deployment
```

Each subagent returns:

```text
Backend Summary:
...

Frontend Summary:
...

Infrastructure Summary:
...
```

The main agent combines them into a final answer.

This resembles MapReduce:

```text
Map Phase:
    Multiple agents analyze independently

Reduce Phase:
    Main agent aggregates results
```

This pattern appears in:

- Claude Code
- OpenAI Codex
- Devin
- Cursor Agent
- OpenHands

---

### ReAct: The Core Agent Pattern

The architecture is an implementation of the ReAct framework.

ReAct stands for:

```text
Reasoning + Acting
```

The loop:

```text
Thought
 ↓
Action
 ↓
Observation
 ↓
Thought
 ↓
Action
 ↓
Observation
```

Example:

```text
Thought:
I need to find large Python files.

Action:
Run find command.

Observation:
Two files found.

Thought:
I should inspect them.

Action:
Run wc and head.

Observation:
Results returned.

Thought:
I have enough information.

Answer:
Generate final response.
```

Modern agents are essentially automated ReAct systems.

---

### Why Tool Calling Is Powerful

Without tools:

```text
LLM
```

The model can only reason about information already in its context.

With tools:

```text
LLM
 ↓
Filesystem
Internet
Databases
APIs
Terminals
Editors
```

The model gains the ability to interact with the external world.

This transforms it from a chatbot into an agent.

---

### Security Concerns

This demo is intentionally simple.

The biggest risk:

```python
shell=True
```

The model can potentially execute:

```bash
rm -rf .
```

or

```bash
curl ...
```

or

```bash
scp ...
```

Real agent systems therefore add:

- Docker sandboxes
- Firecracker VMs
- Permission controls
- Filesystem restrictions
- Network restrictions
- Command allowlists
- Human approval checkpoints

Production-grade agents prioritize safety and isolation.

---

### The Big Picture

The most important idea in this example is not Anthropic, Claude, Python, or Bash.

It is the feedback loop:

```text
LLM
 ↓
Action
 ↓
Environment
 ↓
Observation
 ↓
LLM
```

Everything else is an extension of this pattern.

Modern agent frameworks mainly differ in:

- Number of tools
- Context management
- Memory systems
- Parallel execution
- Subagent orchestration
- Security architecture

The fundamental loop remains the same.

A surprisingly small amount of code can therefore reproduce the core architecture behind today's most advanced coding agents.

---

**Bash is All You Need.**

[← Back to README](../README.md)

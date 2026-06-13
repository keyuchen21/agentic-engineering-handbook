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

**Bash is All You Need.**

[← Back to README](../README.md)

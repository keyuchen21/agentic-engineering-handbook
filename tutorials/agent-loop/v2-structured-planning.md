# v2: Structured Planning with Todo

**~300 lines. +1 tool. Explicit task tracking.**

v1 works. But for complex tasks, the model can lose track.

Ask it to "refactor auth, add tests, update docs" and watch what happens. Without explicit planning, it jumps between tasks, forgets steps, loses focus.

v2 adds one thing: **the Todo tool**. ~100 new lines that fundamentally change how the agent works.

## The Problem

In v1, plans exist only in the model's "head":

```
v1: "I'll do A, then B, then C"  (invisible)
    After 10 tools: "Wait, what was I doing?"
```

The Todo tool makes it explicit:

```
v2:
  [ ] Refactor auth module
  [>] Add unit tests         <- Currently here
  [ ] Update documentation
```

Now both you and the model can see the plan.

## TodoManager

A list with constraints:

```python
class TodoManager:
    def __init__(self):
        self.items = []  # Max 20

    def update(self, items):
        # Validation:
        # - Each needs: content, status, activeForm
        # - Status: pending | in_progress | completed
        # - Only ONE can be in_progress
        # - No duplicates, no empties
```

The constraints matter:

| Rule | Why |
|------|-----|
| Max 20 items | Prevents infinite lists |
| One in_progress | Forces focus |
| Required fields | Structured output |

These aren't arbitrary—they're guardrails.

## The Tool

```python
{
    "name": "TodoWrite",
    "input_schema": {
        "items": [{
            "content": "Task description",
            "status": "pending | in_progress | completed",
            "activeForm": "Present tense: 'Reading files'"
        }]
    }
}
```

The `activeForm` shows what's happening now:

```
[>] Reading authentication code...  <- activeForm
[ ] Add unit tests
```

## System Reminders

Soft constraints to encourage todo usage:

```python
INITIAL_REMINDER = "<reminder>Use TodoWrite for multi-step tasks.</reminder>"
NAG_REMINDER = "<reminder>10+ turns without todo. Please update.</reminder>"
```

Injected as context, not commands:

```python
if rounds_without_todo > 10:
    inject_reminder(NAG_REMINDER)
```

The model sees them but doesn't respond to them.

## The Feedback Loop

When model calls `TodoWrite`:

```
Input:
  [x] Refactor auth (completed)
  [>] Add tests (in_progress)
  [ ] Update docs (pending)

Returned:
  "[x] Refactor auth
   [>] Add tests
   [ ] Update docs
   (1/3 completed)"
```

Model sees its own plan. Updates it. Continues with context.

## When Todos Help

Not every task needs them:

| Good for | Why |
|----------|-----|
| Multi-step work | 5+ steps to track |
| Long conversations | 20+ tool calls |
| Complex refactoring | Multiple files |
| Teaching | Visible "thinking" |

Rule of thumb: **if you'd write a checklist, use todos**.

## Integration

v2 adds to v1 without changing it:

```python
# v1 tools
tools = [bash, read_file, write_file, edit_file]

# v2 adds
tools.append(TodoWrite)
todo_manager = TodoManager()

# v2 tracks usage
if rounds_without_todo > 10:
    inject_reminder()
```

~100 new lines. Same agent loop.

## The Deeper Insight

> **Structure constrains and enables.**

Todo constraints (max items, one in_progress) enable (visible plan, tracked progress).

Pattern in agent design:
- `max_tokens` constrains → enables manageable responses
- Tool schemas constrain → enable structured calls
- Todos constrain → enable complex task completion

Good constraints aren't limitations. They're scaffolding.

---

## Study Notes

### Read the Source in This Order

Open [`v2_todo_agent.py`](./v2_todo_agent.py) and read these pieces first:

1. `TodoManager`
2. `SYSTEM`
3. `TOOLS`
4. `run_todo`
5. `execute_tool`
6. `agent_loop`
7. `main`

The important point is that v2 does not replace the v1 agent loop. It adds one
stateful tool around the same loop.

```text
v1:
model -> tools -> results -> model

v2:
model -> tools + TodoWrite -> results + visible plan -> model
```

### What TodoManager Actually Stores

In the source, `TodoManager` is just an object with one field:

```python
self.items = []
```

The model does not send a small patch like "mark item 2 complete." It sends the
entire new todo list each time:

```python
def update(self, items: list) -> str:
    ...
    self.items = validated
    return self.render()
```

That design is simple and useful for learning:

- The model always owns the full current plan.
- The host validates the plan before accepting it.
- The rendered plan is returned as a tool result.
- The rendered plan goes back into context, so the model can see progress.

### The Three Required Fields

Each todo item must have:

```text
content
status
activeForm
```

Think of them as three different views of the same task:

| Field | Meaning | Example |
|-------|---------|---------|
| `content` | Stable task name | `Add unit tests` |
| `status` | State machine value | `pending`, `in_progress`, `completed` |
| `activeForm` | What the agent is doing now | `Adding unit tests` |

`activeForm` is easy to underestimate. It is not just decoration; it makes
the current activity readable in the trace:

```text
[>] Add unit tests <- Adding unit tests
```

### The Todo List Is a Small State Machine

The status values form a tiny state machine:

```text
pending -> in_progress -> completed
```

The key guardrail is:

```text
only one item can be in_progress
```

That rule forces focus. Without it, the model can claim to be doing many things
at once, which makes the plan less useful.

### How TodoWrite Becomes Part of the Agent Loop

The `TodoWrite` tool is just another tool schema in `TOOLS`:

```python
{
    "name": "TodoWrite",
    "description": "Update the task list. Use to plan and track progress.",
    ...
}
```

The dispatcher routes it like any other tool:

```python
if name == "TodoWrite":
    return run_todo(args["items"])
```

So the core loop still has the same shape:

```text
model chooses tool
host executes tool
host appends tool_result
model observes result
```

The only difference is that one tool updates internal agent state instead of
the filesystem.

### Why Reminders Are Soft, Not Hard

The source includes:

```python
INITIAL_REMINDER = "<reminder>Use TodoWrite for multi-step tasks.</reminder>"
NAG_REMINDER = "<reminder>10+ turns without todo update. Please update todos.</reminder>"
```

This is an important design pattern. The program does not force every task to
use todos. It nudges the model when the task is long enough that a visible plan
would help.

That is why v2 still feels flexible:

- Small task: no checklist needed.
- Multi-step task: TodoWrite creates shared state.
- Long task: reminders reduce drift.

### Common Failure Modes

Watch for these when studying or modifying v2:

1. **Printing a todo is not enough.** It must be returned as a tool result so
   the model can observe it.
2. **Multiple `in_progress` items reduce focus.** The host should reject them.
3. **Too many todos becomes noise.** The max count is a useful constraint.
4. **A hidden plan is not collaboration.** The user and model both need to see
   the state.

### Learning Check

After reading the code, make sure you can answer:

- Where is the todo list stored?
- Why does `update()` receive the full list instead of a diff?
- Where does `TodoWrite` enter the tool dispatcher?
- How does the rendered todo list get back into model context?
- Why does v2 still use the same agent loop as v1?

---

## Full Source

````python
#!/usr/bin/env python3
"""
v2_todo_agent.py - Mini Claude Code: Structured Planning (~300 lines)

Core Philosophy: "Make Plans Visible"
=====================================
v1 works great for simple tasks. But ask it to "refactor auth, add tests,
update docs" and watch what happens. Without explicit planning, the model:
  - Jumps between tasks randomly
  - Forgets completed steps
  - Loses focus mid-way

The Problem - "Context Fade":
----------------------------
In v1, plans exist only in the model's "head":

    v1: "I'll do A, then B, then C"  (invisible)
        After 10 tool calls: "Wait, what was I doing?"

The Solution - TodoWrite Tool:
-----------------------------
v2 adds ONE new tool that fundamentally changes how the agent works:

    v2:
      [ ] Refactor auth module
      [>] Add unit tests         <- Currently working on this
      [ ] Update documentation

Now both YOU and the MODEL can see the plan. The model can:
  - Update status as it works
  - See what's done and what's next
  - Stay focused on one task at a time

Key Constraints (not arbitrary - these are guardrails):
------------------------------------------------------
    | Rule              | Why                              |
    |-------------------|----------------------------------|
    | Max 20 items      | Prevents infinite task lists     |
    | One in_progress   | Forces focus on one thing        |
    | Required fields   | Ensures structured output        |

The Deep Insight:
----------------
> "Structure constrains AND enables."

Todo constraints (max items, one in_progress) ENABLE (visible plan, tracked progress).

This pattern appears everywhere in agent design:
  - max_tokens constrains -> enables manageable responses
  - Tool schemas constrain -> enable structured calls
  - Todos constrain -> enable complex task completion

Good constraints aren't limitations. They're scaffolding.

Usage:
    python v2_todo_agent.py
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("Please install: pip install anthropic python-dotenv")


# =============================================================================
# Configuration
# =============================================================================

API_KEY = os.getenv("ANTHROPIC_API_KEY")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL")
MODEL = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
WORKDIR = Path.cwd()

client = Anthropic(api_key=API_KEY, base_url=BASE_URL) if BASE_URL else Anthropic(api_key=API_KEY)


# =============================================================================
# TodoManager - The core addition in v2
# =============================================================================

class TodoManager:
    """
    Manages a structured task list with enforced constraints.

    Key Design Decisions:
    --------------------
    1. Max 20 items: Prevents the model from creating endless lists
    2. One in_progress: Forces focus - can only work on ONE thing at a time
    3. Required fields: Each item needs content, status, and activeForm

    The activeForm field deserves explanation:
    - It's the PRESENT TENSE form of what's happening
    - Shown when status is "in_progress"
    - Example: content="Add tests", activeForm="Adding unit tests..."

    This gives real-time visibility into what the agent is doing.
    """

    def __init__(self):
        self.items = []

    def update(self, items: list) -> str:
        """
        Validate and update the todo list.

        The model sends a complete new list each time. We validate it,
        store it, and return a rendered view that the model will see.

        Validation Rules:
        - Each item must have: content, status, activeForm
        - Status must be: pending | in_progress | completed
        - Only ONE item can be in_progress at a time
        - Maximum 20 items allowed

        Returns:
            Rendered text view of the todo list
        """
        validated = []
        in_progress_count = 0

        for i, item in enumerate(items):
            # Extract and validate fields
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active_form = str(item.get("activeForm", "")).strip()

            # Validation checks
            if not content:
                raise ValueError(f"Item {i}: content required")
            if status not in ("pending", "in_progress", "completed"):
                raise ValueError(f"Item {i}: invalid status '{status}'")
            if not active_form:
                raise ValueError(f"Item {i}: activeForm required")

            if status == "in_progress":
                in_progress_count += 1

            validated.append({
                "content": content,
                "status": status,
                "activeForm": active_form
            })

        # Enforce constraints
        if len(validated) > 20:
            raise ValueError("Max 20 todos allowed")
        if in_progress_count > 1:
            raise ValueError("Only one task can be in_progress at a time")

        self.items = validated
        return self.render()

    def render(self) -> str:
        """
        Render the todo list as human-readable text.

        Format:
            [x] Completed task
            [>] In progress task <- Doing something...
            [ ] Pending task

            (2/3 completed)

        This rendered text is what the model sees as the tool result.
        It can then update the list based on its current state.
        """
        if not self.items:
            return "No todos."

        lines = []
        for item in self.items:
            if item["status"] == "completed":
                lines.append(f"[x] {item['content']}")
            elif item["status"] == "in_progress":
                lines.append(f"[>] {item['content']} <- {item['activeForm']}")
            else:
                lines.append(f"[ ] {item['content']}")

        completed = sum(1 for t in self.items if t["status"] == "completed")
        lines.append(f"\n({completed}/{len(self.items)} completed)")

        return "\n".join(lines)


# Global todo manager instance
TODO = TodoManager()


# =============================================================================
# System Prompt - Updated for v2
# =============================================================================

SYSTEM = f"""You are a coding agent at {WORKDIR}.

Loop: plan -> act with tools -> update todos -> report.

Rules:
- Use TodoWrite to track multi-step tasks
- Mark tasks in_progress before starting, completed when done
- Prefer tools over prose. Act, don't just explain.
- After finishing, summarize what changed."""


# =============================================================================
# System Reminders - Soft prompts to encourage todo usage
# =============================================================================

# Shown at the start of conversation
INITIAL_REMINDER = "<reminder>Use TodoWrite for multi-step tasks.</reminder>"

# Shown if model hasn't updated todos in a while
NAG_REMINDER = "<reminder>10+ turns without todo update. Please update todos.</reminder>"


# =============================================================================
# Tool Definitions (v1 tools + TodoWrite)
# =============================================================================

TOOLS = [
    # v1 tools (unchanged)
    {
        "name": "bash",
        "description": "Run a shell command.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
    {
        "name": "read_file",
        "description": "Read file contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "edit_file",
        "description": "Replace exact text in file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },

    # NEW in v2: TodoWrite
    # This is the key addition that enables structured planning
    {
        "name": "TodoWrite",
        "description": "Update the task list. Use to plan and track progress.",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "Complete list of tasks (replaces existing)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Task description"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "Task status"
                            },
                            "activeForm": {
                                "type": "string",
                                "description": "Present tense action, e.g. 'Reading files'"
                            },
                        },
                        "required": ["content", "status", "activeForm"],
                    },
                }
            },
            "required": ["items"],
        },
    },
]


# =============================================================================
# Tool Implementations (v1 + TodoWrite)
# =============================================================================

def safe_path(p: str) -> Path:
    """Ensure path stays within workspace."""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


def run_bash(cmd: str) -> str:
    """Execute shell command with safety checks."""
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot"]
    if any(d in cmd for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=60
        )
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout"
    except Exception as e:
        return f"Error: {e}"


def run_read(path: str, limit: int = None) -> str:
    """Read file contents."""
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(text.splitlines()) - limit} more)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"


def run_write(path: str, content: str) -> str:
    """Write content to file."""
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    """Replace exact text in file."""
    try:
        fp = safe_path(path)
        content = fp.read_text()
        if old_text not in content:
            return f"Error: Text not found in {path}"
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


def run_todo(items: list) -> str:
    """
    Update the todo list.

    The model sends a complete new list (not a diff).
    We validate it and return the rendered view.
    """
    try:
        return TODO.update(items)
    except Exception as e:
        return f"Error: {e}"


def execute_tool(name: str, args: dict) -> str:
    """Dispatch tool call to implementation."""
    if name == "bash":
        return run_bash(args["command"])
    if name == "read_file":
        return run_read(args["path"], args.get("limit"))
    if name == "write_file":
        return run_write(args["path"], args["content"])
    if name == "edit_file":
        return run_edit(args["path"], args["old_text"], args["new_text"])
    if name == "TodoWrite":
        return run_todo(args["items"])
    return f"Unknown tool: {name}"


# =============================================================================
# Agent Loop (with todo tracking)
# =============================================================================

# Track how many rounds since last todo update
rounds_without_todo = 0


def agent_loop(messages: list) -> list:
    """
    Agent loop with todo usage tracking.

    Same core loop as v1, but now we track whether the model
    is using todos. If it goes too long without updating,
    we'll inject a reminder in the main() function.
    """
    global rounds_without_todo

    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )

        tool_calls = []
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)
            if block.type == "tool_use":
                tool_calls.append(block)

        if response.stop_reason != "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            return messages

        results = []
        used_todo = False

        for tc in tool_calls:
            print(f"\n> {tc.name}")
            output = execute_tool(tc.name, tc.input)
            preview = output[:300] + "..." if len(output) > 300 else output
            print(f"  {preview}")

            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output,
            })

            # Track todo usage
            if tc.name == "TodoWrite":
                used_todo = True

        # Update counter: reset if used todo, increment otherwise
        if used_todo:
            rounds_without_todo = 0
        else:
            rounds_without_todo += 1

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})


# =============================================================================
# Main REPL
# =============================================================================

def main():
    """
    REPL with reminder injection.

    Key v2 addition: We inject "reminder" messages to encourage
    todo usage without forcing it. This is a soft constraint.

    Reminders are injected as part of the user message, not as
    separate system prompts. The model sees them but doesn't
    respond to them directly.
    """
    global rounds_without_todo

    print(f"Mini Claude Code v2 (with Todos) - {WORKDIR}")
    print("Type 'exit' to quit.\n")

    history = []
    first_message = True

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        # Build user message content
        # May include reminders as context hints
        content = []

        if first_message:
            # Gentle reminder at start
            content.append({"type": "text", "text": INITIAL_REMINDER})
            first_message = False
        elif rounds_without_todo > 10:
            # Nag if model hasn't used todos in a while
            content.append({"type": "text", "text": NAG_REMINDER})

        content.append({"type": "text", "text": user_input})
        history.append({"role": "user", "content": content})

        try:
            agent_loop(history)
        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    main()
````

---

**Explicit planning makes agents reliable.**

[← v1](./v1-model-as-agent.md) | [Back to README](../README.md) | [v3 →](./v3-subagent-mechanism.md)

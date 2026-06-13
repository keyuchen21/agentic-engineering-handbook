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

**Explicit planning makes agents reliable.**

[← v1](./v1-model-as-agent.md) | [Back to README](../README.md) | [v3 →](./v3-subagent-mechanism.md)

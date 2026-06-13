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

**Explicit planning makes agents reliable.**

[← v1](./v1-model-as-agent.md) | [Back to README](../README.md) | [v3 →](./v3-subagent-mechanism.md)

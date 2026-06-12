#!/usr/bin/env python3
"""
Agent Loop From Scratch, v2: Explicit Planning Todo

Run:

    python3 tutorials/agent-loop/v2_explicit_planning_todo.py

What changed from v1
--------------------
v2 adds a tool that does not edit files or run commands:

    TodoWrite

The todo list is visible working state. It helps the user see what the agent is
doing, helps another agent resume the task, and makes drift easier to spot.

The useful constraint is:

    at most one todo item may be in_progress

That turns a plan into a tiny state machine:

    pending -> in_progress -> completed

Original inspiration:
https://claudecn.com/docs/claude-code/advanced/agent-loop/v2-explicit-planning-todo/

Study checkpoints
-----------------
1. Find the `TodoList.update` validation.
2. Watch the trace: the plan changes before and after real work.
3. Ask when TodoWrite is worth the overhead and when it is too much.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional
import shutil
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / ".workdir" / "v2"
Tool = Callable[[Dict[str, object]], str]


@dataclass
class ToolCall:
    name: str
    args: Dict[str, object]


@dataclass
class ModelReply:
    tool: Optional[ToolCall] = None
    final: Optional[str] = None


def seed_lab() -> Path:
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    (WORKDIR / "src").mkdir(parents=True)
    (WORKDIR / "src" / "app.py").write_text(
        textwrap.dedent(
            """\
            def greeting():
                return "hello"


            if __name__ == "__main__":
                print(greeting())
            """
        ),
        encoding="utf-8",
    )
    return WORKDIR


def resolve_path(path: object) -> Path:
    target = (WORKDIR / str(path)).resolve()
    if WORKDIR.resolve() not in target.parents and target != WORKDIR.resolve():
        raise ValueError(f"path escapes lab directory: {path}")
    return target


def bash_tool(args: Dict[str, object]) -> str:
    completed = subprocess.run(
        str(args["command"]),
        cwd=WORKDIR,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
    )
    output = completed.stdout.strip() or "(no output)"
    if completed.returncode:
        output = f"exit={completed.returncode}\n{output}"
    return output


def edit_file_tool(args: Dict[str, object]) -> str:
    target = resolve_path(args["path"])
    text = target.read_text(encoding="utf-8")
    old = str(args["old"])
    if old not in text:
        return f"edit failed: target text not found in {target.relative_to(WORKDIR)}"
    target.write_text(text.replace(old, str(args["new"]), 1), encoding="utf-8")
    return f"edited {target.relative_to(WORKDIR)}"


class TodoList:
    def __init__(self) -> None:
        self.items: List[Dict[str, str]] = []

    def update(self, args: Dict[str, object]) -> str:
        raw_items = args["items"]
        if not isinstance(raw_items, list):
            return "todo update failed: items must be a list"

        items: List[Dict[str, str]] = []
        for raw in raw_items:
            if not isinstance(raw, dict):
                return "todo update failed: each item must be a dict"
            content = str(raw.get("content", "")).strip()
            status = str(raw.get("status", "")).strip()
            active_form = str(raw.get("activeForm", "")).strip()
            if status not in {"pending", "in_progress", "completed"}:
                return f"todo update failed: invalid status {status}"
            if not content or not active_form:
                return "todo update failed: content and activeForm are required"
            items.append(
                {"content": content, "status": status, "activeForm": active_form}
            )

        if sum(item["status"] == "in_progress" for item in items) > 1:
            return "todo update failed: only one item may be in_progress"

        self.items = items
        return self.render()

    def render(self) -> str:
        marker = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]"}
        lines = [
            f"{marker[item['status']]} {item['content']} - {item['activeForm']}"
            for item in self.items
        ]
        done = sum(item["status"] == "completed" for item in self.items)
        lines.append(f"({done}/{len(self.items)} completed)")
        return "\n".join(lines)


def active_form(action: str, status: str) -> str:
    words = {
        "inspect": {
            "pending": "Waiting to inspect the project",
            "in_progress": "Inspecting the project",
            "completed": "Inspected the project",
        },
        "edit": {
            "pending": "Waiting to change the greeting",
            "in_progress": "Changing the greeting",
            "completed": "Changed the greeting",
        },
        "run": {
            "pending": "Waiting to run the app",
            "in_progress": "Running the app",
            "completed": "Ran the app",
        },
    }
    return words[action][status]


def todos(inspect_status: str, edit_status: str, run_status: str) -> List[Dict[str, str]]:
    return [
        {
            "content": "Inspect the project",
            "status": inspect_status,
            "activeForm": active_form("inspect", inspect_status),
        },
        {
            "content": "Change the greeting",
            "status": edit_status,
            "activeForm": active_form("edit", edit_status),
        },
        {
            "content": "Run the app",
            "status": run_status,
            "activeForm": active_form("run", run_status),
        },
    ]


class ScriptedModel:
    def __init__(self) -> None:
        self.steps = [
            ToolCall("TodoWrite", {"items": todos("in_progress", "pending", "pending")}),
            ToolCall("bash", {"command": "find . -maxdepth 3 -type f | sort"}),
            ToolCall("TodoWrite", {"items": todos("completed", "in_progress", "pending")}),
            ToolCall(
                "edit_file",
                {
                    "path": "src/app.py",
                    "old": 'return "hello"',
                    "new": 'return "hello from v2"',
                },
            ),
            ToolCall("TodoWrite", {"items": todos("completed", "completed", "in_progress")}),
            ToolCall("bash", {"command": "python3 src/app.py"}),
            ToolCall("TodoWrite", {"items": todos("completed", "completed", "completed")}),
        ]
        self.index = 0

    def next(self, messages: List[Dict[str, str]]) -> ModelReply:
        if self.index < len(self.steps):
            call = self.steps[self.index]
            self.index += 1
            return ModelReply(tool=call)
        return ModelReply(final="v2 finished. The plan was visible throughout the run.")


def run_agent(model: ScriptedModel, tools: Dict[str, Tool]) -> None:
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Change and verify."}]

    while True:
        reply = model.next(messages)
        if reply.final is not None:
            print("\nFINAL")
            print(reply.final)
            return

        call = reply.tool
        if call is None:
            raise RuntimeError("model returned neither a tool call nor a final answer")

        print(f"\nTOOL CALL: {call.name}({call.args})")
        observation = tools[call.name](call.args)
        print("OBSERVATION:")
        print(textwrap.indent(observation, "  "))
        messages.append({"role": "tool", "content": observation})


def main() -> None:
    seed_lab()
    todo_list = TodoList()
    tools: Dict[str, Tool] = {
        "bash": bash_tool,
        "edit_file": edit_file_tool,
        "TodoWrite": todo_list.update,
    }
    print("Agent Loop From Scratch: v2 Explicit Planning Todo")
    print(f"Lab directory: {WORKDIR}")
    run_agent(ScriptedModel(), tools)


if __name__ == "__main__":
    main()

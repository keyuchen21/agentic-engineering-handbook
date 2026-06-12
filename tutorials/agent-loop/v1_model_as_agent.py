#!/usr/bin/env python3
"""
Agent Loop From Scratch, v1: Model as Agent

Run:

    python3 tutorials/agent-loop/v1_model_as_agent.py

What changed from v0
--------------------
v0 had one universal bash tool. v1 keeps the same loop, but gives the model
several named tools:

    bash, read_file, write_file, edit_file

This makes the harness easier to understand. A trace that says
`edit_file(path="src/app.py", old=..., new=...)` is clearer than a shell
one-liner. It is also easier to validate and approve.

The model is still the decision-maker. The Python code does not hard-code a
workflow like "read, then edit, then run." It only exposes tools and loops.

Original inspiration:
https://claudecn.com/docs/claude-code/advanced/agent-loop/v1-model-as-agent/

Study checkpoints
-----------------
1. Find the `TOOLS` registry.
2. Notice that the loop does not care which tool the model chooses.
3. Compare `edit_file` with doing the same edit through bash.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional
import shutil
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / ".workdir" / "v1"
Tool = Callable[[Dict[str, str]], str]


@dataclass
class ToolCall:
    name: str
    args: Dict[str, str]


@dataclass
class ModelReply:
    tool: Optional[ToolCall] = None
    final: Optional[str] = None


def seed_lab() -> Path:
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    (WORKDIR / "src").mkdir(parents=True)
    (WORKDIR / "README.md").write_text("# Tiny Notes App\n", encoding="utf-8")
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


def resolve_path(path: str) -> Path:
    target = (WORKDIR / path).resolve()
    if WORKDIR.resolve() not in target.parents and target != WORKDIR.resolve():
        raise ValueError(f"path escapes lab directory: {path}")
    return target


def bash_tool(args: Dict[str, str]) -> str:
    command = args["command"]
    completed = subprocess.run(
        command,
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


def read_file_tool(args: Dict[str, str]) -> str:
    return resolve_path(args["path"]).read_text(encoding="utf-8")


def write_file_tool(args: Dict[str, str]) -> str:
    target = resolve_path(args["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(args["content"], encoding="utf-8")
    return f"wrote {target.relative_to(WORKDIR)}"


def edit_file_tool(args: Dict[str, str]) -> str:
    target = resolve_path(args["path"])
    text = target.read_text(encoding="utf-8")
    old = args["old"]
    if old not in text:
        return f"edit failed: target text not found in {target.relative_to(WORKDIR)}"
    target.write_text(text.replace(old, args["new"], 1), encoding="utf-8")
    return f"edited {target.relative_to(WORKDIR)}"


TOOLS: Dict[str, Tool] = {
    "bash": bash_tool,
    "read_file": read_file_tool,
    "write_file": write_file_tool,
    "edit_file": edit_file_tool,
}


class ScriptedModel:
    def __init__(self) -> None:
        self.steps = [
            ToolCall("bash", {"command": "find . -maxdepth 3 -type f | sort"}),
            ToolCall("read_file", {"path": "src/app.py"}),
            ToolCall(
                "write_file",
                {"path": "NOTES.md", "content": "v1 separated bash from file tools.\n"},
            ),
            ToolCall(
                "edit_file",
                {
                    "path": "src/app.py",
                    "old": 'return "hello"',
                    "new": 'return "hello from v1"',
                },
            ),
            ToolCall("bash", {"command": "python3 src/app.py"}),
        ]
        self.index = 0

    def next(self, messages: List[Dict[str, str]]) -> ModelReply:
        if self.index < len(self.steps):
            call = self.steps[self.index]
            self.index += 1
            return ModelReply(tool=call)
        return ModelReply(final="v1 finished. The same loop now has clearer tools.")


def run_agent(model: ScriptedModel) -> None:
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Improve the app."}]

    while True:
        reply = model.next(messages)
        if reply.final is not None:
            print("\nFINAL")
            print(reply.final)
            return

        call = reply.tool
        if call is None:
            raise RuntimeError("model returned neither a tool call nor a final answer")
        if call.name not in TOOLS:
            raise RuntimeError(f"unknown tool: {call.name}")

        print(f"\nTOOL CALL: {call.name}({call.args})")
        observation = TOOLS[call.name](call.args)
        print("OBSERVATION:")
        print(textwrap.indent(observation, "  "))
        messages.append({"role": "tool", "content": observation})


def main() -> None:
    seed_lab()
    print("Agent Loop From Scratch: v1 Model as Agent")
    print(f"Lab directory: {WORKDIR}")
    run_agent(ScriptedModel())


if __name__ == "__main__":
    main()

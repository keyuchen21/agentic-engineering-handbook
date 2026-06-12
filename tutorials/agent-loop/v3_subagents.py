#!/usr/bin/env python3
"""
Agent Loop From Scratch, v3: Subagents

Run:

    python3 tutorials/agent-loop/v3_subagents.py

What changed from v2
--------------------
v3 adds a delegation tool:

    Task(agent_type, instruction)

A subagent is another bounded loop with its own instructions and tool access.
The parent gives it a job, the child does noisy work, and the parent receives a
summary instead of every intermediate detail.

This is mostly about context hygiene. The parent should not have to keep every
search result, file excerpt, and temporary guess in its main context.

Original inspiration:
https://claudecn.com/docs/claude-code/advanced/agent-loop/v3-subagents/

Study checkpoints
-----------------
1. Compare `repo_explorer` and `test_runner`.
2. Notice that the parent receives summaries, not raw child histories.
3. Ask which tools each subagent should be allowed to use in production.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional
import shutil
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / ".workdir" / "v3"
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
    (WORKDIR / "tests").mkdir()
    (WORKDIR / "README.md").write_text(
        "Run the app with `python3 src/app.py` and tests with `python3 -m unittest discover -s tests`.\n",
        encoding="utf-8",
    )
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
    (WORKDIR / "tests" / "test_app.py").write_text(
        textwrap.dedent(
            """\
            import unittest

            from src.app import greeting


            class GreetingTest(unittest.TestCase):
                def test_greeting_has_text(self):
                    self.assertTrue(greeting())


            if __name__ == "__main__":
                unittest.main()
            """
        ),
        encoding="utf-8",
    )
    return WORKDIR


def run_command(command: str) -> str:
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


def edit_file(path: str, old: str, new: str) -> str:
    target = (WORKDIR / path).resolve()
    if WORKDIR.resolve() not in target.parents:
        raise ValueError(f"path escapes lab directory: {path}")
    text = target.read_text(encoding="utf-8")
    if old not in text:
        return f"edit failed: target text not found in {target.relative_to(WORKDIR)}"
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    return f"edited {target.relative_to(WORKDIR)}"


def repo_explorer(instruction: str) -> str:
    """Read-only child agent."""
    print(f"  [subagent repo_explorer] {instruction}")
    files = run_command("find . -maxdepth 3 -type f | sort")
    readme = (WORKDIR / "README.md").read_text(encoding="utf-8")
    return "\n".join(
        [
            "repo_explorer summary:",
            "- Found files:",
            files,
            f"- README length: {len(readme)} characters.",
            "- Entry point appears to be src/app.py.",
        ]
    )


def test_runner(instruction: str) -> str:
    """Verification child agent."""
    print(f"  [subagent test_runner] {instruction}")
    result = run_command("python3 -m unittest discover -s tests")
    return "test_runner summary:\n" + result


def task_tool(args: Dict[str, object]) -> str:
    agent_type = str(args["agent_type"])
    instruction = str(args["instruction"])
    if agent_type == "repo_explorer":
        return repo_explorer(instruction)
    if agent_type == "test_runner":
        return test_runner(instruction)
    return f"unknown subagent type: {agent_type}"


class ScriptedModel:
    def __init__(self) -> None:
        self.steps = [
            ToolCall(
                "Task",
                {
                    "agent_type": "repo_explorer",
                    "instruction": "Map the project and return a concise summary.",
                },
            ),
            ToolCall(
                "edit_file",
                {
                    "path": "src/app.py",
                    "old": 'return "hello"',
                    "new": 'return "hello from v3"',
                },
            ),
            ToolCall(
                "Task",
                {
                    "agent_type": "test_runner",
                    "instruction": "Run tests and summarize the result.",
                },
            ),
        ]
        self.index = 0

    def next(self, messages: List[Dict[str, str]]) -> ModelReply:
        if self.index < len(self.steps):
            call = self.steps[self.index]
            self.index += 1
            return ModelReply(tool=call)
        return ModelReply(
            final=(
                "v3 finished. The parent delegated exploration and verification "
                "while keeping only summaries."
            )
        )


def run_agent(model: ScriptedModel, tools: Dict[str, Tool]) -> None:
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Use subagents to edit safely."}
    ]

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
    tools: Dict[str, Tool] = {
        "Task": task_tool,
        "edit_file": lambda args: edit_file(
            str(args["path"]), str(args["old"]), str(args["new"])
        ),
    }
    print("Agent Loop From Scratch: v3 Subagents")
    print(f"Lab directory: {WORKDIR}")
    run_agent(ScriptedModel(), tools)


if __name__ == "__main__":
    main()

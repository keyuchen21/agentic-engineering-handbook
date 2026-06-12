#!/usr/bin/env python3
"""
Agent Loop From Scratch, v0: Bash Agent

Read this file from top to bottom, then run it:

    python3 tutorials/agent-loop/v0_bash_agent.py

What this version teaches
-------------------------
The smallest useful coding agent is not a giant framework. It is a loop:

    messages -> model -> tool call -> tool result -> messages -> repeat

In v0, the only tool is bash. That sounds almost too simple, but bash can
already inspect files, read source, write files, and run programs.

This is not a production-safe design. A real agent should not get unrestricted
shell access. We start here because it makes the loop impossible to miss.

Original inspiration:
https://claudecn.com/docs/claude-code/advanced/agent-loop/v0-bash-agent/

Study checkpoints
-----------------
1. Find the `while True` loop.
2. Find where the tool result is appended back into `messages`.
3. Find why the loop stops.
4. Ask yourself: what could go wrong if a real model could run any command?
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import shutil
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / ".workdir" / "v0"


@dataclass
class ToolCall:
    name: str
    args: Dict[str, str]


@dataclass
class ModelReply:
    tool: Optional[ToolCall] = None
    final: Optional[str] = None


def seed_lab() -> Path:
    """Create a tiny project so the agent has something real to inspect."""
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    (WORKDIR / "src").mkdir(parents=True)

    (WORKDIR / "README.md").write_text(
        textwrap.dedent(
            """\
            # Tiny Notes App

            This project exists only for the agent-loop tutorial.

            ## Commands

            - Run the app: `python3 src/app.py`
            """
        ),
        encoding="utf-8",
    )
    (WORKDIR / "src" / "app.py").write_text(
        textwrap.dedent(
            """\
            def greeting():
                return "hello from v0"


            if __name__ == "__main__":
                print(greeting())
            """
        ),
        encoding="utf-8",
    )
    return WORKDIR


def bash(command: str, cwd: Path) -> str:
    """
    The single v0 tool.

    This tiny denylist is here so the tutorial cannot accidentally run a very
    dangerous command. It is not a real sandbox.
    """
    denied = ["rm -rf", "sudo ", "git push", "chmod -R 777"]
    if any(pattern in command for pattern in denied):
        return f"blocked unsafe command: {command}"

    completed = subprocess.run(
        command,
        cwd=cwd,
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


class ScriptedModel:
    """
    A fake model for teaching.

    Replace this class with a real LLM call and the loop shape stays the same.
    """

    def __init__(self) -> None:
        self.steps = [
            "pwd",
            "find . -maxdepth 3 -type f | sort",
            "sed -n '1,80p' README.md",
            "python3 src/app.py",
        ]
        self.index = 0

    def next(self, messages: List[Dict[str, str]]) -> ModelReply:
        if self.index < len(self.steps):
            command = self.steps[self.index]
            self.index += 1
            return ModelReply(tool=ToolCall("bash", {"command": command}))

        return ModelReply(
            final=(
                "v0 finished. The agent inspected the project and ran the app "
                "using only one bash tool."
            )
        )


def run_agent(model: ScriptedModel, cwd: Path) -> None:
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Inspect this tiny project and run it."}
    ]

    while True:
        reply = model.next(messages)

        if reply.final is not None:
            print("\nFINAL")
            print(reply.final)
            return

        if reply.tool is None:
            raise RuntimeError("model returned neither a tool call nor a final answer")

        call = reply.tool
        print(f"\nTOOL CALL: {call.name}({call.args})")

        if call.name != "bash":
            raise RuntimeError(f"unknown tool: {call.name}")

        observation = bash(call.args["command"], cwd)
        print("OBSERVATION:")
        print(textwrap.indent(observation, "  "))

        # This line is the heart of the loop: the model sees what happened.
        messages.append({"role": "tool", "content": observation})


def main() -> None:
    cwd = seed_lab()
    print("Agent Loop From Scratch: v0 Bash Agent")
    print(f"Lab directory: {cwd}")
    run_agent(ScriptedModel(), cwd)


if __name__ == "__main__":
    main()

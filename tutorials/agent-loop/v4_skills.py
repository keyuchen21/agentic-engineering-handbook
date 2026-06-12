#!/usr/bin/env python3
"""
Agent Loop From Scratch, v4: Skills

Run:

    python3 tutorials/agent-loop/v4_skills.py

What changed from v3
--------------------
v4 adds on-demand knowledge:

    Skill(name)

Tools are what the agent can do. Skills are what the agent knows how to do.

For this Python-only tutorial, the skill text is stored inside this file and
written into the lab directory at runtime. In a real agent system, a skill
usually lives as a normal editable file, such as `SKILL.md`, with metadata at
the top and detailed instructions below.

The important idea is progressive disclosure:

    always visible: skill name + description
    loaded only when needed: full skill body

Original inspiration:
https://claudecn.com/docs/claude-code/advanced/agent-loop/v4-skills/

Study checkpoints
-----------------
1. Compare `SkillLibrary.descriptions()` with `SkillLibrary.load()`.
2. Notice that the model sees cheap metadata before it loads the full skill.
3. Ask what team knowledge in your own repo should become a skill.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional
import shutil
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / ".workdir" / "v4"
Tool = Callable[[Dict[str, object]], str]


SKILL_FILE_TEXT = """\
---
name: repo-cartographer
description: Map a small repository and summarize structure, entry points, commands, and risks.
---

# Repo Cartographer

Use this checklist when mapping a repository:

1. List top-level files and folders.
2. Identify the runtime entry point.
3. Identify the test command.
4. Say what a new contributor should read first.
5. Mention one risk or unknown.

Return a concise summary with these labels:

- Structure
- Entry point
- Test command
- Read first
- Risk
"""


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
    (WORKDIR / "skills" / "repo-cartographer").mkdir(parents=True)
    (WORKDIR / "README.md").write_text(
        "Run the app with `python3 src/app.py`.\n",
        encoding="utf-8",
    )
    (WORKDIR / "src" / "app.py").write_text(
        textwrap.dedent(
            """\
            def greeting():
                return "hello from v4"


            if __name__ == "__main__":
                print(greeting())
            """
        ),
        encoding="utf-8",
    )
    (WORKDIR / "skills" / "repo-cartographer" / "SKILL.md").write_text(
        SKILL_FILE_TEXT,
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


class SkillLibrary:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.skills = self._index_skills()

    def _index_skills(self) -> Dict[str, Dict[str, str]]:
        skills: Dict[str, Dict[str, str]] = {}
        for path in sorted(self.root.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            metadata, body = self._parse_skill(text)
            name = metadata.get("name", path.parent.name)
            skills[name] = {
                "description": metadata.get("description", ""),
                "body": body,
            }
        return skills

    def _parse_skill(self, text: str) -> tuple[Dict[str, str], str]:
        if not text.startswith("---"):
            return {}, text
        _, frontmatter, body = text.split("---", 2)
        metadata: Dict[str, str] = {}
        for line in frontmatter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        return metadata, body.strip()

    def descriptions(self) -> str:
        lines = []
        for name, skill in self.skills.items():
            lines.append(f"- {name}: {skill['description']}")
        return "\n".join(lines)

    def load(self, args: Dict[str, object]) -> str:
        name = str(args["name"])
        if name not in self.skills:
            return f"skill not found: {name}"
        return self.skills[name]["body"]


class ScriptedModel:
    def __init__(self) -> None:
        self.steps = [
            ToolCall("Skill", {"name": "repo-cartographer"}),
            ToolCall("bash", {"command": "find . -maxdepth 3 -type f | sort"}),
            ToolCall("bash", {"command": "sed -n '1,80p' README.md"}),
        ]
        self.index = 0

    def next(self, messages: List[Dict[str, str]]) -> ModelReply:
        if self.index < len(self.steps):
            call = self.steps[self.index]
            self.index += 1
            return ModelReply(tool=call)
        return ModelReply(
            final=(
                "v4 finished. The agent loaded a reusable skill only when it "
                "needed that knowledge."
            )
        )


def run_agent(model: ScriptedModel, tools: Dict[str, Tool]) -> None:
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Map this project using the right skill."}
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
    skills = SkillLibrary(WORKDIR / "skills")
    tools: Dict[str, Tool] = {
        "Skill": skills.load,
        "bash": lambda args: run_command(str(args["command"])),
    }

    print("Agent Loop From Scratch: v4 Skills")
    print(f"Lab directory: {WORKDIR}")
    print("\nAvailable skill metadata:")
    print(skills.descriptions())
    run_agent(ScriptedModel(), tools)


if __name__ == "__main__":
    main()

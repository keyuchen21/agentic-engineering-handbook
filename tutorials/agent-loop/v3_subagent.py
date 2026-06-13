#!/usr/bin/env python3
"""
v3_subagent.py - Mini Claude Code: Subagent Mechanism (~450 lines)

Core Philosophy: "Divide and Conquer with Context Isolation"
=============================================================
v2 adds planning. But for large tasks like "explore the codebase then
refactor auth", a single agent hits problems:

The Problem - Context Pollution:
-------------------------------
    Single-Agent History:
      [exploring...] cat file1.py -> 500 lines
      [exploring...] cat file2.py -> 300 lines
      ... 15 more files ...
      [now refactoring...] "Wait, what did file1 contain?"

The model's context fills with exploration details, leaving little room
for the actual task. This is "context pollution".

The Solution - Subagents with Isolated Context:
----------------------------------------------
    Main Agent History:
      [Task: explore codebase]
        -> Subagent explores 20 files (in its own context)
        -> Returns ONLY: "Auth in src/auth/, DB in src/models/"
      [now refactoring with clean context]

Each subagent has:
  1. Its own fresh message history
  2. Filtered tools (explore can't write)
  3. Specialized system prompt
  4. Returns only final summary to parent

The Key Insight:
---------------
    Process isolation = Context isolation

By spawning subtasks, we get:
  - Clean context for the main agent
  - Parallel exploration possible
  - Natural task decomposition
  - Same agent loop, different contexts

Agent Type Registry:
-------------------
    | Type    | Tools               | Purpose                     |
    |---------|---------------------|---------------------------- |
    | explore | bash, read_file     | Read-only exploration       |
    | code    | all tools           | Full implementation access  |
    | plan    | bash, read_file     | Design without modifying    |

Typical Flow:
-------------
    User: "Refactor auth to use JWT"

    Main Agent:
      1. Task(explore): "Find all auth-related files"
         -> Subagent reads 10 files
         -> Returns: "Auth in src/auth/login.py..."

      2. Task(plan): "Design JWT migration"
         -> Subagent analyzes structure
         -> Returns: "1. Add jwt lib 2. Create utils..."

      3. Task(code): "Implement JWT tokens"
         -> Subagent writes code
         -> Returns: "Created jwt_utils.py, updated login.py"

      4. Summarize changes to user

Usage:
    python v3_subagent.py
"""

import os
import subprocess
import sys
import time
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
# Agent Type Registry - The core of subagent mechanism
# =============================================================================

AGENT_TYPES = {
    # Explore: Read-only agent for searching and analyzing
    # Cannot modify files - safe for broad exploration
    "explore": {
        "description": "Read-only agent for exploring code, finding files, searching",
        "tools": ["bash", "read_file"],  # No write access
        "prompt": "You are an exploration agent. Search and analyze, but never modify files. Return a concise summary.",
    },

    # Code: Full-powered agent for implementation
    # Has all tools - use for actual coding work
    "code": {
        "description": "Full agent for implementing features and fixing bugs",
        "tools": "*",  # All tools
        "prompt": "You are a coding agent. Implement the requested changes efficiently.",
    },

    # Plan: Analysis agent for design work
    # Read-only, focused on producing plans and strategies
    "plan": {
        "description": "Planning agent for designing implementation strategies",
        "tools": ["bash", "read_file"],  # Read-only
        "prompt": "You are a planning agent. Analyze the codebase and output a numbered implementation plan. Do NOT make changes.",
    },
}


def get_agent_descriptions() -> str:
    """Generate agent type descriptions for the Task tool."""
    return "\n".join(
        f"- {name}: {cfg['description']}"
        for name, cfg in AGENT_TYPES.items()
    )


# =============================================================================
# TodoManager (from v2, unchanged)
# =============================================================================

class TodoManager:
    """Task list manager with constraints. See v2 for details."""

    def __init__(self):
        self.items = []

    def update(self, items: list) -> str:
        validated = []
        in_progress = 0

        for i, item in enumerate(items):
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active = str(item.get("activeForm", "")).strip()

            if not content or not active:
                raise ValueError(f"Item {i}: content and activeForm required")
            if status not in ("pending", "in_progress", "completed"):
                raise ValueError(f"Item {i}: invalid status")
            if status == "in_progress":
                in_progress += 1

            validated.append({
                "content": content,
                "status": status,
                "activeForm": active
            })

        if in_progress > 1:
            raise ValueError("Only one task can be in_progress")

        self.items = validated[:20]
        return self.render()

    def render(self) -> str:
        if not self.items:
            return "No todos."
        lines = []
        for t in self.items:
            mark = "[x]" if t["status"] == "completed" else \
                   "[>]" if t["status"] == "in_progress" else "[ ]"
            lines.append(f"{mark} {t['content']}")
        done = sum(1 for t in self.items if t["status"] == "completed")
        return "\n".join(lines) + f"\n({done}/{len(self.items)} done)"


TODO = TodoManager()


# =============================================================================
# System Prompt
# =============================================================================

SYSTEM = f"""You are a coding agent at {WORKDIR}.

Loop: plan -> act with tools -> report.

You can spawn subagents for complex subtasks:
{get_agent_descriptions()}

Rules:
- Use Task tool for subtasks that need focused exploration or implementation
- Use TodoWrite to track multi-step work
- Prefer tools over prose. Act, don't just explain.
- After finishing, summarize what changed."""


# =============================================================================
# Base Tool Definitions
# =============================================================================

BASE_TOOLS = [
    {
        "name": "bash",
        "description": "Run shell command.",
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
        "description": "Write to file.",
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
        "description": "Replace text in file.",
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
    {
        "name": "TodoWrite",
        "description": "Update task list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"]
                            },
                            "activeForm": {"type": "string"},
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
# Task Tool - The core addition in v3
# =============================================================================

TASK_TOOL = {
    "name": "Task",
    "description": f"""Spawn a subagent for a focused subtask.

Subagents run in ISOLATED context - they don't see parent's history.
Use this to keep the main conversation clean.

Agent types:
{get_agent_descriptions()}

Example uses:
- Task(explore): "Find all files using the auth module"
- Task(plan): "Design a migration strategy for the database"
- Task(code): "Implement the user registration form"
""",
    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Short task name (3-5 words) for progress display"
            },
            "prompt": {
                "type": "string",
                "description": "Detailed instructions for the subagent"
            },
            "agent_type": {
                "type": "string",
                "enum": list(AGENT_TYPES.keys()),
                "description": "Type of agent to spawn"
            },
        },
        "required": ["description", "prompt", "agent_type"],
    },
}

# Main agent gets all tools including Task
ALL_TOOLS = BASE_TOOLS + [TASK_TOOL]


def get_tools_for_agent(agent_type: str) -> list:
    """
    Filter tools based on agent type.

    Each agent type has a whitelist of allowed tools.
    '*' means all tools (but subagents don't get Task to prevent infinite recursion).
    """
    allowed = AGENT_TYPES.get(agent_type, {}).get("tools", "*")

    if allowed == "*":
        return BASE_TOOLS  # All base tools, but NOT Task (no recursion in demo)

    return [t for t in BASE_TOOLS if t["name"] in allowed]


# =============================================================================
# Tool Implementations
# =============================================================================

def safe_path(p: str) -> Path:
    """Ensure path stays within workspace."""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


def run_bash(cmd: str) -> str:
    """Execute shell command with safety checks."""
    if any(d in cmd for d in ["rm -rf /", "sudo", "shutdown"]):
        return "Error: Dangerous command"
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=60
        )
        return ((r.stdout + r.stderr).strip() or "(no output)")[:50000]
    except Exception as e:
        return f"Error: {e}"


def run_read(path: str, limit: int = None) -> str:
    """Read file contents."""
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit:
            lines = lines[:limit]
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
        text = fp.read_text()
        if old_text not in text:
            return f"Error: Text not found in {path}"
        fp.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


def run_todo(items: list) -> str:
    """Update the todo list."""
    try:
        return TODO.update(items)
    except Exception as e:
        return f"Error: {e}"


# =============================================================================
# Subagent Execution - The heart of v3
# =============================================================================

def run_task(description: str, prompt: str, agent_type: str) -> str:
    """
    Execute a subagent task with isolated context.

    This is the core of the subagent mechanism:

    1. Create isolated message history (KEY: no parent context!)
    2. Use agent-specific system prompt
    3. Filter available tools based on agent type
    4. Run the same query loop as main agent
    5. Return ONLY the final text (not intermediate details)

    The parent agent sees just the summary, keeping its context clean.

    Progress Display:
    ----------------
    While running, we show:
      [explore] find auth files ... 5 tools, 3.2s

    This gives visibility without polluting the main conversation.
    """
    if agent_type not in AGENT_TYPES:
        return f"Error: Unknown agent type '{agent_type}'"

    config = AGENT_TYPES[agent_type]

    # Agent-specific system prompt
    sub_system = f"""You are a {agent_type} subagent at {WORKDIR}.

{config["prompt"]}

Complete the task and return a clear, concise summary."""

    # Filtered tools for this agent type
    sub_tools = get_tools_for_agent(agent_type)

    # ISOLATED message history - this is the key!
    # The subagent starts fresh, doesn't see parent's conversation
    sub_messages = [{"role": "user", "content": prompt}]

    # Progress tracking
    print(f"  [{agent_type}] {description}")
    start = time.time()
    tool_count = 0

    # Run the same agent loop (silently - don't print to main chat)
    while True:
        response = client.messages.create(
            model=MODEL,
            system=sub_system,
            messages=sub_messages,
            tools=sub_tools,
            max_tokens=8000,
        )

        if response.stop_reason != "tool_use":
            break

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        results = []

        for tc in tool_calls:
            tool_count += 1
            output = execute_tool(tc.name, tc.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output
            })

            # Update progress line (in-place)
            elapsed = time.time() - start
            sys.stdout.write(
                f"\r  [{agent_type}] {description} ... {tool_count} tools, {elapsed:.1f}s"
            )
            sys.stdout.flush()

        sub_messages.append({"role": "assistant", "content": response.content})
        sub_messages.append({"role": "user", "content": results})

    # Final progress update
    elapsed = time.time() - start
    sys.stdout.write(
        f"\r  [{agent_type}] {description} - done ({tool_count} tools, {elapsed:.1f}s)\n"
    )

    # Extract and return only the final text
    # This is what the parent agent sees - a clean summary
    for block in response.content:
        if hasattr(block, "text"):
            return block.text

    return "(subagent returned no text)"


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
    if name == "Task":
        return run_task(args["description"], args["prompt"], args["agent_type"])
    return f"Unknown tool: {name}"


# =============================================================================
# Main Agent Loop
# =============================================================================

def agent_loop(messages: list) -> list:
    """
    Main agent loop with subagent support.

    Same pattern as v1/v2, but now includes the Task tool.
    When model calls Task, it spawns a subagent with isolated context.
    """
    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=ALL_TOOLS,
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
        for tc in tool_calls:
            # Task tool has special display handling
            if tc.name == "Task":
                print(f"\n> Task: {tc.input.get('description', 'subtask')}")
            else:
                print(f"\n> {tc.name}")

            output = execute_tool(tc.name, tc.input)

            # Don't print full Task output (it manages its own display)
            if tc.name != "Task":
                preview = output[:200] + "..." if len(output) > 200 else output
                print(f"  {preview}")

            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})


# =============================================================================
# Main REPL
# =============================================================================

def main():
    print(f"Mini Claude Code v3 (with Subagents) - {WORKDIR}")
    print(f"Agent types: {', '.join(AGENT_TYPES.keys())}")
    print("Type 'exit' to quit.\n")

    history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        history.append({"role": "user", "content": user_input})

        try:
            agent_loop(history)
        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    main()

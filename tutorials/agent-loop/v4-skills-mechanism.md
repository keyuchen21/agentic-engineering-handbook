# v4: Skills Mechanism

**Core insight: Skills are knowledge packages, not tools.**

## Knowledge Externalization: From Training to Editing

Skills embody a profound paradigm shift: **Knowledge Externalization**.

### Traditional Approach: Knowledge Internalized in Parameters

Traditional AI systems store all knowledge in model parameters. You can't access it, modify it, or reuse it.

Want the model to learn a new skill? You need to:
1. Collect massive training data
2. Set up distributed training clusters
3. Perform complex parameter fine-tuning (LoRA, full fine-tuning, etc.)
4. Deploy a new model version

It's like your brain suddenly losing memory, but you have no notes to restore it. Knowledge is locked in the neural network's weight matrices, completely opaque to users.

### New Paradigm: Knowledge Externalized as Documents

The code execution paradigm changes everything.

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Knowledge Storage Hierarchy                       │
│                                                                       │
│  Model Parameters → Context Window → File System → Skill Library      │
│    (internalized)     (runtime)       (persistent)   (structured)     │
│                                                                       │
│  ←────── Requires Training ──────→  ←─── Natural Language Edit ────→  │
│    Needs clusters, data, expertise        Anyone can modify           │
└──────────────────────────────────────────────────────────────────────┘
```

**Key Breakthrough**:
- **Before**: Modify model behavior = Modify parameters = Requires training = GPU clusters + training data + ML expertise
- **Now**: Modify model behavior = Edit SKILL.md = Edit text file = Anyone can do it

It's like attaching a hot-swappable LoRA adapter to a base model, but without any parameter training.

### Why This Matters

1. **Democratization**: No ML expertise required to customize model behavior
2. **Transparency**: Knowledge stored in human-readable Markdown, auditable and understandable
3. **Reusability**: Write a skill once, use it on any compatible agent
4. **Version Control**: Git manages knowledge changes, supports collaboration and rollback
5. **Online Learning**: Model "learns" in the larger context window, no offline training needed

Traditional fine-tuning is **offline learning**: collect data -> train -> deploy -> use.
Skills enable **online learning**: load knowledge on-demand at runtime, effective immediately.

### Knowledge Hierarchy Comparison

| Layer | Modification | Effective Time | Persistence | Cost |
|-------|--------------|----------------|-------------|------|
| Model Parameters | Training/Fine-tuning | Hours to Days | Permanent | $10K-$1M+ |
| Context Window | API call | Instant | Per-session | ~$0.01/call |
| File System | Edit file | Next load | Permanent | Free |
| **Skill Library** | **Edit SKILL.md** | **Next trigger** | **Permanent** | **Free** |

Skills hit the sweet spot: persistent storage + on-demand loading + human-editable.

### Practical Example

Suppose you want Claude to learn your company's specific coding standards:

**Traditional Way**:
```
1. Collect company codebase as training data
2. Prepare fine-tuning scripts and infrastructure
3. Run LoRA fine-tuning (requires GPU)
4. Deploy custom model
5. Cost: $1000+ and weeks of time
```

**Skills Way**:
```markdown
# skills/company-standards/SKILL.md
---
name: company-standards
description: Company coding standards and best practices
---

## Naming Conventions
- Functions use lowercase_with_underscores
- Classes use PascalCase
...
```
```
Cost: $0, Time: 5 minutes
```

This is the power of knowledge externalization: **turning knowledge that used to require training to encode into documents anyone can edit**.

## The Problem

v3 gave us subagents for task decomposition. But there's a deeper question: **How does the model know HOW to handle domain-specific tasks?**

- Processing PDFs? It needs to know `pdftotext` vs `PyMuPDF`
- Building MCP servers? It needs protocol specs and best practices
- Code review? It needs a systematic checklist

This knowledge isn't a tool—it's **expertise**. Skills solve this by letting the model load domain knowledge on-demand.

## Key Concepts

### 1. Tools vs Skills

| Concept | What it is | Example |
|---------|------------|---------|
| **Tool** | What model CAN do | bash, read_file, write_file |
| **Skill** | How model KNOWS to do | PDF processing, MCP building |

Tools are capabilities. Skills are knowledge.

### 2. Progressive Disclosure

```
Layer 1: Metadata (always loaded)     ~100 tokens/skill
         └─ name + description

Layer 2: SKILL.md body (on trigger)   ~2000 tokens
         └─ Detailed instructions

Layer 3: Resources (as needed)        Unlimited
         └─ scripts/, references/, assets/
```

This keeps context lean while allowing arbitrary depth of knowledge.

### 3. SKILL.md Standard

```
skills/
├── pdf/
│   └── SKILL.md          # Required
├── mcp-builder/
│   ├── SKILL.md
│   └── references/       # Optional
└── code-review/
    ├── SKILL.md
    └── scripts/          # Optional
```

**SKILL.md format**: YAML frontmatter + Markdown body

```markdown
---
name: pdf
description: Process PDF files. Use when reading, creating, or merging PDFs.
---

# PDF Processing Skill

## Reading PDFs

Use pdftotext for quick extraction:
\`\`\`bash
pdftotext input.pdf -
\`\`\`
...
```

## Implementation (~100 lines added)

### SkillLoader Class

```python
class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills = {}
        self.load_skills()

    def parse_skill_md(self, path: Path) -> dict:
        """Parse YAML frontmatter + Markdown body."""
        content = path.read_text()
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        # Returns {name, description, body, path, dir}

    def get_descriptions(self) -> str:
        """Generate metadata for system prompt."""
        return "\n".join(f"- {name}: {skill['description']}"
                        for name, skill in self.skills.items())

    def get_skill_content(self, name: str) -> str:
        """Get full content for context injection."""
        return f"# Skill: {name}\n\n{skill['body']}"
```

### Skill Tool

```python
SKILL_TOOL = {
    "name": "Skill",
    "description": "Load a skill to gain specialized knowledge.",
    "input_schema": {
        "properties": {"skill": {"type": "string"}},
        "required": ["skill"]
    }
}
```

### Message Injection (Cache-Preserving)

The key insight: Skill content goes into **tool_result** (part of user message), NOT system prompt:

```python
def run_skill(skill_name: str) -> str:
    content = SKILLS.get_skill_content(skill_name)
    # Full content returned as tool_result
    # Becomes part of conversation history (user message)
    return f"""<skill-loaded name="{skill_name}">
{content}
</skill-loaded>

Follow the instructions in the skill above."""

def agent_loop(messages: list) -> list:
    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,  # Never changes - cache preserved!
            messages=messages,
            tools=ALL_TOOLS,
        )
        # Skill content enters messages as tool_result...
```

**Key insight**:
- Skill content is **appended to the end** as new message
- Everything before (system prompt + all previous messages) is cached and reused
- Only the newly appended skill content needs computation — **entire prefix hits cache**

## Comparison with Production

| Mechanism | Claude Code / Kode | v4 |
|-----------|-------------------|-----|
| Format | SKILL.md (YAML + MD) | Same |
| Loading | Container API | SkillLoader class |
| Triggering | Auto + Skill tool | Skill tool only |
| Injection | newMessages (user message) | tool_result (user message) |
| Caching | Append to end, entire prefix cached | Append to end, entire prefix cached |
| Versioning | Skill Versions API | Omitted |
| Permissions | allowed-tools field | Omitted |

**Key similarity**: Both inject skill content into conversation history (not system prompt), preserving prompt cache.

## Why This Matters: Caching Economics

### The Cost of Ignoring Cache

Many developers using **LangGraph, LangChain, AutoGen** habitually:
- Inject dynamic state into system prompts
- Edit and compress message history
- Use sliding windows to truncate conversations

**These operations invalidate cache and explode costs 7-50x.**

A typical 50-round SWE task:
- **Cache破坏**: $14.06 (modifying system prompt each round)
- **Cache optimized**: $1.85 (append-only)
- **Savings**: 86.9%

For an app handling 100 tasks daily, this means **$45,000+ annual savings**.

### Autoregressive Models and KV Cache

LLMs are autoregressive: generating each token requires attending to all previous tokens. To avoid redundant computation, providers implement **KV Cache**:

```
Request 1: [System, User1, Asst1, User2]
           ←────── compute all ──────→

Request 2: [System, User1, Asst1, User2, Asst2, User3]
           ←────── cache hit ──────→ ←─ new ─→
                   (0.1x price)        (normal price)
```

Cache hit requires **exact prefix match**. Modifying system prompt or history invalidates the entire prefix cache.

### Common Anti-Patterns

| Anti-Pattern | Effect | Cost Multiplier |
|--------------|--------|-----------------|
| Dynamic system prompt | 100% cache miss | **20-50x** |
| Message compression | Invalidates from replacement point | **5-15x** |
| Sliding window | 100% cache miss | **30-50x** |
| Message editing | Invalidates from edit point | **10-30x** |
| Multi-agent full mesh | Context explosion | **3-4x** (vs single agent) |

### Provider Differences

| Provider | Auto Cache | Discount | Config |
|----------|-----------|----------|--------|
| Claude | ✗ | 90% | Requires `cache_control` |
| GPT-5.2 | ✓ | 90% | No config needed |
| Kimi K2 | ✓ | 90% | No config needed |
| GLM-4.7 | ✓ | 82% | No config needed |
| MiniMax M2.1 | ✗ | 90% | Requires `cache_control` |
| Gemini 3 | ✓ (implicit) | 90% | No config needed |

**Important**: Claude and MiniMax require explicit `cache_control` configuration—no cache hits otherwise.

### Recommended: Append-Only

```python
# Wrong: edit history
messages[2]["content"] = "edited"  # Cache invalidated!

# Right: append only
messages.append(new_msg)  # Prefix unchanged, cache hit

# Wrong: dynamic system prompt
system = f"State: {state}"  # Changes every time!

# Right: fixed system, state in messages
SYSTEM = "You are an assistant."  # Never changes
messages.append({"role": "user", "content": f"State: {state}"})
```

### Context Length Support

Modern models support large context windows:
- Claude Sonnet 4.5 / Opus 4.5: **200K**
- GPT-5.2: **256K+**
- Gemini 3 Flash/Pro: **1M-2M**

200K tokens ≈ 150K words ≈ a 500-page book. For most Agent tasks, existing context windows are sufficient.

> **Treat context as append-only log, not editable document.**

### Deep Dive

For comprehensive coverage of caching economics:
1. **Common Anti-Patterns**: 5 cache-breaking mistakes in LangGraph/LangChain
2. **Detailed Calculations**: Round-by-round cost analysis for 50-round SWE tasks
3. **Provider Strategies**: Cache mechanisms and pricing comparison across providers
4. **Agent Orchestration**: Token consumption differences (multi-agent ~3-4x vs single agent)
5. **Best Practices**: How to detect and fix cache-breaking issues

See: [Context Caching Economics: Cost Optimization Guide for Agent Developers](../articles/上下文缓存经济学.md) (Chinese)

## Philosophy: Knowledge Externalization in Practice

> **Knowledge as a first-class citizen**

Returning to the knowledge externalization paradigm discussed at the beginning. Traditional view: AI agents are "tool callers"—model decides which tool, code executes.

But this misses a key dimension: **How does the model know what to do?**

Skills are the complete practice of knowledge externalization:

**Before (Knowledge Internalized)**:
- Knowledge locked in model parameters
- Modification requires training (LoRA, full fine-tuning)
- Users cannot access or understand
- Cost: $10K-$1M+, Timeline: Weeks

**Now (Knowledge Externalized)**:
- Knowledge stored in SKILL.md files
- Modification is just editing text
- Human-readable, auditable
- Cost: Free, Timeline: Instant

Skills acknowledge that **domain knowledge is itself a resource** that needs explicit management.

1. **Separate metadata from content**: Description is index, body is content
2. **Load on demand**: Context window is precious cognitive resource
3. **Standardized format**: Write once, use in any compatible agent
4. **Inject, don't return**: Skills change cognition, not just provide data
5. **Online learning**: Learn instantly in larger context windows, no offline training needed

The essence of knowledge externalization is **turning implicit knowledge into explicit documents**:
- Developers "teach" models new skills in natural language
- Git manages and shares knowledge
- Version control, auditing, rollback

**This is a paradigm shift from "training AI" to "educating AI".**

## Series Summary

| Version | Theme | Lines Added | Key Insight |
|---------|-------|-------------|-------------|
| v1 | Model as Agent | ~200 | Model is 80%, code is just the loop |
| v2 | Structured Planning | ~100 | Todo makes plans visible |
| v3 | Divide and Conquer | ~150 | Subagents isolate context |
| **v4** | **Domain Expert** | **~100** | **Skills inject expertise** |

---

## Study Notes

### Read the Source in This Order

Open [`v4_skills_agent.py`](./v4_skills_agent.py) and read these pieces first:

1. `SKILLS_DIR`
2. `SkillLoader`
3. `SKILLS = SkillLoader(SKILLS_DIR)`
4. `SYSTEM`
5. `SKILL_TOOL`
6. `run_skill`
7. `execute_tool`
8. `agent_loop`

v4 is v3 plus one new idea:

```text
tools let the model act
skills teach the model how to act in a domain
```

### The Skill Directory Is the Knowledge Base

The code points at:

```python
SKILLS_DIR = WORKDIR / "skills"
```

Each skill is a folder with a required `SKILL.md`:

```text
skills/
  pdf/
    SKILL.md
  mcp-builder/
    SKILL.md
  code-review/
    SKILL.md
```

This is the core shift from hidden knowledge to editable knowledge. A team can
change agent behavior by editing Markdown files in git.

### SkillLoader Separates Metadata From Full Content

`SkillLoader` does not dump every skill into the prompt. It first indexes the
cheap metadata:

```python
def get_descriptions(self) -> str:
    return "\n".join(
        f"- {name}: {skill['description']}"
        for name, skill in self.skills.items()
    )
```

That metadata is added to the system prompt:

```python
**Skills available** (invoke with Skill tool when task matches):
{SKILLS.get_descriptions()}
```

The model can see which skills exist, but the expensive body stays out of
context until needed.

### Loading a Skill Is a Tool Call

The `Skill` tool schema is:

```python
SKILL_TOOL = {
    "name": "Skill",
    "description": "Load a skill to gain specialized knowledge for a task.",
    ...
}
```

When the model calls it, the dispatcher routes to:

```python
if name == "Skill":
    return run_skill(args["skill"])
```

That means skills fit into the same loop as every other action:

```text
model chooses Skill
host loads SKILL.md
host returns skill content as tool_result
model continues with new knowledge
```

### run_skill Is the Key Mechanism

The heart of v4 is:

```python
def run_skill(skill_name: str) -> str:
    content = SKILLS.get_skill_content(skill_name)
    return f"""<skill-loaded name="{skill_name}">
{content}
</skill-loaded>

Follow the instructions in the skill above to complete the user's task."""
```

This is not the same as returning data from a search tool. A skill changes how
the model approaches the rest of the task.

Think of it as temporarily adding a specialized operating manual to the
conversation.

### Why Skill Content Goes Into tool_result

The source is explicit about this design:

```text
Why tool_result instead of system prompt?
- System prompt changes invalidate cache
- Tool results append to end
```

This is a subtle but important production lesson. Keep the system prompt stable.
Append new information to messages.

That preserves prompt caching:

```text
stable prefix -> cache hit
new skill content -> only new suffix is processed
```

### Skill Loading Has Three Layers

The code implements progressive disclosure:

| Layer | Source code location | What the model sees |
|-------|----------------------|---------------------|
| Metadata | `get_descriptions()` | name + description |
| Body | `get_skill_content()` | full `SKILL.md` body |
| Resources | `scripts/`, `references/`, `assets/` hints | extra files to inspect or run |

This lets the agent know what skills exist without paying the context cost of
loading every manual upfront.

### How v4 Combines Earlier Versions

v4 still contains the earlier mechanisms:

```text
v1: bash/read/write/edit tools
v2: TodoWrite
v3: Task subagents
v4: Skill loading
```

In `ALL_TOOLS`, the final agent gets:

```python
ALL_TOOLS = BASE_TOOLS + [TASK_TOOL, SKILL_TOOL]
```

So v4 is not a different architecture. It is the same loop with more carefully
designed context sources.

### Tools vs Skills: The Practical Test

Ask this question:

```text
Does this help the model do something, or know how to do something?
```

If it performs an action, it is probably a tool:

```text
bash
read_file
write_file
edit_file
Task
```

If it teaches a method, checklist, convention, or domain workflow, it is
probably a skill:

```text
code-review
mcp-builder
pdf
agent-builder
```

### Common Failure Modes

When building your own skills, avoid:

1. **Descriptions that are too vague.** The model will not know when to load the
   skill.
2. **Huge always-loaded prompts.** That defeats progressive disclosure.
3. **Putting secrets in skills.** Skills are files; treat them as repo content.
4. **Mixing tools and skills.** A skill can mention scripts, but the execution
   still happens through tools.
5. **Changing the system prompt every time.** Prefer append-only message
   injection for cache friendliness.

### Learning Check

After reading the code, make sure you can answer:

- Where does v4 discover available skills?
- Which method reads only skill metadata?
- Which method loads the full skill body?
- Why does `run_skill` return XML-like tags?
- Why is skill content returned as a `tool_result` instead of inserted into the
  system prompt?
- How do skills compose with todos and subagents?

---

## Full Source

````python
#!/usr/bin/env python3
"""
v4_skills_agent.py - Mini Claude Code: Skills Mechanism (~550 lines)

Core Philosophy: "Knowledge Externalization"
============================================
v3 gave us subagents for task decomposition. But there's a deeper question:

    How does the model know HOW to handle domain-specific tasks?

- Processing PDFs? It needs to know pdftotext vs PyMuPDF
- Building MCP servers? It needs protocol specs and best practices
- Code review? It needs a systematic checklist

This knowledge isn't a tool - it's EXPERTISE. Skills solve this by letting
the model load domain knowledge on-demand.

The Paradigm Shift: Knowledge Externalization
--------------------------------------------
Traditional AI: Knowledge locked in model parameters
  - To teach new skills: collect data -> train -> deploy
  - Cost: $10K-$1M+, Timeline: Weeks
  - Requires ML expertise, GPU clusters

Skills: Knowledge stored in editable files
  - To teach new skills: write a SKILL.md file
  - Cost: Free, Timeline: Minutes
  - Anyone can do it

It's like attaching a hot-swappable LoRA adapter without any training!

Tools vs Skills:
---------------
    | Concept   | What it is              | Example                    |
    |-----------|-------------------------|---------------------------|
    | **Tool**  | What model CAN do       | bash, read_file, write    |
    | **Skill** | How model KNOWS to do   | PDF processing, MCP dev   |

Tools are capabilities. Skills are knowledge.

Progressive Disclosure:
----------------------
    Layer 1: Metadata (always loaded)      ~100 tokens/skill
             name + description only

    Layer 2: SKILL.md body (on trigger)    ~2000 tokens
             Detailed instructions

    Layer 3: Resources (as needed)         Unlimited
             scripts/, references/, assets/

This keeps context lean while allowing arbitrary depth.

SKILL.md Standard:
-----------------
    skills/
    |-- pdf/
    |   |-- SKILL.md          # Required: YAML frontmatter + Markdown body
    |-- mcp-builder/
    |   |-- SKILL.md
    |   |-- references/       # Optional: docs, specs
    |-- code-review/
        |-- SKILL.md
        |-- scripts/          # Optional: helper scripts

Cache-Preserving Injection:
--------------------------
Critical insight: Skill content goes into tool_result (user message),
NOT system prompt. This preserves prompt cache!

    Wrong: Edit system prompt each time (cache invalidated, 20-50x cost)
    Right: Append skill as tool result (prefix unchanged, cache hit)

This is how production Claude Code works - and why it's cost-efficient.

Usage:
    python v4_skills_agent.py
"""

import os
import re
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
SKILLS_DIR = WORKDIR / "skills"

client = Anthropic(api_key=API_KEY, base_url=BASE_URL) if BASE_URL else Anthropic(api_key=API_KEY)


# =============================================================================
# SkillLoader - The core addition in v4
# =============================================================================

class SkillLoader:
    """
    Loads and manages skills from SKILL.md files.

    A skill is a FOLDER containing:
    - SKILL.md (required): YAML frontmatter + markdown instructions
    - scripts/ (optional): Helper scripts the model can run
    - references/ (optional): Additional documentation
    - assets/ (optional): Templates, files for output

    SKILL.md Format:
    ----------------
        ---
        name: pdf
        description: Process PDF files. Use when reading, creating, or merging PDFs.
        ---

        # PDF Processing Skill

        ## Reading PDFs

        Use pdftotext for quick extraction:
        ```bash
        pdftotext input.pdf -
        ```
        ...

    The YAML frontmatter provides metadata (name, description).
    The markdown body provides detailed instructions.
    """

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills = {}
        self.load_skills()

    def parse_skill_md(self, path: Path) -> dict:
        """
        Parse a SKILL.md file into metadata and body.

        Returns dict with: name, description, body, path, dir
        Returns None if file doesn't match format.
        """
        content = path.read_text()

        # Match YAML frontmatter between --- markers
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if not match:
            return None

        frontmatter, body = match.groups()

        # Parse YAML-like frontmatter (simple key: value)
        metadata = {}
        for line in frontmatter.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip("\"'")

        # Require name and description
        if "name" not in metadata or "description" not in metadata:
            return None

        return {
            "name": metadata["name"],
            "description": metadata["description"],
            "body": body.strip(),
            "path": path,
            "dir": path.parent,
        }

    def load_skills(self):
        """
        Scan skills directory and load all valid SKILL.md files.

        Only loads metadata at startup - body is loaded on-demand.
        This keeps the initial context lean.
        """
        if not self.skills_dir.exists():
            return

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            skill = self.parse_skill_md(skill_md)
            if skill:
                self.skills[skill["name"]] = skill

    def get_descriptions(self) -> str:
        """
        Generate skill descriptions for system prompt.

        This is Layer 1 - only name and description, ~100 tokens per skill.
        Full content (Layer 2) is loaded only when Skill tool is called.
        """
        if not self.skills:
            return "(no skills available)"

        return "\n".join(
            f"- {name}: {skill['description']}"
            for name, skill in self.skills.items()
        )

    def get_skill_content(self, name: str) -> str:
        """
        Get full skill content for injection.

        This is Layer 2 - the complete SKILL.md body, plus any available
        resources (Layer 3 hints).

        Returns None if skill not found.
        """
        if name not in self.skills:
            return None

        skill = self.skills[name]
        content = f"# Skill: {skill['name']}\n\n{skill['body']}"

        # List available resources (Layer 3 hints)
        resources = []
        for folder, label in [
            ("scripts", "Scripts"),
            ("references", "References"),
            ("assets", "Assets")
        ]:
            folder_path = skill["dir"] / folder
            if folder_path.exists():
                files = list(folder_path.glob("*"))
                if files:
                    resources.append(f"{label}: {', '.join(f.name for f in files)}")

        if resources:
            content += f"\n\n**Available resources in {skill['dir']}:**\n"
            content += "\n".join(f"- {r}" for r in resources)

        return content

    def list_skills(self) -> list:
        """Return list of available skill names."""
        return list(self.skills.keys())


# Global skill loader instance
SKILLS = SkillLoader(SKILLS_DIR)


# =============================================================================
# Agent Type Registry (from v3)
# =============================================================================

AGENT_TYPES = {
    "explore": {
        "description": "Read-only agent for exploring code, finding files, searching",
        "tools": ["bash", "read_file"],
        "prompt": "You are an exploration agent. Search and analyze, but never modify files. Return a concise summary.",
    },
    "code": {
        "description": "Full agent for implementing features and fixing bugs",
        "tools": "*",
        "prompt": "You are a coding agent. Implement the requested changes efficiently.",
    },
    "plan": {
        "description": "Planning agent for designing implementation strategies",
        "tools": ["bash", "read_file"],
        "prompt": "You are a planning agent. Analyze the codebase and output a numbered implementation plan. Do NOT make changes.",
    },
}


def get_agent_descriptions() -> str:
    """Generate agent type descriptions for system prompt."""
    return "\n".join(
        f"- {name}: {cfg['description']}"
        for name, cfg in AGENT_TYPES.items()
    )


# =============================================================================
# TodoManager (from v2)
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
# System Prompt - Updated for v4
# =============================================================================

SYSTEM = f"""You are a coding agent at {WORKDIR}.

Loop: plan -> act with tools -> report.

**Skills available** (invoke with Skill tool when task matches):
{SKILLS.get_descriptions()}

**Subagents available** (invoke with Task tool for focused subtasks):
{get_agent_descriptions()}

Rules:
- Use Skill tool IMMEDIATELY when a task matches a skill description
- Use Task tool for subtasks needing focused exploration or implementation
- Use TodoWrite to track multi-step work
- Prefer tools over prose. Act, don't just explain.
- After finishing, summarize what changed."""


# =============================================================================
# Tool Definitions
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

# Task tool (from v3)
TASK_TOOL = {
    "name": "Task",
    "description": f"Spawn a subagent for a focused subtask.\n\nAgent types:\n{get_agent_descriptions()}",
    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Short task description (3-5 words)"
            },
            "prompt": {
                "type": "string",
                "description": "Detailed instructions for the subagent"
            },
            "agent_type": {
                "type": "string",
                "enum": list(AGENT_TYPES.keys())
            },
        },
        "required": ["description", "prompt", "agent_type"],
    },
}

# NEW in v4: Skill tool
SKILL_TOOL = {
    "name": "Skill",
    "description": f"""Load a skill to gain specialized knowledge for a task.

Available skills:
{SKILLS.get_descriptions()}

When to use:
- IMMEDIATELY when user task matches a skill description
- Before attempting domain-specific work (PDF, MCP, etc.)

The skill content will be injected into the conversation, giving you
detailed instructions and access to resources.""",
    "input_schema": {
        "type": "object",
        "properties": {
            "skill": {
                "type": "string",
                "description": "Name of the skill to load"
            }
        },
        "required": ["skill"],
    },
}

ALL_TOOLS = BASE_TOOLS + [TASK_TOOL, SKILL_TOOL]


def get_tools_for_agent(agent_type: str) -> list:
    """Filter tools based on agent type."""
    allowed = AGENT_TYPES.get(agent_type, {}).get("tools", "*")
    if allowed == "*":
        return BASE_TOOLS
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
    """Execute shell command."""
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


def run_skill(skill_name: str) -> str:
    """
    Load a skill and inject it into the conversation.

    This is the key mechanism:
    1. Get skill content (SKILL.md body + resource hints)
    2. Return it wrapped in <skill-loaded> tags
    3. Model receives this as tool_result (user message)
    4. Model now "knows" how to do the task

    Why tool_result instead of system prompt?
    - System prompt changes invalidate cache (20-50x cost increase)
    - Tool results append to end (prefix unchanged, cache hit)

    This is how production systems stay cost-efficient.
    """
    content = SKILLS.get_skill_content(skill_name)

    if content is None:
        available = ", ".join(SKILLS.list_skills()) or "none"
        return f"Error: Unknown skill '{skill_name}'. Available: {available}"

    # Wrap in tags so model knows it's skill content
    return f"""<skill-loaded name="{skill_name}">
{content}
</skill-loaded>

Follow the instructions in the skill above to complete the user's task."""


def run_task(description: str, prompt: str, agent_type: str) -> str:
    """Execute a subagent task (from v3). See v3 for details."""
    if agent_type not in AGENT_TYPES:
        return f"Error: Unknown agent type '{agent_type}'"

    config = AGENT_TYPES[agent_type]
    sub_system = f"""You are a {agent_type} subagent at {WORKDIR}.

{config["prompt"]}

Complete the task and return a clear, concise summary."""

    sub_tools = get_tools_for_agent(agent_type)
    sub_messages = [{"role": "user", "content": prompt}]

    print(f"  [{agent_type}] {description}")
    start = time.time()
    tool_count = 0

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

            elapsed = time.time() - start
            sys.stdout.write(
                f"\r  [{agent_type}] {description} ... {tool_count} tools, {elapsed:.1f}s"
            )
            sys.stdout.flush()

        sub_messages.append({"role": "assistant", "content": response.content})
        sub_messages.append({"role": "user", "content": results})

    elapsed = time.time() - start
    sys.stdout.write(
        f"\r  [{agent_type}] {description} - done ({tool_count} tools, {elapsed:.1f}s)\n"
    )

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
    if name == "Skill":
        return run_skill(args["skill"])
    return f"Unknown tool: {name}"


# =============================================================================
# Main Agent Loop
# =============================================================================

def agent_loop(messages: list) -> list:
    """
    Main agent loop with skills support.

    Same pattern as v3, but now with Skill tool.
    When model loads a skill, it receives domain knowledge.
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
            # Special display for different tool types
            if tc.name == "Task":
                print(f"\n> Task: {tc.input.get('description', 'subtask')}")
            elif tc.name == "Skill":
                print(f"\n> Loading skill: {tc.input.get('skill', '?')}")
            else:
                print(f"\n> {tc.name}")

            output = execute_tool(tc.name, tc.input)

            # Skill tool shows summary, not full content
            if tc.name == "Skill":
                print(f"  Skill loaded ({len(output)} chars)")
            elif tc.name != "Task":
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
    print(f"Mini Claude Code v4 (with Skills) - {WORKDIR}")
    print(f"Skills: {', '.join(SKILLS.list_skills()) or 'none'}")
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
````

---

**Tools let models act. Skills let models know how.**

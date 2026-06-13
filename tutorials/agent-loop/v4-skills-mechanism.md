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

**Tools let models act. Skills let models know how.**

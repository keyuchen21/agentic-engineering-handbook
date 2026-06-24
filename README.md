# Agentic Engineering Handbook

> The definitive OpenAI, Anthropic, Google, MCP, Harness, Evals, and Production Agent Systems learning roadmap.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--06--24-blue.svg)](#)

If this repository helps you, consider giving it a ⭐

---

## Why This Repository?

The AI industry has entered the **Agentic Era**. Building production-grade AI systems now requires mastering agents, tool use, MCP, memory, long-running workflows, coding agents, agent harnesses, evals, and safety — but the knowledge is scattered across OpenAI blogs, Anthropic engineering posts, SDK docs, cookbooks, and research papers.

This repository consolidates **168 curated resources** into one structured learning roadmap.

**The goal: Become a world-class Agentic Engineer.**

---

## How To Use This Handbook

Pick the path that matches your starting point:

- **New to agents:** follow the [Learning Roadmap](#learning-roadmap) from Phase 0 to Phase 6. Treat each `Read First`, `Then Read`, and `Build Exercise` as a checklist.
- **Already building LLM apps:** start at [Phase 2](#phase-2--mcp--tool-ecosystem) or [Phase 3](#phase-3--context-memory--skills), then fill gaps in agent loop, tool calling, evals, and production engineering.
- **Trying to build projects:** use the phase-level `Build Exercise` prompts, then branch into [Applied Practice Tracks](#applied-practice-tracks) for coding agents, security, code review, or SRE.
- **Looking for references:** jump to the [Full Reading Table](#full-reading-table). Read `P0` first, use `P1` for implementation detail, and keep `P2` as optional background.

---

## Learning Roadmap

### Phase 0 — Agent Loop From Scratch

If you treat Claude Code as a coding CLI, many capabilities can feel like magic: it reads files, runs commands, edits code, delegates work, and stays oriented during complex tasks.

From an engineering perspective, the core is much simpler:

**model + tools + one loop.**

Understanding that loop makes the rest of the system easier to reason about:

- When the agent should plan first, and when it should act immediately
- Why an explicit todo list reduces drift in longer tasks
- Why subagents improve exploration while protecting the main context
- How skills, MCP, and hooks each add capability around the same core loop

These pages are based on the upstream English Markdown tutorials from [shareAI-lab/mini-claude-code](https://github.com/shareAI-lab/mini-claude-code), with added Study Notes and inline source code for this handbook.

| Step | Page | Code |
|------|------|------|
| v0 | [Bash is All You Need](tutorials/agent-loop/v0-bash-is-all-you-need.md) | [v0_bash_agent.py](tutorials/agent-loop/v0_bash_agent.py) |
| v1 | [Model as Agent](tutorials/agent-loop/v1-model-as-agent.md) | [v1_basic_agent.py](tutorials/agent-loop/v1_basic_agent.py) |
| v2 | [Structured Planning](tutorials/agent-loop/v2-structured-planning.md) | [v2_todo_agent.py](tutorials/agent-loop/v2_todo_agent.py) |
| v3 | [Subagent Mechanism](tutorials/agent-loop/v3-subagent-mechanism.md) | [v3_subagent.py](tutorials/agent-loop/v3_subagent.py) |
| v4 | [Skills Mechanism](tutorials/agent-loop/v4-skills-mechanism.md) | [v4_skills_agent.py](tutorials/agent-loop/v4_skills_agent.py) |

Supporting files are included in the same folder: `requirements.txt`, `.env.example`, `v0_bash_agent_mini.py`, and `skills/`.

---

### Phase 1 — Agent Foundations

> Build shared vocabulary for workflow vs agent, tool loop, handoff, guardrails.

#### Key Mental Models

**Should I build an agent?** (4-question checklist from Barry Zhang's talk)

| Question | If No → Workflow | If Yes → Agent |
|----------|-----------------|----------------|
| Is the task complex enough? | Decision tree is fully mappable | Ambiguous problem space |
| Is the task valuable enough? | <$0.10 per run | >$1 per run, cost doesn't matter |
| Are all core capabilities doable? | Weak links break the chain | Model handles every step well |
| Is error cost low & detectable? | High cost + hard to detect → human-in-the-loop | Errors caught by tests/CI |

**Think like the agent.** Most failures come from designing with a human perspective. Put yourself inside the agent's context window: you only see ~10K–20K tokens (system prompt + tool descriptions + recent observations). Ask: does the agent have enough information to act correctly at each step?

→ Source: [How We Build Effective Agents](https://www.youtube.com/watch?v=D7_ipDqhtwk)

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts) | Anthropic |
| 2 | [Prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance) | OpenAI |
| 3 | [Function Calling](https://developers.openai.com/api/docs/guides/function-calling) | OpenAI |
| 4 | [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | Anthropic |
| 5 | [Function calling - Gemini API](https://ai.google.dev/gemini-api/docs/function-calling) | Google |
| 6 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic |
| 7 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI |
| 8 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [How We Build Effective Agents: Barry Zhang, Anthropic](https://www.youtube.com/watch?v=D7_ipDqhtwk) | Anthropic |
| [Phistory — Claude Code & Codex CLI System Prompt Diff History](https://phistory.cc/) | Community |
| [Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101) | Cognition |
| [OpenAI Agents SDK examples](https://openai.github.io/openai-agents-python/examples/) | OpenAI |
| [Structured Outputs for Multi-Agent Systems](https://developers.openai.com/cookbook/examples/structured_outputs_multi_agent) | OpenAI |

#### Build Exercise

Build a customer service/ticket triage agent: router → specialist → evaluator, with all outputs constrained by structured schemas.

---

### Phase 2 — MCP & Tool Ecosystem

> Understand MCP server/client, remote vs local, tool loading, approval, connector boundaries.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic |
| 2 | [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | OpenAI |
| 3 | [Building MCP servers for ChatGPT Apps and API integrations](https://developers.openai.com/api/docs/mcp) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic |
| [Writing effective tools for AI agents - with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic |
| [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI |
| [Build a Remote MCP server](https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/#add-authentication) | Cloudflare |
| [Introducing the MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) | MCP |
| [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | OpenAI |
| [Build your ChatGPT UI](https://developers.openai.com/apps-sdk/build/chatgpt-ui) | OpenAI |

#### Build Exercise

Build a read-only repo/docs MCP server, then create an eval to verify the agent correctly cites documentation.

---

### Phase 3 — Context, Memory & Skills

> Learn to control context window, short/long-term memory, skills/plugins, CLAUDE.md/AGENTS.md.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Agent Skills Specification](https://agentskills.io/specification) | Agent Skills |
| 2 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic |
| 3 | [How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) | Drew Breunig |
| 4 | [Context Rot](https://research.trychroma.com/context-rot) | Chroma |
| 5 | [Progressive disclosure](https://docs.claude-mem.ai/progressive-disclosure) | Claude-Mem |
| 6 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic |
| 7 | [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Anthropic |
| 8 | [Skills](https://developers.openai.com/api/docs/guides/tools-skills) | OpenAI |
| 9 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Custom instructions with AGENTS.md - Codex](https://developers.openai.com/codex/guides/agents-md) | OpenAI |
| [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic |
| [Agent Skills - Codex](https://developers.openai.com/codex/skills) | OpenAI |
| [Skills in OpenAI API](https://developers.openai.com/cookbook/examples/skills_in_api) | OpenAI |

#### Build Exercise

Implement the same task as a Skill/Plugin, then measure accuracy and token cost across three variants: no skill, long prompt, and skill-based.

---

### Phase 4 — Harness & Long-Running Agents

> Master agent runtime: event stream, thread, tool execution, state, sandbox, approval, recovery.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI |
| 2 | [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | OpenAI |
| 3 | [Agent Harness Engineering: A Survey](https://picrew.github.io/LLM-Harness/) | Academic |
| 4 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic |

#### Then Read

| Title | Vendor |
|-------|--------|
| [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI |
| [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans) | OpenAI |
| [Build long-running AI agents that pause, resume, and never lose context with ADK](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) | Google |
| [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic |
| [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Anthropic |

#### Build Exercise

Build a mini coding harness: plan file, shell tool, apply patch, test gate, event log, and resume capability.

---

### Phase 5 — Coding & Workspace Agents

> Compare Codex vs Claude Code product/SDK forms; learn multi-agent, IDE, workspace collaboration.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Introducing Codex](https://openai.com/index/introducing-codex/) | OpenAI |
| 2 | [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic |
| 3 | [How Claude Code works in large codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start) | Anthropic |
| 4 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) | OpenAI |
| [Introducing workspace agents in ChatGPT](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) | OpenAI |
| [Apple's Xcode now supports Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | Anthropic |
| [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI |
| [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | Anthropic |
| [The spec is dead, long live the spec!](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code) | Ravi on Product |
| [How Anthropic teams use Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) | Anthropic |
| [Multi-stack Web App Builds](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8) | Community |

#### Build Exercise

Run both OpenAI/Codex and Claude Code style workflows on the same repo: issue → plan → patch → tests → PR summary.

---

### Phase 6 — Evals, Safety & Production

> Build pre/post-launch eval loop, trace loop, safety boundaries, permissions, regression monitoring.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic |
| 2 | [The six generations of AI agents and how to eval them](https://www.braintrust.dev/blog/six-generations-ai-agents) | Braintrust |
| 3 | [Agent observability powers agent evaluation](https://www.langchain.com/blog/agent-observability-powers-agent-evaluation) | LangChain |
| 4 | [Agent Evaluation Readiness Checklist](https://www.langchain.com/blog/agent-evaluation-readiness-checklist) | LangChain |
| 5 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI |
| 6 | [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems) | OpenAI |
| 7 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [How we build evals for Deep Agents](https://www.langchain.com/blog/how-we-build-evals-for-deep-agents) | LangChain |
| [How to Evaluate Tool-Calling Agents](https://arize.com/blog/how-to-evaluate-tool-calling-agents/) | Arize |
| [AI agent evaluation: How to test, debug, and improve agents in production](https://arize.com/blog/why-testing-ai-agents-is-non-negotiable/) | Arize |
| [A Survey on Agent-as-a-Judge](https://arxiv.org/html/2601.05111v1) | Academic |
| [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI |
| [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic |
| [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI |
| [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic |

#### Build Exercise

Build a smoke/macro eval suite for your agent: task success rate, tool misuse, prompt injection resistance, latency, cost, and human approval count.

---

## Applied Practice Tracks

Use these tracks after the core roadmap when you want to practice agentic engineering in real engineering workflows.

| Track | Start Here | Why It Matters |
|-------|------------|----------------|
| Agentic coding workflow | [Coding Agents 101](https://devin.ai/agents101), [How Claude Code works in large codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start), [How Anthropic teams use Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) | Turns agent theory into day-to-day engineering habits: prompting, checkpoints, verification, parallel work, and team rollout. |
| Spec-driven building | [The spec is dead, long live the spec!](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code), [Multi-stack Web App Builds](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8) | Treats specs, prompts, and assignments as executable source material for agents. |
| Context failure modes | [How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html), [Context Rot](https://research.trychroma.com/context-rot), [Progressive disclosure](https://docs.claude-mem.ai/progressive-disclosure) | Helps diagnose context poisoning, distraction, confusion, context degradation, and retrieval overload. |
| Evals and observability | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [Agent observability powers agent evaluation](https://www.langchain.com/blog/agent-observability-powers-agent-evaluation), [Agent Evaluation Readiness Checklist](https://www.langchain.com/blog/agent-evaluation-readiness-checklist) | Builds the feedback loop for traces, datasets, graders, offline/online evals, and regression gates. |
| MCP operations | [Build a Remote MCP server](https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/#add-authentication), [Introducing the MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) | Shows how MCP moves from local prototypes to authenticated, discoverable, production-grade tool ecosystems. |
| Agent security | [OWASP Top Ten](https://owasp.org/www-project-top-ten/), [SAST vs. DAST vs. RASP](https://www.splunk.com/en_us/blog/learn/sast-vs-dast.html), [Copilot Remote Code Execution via Prompt Injection](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) | Grounds agent security in classic AppSec plus new prompt-injection and tool-permission failure modes. |
| Code review systems | [How to Review Code Effectively](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/), [AI-Assisted Assessment of Coding Practices in Modern Code Review](https://arxiv.org/pdf/2405.13565), [AI Code Review Implementation Best Practices](https://graphite.dev/guides/ai-code-review-implementation-best-practices) | Connects human review quality with AI-assisted review, automated comments, and review policy design. |
| Production and SRE agents | [ML and LLM system design](https://www.evidentlyai.com/ml-system-design), [Introduction to Site Reliability Engineering](https://sre.google/sre-book/introduction/), [Observability Basics You Should Know](https://last9.io/blog/traces-spans-observability-basics/) | Extends agents beyond coding into incidents, observability, root-cause analysis, on-call, and production operations. |

---

## Full Reading Table

> **Priority guide:** P0 = must-read (architectural/conceptual), P1 = highly useful (implementation detail), P2 = optional context (background/releases).

| Priority | Title | Vendor | Topic | Key Idea | Date |
|----------|-------|--------|-------|----------|------|
| P0 | [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | OpenAI | Agents; MCP; Platform | Annual overview: systematic walkthrough of Responses API, Agents SDK, AgentKit, Codex, MCP, Apps SDK, and AGENTS.md. | 2025-12-30 |
| P0 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI | Agents; Responses API; Tools | Key starting point for OpenAI's agent platform: Responses API, built-in web/file/computer tools, Agents SDK, tracing/observability. | 2025-03-11 |
| P0 | [Introducing AgentKit](https://openai.com/index/introducing-agentkit/) | OpenAI | Agents; Evals; AgentKit | AgentKit, expanded evals, agent RFT: the official agent toolchain from prototype to production. | 2025-10-06 |
| P0 | [Prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance) | OpenAI | Prompting; Models; Agent UX | Official model-specific prompting guidance for outcome-first prompts, reasoning effort, preambles, and validation rules in tool-heavy workflows. | Current docs |
| P0 | [System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts) | Anthropic | System prompts; Claude; Behavior | Claude web/mobile system prompt release notes; useful for studying production prompting patterns and behavioral scaffolding. | Current docs |
| P0 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI | Agents; SDK | Official SDK entry point: concepts and boundaries of agent, tool, handoff, guardrail, and tracing. | Current docs |
| P0 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic | MCP; Standards | The origin article for MCP: an open standard connecting AI assistants to data, tools, and systems. | 2024-11-25 |
| P0 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic | Agents; Patterns; Frameworks | Essential agent primer: workflow vs agent, prompt/tool/retrieval, orchestrator-worker, evaluator-optimizer patterns. | 2024-12-19 |
| P0 | [Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101) | Cognition | Coding agents; Workflows; Practice | Product-agnostic guide to prompting, delegation, verification, environment setup, security, and cost management for coding agents. | 2025-06 |
| P0 | [New tools and features in the Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/) | OpenAI | MCP; Responses API; Tools | Responses API extended to remote MCP servers, image/code/file tools; see how OpenAI integrates MCP into its runtime. | 2025-05-21 |
| P0 | [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | OpenAI | MCP; Connectors; Responses API | Official guide to connecting remote MCP servers and connectors; includes approvals and security considerations. | Current docs |
| P0 | [Building MCP servers for ChatGPT Apps and API integrations](https://developers.openai.com/api/docs/mcp) | OpenAI | MCP; ChatGPT Apps; API | Official guide to writing MCP servers: supply tools/knowledge to ChatGPT Apps, deep research, and API integrations. | Current docs |
| P0 | [Building a Deep Research MCP Server](https://developers.openai.com/cookbook/examples/deep_research_api/how_to_build_a_deep_research_mcp_server/readme) | OpenAI | MCP; Deep research | Minimal implementation of a search/fetch MCP server for Deep Research. | 2025-06-25 |
| P0 | [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI | MCP; Codex | How Codex CLI/IDE connects to MCP servers, adding Figma, browser, docs, and internal tool context to agents. | Current docs |
| P0 | [Introducing Codex](https://openai.com/index/introducing-codex/) | OpenAI | Agents; Coding; Sandbox | Cloud-based software engineering agent: parallel tasks, repo sandbox, running tests/linters/type checkers, producing auditable evidence. | 2025-05-16 |
| P0 | [Agent Harness Engineering: A Survey](https://picrew.github.io/LLM-Harness/) | Academic | Harness; Taxonomy; Agent architecture | Survey that frames harness engineering as its own system layer and introduces the ETCLOVG taxonomy: Execution, Tooling, Context, Lifecycle, Observability, Verification, and Governance. | 2026 |
| P0 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI | Harness; Agent loop; Codex | How Codex CLI chains prompt, tool schema, MCP tools, Responses API, and context management into an agent loop. | 2026-01-23 |
| P0 | [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | OpenAI | Harness; Codex App Server; JSON-RPC | Core harness article: Codex core, App Server, JSON-RPC, streaming progress, approval, diff, and thread management. | 2026-02-04 |
| P0 | [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/) | OpenAI | Harness; Responses API; Sandbox | Responses API + shell tool + hosted containers form the agent runtime; essential for understanding the model-to-agent execution environment. | 2026-03-10 |
| P0 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | OpenAI | Harness; Agent-first engineering | Design product code, tests, CI, docs, and observability to be agent-readable/executable; learn agent-first repo organization. | 2026-02-11 |
| P0 | [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI | Harness; Agents SDK; MCP; Skills | Agents SDK harness becomes more complete: memory, sandbox orchestration, Codex-like filesystem tools, MCP, skills, AGENTS.md. | 2026-04-15 |
| P0 | [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI | MCP; Codex; Agents SDK | Codex CLI as an MCP server integrated with Agents SDK; real multi-agent dev workflow. | 2025-10-01 |
| P0 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI | Memory; Compaction; Reliability | Memory and compaction design for long-context/multi-turn agents. | 2026-05-01 |
| P0 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI | Evals; Traces; Self-improvement | Connect traces, evals, and Codex fixes into an agent improvement loop. | 2026-05-12 |
| P0 | [Eval Driven System Design - From Prototype to Production](https://developers.openai.com/cookbook/topic/evals) | OpenAI | Evals; Production | Use evals as the driving force for system design; ideal for moving agents from demo to production. | 2025-06-02 |
| P0 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI | Evals; Skills; Agents | Systematically test agent skills with evals; establish quality gates before skill release. | 2026-01-22 |
| P0 | [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI | MCP; Evals | Evaluate QA/retrieval capabilities with MCP tools; ideal for building an MCP regression suite. | 2025-06-09 |
| P0 | [The six generations of AI agents and how to eval them](https://www.braintrust.dev/blog/six-generations-ai-agents) | Braintrust | Evals; Agent architecture; Harness | Maps six generations of agent architecture to the eval strategy each generation requires, from prompts to AI harnesses. | 2026-05-21 |
| P0 | [Agent observability powers agent evaluation](https://www.langchain.com/blog/agent-observability-powers-agent-evaluation) | LangChain | Evals; Observability; Traces | Explains why traces are the source of truth for agent behavior and how observability feeds evaluation. | 2026-01-27 |
| P0 | [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI | Safety; Sandbox; Codex | How OpenAI runs Codex internally: sandbox, approvals, network policy, agent-native telemetry. | 2026-05-20 |
| P0 | [Building Governed AI Agents - A Practical Guide to Agentic Scaffolding](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Governance; Guardrails; Agents | Governed agent scaffolding: permissions, guardrails, auditing, and organizational policies. | 2026-02-23 |
| P0 | [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems) | OpenAI | Evals; Agentic systems | Evaluate agents at the end-to-end/macro level, not just individual step outputs. | 2026-05-19 |
| P0 | [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic | Coding agents; Claude Code | Claude Code methodology: verification loop, explore-plan-code, CLAUDE.md, permissions, MCP, subagents, context management. | 2025-04-18 |
| P0 | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | Anthropic | Claude Code; Coding agents; Workflow | Official Claude Code docs for planning, CLAUDE.md, verification, tool use, and team workflows. | Current docs |
| P0 | [How Claude Code works in large codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start) | Anthropic | Claude Code; Large codebases; Enterprise | Patterns for large-codebase Claude Code adoption: layered CLAUDE.md, hooks, skills, plugins, MCP, LSP, subagents, and rollout ownership. | 2026-05-14 |
| P0 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic | Agents; Multi-agent; Research | Claude Research multi-agent architecture: planner + parallel research agents + synthesis; production multi-agent experience. | 2025-06-13 |
| P0 | [Writing effective tools for AI agents - with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic | Tools; MCP; Evals | Tool quality determines agent quality: tool descriptions, context budget, eval, and letting Claude optimize its own tools. | 2025-09-11 |
| P0 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic | Context; Agents | Context is the agent's core resource: selection, compression, isolation, persistence, and context pollution control. | 2025-09-29 |
| P0 | [How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) | Drew Breunig | Context; Long context; Agents | Taxonomy of context poisoning, distraction, confusion, and clash; practical fixes for overloaded agent contexts. | 2025-06-22 |
| P0 | [Context Rot](https://research.trychroma.com/context-rot) | Chroma | Context; Long-context evals | Research on how LLM performance degrades as input grows, especially with distractors and similar-but-wrong context. | 2025-07-16 |
| P0 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic | Claude Code; Agent SDK; Subagents | Claude Agent SDK, subagents, hooks, background tasks, checkpoints, and other autonomous coding agent capabilities. | 2025-09-29 |
| P0 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic | Skills; Agents | Agent Skills as modular capability packages: instructions, resources, scripts — reducing context burden and improving reliability. | 2025-10-16 |
| P0 | [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Anthropic | Skills; Claude; Progressive disclosure | Official Claude Agent Skills docs: modular instructions, metadata, scripts, resources, and on-demand loading across Claude products. | Current docs |
| P0 | [Skills](https://developers.openai.com/api/docs/guides/tools-skills) | OpenAI | Skills; API; Shell environments | Official OpenAI API guide for uploading, managing, and attaching reusable Skills to hosted and local shell environments. | Current docs |
| P0 | [Agent Skills Specification](https://agentskills.io/specification) | Agent Skills | Skills; Specification; Progressive disclosure | Complete skill package format: SKILL.md frontmatter, optional scripts/references/assets, file references, and validation. | Current docs |
| P0 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic | MCP; Code execution; Context | Key article on MCP scale challenges: reduce token overhead with code execution/on-demand tools; learn progressive disclosure. | 2025-11-04 |
| P0 | [Introducing advanced tool use on Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic | Tools; MCP; Advanced tool use | Tool search, deferred loading, programmatic tool calling; solving context pollution from large numbers of MCP tools. | 2025-11-24 |
| P0 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic | Harness; Long-running agents | Essential harness reading: working across multiple context windows, task logging, external state, agent self-recovery. | 2025-11-26 |
| P0 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic | Evals; Agents | Agent evals are more complex than static evals: multi-turn, tools, state changes, creative solutions, failure taxonomy. | 2026-01-09 |
| P0 | [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic | Agents; Autonomy; Measurement | Quantify agent autonomy using metrics like task duration and supervision needs; ideal for building autonomy benchmarks. | 2026-02-18 |
| P0 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic | Harness; Application development | Harness design patterns for delegating long-running app development tasks to agents; compare with OpenAI Codex harness. | 2026-03-24 |
| P0 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Anthropic | Managed agents; Harness | Decouple the model brain from execution hands/harness, keeping interfaces stable as the harness evolves. | 2026-04-08 |
| P0 | [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic | Safety; Containment; Agents | Blast radius of powerful agent releases, human-in-the-loop, and containment strategies. | 2026-05-25 |
| P1 | [Structured Outputs for Multi-Agent Systems](https://developers.openai.com/cookbook/examples/structured_outputs_multi_agent) | OpenAI | Agents; Multi-agent; Structured outputs | Use strict schemas to constrain structured messages and handoffs between multiple agents. | 2024-08-06 |
| P1 | [Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku](https://www.anthropic.com/news/3-5-models-and-computer-use) | Anthropic | Agents; Computer use | Claude computer use beta starting point: the model uses a computer via screenshots and actions. | 2024-10-22 |
| P1 | [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) | Anthropic | Agents; Coding; Evals | SWE-bench agent scaffolding article: same model performance strongly depends on harness/scaffolding. | 2025-01-06 |
| P1 | [Introducing Operator](https://openai.com/index/introducing-operator/) | OpenAI | Agents; Computer use; Safety | Early product form of browser-based agents: model clicks, types, and executes tasks on web pages, emphasizing user confirmation and safety boundaries. | 2025-01-23 |
| P1 | [Computer-Using Agent](https://openai.com/index/computer-using-agent/) | OpenAI | Agents; Computer use | Understand how CUA combines vision, mouse/keyboard actions, and environment feedback into an agent loop; compare with Claude computer use. | 2025-01-23 |
| P1 | [Claude 3.7 Sonnet and Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet) | Anthropic | Agents; Coding; Claude Code | Early release of Claude Code, marking Claude's entry into the agentic coding tool space. | 2025-02-24 |
| P1 | [The think tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) | Anthropic | Tools; Reasoning; Agents | Give the model an explicit think tool in complex tool-use chains; learn tool design for policy-heavy/multi-step decisions. | 2025-03-20 |
| P1 | [Evaluating Agents with Langfuse](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; Agents | Observe and evaluate Agents SDK runs with Langfuse; learn tracing/eval workflows. | 2025-03-31 |
| P1 | [Parallel Agents with the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/parallel_agents) | OpenAI | Agents; Parallelism; Agents SDK | Parallel agent patterns: decompose tasks, execute in parallel, aggregate results. | 2025-05-01 |
| P1 | [Multi-Agent Portfolio Collaboration with OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration) | OpenAI | Agents; Multi-agent; Portfolio | Multi-agent collaboration business example: research, analysis, combined output. | 2025-05-28 |
| P1 | [MCP-Powered Agentic Voice Framework](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Voice; Agents | Voice agent + MCP paradigm: real-time interaction, tool extension, task execution. | 2025-06-17 |
| P1 | [Deep Research API with the Agents SDK](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Deep research; Agents SDK | Integrate Deep Research API into Agents SDK workflows. | 2025-06-25 |
| P1 | [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) | Anthropic | MCP; Claude Desktop; Packaging | Package local MCP servers as one-click install extensions; learn MCP distribution/installation/local permission issues. | 2025-06-26 |
| P1 | [Building a Supply-Chain Copilot with OpenAI Agent SDK and Databricks MCP Servers](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Agents; Databricks | Enterprise data platform MCP + Agent SDK business agent example. | 2025-07-08 |
| P1 | [Introducing ChatGPT agent: bridging research and action](https://openai.com/index/introducing-chatgpt-agent/) | OpenAI | Agents; ChatGPT; Computer use | End-user-facing ChatGPT agent: combining research, browser, computer use, file/slide capabilities. | 2025-07-17 |
| P1 | [ChatGPT agent System Card](https://openai.com/index/chatgpt-agent-system-card/) | OpenAI | Agents; Safety; Evals | Learn pre-launch risk classification, evaluation, permissions, human confirmation, and abuse prevention for agent products. | 2025-07-17 |
| P1 | [Context Engineering - Short-Term Memory Management with Sessions](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Sessions; Agents | How short-term memory/session state affects agent reliability. | 2025-09-09 |
| P1 | [Progressive disclosure](https://docs.claude-mem.ai/progressive-disclosure) | Claude-Mem | Context; Memory; Progressive disclosure | Make retrieval costs visible and let the agent fetch details on demand, reducing context pollution and attention waste. | Current docs |
| P1 | [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) | OpenAI | Agents; Coding; IDE | Codex evolves from research preview to daily dev tool: CLI, IDE, web/mobile collaboration, and more independent task execution. | 2025-09-15 |
| P1 | [Introducing Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) | Anthropic | Agents; Claude Agent SDK; Computer use | Sonnet 4.5 emphasizes coding, complex agents, computer use, with simultaneous Agent SDK launch. | 2025-09-29 |
| P1 | [Introducing apps in ChatGPT and the new Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/) | OpenAI | MCP; Apps; ChatGPT | Apps SDK extends UI and tool server via MCP; entry point for understanding the ChatGPT app / MCP app ecosystem. | 2025-10-06 |
| P1 | [Build your ChatGPT UI](https://developers.openai.com/apps-sdk/build/chatgpt-ui) | OpenAI | MCP; Apps SDK; UI | Build custom UI components that turn structured MCP tool results into interactive ChatGPT app interfaces. | Current docs |
| P1 | [Codex is now generally available](https://openai.com/index/codex-now-generally-available/) | OpenAI | Agents; Coding; Codex SDK | Codex GA, Slack integration, Codex SDK, admin tools; see how coding agents enter enterprise management. | 2025-10-06 |
| P1 | [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans) | OpenAI | Codex; Long-running; Planning | ExecPlan files and cross-context task management for multi-hour coding-agent work. | 2025-10-07 |
| P1 | [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/beyond-permission-prompts) | Anthropic | Safety; Permissions; Claude Code | From simple permission prompts to fine-grained security policies, reducing autonomous mode risk and interruptions. | 2025-10-20 |
| P1 | [Introducing Aardvark: OpenAI's agentic security researcher](https://openai.com/index/introducing-aardvark/) | OpenAI | Agents; Security | Security-domain agent form: continuous scanning, issue verification, fix suggestions; later integrated as Codex Security. | 2025-10-30 |
| P1 | [Build a coding agent with GPT 5.1](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Coding | Build a coding agent from scratch: understand file editing, command execution, loops, and verification. | 2025-11-13 |
| P1 | [OpenAI co-founds Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) | OpenAI | MCP; Standards; AGENTS.md | MCP, AGENTS.md, and agent standards enter the Linux Foundation/AAIF context; understand ecosystem standardization. | 2025-12-09 |
| P1 | [Donating MCP and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | Anthropic | MCP; Standards; AAIF | Anthropic donates MCP to Linux Foundation/AAIF; read alongside OpenAI's AAIF article. | 2025-12-09 |
| P1 | [Context Engineering for Personalization - Long-Term Memory Notes](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Long-term memory; Agents | How long-term memory serves as agent personalization/state management. | 2026-01-05 |
| P1 | [Supercharging Codex with JetBrains MCP at Skyscanner](https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp) | OpenAI | MCP; Codex; IDE | Real IDE/MCP case study: how Codex CLI accesses IDE context and dev tools via JetBrains MCP. | 2026-01-11 |
| P1 | [Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | Anthropic | Evals; Technical hiring | How strong agents continuously break technical evaluations; relevant to benchmark contamination prevention and eval design. | 2026-01-21 |
| P1 | [Agent Evaluation Readiness Checklist](https://www.langchain.com/blog/agent-evaluation-readiness-checklist) | LangChain | Evals; Agents; Checklist | Practical checklist for selecting eval levels, constructing datasets, designing graders, and connecting offline and online evals. | 2026 |
| P1 | [Inside OpenAI's in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/) | OpenAI | Agents; Data; Memory | Internal data agent case study: memory, Codex, data context, reliability; learn enterprise knowledge/data agents. | 2026-01-29 |
| P1 | [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) | OpenAI | Agents; Coding; Multi-agent | Desktop command center for agents: multi-threaded/parallel long tasks, project-level agent workflows. | 2026-02-02 |
| P1 | [Apple's Xcode now supports Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | Anthropic | Claude Agent SDK; Xcode; MCP | Embed Claude Agent SDK in Xcode: harness, subagents, background tasks, plugins, MCP. | 2026-02-03 |
| P1 | [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | Anthropic | Evals; Coding agents; Infrastructure | Environment configuration significantly impacts scores in agentic coding evals; control infrastructure noise in both production and benchmarks. | 2026-02-05 |
| P1 | [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | Anthropic | Multi-agent; Coding; Long-running | Parallel Claude teams completing large engineering tasks; learn multi-agent division of labor, coordination, and long-running execution. | 2026-02-05 |
| P1 | [Codex Security: now in research preview](https://openai.com/index/codex-security-now-in-research-preview/) | OpenAI | Agents; Security; Codex | Productization of an agentic security researcher: vulnerability discovery, verification, fix suggestions, reducing triage noise. | 2026-03-06 |
| P1 | [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering) | Anthropic | Evals; Agent awareness | Risk of models recognizing/adapting to evaluations; relevant to agent benchmark credibility discussions. | 2026-03-06 |
| P1 | [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) | Anthropic | Safety; Permissions; Autonomy | Claude Code auto mode risk classification, allow/block rules, exception handling, and security testing. | 2026-03-25 |
| P1 | [How we build evals for Deep Agents](https://www.langchain.com/blog/how-we-build-evals-for-deep-agents) | LangChain | Evals; Deep agents; Traces | Targeted eval design for deep agents: select production behaviors, tag evals, inspect traces, and avoid false confidence from broad but shallow suites. | 2026-03-26 |
| P1 | [How to Evaluate Tool-Calling Agents](https://arize.com/blog/how-to-evaluate-tool-calling-agents/) | Arize | Evals; Tool calling; Trajectories | Evaluation workflow for tool selection, tool arguments, trajectories, and LLM-as-judge scoring of tool-using agents. | 2026 |
| P1 | [A Survey on Agent-as-a-Judge](https://arxiv.org/html/2601.05111v1) | Academic | Evals; Agent-as-a-judge; Survey | Survey of agent-based evaluation methods that extend LLM-as-judge with multi-step reasoning, tools, and external observation. | 2026 |
| P1 | [Migrate a Legacy Codebase with Sandbox Agents](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Sandbox; Evals | Sandbox agent evaluation and execution patterns in large legacy code migrations. | 2026-04-07 |
| P1 | [Codex for (almost) everything](https://openai.com/index/codex-for-almost-everything/) | OpenAI | Agents; Codex; MCP; Plugins | Codex app expanded to Windows/macOS, computer use, in-app browser, memory, plugins, MCP servers. | 2026-04-16 |
| P1 | [Computer Use Agents in Daytona Sandboxes](https://developers.openai.com/cookbook/examples/agents_sdk/computer_use_with_daytona/computer_use_with_daytona) | OpenAI | Computer use; Sandbox; Agents | Computer-use agents and sandbox runtimes; compare with Operator/CUA/Claude computer use. | 2026-04-19 |
| P1 | [Introducing workspace agents in ChatGPT](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) | OpenAI | Agents; Workspace; Governance | Workspace agents: shared agents, permissions, tools, memory, safeguards; ideal for team collaboration agent design. | 2026-04-22 |
| P1 | [Building workspace agents in ChatGPT to complete repeatable, end-to-end work](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Workspace agents; ChatGPT | Practical workspace agents for repeatable end-to-end team workflows. | 2026-04-22 |
| P1 | [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/) | OpenAI | Agents; Latency; Responses API | Optimize latency by treating agentic rollouts as long-lived connections/tasks; learn production agent transport and caching. | 2026-05-01 |
| P1 | [Agents for financial services](https://www.anthropic.com/news/finance-agents) | Anthropic | Agents; Finance; MCP | Ten ready-to-run agent templates, Claude Code/Cowork plugins, Managed Agents cookbooks, MCP app. | 2026-05-05 |
| P1 | [Migrate from the Claude Agent SDK to the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/migrate-from-claude-agent-sdk/readme) | OpenAI | Agents SDK; Migration | Compare Claude Agent SDK and OpenAI Agents SDK from a migration perspective; ideal for dual-stack learning. | 2026-05-07 |
| P1 | [AI agent evaluation: How to test, debug, and improve agents in production](https://arize.com/blog/why-testing-ai-agents-is-non-negotiable/) | Arize | Evals; Production; Observability | Production-oriented agent eval guide covering planning, memory, traces, debugging, and improvement loops. | 2026 |
| P1 | [Build long-running AI agents that pause, resume, and never lose context with ADK](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) | Google | Harness; Long-running agents; ADK | Practical ADK tutorial for durable state machines, persistent sessions, event-driven resume, multi-agent delegation, and evals. | 2026-05-12 |
| P1 | [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/) | OpenAI | Safety; Sandbox; Codex | Coding agent sandbox design on Windows: file access, network restrictions, approval tradeoffs. | 2026-05-13 |
| P1 | [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) | OpenAI | Agents; Evals; Self-improvement | Combine production traces, expert feedback, Codex loop, and eval infrastructure into self-improving business agents. | 2026-05-27 |
| P1 | [SchemaFlow: Agentic Database Change Impact Analysis, SQL Generation, and Eval Guardrails](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; SQL; Agent guardrails | Guardrails and eval guardrails examples for data/SQL agents. | 2026-06-05 |
| P1 | [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart) | OpenAI | Agents; SDK | Quickly build a minimal agent; understand the code patterns of run, tool, and handoff. | Current docs |
| P1 | [OpenAI Agents SDK examples](https://openai.github.io/openai-agents-python/examples/) | OpenAI | Agents SDK; Patterns; Examples | Practical examples for agent patterns, MCP, memory, guardrails, approvals, handoffs, and streaming. | Current docs |
| P1 | [MCP Apps compatibility in ChatGPT](https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt) | OpenAI | MCP; Apps SDK; UI | Understand MCP Apps UI standards, iframe/bridge, and compatibility between ChatGPT and other hosts. | Current docs |
| P1 | [Use Codex with the Agents SDK](https://developers.openai.com/codex/guides/agents-sdk) | OpenAI | MCP; Codex; Agents SDK | Use Codex as an MCP server for other agents to call; ideal for multi-agent dev workflows. | Current docs |
| P1 | [Agent approvals and security - Codex](https://developers.openai.com/codex/agent-approvals-security) | OpenAI | Safety; Approvals; Codex | Official reference for Codex approval modes, sandbox, network access; read alongside OpenAI/Anthropic safety articles. | Current docs |
| P1 | [Agent Skills - Codex](https://developers.openai.com/codex/skills) | OpenAI | Codex; Skills; Plugins | Skills/Plugins as reusable workflow packages; compare with Anthropic Agent Skills. | Current docs |
| P1 | [Skills in OpenAI API](https://developers.openai.com/cookbook/examples/skills_in_api) | OpenAI | Skills; OpenAI API | Cookbook example for using Skills in the OpenAI API and connecting skill bundles to agent workflows. | Current docs |
| P1 | [Custom instructions with AGENTS.md - Codex](https://developers.openai.com/codex/guides/agents-md) | OpenAI | AGENTS.md; Context | How AGENTS.md provides persistent project specifications for agents; establish repo-level agent contracts. | Current docs |
| P1 | [Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) | OpenAI | Observability; MCP; Tracing | Tracing, MCP integration, provider/observability; essential for production agent debugging. | Current docs |
| P1 | [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) | OpenAI | MCP; Security; Private tools | Securely expose private/intranet MCP servers to supported OpenAI surfaces; ideal for enterprise deployment. | Current docs |
| P1 | [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | Anthropic | Claude Code; Agentic loop; Harness | Under-the-hood architecture of Claude Code: the agentic loop (gather context → act → verify), built-in tool categories, context window management, and extension points. | Current docs |
| P1 | [The spec is dead, long live the spec!](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code) | Ravi on Product | Specs; Product; Agentic development | Argues that specs and prompts become durable source material when AI can generate implementation rapidly. | 2025-07-31 |
| P1 | [Build a Remote MCP server](https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/#add-authentication) | Cloudflare | MCP; Remote servers; Authentication | Practical guide to deploying remote MCP servers with Streamable HTTP, OAuth, session state, and authorization boundaries. | Current docs |
| P1 | [Introducing the MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) | MCP | MCP; Registry; Discovery | Official preview of the MCP Registry as a source of truth for discovering and distributing public MCP servers. | 2025-09-08 |
| P1 | [How Anthropic teams use Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) | Anthropic | Claude Code; Team workflows; Case studies | Internal Anthropic examples across data infrastructure, product, security, inference, design, legal, and RL engineering. | Current PDF |
| P1 | [SAST vs. DAST vs. RASP](https://www.splunk.com/en_us/blog/learn/sast-vs-dast.html) | Splunk | Security; AppSec; Testing | Clear comparison of static, dynamic, and runtime application security testing methods for agent safety baselines. | Current article |
| P1 | [GitHub Copilot: Remote Code Execution via Prompt Injection](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) | Embrace The Red | Security; Prompt injection; Coding agents | Concrete RCE case study showing how agent-controlled configuration changes can collapse permission boundaries. | 2025-08-12 |
| P1 | [Finding vulnerabilities in modern web apps using Claude Code and OpenAI Codex](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/) | Semgrep | Security; Coding agents; Vulnerability research | Empirical study of Claude Code and Codex on vulnerability discovery, including true positives, false positives, and failure modes. | 2025-09-02 |
| P1 | [AI Agents Are Here. So Are the Threats.](https://unit42.paloaltonetworks.com/agentic-ai-threats/) | Unit 42 | Security; Agent threats; Prompt injection | Threat scenarios for multi-agent systems: instruction extraction, tool misuse, internal access, impersonation, and RCE. | Current article |
| P1 | [OWASP Top Ten](https://owasp.org/www-project-top-ten/) | OWASP | Security; Web applications; AppSec | Foundational web application risk taxonomy; useful baseline when asking agents to build or review web apps. | Current project |
| P1 | [How to review code effectively](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/) | GitHub | Code review; Engineering practice | Staff-engineer philosophy for effective code review: reviewer intent, clarity, scope, and human communication. | Current article |
| P1 | [AI-Assisted Assessment of Coding Practices in Modern Code Review](https://arxiv.org/pdf/2405.13565) | Academic | Code review; AI review; Google | AutoCommenter paper: architecture, deployment, and evaluation of an LLM-assisted code-review system at Google scale. | 2024-05-22 |
| P1 | [AI code review implementation and best practices](https://graphite.dev/guides/ai-code-review-implementation-best-practices) | Graphite | Code review; AI review; Workflow | Implementation checklist for introducing AI code review into repository hooks, policies, team rules, and review workflows. | Current article |
| P1 | [ML and LLM system design: 800 case studies to learn from](https://www.evidentlyai.com/ml-system-design) | Evidently AI | ML systems; LLM systems; Case studies | Database of production ML and LLM case studies from 150+ companies, including GenAI, RAG, AI agents, evaluation, and deployment architecture examples. | 2025-12-22 |
| P1 | [Introduction to Site Reliability Engineering](https://sre.google/sre-book/introduction/) | Google | SRE; Production; Reliability | Foundational SRE framing: software engineering applied to operations, toil reduction, risk, and reliable production systems. | Current book |
| P1 | [Traces & Spans: Observability Basics You Should Know](https://last9.io/blog/traces-spans-observability-basics/) | Last9 | Observability; Tracing; Production | Practical primer on traces and spans for debugging distributed systems and giving agents useful production evidence. | 2025-04-23 |
| P1 | [Kubernetes Troubleshooting in Resolve AI](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai) | Resolve AI | SRE agents; Kubernetes; Troubleshooting | Production-agent case study for Kubernetes root-cause analysis across pods, deployments, logs, metrics, and infrastructure signals. | 2026-05-21 |
| P1 | [The role of multi agent systems in making software engineers AI-native](https://resolve.ai/blog/role-of-multi-agent-systems-AI-native-engineering) | Resolve AI | Multi-agent; SRE; AI-native engineering | Argues that production engineering needs specialized multi-agent systems for parallel investigation and domain-aware coordination. | 2026-03-20 |
| P0 | [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | Community | Harness; Agent loop; Tools; Context | Hands-on 20-lesson tutorial building a Claude Code–like agent harness from scratch: agent loop, tool integration, context compaction, multi-agent coordination, permissions, MCP plugins. | 2026 |
| P0 | [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](https://arxiv.org/abs/2604.14228) | Academic | Agent architecture; Claude Code; Design space | Deep technical analysis of Claude Code's architecture: agentic loop, permission system, context compaction, extensibility (MCP/plugins/skills/hooks), subagent delegation, and comparison with open-source alternatives. | 2026-04-14 |
| P0 | [Function Calling](https://developers.openai.com/api/docs/guides/function-calling) | OpenAI | Tools; Function calling; API | Official guide to function/tool calling: define functions with JSON schemas, handle model tool calls, execute and return results. | Current docs |
| P0 | [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | Anthropic | Tools; Tool use; API | Connect Claude to external tools and APIs: client vs server tools, the agentic loop, strict schema conformance, and when Claude decides to call tools. | Current docs |
| P0 | [Function calling - Gemini API](https://ai.google.dev/gemini-api/docs/function-calling) | Google | Tools; Function calling; API | Enable Gemini models to connect with external tools via function calling: single-turn, multi-turn, parallel, and sequential function chains. | Current docs |
| P2 | [Vulnerability Prompt Analysis with O3](https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt) | Community | Security; Prompting; Vulnerability research | Concrete vulnerability-analysis prompt used with o3; useful as a prompt artifact to study, not a general framework. | 2025 |
| P2 | [Code Reviews: Just Do It](https://blog.codinghorror.com/code-reviews-just-do-it/) | Coding Horror | Code review; Engineering practice | Classic argument for peer review as one of the highest-leverage software quality practices. | 2006-01-21 |
| P2 | [Code Review Essentials for Software Teams](https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html) | Blake Smith | Code review; Team practice | Practical code review hierarchy: shared mental models, design clarity, pull request quality, and constructive feedback. | 2015-02-09 |
| P2 | [Lessons from millions of AI code reviews](https://www.youtube.com/watch?v=TswQeKftnaw) | Greptile | AI code review; Lessons | Talk on patterns from large-scale AI code review usage; useful qualitative context for review-agent design. | Video |
| P2 | [Multi-stack Web App Builds](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8) | Community | Assignments; Full-stack; Practice | Practice assignment for multi-stack web app builds; useful as an applied testbed for coding agents. | Current repo |
| P2 | [AI Production Engineer](https://resolve.ai/blog/product-deep-dive) | Resolve AI | SRE agents; Product case study | Product deep dive on autonomous production engineering agents for alerts, RCA, remediation, and post-incident review. | 2026-03-28 |
| P2 | [The Top 5 Benefits of Agentic AI in On-call Engineering](https://resolve.ai/blog/Top-5-Benefits) | Resolve AI | SRE agents; On-call; Operations | Overview of agentic AI benefits for incident response, dynamic knowledge, and on-call operations. | 2025-07-25 |
| P2 | [Orchestrating Agents: Routines and Handoffs (archived)](https://developers.openai.com/cookbook/examples/orchestrating_agents) | OpenAI | Agents; Handoffs; Orchestration | Historical cookbook for routines and handoffs; useful conceptually, but archived and not the current recommended implementation path. | 2024-10-10 |
| P2 | [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | Anthropic | Context; Retrieval; RAG | Not agent-specific, but important for agent RAG/context: prepend context to chunks before retrieval to improve recall. | 2024-09-19 |
| P2 | [Developing a computer use model](https://www.anthropic.com/news/developing-computer-use) | Anthropic | Computer use; Agents | More technical explanation of how the computer-use model moves the mouse, clicks, types, and reads screen feedback. | 2024-10-22 |
| P2 | [Introducing Claude 4](https://www.anthropic.com/news/claude-4) | Anthropic | Agents; Coding; Long-running | Overview of Claude Opus/Sonnet 4 capabilities: coding, advanced reasoning, agent workflows. | 2025-05-22 |
| P2 | [Claude for Financial Services](https://www.anthropic.com/news/claude-for-financial-services) | Anthropic | Agents; Connectors; Finance | Vertical industry agent/connector productization case; understand data, permissions, and tool integration in finance. | 2025-07-15 |
| P2 | [Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services) | Anthropic | Agents; Skills; Finance | Claude for Excel, real-time data connectors, pre-built Agent Skills for vertical industry productization. | 2025-10-27 |
| P2 | [Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) | OpenAI | Agents; Coding model; Evals | Codex-native model and long-running coding/terminal/agentic benchmarks; understand how model capabilities serve the harness. | 2026-02-05 |
| P2 | [Introducing OpenAI Frontier](https://openai.com/index/introducing-openai-frontier/) | OpenAI | Agents; Enterprise; Governance | Enterprise AI coworker/agent platform: shared context, onboarding, permissions, guardrails, governance. | 2026-02-10 |
| P2 | [Introducing Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) | Anthropic | Agents; Planning; Computer use | Sonnet 4.6 emphasizes coding, computer use, long-context reasoning, agent planning. | 2026-02-17 |
| P2 | [Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) | Anthropic | Agents; Long-running; Tool use | Model release perspective on long-running tasks, agentic harness, subagents, and tool call capabilities. | 2026-02-25 |
| P2 | [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) | Anthropic | Agents; Long-running; Coding | Stronger software engineering and long-running task performance; track how model capabilities impact agent workloads. | 2026-04-16 |
| P2 | [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) | Anthropic | Reliability; Claude Code; Agent SDK | Postmortem on Claude Code/Agent SDK quality regression; learn agent product operations and regression control. | 2026-04-23 |
| P2 | [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) | Anthropic | Agents; Dynamic workflows; Long-running | Dynamic workflows, hundreds of parallel subagents, long-running agentic tasks — latest model/product direction. | 2026-05-28 |
| P2 | [Codex for every role, tool, and workflow](https://openai.com/index/codex-for-every-role-tool-workflow/) | OpenAI | Agents; Codex; Plugins | Codex expands from development to knowledge work: role-specific plugins, Sites, annotations, parallel workflows. | 2026-06-02 |
| P2 | [Codex is becoming a productivity tool for everyone](https://openai.com/index/codex-for-knowledge-work/) | OpenAI | Agents; Knowledge work | Usage data shows how non-developers use Codex for reports, spreadsheets, research, automation, and lightweight tools. | 2026-06-02 |
| P2 | [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | OpenAI | MCP; Docs; Context | Official OpenAI docs MCP server; connect docs directly to local agents/IDEs. | Current docs |
| P2 | [Codex SDK](https://developers.openai.com/codex/sdk) | OpenAI | Codex SDK; Automation | Programmatically control Codex in CI/CD or internal tools; embed coding agents into existing workflows. | Current docs |
| P2 | [When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement) | Anthropic | Agents; Recursive self-improvement; Safety | How AI systems accelerate their own development through recursive self-improvement; three possible futures and the need for verifiable coordination. | 2026-05 |

---

## Who Is This For?

- AI Engineers
- Agent Engineers
- LLM Engineers
- Platform Engineers
- Research Engineers
- AI Startup Founders

---

## Contributing

Contributions are welcome. If you find:

- New OpenAI resources
- New Anthropic resources
- MCP updates
- Agent evaluation frameworks
- Production engineering articles

Please open a pull request.

---

## Vision

> The goal of this project is to become the **System Design Primer** for Agentic Engineering.

If you're serious about building production AI agents, start here.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=keyuchen21/agentic-engineering-handbook&type=Date)](https://star-history.com/#keyuchen21/agentic-engineering-handbook&Date)

---

## License

[MIT](LICENSE)

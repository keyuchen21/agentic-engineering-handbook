# Agentic Engineering Handbook

> The definitive OpenAI, Claude, MCP, Harness, Evals, and Production Agent Systems learning roadmap.

[![Stars](https://img.shields.io/github/stars/keyuchen21/agentic-engineering-handbook?style=social)](https://github.com/keyuchen21/agentic-engineering-handbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--06--09-blue.svg)](#)

---

## Why This Repository?

The AI industry has entered the **Agentic Era**. Building production-grade AI systems now requires mastering agents, tool use, MCP, memory, long-running workflows, coding agents, agent harnesses, evals, and safety — but the knowledge is scattered across OpenAI blogs, Anthropic engineering posts, SDK docs, cookbooks, and research papers.

This repository consolidates **114 official resources** into one structured learning roadmap.

**The goal: Become a world-class Agentic Engineer.**

---

## Learning Roadmap

### Phase 1 — Agent Foundations

> Build shared vocabulary for workflow vs agent, tool loop, handoff, guardrails.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic |
| 2 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI |
| 3 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) | OpenAI |
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
| [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI |
| [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | OpenAI |

#### Build Exercise

Build a read-only repo/docs MCP server, then create an eval to verify the agent correctly cites documentation.

---

### Phase 3 — Context, Memory & Skills

> Learn to control context window, short/long-term memory, skills/plugins, CLAUDE.md/AGENTS.md.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic |
| 2 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic |
| 3 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Custom instructions with AGENTS.md - Codex](https://developers.openai.com/codex/guides/agents-md) | OpenAI |
| [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic |
| [Agent Skills - Codex](https://developers.openai.com/codex/skills) | OpenAI |

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
| 3 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic |

#### Then Read

| Title | Vendor |
|-------|--------|
| [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI |
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
| 3 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) | OpenAI |
| [Introducing workspace agents in ChatGPT](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) | OpenAI |
| [Apple's Xcode now supports Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | Anthropic |
| [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI |

#### Build Exercise

Run both OpenAI/Codex and Claude Code style workflows on the same repo: issue → plan → patch → tests → PR summary.

---

### Phase 6 — Evals, Safety & Production

> Build pre/post-launch eval loop, trace loop, safety boundaries, permissions, regression monitoring.

#### Read First

| # | Title | Vendor |
|---|-------|--------|
| 1 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic |
| 2 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI |
| 3 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI |

#### Then Read

| Title | Vendor |
|-------|--------|
| [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI |
| [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic |
| [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI |
| [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic |

#### Build Exercise

Build a smoke/macro eval suite for your agent: task success rate, tool misuse, prompt injection resistance, latency, cost, and human approval count.

---

## Recommended Reading Order

If you're new to agentic engineering, read the P0 articles in this order:

| # | Title | Vendor |
|---|-------|--------|
| 1 | [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | OpenAI |
| 2 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI |
| 3 | [Introducing AgentKit](https://openai.com/index/introducing-agentkit/) | OpenAI |
| 4 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI |
| 5 | [Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) | OpenAI |
| 6 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic |
| 7 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic |
| 8 | [New tools and features in the Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/) | OpenAI |
| 9 | [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | OpenAI |
| 10 | [Building MCP servers for ChatGPT Apps and API integrations](https://developers.openai.com/api/docs/mcp) | OpenAI |
| 11 | [Building a Deep Research MCP Server](https://developers.openai.com/cookbook/examples/deep_research_api/how_to_build_a_deep_research_mcp_server/readme) | OpenAI |
| 11 | [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI |
| 12 | [Introducing Codex](https://openai.com/index/introducing-codex/) | OpenAI |
| 13 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI |
| 14 | [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | OpenAI |
| 15 | [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/) | OpenAI |
| 16 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | OpenAI |
| 17 | [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI |
| 18 | [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI |
| 19 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI |
| 20 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI |
| 21 | [Eval Driven System Design - From Prototype to Production](https://developers.openai.com/cookbook/topic/evals) | OpenAI |
| 22 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI |
| 23 | [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI |
| 24 | [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI |
| 25 | [Building Governed AI Agents - A Practical Guide to Agentic Scaffolding](https://developers.openai.com/cookbook/topic/agents) | OpenAI |
| 26 | [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/topic/agents) | OpenAI |
| 27 | [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic |
| 28 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic |
| 29 | [Writing effective tools for AI agents - with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic |
| 30 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic |
| 31 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic |
| 32 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic |
| 33 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic |
| 34 | [Introducing advanced tool use on Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic |
| 35 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic |
| 36 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic |
| 37 | [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic |
| 38 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic |
| 39 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Anthropic |
| 40 | [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic |

---

## Full Reading Table

### P0 — Must Read (40 articles)

| # | Title | Vendor | Topic | Key Idea | Date |
|---|-------|--------|-------|----------|------|
| 1 | [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | OpenAI | Agents; MCP; Platform | Annual overview: systematic walkthrough of Responses API, Agents SDK, AgentKit, Codex, MCP, Apps SDK, and AGENTS.md. | 2025-12-30 |
| 2 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI | Agents; Responses API; Tools | Key starting point for OpenAI's agent platform: Responses API, built-in web/file/computer tools, Agents SDK, tracing/observability. | 2025-03-11 |
| 3 | [Introducing AgentKit](https://openai.com/index/introducing-agentkit/) | OpenAI | Agents; Evals; AgentKit | AgentKit, expanded evals, agent RFT: the official agent toolchain from prototype to production. | 2025-10-06 |
| 4 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI | Agents; SDK | Official SDK entry point: concepts and boundaries of agent, tool, handoff, guardrail, and tracing. | Current docs |
| 5 | [Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) | OpenAI | Agents; Handoffs; Orchestration | Classic introduction: how routines, handoffs, and tool calling combine into controllable multi-flow agents. | 2024-10-10 |
| 6 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic | MCP; Standards | The origin article for MCP: an open standard connecting AI assistants to data, tools, and systems. | 2024-11-25 |
| 7 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic | Agents; Patterns; Frameworks | Essential agent primer: workflow vs agent, prompt/tool/retrieval, orchestrator-worker, evaluator-optimizer patterns. | 2024-12-19 |
| 8 | [New tools and features in the Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/) | OpenAI | MCP; Responses API; Tools | Responses API extended to remote MCP servers, image/code/file tools; see how OpenAI integrates MCP into its runtime. | 2025-05-21 |
| 9 | [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | OpenAI | MCP; Connectors; Responses API | Official guide to connecting remote MCP servers and connectors; includes approvals and security considerations. | Current docs |
| 10 | [Building MCP servers for ChatGPT Apps and API integrations](https://developers.openai.com/api/docs/mcp) | OpenAI | MCP; ChatGPT Apps; API | Official guide to writing MCP servers: supply tools/knowledge to ChatGPT Apps, deep research, and API integrations. | Current docs |
| 11 | [Building a Deep Research MCP Server](https://developers.openai.com/cookbook/examples/deep_research_api/how_to_build_a_deep_research_mcp_server/readme) | OpenAI | MCP; Deep research | Minimal implementation of a search/fetch MCP server for Deep Research. | 2025-06-25 |
| 11 | [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI | MCP; Codex | How Codex CLI/IDE connects to MCP servers, adding Figma, browser, docs, and internal tool context to agents. | Current docs |
| 12 | [Introducing Codex](https://openai.com/index/introducing-codex/) | OpenAI | Agents; Coding; Sandbox | Cloud-based software engineering agent: parallel tasks, repo sandbox, running tests/linters/type checkers, producing auditable evidence. | 2025-05-16 |
| 13 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI | Harness; Agent loop; Codex | How Codex CLI chains prompt, tool schema, MCP tools, Responses API, and context management into an agent loop. | 2026-01-23 |
| 14 | [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | OpenAI | Harness; Codex App Server; JSON-RPC | Core harness article: Codex core, App Server, JSON-RPC, streaming progress, approval, diff, and thread management. | 2026-02-04 |
| 15 | [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/) | OpenAI | Harness; Responses API; Sandbox | Responses API + shell tool + hosted containers form the agent runtime; essential for understanding the model-to-agent execution environment. | 2026-03-10 |
| 16 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | OpenAI | Harness; Agent-first engineering | Design product code, tests, CI, docs, and observability to be agent-readable/executable; learn agent-first repo organization. | 2026-02-11 |
| 17 | [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI | Harness; Agents SDK; MCP; Skills | Agents SDK harness becomes more complete: memory, sandbox orchestration, Codex-like filesystem tools, MCP, skills, AGENTS.md. | 2026-04-15 |
| 18 | [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI | MCP; Codex; Agents SDK | Codex CLI as an MCP server integrated with Agents SDK; real multi-agent dev workflow. | 2025-10-01 |
| 19 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI | Memory; Compaction; Reliability | Memory and compaction design for long-context/multi-turn agents. | 2026-05-01 |
| 20 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI | Evals; Traces; Self-improvement | Connect traces, evals, and Codex fixes into an agent improvement loop. | 2026-05-12 |
| 21 | [Eval Driven System Design - From Prototype to Production](https://developers.openai.com/cookbook/topic/evals) | OpenAI | Evals; Production | Use evals as the driving force for system design; ideal for moving agents from demo to production. | 2025-06-02 |
| 22 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI | Evals; Skills; Agents | Systematically test agent skills with evals; establish quality gates before skill release. | 2026-01-22 |
| 23 | [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI | MCP; Evals | Evaluate QA/retrieval capabilities with MCP tools; ideal for building an MCP regression suite. | 2025-06-09 |
| 24 | [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI | Safety; Sandbox; Codex | How OpenAI runs Codex internally: sandbox, approvals, network policy, agent-native telemetry. | 2026-05-20 |
| 25 | [Building Governed AI Agents - A Practical Guide to Agentic Scaffolding](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Governance; Guardrails; Agents | Governed agent scaffolding: permissions, guardrails, auditing, and organizational policies. | 2026-02-23 |
| 26 | [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; Agentic systems | Evaluate agents at the end-to-end/macro level, not just individual step outputs. | 2026-05-19 |
| 27 | [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic | Coding agents; Claude Code | Claude Code methodology: verification loop, explore-plan-code, CLAUDE.md, permissions, MCP, subagents, context management. | 2025-04-18 |
| 28 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic | Agents; Multi-agent; Research | Claude Research multi-agent architecture: planner + parallel research agents + synthesis; production multi-agent experience. | 2025-06-13 |
| 29 | [Writing effective tools for AI agents - with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic | Tools; MCP; Evals | Tool quality determines agent quality: tool descriptions, context budget, eval, and letting Claude optimize its own tools. | 2025-09-11 |
| 30 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic | Context; Agents | Context is the agent's core resource: selection, compression, isolation, persistence, and context pollution control. | 2025-09-29 |
| 31 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic | Claude Code; Agent SDK; Subagents | Claude Agent SDK, subagents, hooks, background tasks, checkpoints, and other autonomous coding agent capabilities. | 2025-09-29 |
| 32 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic | Skills; Agents | Agent Skills as modular capability packages: instructions, resources, scripts — reducing context burden and improving reliability. | 2025-10-16 |
| 33 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic | MCP; Code execution; Context | Key article on MCP scale challenges: reduce token overhead with code execution/on-demand tools; learn progressive disclosure. | 2025-11-04 |
| 34 | [Introducing advanced tool use on Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic | Tools; MCP; Advanced tool use | Tool search, deferred loading, programmatic tool calling; solving context pollution from large numbers of MCP tools. | 2025-11-24 |
| 35 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic | Harness; Long-running agents | Essential harness reading: working across multiple context windows, task logging, external state, agent self-recovery. | 2025-11-26 |
| 36 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic | Evals; Agents | Agent evals are more complex than static evals: multi-turn, tools, state changes, creative solutions, failure taxonomy. | 2026-01-09 |
| 37 | [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic | Agents; Autonomy; Measurement | Quantify agent autonomy using metrics like task duration and supervision needs; ideal for building autonomy benchmarks. | 2026-02-18 |
| 38 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic | Harness; Application development | Harness design patterns for delegating long-running app development tasks to agents; compare with OpenAI Codex harness. | 2026-03-24 |
| 39 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Anthropic | Managed agents; Harness | Decouple the model brain from execution hands/harness, keeping interfaces stable as the harness evolves. | 2026-04-08 |
| 40 | [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic | Safety; Containment; Agents | Blast radius of powerful agent releases, human-in-the-loop, and containment strategies. | 2026-05-25 |

---

### P1 — Highly Useful (49 articles)

<details>
<summary>Click to expand P1 reading list</summary>

| Title | Vendor | Topic | Key Idea | Date |
|-------|--------|-------|----------|------|
| [Structured Outputs for Multi-Agent Systems](https://developers.openai.com/cookbook/examples/structured_outputs_multi_agent) | OpenAI | Agents; Multi-agent; Structured outputs | Use strict schemas to constrain structured messages and handoffs between multiple agents. | 2024-08-06 |
| [Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku](https://www.anthropic.com/news/3-5-models-and-computer-use) | Anthropic | Agents; Computer use | Claude computer use beta starting point: the model uses a computer via screenshots and actions. | 2024-10-22 |
| [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) | Anthropic | Agents; Coding; Evals | SWE-bench agent scaffolding article: same model performance strongly depends on harness/scaffolding. | 2025-01-06 |
| [Introducing Operator](https://openai.com/index/introducing-operator/) | OpenAI | Agents; Computer use; Safety | Early product form of browser-based agents: model clicks, types, and executes tasks on web pages, emphasizing user confirmation and safety boundaries. | 2025-01-23 |
| [Computer-Using Agent](https://openai.com/index/computer-using-agent/) | OpenAI | Agents; Computer use | Understand how CUA combines vision, mouse/keyboard actions, and environment feedback into an agent loop; compare with Claude computer use. | 2025-01-23 |
| [Claude 3.7 Sonnet and Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet) | Anthropic | Agents; Coding; Claude Code | Early release of Claude Code, marking Claude's entry into the agentic coding tool space. | 2025-02-24 |
| [The think tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) | Anthropic | Tools; Reasoning; Agents | Give the model an explicit think tool in complex tool-use chains; learn tool design for policy-heavy/multi-step decisions. | 2025-03-20 |
| [Evaluating Agents with Langfuse](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; Agents | Observe and evaluate Agents SDK runs with Langfuse; learn tracing/eval workflows. | 2025-03-31 |
| [Parallel Agents with the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/parallel_agents) | OpenAI | Agents; Parallelism; Agents SDK | Parallel agent patterns: decompose tasks, execute in parallel, aggregate results. | 2025-05-01 |
| [Multi-Agent Portfolio Collaboration with OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration) | OpenAI | Agents; Multi-agent; Portfolio | Multi-agent collaboration business example: research, analysis, combined output. | 2025-05-28 |
| [MCP-Powered Agentic Voice Framework](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Voice; Agents | Voice agent + MCP paradigm: real-time interaction, tool extension, task execution. | 2025-06-17 |
| [Deep Research API with the Agents SDK](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Deep research; Agents SDK | Integrate Deep Research API into Agents SDK workflows. | 2025-06-25 |
| [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) | Anthropic | MCP; Claude Desktop; Packaging | Package local MCP servers as one-click install extensions; learn MCP distribution/installation/local permission issues. | 2025-06-26 |
| [Building a Supply-Chain Copilot with OpenAI Agent SDK and Databricks MCP Servers](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Agents; Databricks | Enterprise data platform MCP + Agent SDK business agent example. | 2025-07-08 |
| [Introducing ChatGPT agent: bridging research and action](https://openai.com/index/introducing-chatgpt-agent/) | OpenAI | Agents; ChatGPT; Computer use | End-user-facing ChatGPT agent: combining research, browser, computer use, file/slide capabilities. | 2025-07-17 |
| [ChatGPT agent System Card](https://openai.com/index/chatgpt-agent-system-card/) | OpenAI | Agents; Safety; Evals | Learn pre-launch risk classification, evaluation, permissions, human confirmation, and abuse prevention for agent products. | 2025-07-17 |
| [Context Engineering - Short-Term Memory Management with Sessions](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Sessions; Agents | How short-term memory/session state affects agent reliability. | 2025-09-09 |
| [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) | OpenAI | Agents; Coding; IDE | Codex evolves from research preview to daily dev tool: CLI, IDE, web/mobile collaboration, and more independent task execution. | 2025-09-15 |
| [Introducing Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) | Anthropic | Agents; Claude Agent SDK; Computer use | Sonnet 4.5 emphasizes coding, complex agents, computer use, with simultaneous Agent SDK launch. | 2025-09-29 |
| [Introducing apps in ChatGPT and the new Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/) | OpenAI | MCP; Apps; ChatGPT | Apps SDK extends UI and tool server via MCP; entry point for understanding the ChatGPT app / MCP app ecosystem. | 2025-10-06 |
| [Codex is now generally available](https://openai.com/index/codex-now-generally-available/) | OpenAI | Agents; Coding; Codex SDK | Codex GA, Slack integration, Codex SDK, admin tools; see how coding agents enter enterprise management. | 2025-10-06 |
| [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Codex; Long-running; Planning | Plan files and cross-context task management for long-running coding agents. | 2025-10-07 |
| [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/beyond-permission-prompts) | Anthropic | Safety; Permissions; Claude Code | From simple permission prompts to fine-grained security policies, reducing autonomous mode risk and interruptions. | 2025-10-20 |
| [Introducing Aardvark: OpenAI's agentic security researcher](https://openai.com/index/introducing-aardvark/) | OpenAI | Agents; Security | Security-domain agent form: continuous scanning, issue verification, fix suggestions; later integrated as Codex Security. | 2025-10-30 |
| [Build a coding agent with GPT 5.1](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Coding | Build a coding agent from scratch: understand file editing, command execution, loops, and verification. | 2025-11-13 |
| [OpenAI co-founds Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) | OpenAI | MCP; Standards; AGENTS.md | MCP, AGENTS.md, and agent standards enter the Linux Foundation/AAIF context; understand ecosystem standardization. | 2025-12-09 |
| [Donating MCP and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | Anthropic | MCP; Standards; AAIF | Anthropic donates MCP to Linux Foundation/AAIF; read alongside OpenAI's AAIF article. | 2025-12-09 |
| [Context Engineering for Personalization - Long-Term Memory Notes](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Long-term memory; Agents | How long-term memory serves as agent personalization/state management. | 2026-01-05 |
| [Supercharging Codex with JetBrains MCP at Skyscanner](https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp) | OpenAI | MCP; Codex; IDE | Real IDE/MCP case study: how Codex CLI accesses IDE context and dev tools via JetBrains MCP. | 2026-01-11 |
| [Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | Anthropic | Evals; Technical hiring | How strong agents continuously break technical evaluations; relevant to benchmark contamination prevention and eval design. | 2026-01-21 |
| [Inside OpenAI's in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/) | OpenAI | Agents; Data; Memory | Internal data agent case study: memory, Codex, data context, reliability; learn enterprise knowledge/data agents. | 2026-01-29 |
| [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) | OpenAI | Agents; Coding; Multi-agent | Desktop command center for agents: multi-threaded/parallel long tasks, project-level agent workflows. | 2026-02-02 |
| [Apple's Xcode now supports Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | Anthropic | Claude Agent SDK; Xcode; MCP | Embed Claude Agent SDK in Xcode: harness, subagents, background tasks, plugins, MCP. | 2026-02-03 |
| [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | Anthropic | Evals; Coding agents; Infrastructure | Environment configuration significantly impacts scores in agentic coding evals; control infrastructure noise in both production and benchmarks. | 2026-02-05 |
| [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | Anthropic | Multi-agent; Coding; Long-running | Parallel Claude teams completing large engineering tasks; learn multi-agent division of labor, coordination, and long-running execution. | 2026-02-05 |
| [Codex Security: now in research preview](https://openai.com/index/codex-security-now-in-research-preview/) | OpenAI | Agents; Security; Codex | Productization of an agentic security researcher: vulnerability discovery, verification, fix suggestions, reducing triage noise. | 2026-03-06 |
| [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering) | Anthropic | Evals; Agent awareness | Risk of models recognizing/adapting to evaluations; relevant to agent benchmark credibility discussions. | 2026-03-06 |
| [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) | Anthropic | Safety; Permissions; Autonomy | Claude Code auto mode risk classification, allow/block rules, exception handling, and security testing. | 2026-03-25 |
| [Migrate a Legacy Codebase with Sandbox Agents](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Sandbox; Evals | Sandbox agent evaluation and execution patterns in large legacy code migrations. | 2026-04-07 |
| [Codex for (almost) everything](https://openai.com/index/codex-for-almost-everything/) | OpenAI | Agents; Codex; MCP; Plugins | Codex app expanded to Windows/macOS, computer use, in-app browser, memory, plugins, MCP servers. | 2026-04-16 |
| [Computer Use Agents in Daytona Sandboxes](https://developers.openai.com/cookbook/examples/agents_sdk/computer_use_with_daytona/computer_use_with_daytona) | OpenAI | Computer use; Sandbox; Agents | Computer-use agents and sandbox runtimes; compare with Operator/CUA/Claude computer use. | 2026-04-19 |
| [Introducing workspace agents in ChatGPT](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) | OpenAI | Agents; Workspace; Governance | Workspace agents: shared agents, permissions, tools, memory, safeguards; ideal for team collaboration agent design. | 2026-04-22 |
| [Building workspace agents in ChatGPT to complete repeatable, end-to-end work](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Workspace agents; ChatGPT | Practical workspace agents for repeatable end-to-end team workflows. | 2026-04-22 |
| [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/) | OpenAI | Agents; Latency; Responses API | Optimize latency by treating agentic rollouts as long-lived connections/tasks; learn production agent transport and caching. | 2026-05-01 |
| [Agents for financial services](https://www.anthropic.com/news/finance-agents) | Anthropic | Agents; Finance; MCP | Ten ready-to-run agent templates, Claude Code/Cowork plugins, Managed Agents cookbooks, MCP app. | 2026-05-05 |
| [Migrate from the Claude Agent SDK to the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/migrate-from-claude-agent-sdk/readme) | OpenAI | Agents SDK; Migration | Compare Claude Agent SDK and OpenAI Agents SDK from a migration perspective; ideal for dual-stack learning. | 2026-05-07 |
| [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/) | OpenAI | Safety; Sandbox; Codex | Coding agent sandbox design on Windows: file access, network restrictions, approval tradeoffs. | 2026-05-13 |
| [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) | OpenAI | Agents; Evals; Self-improvement | Combine production traces, expert feedback, Codex loop, and eval infrastructure into self-improving business agents. | 2026-05-27 |
| [SchemaFlow: Agentic Database Change Impact Analysis, SQL Generation, and Eval Guardrails](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; SQL; Agent guardrails | Guardrails and eval guardrails examples for data/SQL agents. | 2026-06-05 |
| [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart) | OpenAI | Agents; SDK | Quickly build a minimal agent; understand the code patterns of run, tool, and handoff. | Current docs |
| [MCP Apps compatibility in ChatGPT](https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt) | OpenAI | MCP; Apps SDK; UI | Understand MCP Apps UI standards, iframe/bridge, and compatibility between ChatGPT and other hosts. | Current docs |
| [Use Codex with the Agents SDK](https://developers.openai.com/codex/guides/agents-sdk) | OpenAI | MCP; Codex; Agents SDK | Use Codex as an MCP server for other agents to call; ideal for multi-agent dev workflows. | Current docs |
| [Agent approvals and security - Codex](https://developers.openai.com/codex/agent-approvals-security) | OpenAI | Safety; Approvals; Codex | Official reference for Codex approval modes, sandbox, network access; read alongside OpenAI/Anthropic safety articles. | Current docs |
| [Agent Skills - Codex](https://developers.openai.com/codex/skills) | OpenAI | Codex; Skills; Plugins | Skills/Plugins as reusable workflow packages; compare with Anthropic Agent Skills. | Current docs |
| [Custom instructions with AGENTS.md - Codex](https://developers.openai.com/codex/guides/agents-md) | OpenAI | AGENTS.md; Context | How AGENTS.md provides persistent project specifications for agents; establish repo-level agent contracts. | Current docs |
| [Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) | OpenAI | Observability; MCP; Tracing | Tracing, MCP integration, provider/observability; essential for production agent debugging. | Current docs |
| [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) | OpenAI | MCP; Security; Private tools | Securely expose private/intranet MCP servers to supported OpenAI surfaces; ideal for enterprise deployment. | Current docs |

</details>

---

### P2 — Optional Context (14 articles)

<details>
<summary>Click to expand P2 reading list</summary>

| Title | Vendor | Topic | Key Idea | Date |
|-------|--------|-------|----------|------|
| [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | Anthropic | Context; Retrieval; RAG | Not agent-specific, but important for agent RAG/context: prepend context to chunks before retrieval to improve recall. | 2024-09-19 |
| [Developing a computer use model](https://www.anthropic.com/news/developing-computer-use) | Anthropic | Computer use; Agents | More technical explanation of how the computer-use model moves the mouse, clicks, types, and reads screen feedback. | 2024-10-22 |
| [Introducing Claude 4](https://www.anthropic.com/news/claude-4) | Anthropic | Agents; Coding; Long-running | Overview of Claude Opus/Sonnet 4 capabilities: coding, advanced reasoning, agent workflows. | 2025-05-22 |
| [Claude for Financial Services](https://www.anthropic.com/news/claude-for-financial-services) | Anthropic | Agents; Connectors; Finance | Vertical industry agent/connector productization case; understand data, permissions, and tool integration in finance. | 2025-07-15 |
| [Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services) | Anthropic | Agents; Skills; Finance | Claude for Excel, real-time data connectors, pre-built Agent Skills for vertical industry productization. | 2025-10-27 |
| [Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) | OpenAI | Agents; Coding model; Evals | Codex-native model and long-running coding/terminal/agentic benchmarks; understand how model capabilities serve the harness. | 2026-02-05 |
| [Introducing OpenAI Frontier](https://openai.com/index/introducing-openai-frontier/) | OpenAI | Agents; Enterprise; Governance | Enterprise AI coworker/agent platform: shared context, onboarding, permissions, guardrails, governance. | 2026-02-10 |
| [Introducing Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) | Anthropic | Agents; Planning; Computer use | Sonnet 4.6 emphasizes coding, computer use, long-context reasoning, agent planning. | 2026-02-17 |
| [Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) | Anthropic | Agents; Long-running; Tool use | Model release perspective on long-running tasks, agentic harness, subagents, and tool call capabilities. | 2026-02-25 |
| [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) | Anthropic | Agents; Long-running; Coding | Stronger software engineering and long-running task performance; track how model capabilities impact agent workloads. | 2026-04-16 |
| [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) | Anthropic | Reliability; Claude Code; Agent SDK | Postmortem on Claude Code/Agent SDK quality regression; learn agent product operations and regression control. | 2026-04-23 |
| [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) | Anthropic | Agents; Dynamic workflows; Long-running | Dynamic workflows, hundreds of parallel subagents, long-running agentic tasks — latest model/product direction. | 2026-05-28 |
| [Codex for every role, tool, and workflow](https://openai.com/index/codex-for-every-role-tool-workflow/) | OpenAI | Agents; Codex; Plugins | Codex expands from development to knowledge work: role-specific plugins, Sites, annotations, parallel workflows. | 2026-06-02 |
| [Codex is becoming a productivity tool for everyone](https://openai.com/index/codex-for-knowledge-work/) | OpenAI | Agents; Knowledge work | Usage data shows how non-developers use Codex for reports, spreadsheets, research, automation, and lightweight tools. | 2026-06-02 |
| [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | OpenAI | MCP; Docs; Context | Official OpenAI docs MCP server; connect docs directly to local agents/IDEs. | Current docs |
| [Codex SDK](https://developers.openai.com/codex/sdk) | OpenAI | Codex SDK; Automation | Programmatically control Codex in CI/CD or internal tools; embed coding agents into existing workflows. | Current docs |

</details>

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

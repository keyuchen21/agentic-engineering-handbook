# Agentic Engineering Handbook

> The definitive OpenAI, Claude, MCP, Harness, Evals, and Production Agent Systems learning roadmap.

[![Stars](https://img.shields.io/github/stars/your-username/agentic-engineering-handbook?style=social)](https://github.com/your-username/agentic-engineering-handbook)
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

做一个客服/工单 triage agent：router → specialist → evaluator，所有输出用 schema 约束。

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

写一个只读 repo/docs MCP server，再做一个 eval 检查 agent 是否能正确引用文档。

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

把同一任务做成 Skill/Plugin，并测量无 skill、长 prompt、skill 版本的准确率和 token cost。

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

实现一个 mini coding harness：计划文件、shell tool、apply patch、test gate、事件日志、resume。

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

同一 repo 上分别跑 OpenAI/Codex 和 Claude Code 风格流程：issue → plan → patch → tests → PR summary。

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

为你的 agent 建一套 smoke/macro eval：任务成功率、tool misuse、prompt injection、latency、cost、human approval 次数。

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
| 1 | [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | OpenAI | Agents; MCP; Platform | 年度总览：Responses API、Agents SDK、AgentKit、Codex、MCP、Apps SDK、AGENTS.md 的体系化梳理。 | 2025-12-30 |
| 2 | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | OpenAI | Agents; Responses API; Tools | OpenAI agents 平台的关键起点：Responses API、内置 web/file/computer tools、Agents SDK、tracing/observability。 | 2025-03-11 |
| 3 | [Introducing AgentKit](https://openai.com/index/introducing-agentkit/) | OpenAI | Agents; Evals; AgentKit | AgentKit、expanded evals、agent RFT：从 prototype 到 production 的官方 agent 工具链。 | 2025-10-06 |
| 4 | [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) | OpenAI | Agents; SDK | 官方 SDK 起点：agent、tool、handoff、guardrail、tracing 的概念与适用边界。 | Current docs |
| 5 | [Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) | OpenAI | Agents; Handoffs; Orchestration | 经典入门：routines、handoffs、tool calling 如何组合成可控多流程 agent。 | 2024-10-10 |
| 6 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic | MCP; Standards | MCP 原点文章：把 AI assistant 连接到数据、工具和系统的开放标准。 | 2024-11-25 |
| 7 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic | Agents; Patterns; Frameworks | agent 入门必读：workflow vs agent、prompt/tool/retrieval、orchestrator-worker、evaluator-optimizer 等模式。 | 2024-12-19 |
| 8 | [New tools and features in the Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/) | OpenAI | MCP; Responses API; Tools | Responses API 扩展到远程 MCP server、image/code/file 等工具；适合看 OpenAI 如何把 MCP 接入运行时。 | 2025-05-21 |
| 9 | [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | OpenAI | MCP; Connectors; Responses API | OpenAI 对远程 MCP server 与 connectors 的官方接入指南；含 approvals、安全注意事项。 | Current docs |
| 10 | [Building MCP servers for ChatGPT Apps and API integrations](https://developers.openai.com/api/docs/mcp) | OpenAI | MCP; ChatGPT Apps; API | 写 MCP server 的官方指南：给 ChatGPT Apps、deep research、API integrations 供 tool/knowledge。 | Current docs |
| 11 | [Building a Deep Research MCP Server](https://developers.openai.com/cookbook/examples/deep_research_api/how_to_build_a_deep_research_mcp_server/readme) | OpenAI | MCP; Deep research | Deep Research 所需 search/fetch MCP server 的最小实现。 | 2025-06-25 |
| 11 | [Model Context Protocol - Codex](https://developers.openai.com/codex/mcp) | OpenAI | MCP; Codex | Codex CLI/IDE 如何连接 MCP servers，给 agent 增加 Figma、browser、docs、内部工具等上下文。 | Current docs |
| 12 | [Introducing Codex](https://openai.com/index/introducing-codex/) | OpenAI | Agents; Coding; Sandbox | 云端软件工程 agent：并行任务、repo sandbox、运行测试/linters/type checkers、产出可审计证据。 | 2025-05-16 |
| 13 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI | Harness; Agent loop; Codex | Codex CLI 如何把 prompt、tool schema、MCP tools、Responses API、context 管理串成 agent loop。 | 2026-01-23 |
| 14 | [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | OpenAI | Harness; Codex App Server; JSON-RPC | 非常核心的 harness 文章：Codex core、App Server、JSON-RPC、streaming progress、approval、diff、thread 管理。 | 2026-02-04 |
| 15 | [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/) | OpenAI | Harness; Responses API; Sandbox | Responses API + shell tool + hosted containers 组成 agent runtime；适合理解从模型到 agent 的运行环境。 | 2026-03-10 |
| 16 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | OpenAI | Harness; Agent-first engineering | 把产品代码、测试、CI、docs、observability 都面向 agent 可读/可执行来设计；适合学习 agent-first repo 组织。 | 2026-02-11 |
| 17 | [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | OpenAI | Harness; Agents SDK; MCP; Skills | Agents SDK harness 变得更完整：memory、sandbox orchestration、Codex-like filesystem tools、MCP、skills、AGENTS.md。 | 2026-04-15 |
| 18 | [Building Consistent Workflows with Codex CLI & Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) | OpenAI | MCP; Codex; Agents SDK | Codex CLI 作为 MCP server 接入 Agents SDK；实际多 agent dev workflow。 | 2025-10-01 |
| 19 | [Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction) | OpenAI | Memory; Compaction; Reliability | 长上下文/多轮 agent 的 memory 与 compaction 设计。 | 2026-05-01 |
| 20 | [Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | OpenAI | Evals; Traces; Self-improvement | 将 traces、evals、Codex 修复连成 agent improvement loop。 | 2026-05-12 |
| 21 | [Eval Driven System Design - From Prototype to Production](https://developers.openai.com/cookbook/topic/evals) | OpenAI | Evals; Production | 把 eval 作为系统设计驱动力，适合把 agent 从 demo 推向 production。 | 2025-06-02 |
| 22 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI | Evals; Skills; Agents | 用 evals 系统化测试 agent skills；适合建立 skill 发布前的质量门槛。 | 2026-01-22 |
| 23 | [Evals API Use-case - MCP Evaluation](https://developers.openai.com/cookbook/examples/evaluation/use-cases/mcp_eval_notebook) | OpenAI | MCP; Evals | 专门评估带 MCP tool 的问答/检索能力；适合搭 MCP regression suite。 | 2025-06-09 |
| 24 | [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | OpenAI | Safety; Sandbox; Codex | OpenAI 内部如何运行 Codex：sandbox、approvals、network policy、agent-native telemetry。 | 2026-05-20 |
| 25 | [Building Governed AI Agents - A Practical Guide to Agentic Scaffolding](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Governance; Guardrails; Agents | 治理型 agent scaffolding：权限、guardrails、审计、组织规范。 | 2026-02-23 |
| 26 | [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; Agentic systems | 从 end-to-end/macro 层面评估 agent，而不是只看单步输出。 | 2026-05-19 |
| 27 | [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic | Coding agents; Claude Code | Claude Code 使用方法论：verification loop、explore-plan-code、CLAUDE.md、permissions、MCP、subagents、context 管理。 | 2025-04-18 |
| 28 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic | Agents; Multi-agent; Research | Claude Research 多 agent 架构：planner + parallel research agents + synthesis；生产 multi-agent 经验。 | 2025-06-13 |
| 29 | [Writing effective tools for AI agents - with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic | Tools; MCP; Evals | 工具质量决定 agent 质量：tool description、context budget、eval、让 Claude 优化自己的工具。 | 2025-09-11 |
| 30 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic | Context; Agents | context 是 agent 的核心资源：选择、压缩、隔离、持久化与上下文污染控制。 | 2025-09-29 |
| 31 | [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) | Anthropic | Claude Code; Agent SDK; Subagents | Claude Agent SDK、subagents、hooks、background tasks、checkpoints 等自主 coding agent 能力。 | 2025-09-29 |
| 32 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Anthropic | Skills; Agents | Agent Skills 作为模块化能力包：instructions、resources、scripts，降低上下文负担并提升可靠性。 | 2025-10-16 |
| 33 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic | MCP; Code execution; Context | MCP scale 问题的关键文章：用 code execution/on-demand tools 把 token overhead 降低，学习 progressive disclosure。 | 2025-11-04 |
| 34 | [Introducing advanced tool use on Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic | Tools; MCP; Advanced tool use | tool search、deferred loading、programmatic tool calling；解决大量 MCP tools 带来的上下文污染。 | 2025-11-24 |
| 35 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic | Harness; Long-running agents | harness 核心必读：跨多个上下文窗口工作、任务记录、外部状态、agent 自我恢复。 | 2025-11-26 |
| 36 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic | Evals; Agents | agent eval 比静态 eval 更复杂：多轮、工具、状态改变、creative solution、failure taxonomy。 | 2026-01-09 |
| 37 | [Measuring AI agent autonomy in practice](https://www.anthropic.com/news/measuring-agent-autonomy) | Anthropic | Agents; Autonomy; Measurement | 把 agent autonomy 用任务持续时间/监督需求等指标量化；适合建 autonomy benchmark。 | 2026-02-18 |
| 38 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic | Harness; Application development | 把长程 app development 任务交给 agent 的 harness 设计模式；和 OpenAI Codex harness 对照。 | 2026-03-24 |
| 39 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Anthropic | Managed agents; Harness | 把模型 brain 与执行 hands/harness 解耦，让接口在 harness 变化时保持稳定。 | 2026-04-08 |
| 40 | [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | Anthropic | Safety; Containment; Agents | 强 agent 发布的 blast radius、human-in-the-loop、containment 策略。 | 2026-05-25 |

---

### P1 — Highly Useful (49 articles)

<details>
<summary>Click to expand P1 reading list</summary>

| Title | Vendor | Topic | Key Idea | Date |
|-------|--------|-------|----------|------|
| [Structured Outputs for Multi-Agent Systems](https://developers.openai.com/cookbook/examples/structured_outputs_multi_agent) | OpenAI | Agents; Multi-agent; Structured outputs | 用 strict schema 约束多 agent 间的结构化消息与 handoff。 | 2024-08-06 |
| [Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku](https://www.anthropic.com/news/3-5-models-and-computer-use) | Anthropic | Agents; Computer use | Claude computer use beta 起点：模型通过截图和动作使用电脑。 | 2024-10-22 |
| [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) | Anthropic | Agents; Coding; Evals | SWE-bench agent scaffolding 文章：同一模型性能强依赖 harness/scaffolding。 | 2025-01-06 |
| [Introducing Operator](https://openai.com/index/introducing-operator/) | OpenAI | Agents; Computer use; Safety | 浏览器型 agent 的早期产品形态：让模型在网页上点击、输入、执行任务，并强调用户确认与安全边界。 | 2025-01-23 |
| [Computer-Using Agent](https://openai.com/index/computer-using-agent/) | OpenAI | Agents; Computer use | 理解 CUA 如何把视觉、鼠标/键盘动作、环境反馈组成 agent loop；适合和 Claude computer use 对照学习。 | 2025-01-23 |
| [Claude 3.7 Sonnet and Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet) | Anthropic | Agents; Coding; Claude Code | Claude Code 的早期发布，标志 Claude 进入 agentic coding 工具形态。 | 2025-02-24 |
| [The think tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) | Anthropic | Tools; Reasoning; Agents | 在复杂 tool-use chain 中给模型一个显式 think tool；学习 policy-heavy/多步决策的工具设计。 | 2025-03-20 |
| [Evaluating Agents with Langfuse](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; Agents | 用 Langfuse 观测和评估 Agents SDK 运行，学习 tracing/eval workflow。 | 2025-03-31 |
| [Parallel Agents with the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/parallel_agents) | OpenAI | Agents; Parallelism; Agents SDK | 并行 agent 模式：拆任务、并行执行、聚合结果。 | 2025-05-01 |
| [Multi-Agent Portfolio Collaboration with OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration) | OpenAI | Agents; Multi-agent; Portfolio | 多 agent 协作的业务场景样例：研究、分析、组合输出。 | 2025-05-28 |
| [MCP-Powered Agentic Voice Framework](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Voice; Agents | 语音 agent + MCP 的范式：实时交互、工具扩展、任务执行。 | 2025-06-17 |
| [Deep Research API with the Agents SDK](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Deep research; Agents SDK | 把 Deep Research API 放进 Agents SDK workflow。 | 2025-06-25 |
| [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) | Anthropic | MCP; Claude Desktop; Packaging | 把本地 MCP server 打包成一键安装扩展；学习 MCP 分发/安装/本地权限问题。 | 2025-06-26 |
| [Building a Supply-Chain Copilot with OpenAI Agent SDK and Databricks MCP Servers](https://developers.openai.com/cookbook/topic/agents) | OpenAI | MCP; Agents; Databricks | 企业数据平台 MCP + Agent SDK 的业务 agent 样例。 | 2025-07-08 |
| [Introducing ChatGPT agent: bridging research and action](https://openai.com/index/introducing-chatgpt-agent/) | OpenAI | Agents; ChatGPT; Computer use | 面向终端用户的 ChatGPT agent：研究、浏览器、电脑操作、文件/幻灯片等能力组合。 | 2025-07-17 |
| [ChatGPT agent System Card](https://openai.com/index/chatgpt-agent-system-card/) | OpenAI | Agents; Safety; Evals | 学习 agent 产品上线前的风险分类、评测、权限、人类确认与滥用防护。 | 2025-07-17 |
| [Context Engineering - Short-Term Memory Management with Sessions](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Sessions; Agents | 短期记忆/会话状态如何影响 agent 可靠性。 | 2025-09-09 |
| [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) | OpenAI | Agents; Coding; IDE | Codex 从研究预览走向日常开发工具：CLI、IDE、web/mobile 协作与更独立的任务执行。 | 2025-09-15 |
| [Introducing Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) | Anthropic | Agents; Claude Agent SDK; Computer use | Sonnet 4.5 强调 coding、complex agents、computer use，并同步推出 Agent SDK。 | 2025-09-29 |
| [Introducing apps in ChatGPT and the new Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/) | OpenAI | MCP; Apps; ChatGPT | Apps SDK 基于 MCP 扩展 UI 与 tool server，是理解 ChatGPT app / MCP app 生态的入口。 | 2025-10-06 |
| [Codex is now generally available](https://openai.com/index/codex-now-generally-available/) | OpenAI | Agents; Coding; Codex SDK | Codex GA、Slack integration、Codex SDK、admin tools；看 coding agent 如何进入企业管理面。 | 2025-10-06 |
| [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Codex; Long-running; Planning | 长程 coding agent 的计划文件与跨上下文任务管理。 | 2025-10-07 |
| [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/beyond-permission-prompts) | Anthropic | Safety; Permissions; Claude Code | 从简单权限弹窗到更细粒度安全策略，降低自主模式风险与打扰。 | 2025-10-20 |
| [Introducing Aardvark: OpenAI's agentic security researcher](https://openai.com/index/introducing-aardvark/) | OpenAI | Agents; Security | 安全领域的 agent 形态：持续扫描、验证问题、提出修复；后来整合为 Codex Security。 | 2025-10-30 |
| [Build a coding agent with GPT 5.1](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Coding | 从零构建 coding agent，理解文件编辑、命令执行、循环与验证。 | 2025-11-13 |
| [OpenAI co-founds Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) | OpenAI | MCP; Standards; AGENTS.md | MCP、AGENTS.md、agent standards 进入 Linux Foundation/AAIF 语境；适合理解生态标准化。 | 2025-12-09 |
| [Donating MCP and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | Anthropic | MCP; Standards; AAIF | Anthropic 把 MCP 捐给 Linux Foundation/AAIF；和 OpenAI 的 AAIF 文章一起读。 | 2025-12-09 |
| [Context Engineering for Personalization - Long-Term Memory Notes](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Context; Long-term memory; Agents | 长期记忆如何作为 agent personalization/state 管理。 | 2026-01-05 |
| [Supercharging Codex with JetBrains MCP at Skyscanner](https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp) | OpenAI | MCP; Codex; IDE | 真实 IDE/MCP case study：Codex CLI 如何通过 JetBrains MCP 拿到 IDE 上下文与开发工具。 | 2026-01-11 |
| [Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | Anthropic | Evals; Technical hiring | 技术评估如何被强 agent 持续攻破；适合思考 benchmark 防污染与评测设计。 | 2026-01-21 |
| [Inside OpenAI's in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/) | OpenAI | Agents; Data; Memory | 内部数据 agent 案例：memory、Codex、数据上下文、可靠性，适合学习企业内知识/数据 agent。 | 2026-01-29 |
| [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) | OpenAI | Agents; Coding; Multi-agent | 桌面 command center for agents：多线程/并行长任务、项目级 agent 工作流。 | 2026-02-02 |
| [Apple's Xcode now supports Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | Anthropic | Claude Agent SDK; Xcode; MCP | 把 Claude Agent SDK 嵌进 Xcode：harness、subagents、background tasks、plugins、MCP。 | 2026-02-03 |
| [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | Anthropic | Evals; Coding agents; Infrastructure | agentic coding eval 里环境配置会显著影响分数；生产/benchmark 都要控制基础设施噪声。 | 2026-02-05 |
| [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | Anthropic | Multi-agent; Coding; Long-running | 并行 Claude 团队完成大型工程任务；学习多 agent 分工、协调和长程执行。 | 2026-02-05 |
| [Codex Security: now in research preview](https://openai.com/index/codex-security-now-in-research-preview/) | OpenAI | Agents; Security; Codex | agentic security researcher 的产品化：漏洞发现、验证、修复建议、降低 triage noise。 | 2026-03-06 |
| [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering) | Anthropic | Evals; Agent awareness | 模型识别/适应评测的风险；适合 agent benchmark 可信度讨论。 | 2026-03-06 |
| [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) | Anthropic | Safety; Permissions; Autonomy | Claude Code auto mode 的风险分类、allow/block rules、异常处理与安全测试。 | 2026-03-25 |
| [Migrate a Legacy Codebase with Sandbox Agents](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Agents; Sandbox; Evals | sandbox agent 在大型 legacy code 迁移中的评测和执行模式。 | 2026-04-07 |
| [Codex for (almost) everything](https://openai.com/index/codex-for-almost-everything/) | OpenAI | Agents; Codex; MCP; Plugins | Codex app 扩展到 Windows/macOS、computer use、in-app browser、memory、plugins、MCP servers。 | 2026-04-16 |
| [Computer Use Agents in Daytona Sandboxes](https://developers.openai.com/cookbook/examples/agents_sdk/computer_use_with_daytona/computer_use_with_daytona) | OpenAI | Computer use; Sandbox; Agents | 电脑使用型 agent 与 sandbox runtime；适合和 Operator/CUA/Claude computer use 对照。 | 2026-04-19 |
| [Introducing workspace agents in ChatGPT](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) | OpenAI | Agents; Workspace; Governance | workspace agents：共享 agent、权限、工具、memory、safeguards；适合团队协作 agent 设计。 | 2026-04-22 |
| [Building workspace agents in ChatGPT to complete repeatable, end-to-end work](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Workspace agents; ChatGPT | 面向团队可重复端到端工作流的 workspace agent 实战。 | 2026-04-22 |
| [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/) | OpenAI | Agents; Latency; Responses API | 把 agentic rollout 作为长连接/长任务来优化延迟；适合学习生产 agent 的 transport 与 caching。 | 2026-05-01 |
| [Agents for financial services](https://www.anthropic.com/news/finance-agents) | Anthropic | Agents; Finance; MCP | 十个 ready-to-run agent templates、Claude Code/Cowork plugins、Managed Agents cookbooks、MCP app。 | 2026-05-05 |
| [Migrate from the Claude Agent SDK to the OpenAI Agents SDK](https://developers.openai.com/cookbook/examples/agents_sdk/migrate-from-claude-agent-sdk/readme) | OpenAI | Agents SDK; Migration | 对比 Claude Agent SDK 与 OpenAI Agents SDK 的迁移视角；适合双栈学习。 | 2026-05-07 |
| [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/) | OpenAI | Safety; Sandbox; Codex | Windows 上的 coding agent sandbox 设计：文件访问、网络限制、approval tradeoff。 | 2026-05-13 |
| [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) | OpenAI | Agents; Evals; Self-improvement | 把生产 traces、专家反馈、Codex loop、eval infrastructure 融成自改进业务 agent。 | 2026-05-27 |
| [SchemaFlow: Agentic Database Change Impact Analysis, SQL Generation, and Eval Guardrails](https://developers.openai.com/cookbook/topic/agents) | OpenAI | Evals; SQL; Agent guardrails | 数据/SQL agent 的 guardrails 和 eval guardrails 示例。 | 2026-06-05 |
| [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart) | OpenAI | Agents; SDK | 快速搭一个最小 agent，理解 run、tool、handoff 的代码形态。 | Current docs |
| [MCP Apps compatibility in ChatGPT](https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt) | OpenAI | MCP; Apps SDK; UI | 理解 MCP Apps UI 标准、iframe/bridge、ChatGPT 与其他 host 的兼容方式。 | Current docs |
| [Use Codex with the Agents SDK](https://developers.openai.com/codex/guides/agents-sdk) | OpenAI | MCP; Codex; Agents SDK | 把 Codex 作为 MCP server 供其他 agent 调用；适合多 agent 开发工作流。 | Current docs |
| [Agent approvals and security - Codex](https://developers.openai.com/codex/agent-approvals-security) | OpenAI | Safety; Approvals; Codex | Codex approval modes、sandbox、network access 的官方参考；和 OpenAI/Anthropic safety 文章一起读。 | Current docs |
| [Agent Skills - Codex](https://developers.openai.com/codex/skills) | OpenAI | Codex; Skills; Plugins | Skill/Plugin 作为可复用 workflow 包；和 Anthropic Agent Skills 对照。 | Current docs |
| [Custom instructions with AGENTS.md - Codex](https://developers.openai.com/codex/guides/agents-md) | OpenAI | AGENTS.md; Context | AGENTS.md 如何给 agent 持久项目规范；适合建立 repo-level agent contract。 | Current docs |
| [Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) | OpenAI | Observability; MCP; Tracing | Tracing、MCP integration、provider/observability；生产 agent 调试必看。 | Current docs |
| [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) | OpenAI | MCP; Security; Private tools | 把私有/内网 MCP server 安全暴露给支持的 OpenAI surface；适合企业落地。 | Current docs |

</details>

---

### P2 — Optional Context (14 articles)

<details>
<summary>Click to expand P2 reading list</summary>

| Title | Vendor | Topic | Key Idea | Date |
|-------|--------|-------|----------|------|
| [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | Anthropic | Context; Retrieval; RAG | 虽然不是 agent 专文，但对 agent RAG/context 很重要：检索前给 chunk 加上下文以提升召回。 | 2024-09-19 |
| [Developing a computer use model](https://www.anthropic.com/news/developing-computer-use) | Anthropic | Computer use; Agents | 更技术化地解释 computer-use model 如何移动鼠标、点击、输入、读取屏幕反馈。 | 2024-10-22 |
| [Introducing Claude 4](https://www.anthropic.com/news/claude-4) | Anthropic | Agents; Coding; Long-running | Claude Opus/Sonnet 4 的 coding、advanced reasoning、agent workflows 能力总览。 | 2025-05-22 |
| [Claude for Financial Services](https://www.anthropic.com/news/claude-for-financial-services) | Anthropic | Agents; Connectors; Finance | 垂直行业 agent/connector 产品化案例；了解金融场景里数据、权限、工具整合。 | 2025-07-15 |
| [Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services) | Anthropic | Agents; Skills; Finance | Claude for Excel、实时数据 connectors、预置 Agent Skills 的垂直场景产品化。 | 2025-10-27 |
| [Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) | OpenAI | Agents; Coding model; Evals | Codex-native 模型与长程 coding/terminal/agentic benchmarks；可了解模型能力如何服务 harness。 | 2026-02-05 |
| [Introducing OpenAI Frontier](https://openai.com/index/introducing-openai-frontier/) | OpenAI | Agents; Enterprise; Governance | 企业 AI coworker/agent 平台：共享上下文、onboarding、权限、guardrails、治理。 | 2026-02-10 |
| [Introducing Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) | Anthropic | Agents; Planning; Computer use | Sonnet 4.6 强调 coding、computer use、long-context reasoning、agent planning。 | 2026-02-17 |
| [Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) | Anthropic | Agents; Long-running; Tool use | 长程任务、agentic harness、subagents 和 tool calls 能力的模型发布视角。 | 2026-02-25 |
| [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) | Anthropic | Agents; Long-running; Coding | 更强的软件工程与长程任务表现；适合关注模型能力对 agent workload 的影响。 | 2026-04-16 |
| [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) | Anthropic | Reliability; Claude Code; Agent SDK | Claude Code/Agent SDK 质量回归的 postmortem，适合学习 agent 产品运维与回归控制。 | 2026-04-23 |
| [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) | Anthropic | Agents; Dynamic workflows; Long-running | 动态工作流、数百并行 subagents、长程 agentic tasks 的最新模型/产品方向。 | 2026-05-28 |
| [Codex for every role, tool, and workflow](https://openai.com/index/codex-for-every-role-tool-workflow/) | OpenAI | Agents; Codex; Plugins | Codex 从开发扩展到知识工作：role-specific plugins、Sites、annotations、并行工作流。 | 2026-06-02 |
| [Codex is becoming a productivity tool for everyone](https://openai.com/index/codex-for-knowledge-work/) | OpenAI | Agents; Knowledge work | 从使用数据看非开发者如何把 Codex 用于报告、表格、研究、自动化和轻量工具。 | 2026-06-02 |
| [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | OpenAI | MCP; Docs; Context | OpenAI 官方文档 MCP server；适合把 docs 直接接进本地 agent/IDE。 | Current docs |
| [Codex SDK](https://developers.openai.com/codex/sdk) | OpenAI | Codex SDK; Automation | 在 CI/CD 或内部工具中程序化控制 Codex；适合把 coding agent 嵌入现有工作流。 | Current docs |

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

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/agentic-engineering-handbook&type=Date)](https://star-history.com/#your-username/agentic-engineering-handbook&Date)

---

## License

[MIT](LICENSE)

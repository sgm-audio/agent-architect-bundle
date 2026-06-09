---
name: 12-factor-agents
description: "12-factor agent methodology: 12 principles for building reliable LLM applications. Covers natural language to tool calls, owning prompts/context, tools as structured outputs, unified state, launch/pause/resume, human-in-the-loop via tool calls, explicit control flow, compacting errors into context, small focused agents, triggering from anywhere, and stateless reducer patterns. Use when designing agent architectures, reviewing agent system designs, or building production-grade LLM applications."
metadata:
  source: "https://github.com/humanlayer/12-factor-agents"
  version: "1.0"
  related_skills:
    - coding
    - ai-agent-multi-agent-orchestration-langgraph-autogen
---

# 12-Factor Agent Methodology

Principles for building production-grade LLM applications. Based on [12-factor agents](https://github.com/humanlayer/12-factor-agents).

## The 12 Factors

| # | Factor | Core Idea |
|---|--------|-----------|
| 1 | **NL → Tool Calls** | Natural language input maps to structured tool calls, not free-form generation |
| 2 | **Own Your Prompts** | System prompts live in your codebase, not buried in a framework |
| 3 | **Own Your Context Window** | Explicitly control what goes in/out of context; don't just accumulate |
| 4 | **Tools Are Structured Outputs** | Tool returns are typed schemas (Zod, Pydantic, BAML), not unstructured text |
| 5 | **Unify Execution & Business State** | One state object tracks both the agent's progress and the domain data |
| 6 | **Launch/Pause/Resume** | Workflows are pausable/resumable via simple APIs (not in-memory only) |
| 7 | **Contact Humans with Tool Calls** | Human-in-the-loop is a first-class tool call, not a side-channel |
| 8 | **Own Your Control Flow** | Routing between agents is explicit code (DAG, graph), not buried in prompts |
| 9 | **Compact Errors Into Context** | Errors are summarized and fed back into context for self-correction |
| 10 | **Small, Focused Agents** | Each agent does one thing well; compose them like microservices |
| 11 | **Trigger From Anywhere** | API, CLI, webhook, cron, events — not just chat |
| 12 | **Stateless Reducer** | Each agent returns a diff/partial state; no shared mutable state |

## Design Questions

When reviewing an agent system, ask:

- Are tool outputs typed schemas or free text? (Factor 4)
- Is state persisted across restarts? (Factor 6)
- Is the routing graph visible in code, or hidden in prompts? (Factor 8)
- Does each agent have a single clear responsibility? (Factor 10)
- Are human handoffs done via tool calls, not callbacks? (Factor 7)
- Can you pause mid-workflow and resume later? (Factor 6)
- Are errors compacted and fed back, or just logged? (Factor 9)

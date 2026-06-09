---
name: ai-agent-multi-agent-orchestration-langgraph-autogen
description: >-
  Use this skill when the user is working on or asking about LangGraph, AutoGen, multi-agent systems, agent orchestration, or building workflows with multiple AI agents.
version: 1.0.0
---

# Skill: AI Agent Multi-Agent Orchestration (LangGraph/AutoGen)
## 📖 1. Overview
Architects multi-agent workflows where specialized AI agents collaborate (MIDI gen → DSP patch → mix critique) for automated music production.
## ⚙️ 2. Core Functionality
- Agent Roles: Composer, Sound Designer, Mixing Engineer
- Workflow Graph: State machines with conditional routing
- Tool Integration: MIDI export, plugin control, audio analysis
- Conflict Resolution: Consensus voting, human-in-the-loop override
## 📥📤 3. Input/Output Schema
| Inputs | User brief, agent prompts, tool APIs, state graph | Outputs | Final audio/MIDI, workflow logs, agent critiques |
## 🏗️ 4. Architecture
LangGraph state machine: `composer.generate() → sound_designer.patch() → mixer.critique() → loop if score < threshold`. Async execution.
## 🔗 5. Dependencies
`langgraph`, `autogen`, `llama.cpp`, custom DSP tools
## ⚠️ 6. Edge Cases
| Agent Loop | Infinite refinement | Max iteration cap, early stop |
| Conflicting Goals | Muddy mix | Weighted scoring, prioritize human feedback |
| Tool Failure | Deadlock | Timeout, fallback to default patch |
## 🛡️ 7. Constraints
- Latency: < 5s per graph step
- Cost: < $0.50/run (cloud) or < 10% CPU (local)
- Safety: User approval before export
## 🤖 8. Usage
- *Prompt:* "Design a LangGraph workflow for automated track generation with composer, patcher, and mixer agents, including human approval gate."
## 🧪 9. Testing
- Loop detection validation
- Tool call accuracy
- Output quality vs human baseline
## 📝 10. Best Practices
- Log agent reasoning for transparency
- Implement retry with backoff
- Keep state serializable for resume
*Skill Version: 1.0.0 | Standards: LangGraph, AutoGen, State Machines | Domain: Audio AI & ML*
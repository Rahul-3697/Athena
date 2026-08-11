# Project Athena

> A modular AI agent framework designed to explore, build, and understand the foundations of modern agentic AI systems.

## Vision

Project Athena is an evolving AI Agent Framework built with a strong focus on **modularity, explicit execution flow, typed contracts, and reusable AI capabilities**.

The goal is not to simply wrap an existing agent framework.

Athena is being developed as a learning-driven engineering platform where concepts such as:

- Agents
- Workflows
- Skills
- Context
- LLM abstraction
- Structured outputs
- Tools
- Memory
- Routing
- LangGraph

can be understood, implemented, and composed incrementally.

The framework currently starts with a simple research-oriented agent and will progressively evolve toward a general-purpose agent engineering platform.

---

# Current Version

**v1.1 — Foundation & Intelligence Layer**

Current capabilities:

- Agent abstraction
- Workflow execution
- Shared Context
- Skill abstraction
- Typed dataclass contracts
- Prompt layer
- LLM abstraction
- OpenAI integration
- Structured execution plans
- LLM response parsing
- Report generation

---

# Architecture

```text
                         User Goal
                            │
                            ▼
                         Agent
                            │
                            ▼
                         Workflow
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
           PlannerSkill        ReportGeneratorSkill
                 │                     ▲
                 ▼                     │
              Prompt                   │
                 │                     │
                 ▼                     │
                LLM                    │
                 │                     │
                 ▼                     │
              Parser                   │
                 │                     │
                 ▼                     │
          ExecutionPlan ───────────────┘
                 │
                 ▼
               Context
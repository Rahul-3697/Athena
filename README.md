# 🦉 Athena

> **A modular AI engineering framework for building intelligent agents using reusable skills, workflows, and modern AI frameworks.**

Athena is an open-source AI engineering framework designed to simplify the development of intelligent applications by combining a clean architecture with the latest AI ecosystem.

Rather than replacing frameworks like LangGraph or LangChain, Athena provides a consistent developer experience while allowing different AI technologies to be integrated underneath.

---

# 🚀 Vision

The AI ecosystem evolves rapidly.

New frameworks, tools, and models appear every few months.

Athena provides a stable architecture that allows developers to learn, experiment, and build production-ready AI agents without rewriting their applications whenever the ecosystem changes.

---

# 🏗 Architecture

```
                User
                  │
                  ▼
               Agent
                  │
                  ▼
              Workflow
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
     Planner Skill      Search Skill
        ▼                   ▼
     Writer Skill      Report Skill
                  │
                  ▼
               Context
```

Every Skill performs one responsibility.

The Workflow orchestrates the Skills.

The Agent orchestrates the Workflow.

The Context becomes the shared knowledge between every Skill.

---

# 📂 Repository Structure

```
athena/
│
├── agent/             # Agent orchestration
├── context/           # Shared execution context
├── contracts/         # Common contracts & interfaces
├── core/              # Runtime & execution engine
├── prompts/           # Prompt templates
├── skills/            # Reusable AI Skills
├── tools/             # External tools & integrations
├── workflow/          # Workflow orchestration
│
└── __init__.py
```

---

# 🎯 Core Concepts

## Agent

The public entry point of Athena.

An Agent receives a user request, creates a Context, executes a Workflow, and returns the final result.

---

## Workflow

A Workflow is an ordered collection of Skills.

```python
workflow = (
    Workflow("Research")
        .add(PlannerSkill())
        .add(SearchSkill())
        .add(ReportGeneratorSkill())
)
```

---

## Skills

Skills are reusable execution units.

Each Skill performs one responsibility.

Examples:

- PlannerSkill
- SearchSkill
- ReportGeneratorSkill
- SQLSkill
- BrowserSkill
- VisionSkill

---

## Context

Context represents the shared knowledge of the running workflow.

Every Skill receives the same Context.

```python
context.set("goal", goal)

plan = context.get("plan")
```

---

# ⚡ Quick Example

```python
from athena.agent.agent import Agent
from athena.workflow.workflow import Workflow

from athena.skills.planner_skill import PlannerSkill
from athena.skills.report_generator_skill import ReportGeneratorSkill

workflow = (
    Workflow("Research")
        .add(PlannerSkill())
        .add(ReportGeneratorSkill())
)

agent = Agent(
    name="Research Agent",
    workflow=workflow
)

response = agent.invoke(
    "Explain LangGraph."
)

print(response)
```

---

# 🌱 Current Status

Current Version: **v0.1**

Implemented:

- ✅ Modular Architecture
- ✅ Agent
- ✅ Workflow
- ✅ Context
- ✅ BaseSkill
- ✅ Planner Skill
- ✅ Report Generator Skill
- ✅ Initial Runtime Structure

In Progress:

- 🔄 Search Skill
- 🔄 LangChain Integration
- 🔄 LangGraph Integration
- 🔄 Runtime Manager
- 🔄 Tool Registry

Planned:

- Memory
- RAG
- SQL Skills
- Browser Skills
- Vision Skills
- Multi-Agent Workflows
- Plugin System
- Athena Studio (Visual Workflow Builder)

---

# 🛣 Roadmap

## Phase 1

- Core Architecture
- Workflow Engine
- Skills

## Phase 2

- LangChain Integration
- LangGraph Integration
- Tool Calling

## Phase 3

- Memory
- RAG
- Reflection
- Decision Engine

## Phase 4

- Multi-Agent Workflows
- Plugin Ecosystem

## Phase 5

- Athena Studio
- Visual Workflow Builder

---

# 🎯 Design Principles

- One Skill = One Responsibility
- Workflows orchestrate Skills
- Agents orchestrate Workflows
- Context is the single source of truth
- Build on top of existing AI frameworks instead of replacing them
- Keep the public API simple and stable

---

# 🤝 Contributing

Athena is an experimental framework focused on learning modern AI engineering while building practical and reusable software.

Contributions, ideas, and discussions are always welcome.

---

# 📜 License

MIT License

---

## ⭐ Philosophy

> "Athena provides a stable developer experience while the AI ecosystem evolves underneath it."

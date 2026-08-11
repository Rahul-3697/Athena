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
The architecture is intentionally modular so that individual layers can evolve without tightly coupling the entire framework.

Core Concepts
Agent

The Agent is the public entry point into Athena.

Responsibilities:

Accept a user goal.
Create the initial Context.
Execute the configured Workflow.
Return the final result.

Example:

agent = Agent(
    name="Research Agent",
    workflow=workflow
)

result = agent.invoke(
    "Explain LangGraph and compare it with LangChain."
)
Workflow

A Workflow defines the sequence of Skills that should execute.

workflow = (
    Workflow("Research Workflow")
    .add(PlannerSkill(llm))
    .add(ReportGeneratorSkill())
)

The Workflow defines what should execute.

It does not contain the implementation of the individual tasks.

Skill

A Skill represents a reusable unit of business or agent capability.

Current examples:

PlannerSkill
ReportGeneratorSkill

A Skill follows a simple pattern:

Context
   │
   ▼
Skill
   │
   ├── Read required data
   ├── Perform its task
   └── Update Context

Skills should remain independently testable and should not directly invoke other Skills.

Context

Context is the shared state of an Athena execution.

It allows Skills to communicate without directly depending on one another.

Conceptually:

Context
│
├── goal
├── plan
├── report
└── metadata

The long-term goal is to keep the important execution data strongly typed while retaining flexible metadata for extensions.

Contracts

Athena uses dataclasses to define the structure of important objects flowing through the system.

Example:

@dataclass
class PlanStep:
    id: int
    title: str

and:

@dataclass
class ExecutionPlan:
    steps: list[PlanStep]

This provides a clear contract between Skills.

Instead of passing loosely structured dictionaries:

plan["steps"][0]["title"]

Athena works with explicit domain objects:

plan.steps[0].title
LLM Layer

LLM providers are abstracted behind a common interface.

BaseLLM
   │
   ├── OpenAILLM
   ├── GeminiLLM       (planned)
   ├── AnthropicLLM    (planned)
   └── Other Providers

Skills should depend on the BaseLLM abstraction rather than directly depending on a specific provider.

Example:

class PlannerSkill(BaseSkill):

    def __init__(self, llm):
        self.llm = llm

This allows the underlying model provider to change without rewriting the Skill.

Prompt Layer

Prompts are maintained separately from Skills.

Example:

athena/
└── prompts/
    └── planner.py

This keeps prompt engineering separate from execution logic.

A Skill is responsible for using a prompt.

The prompt module is responsible for defining it.

Parser

LLM responses are converted into Athena contracts through a dedicated parser layer.

LLM Response
     │
     ▼
Parser
     │
     ▼
ExecutionPlan

For example:

plan = Parser.to_execution_plan(response)

The objective is to keep raw model output at the boundary of the system and use structured Python objects internally.

Project Structure
Project Athena/
│
├── athena/
│   │
│   ├── agent/
│   │   └── agent.py
│   │
│   ├── context/
│   │   └── context.py
│   │
│   ├── contracts/
│   │   ├── plan_step.py
│   │   ├── execution_plan.py
│   │   └── report.py
│   │
│   ├── llms/
│   │   ├── base.py
│   │   ├── openai.py
│   │   └── factory.py
│   │
│   ├── prompts/
│   │   └── planner.py
│   │
│   ├── skills/
│   │   ├── base_skill.py
│   │   ├── planner_skill.py
│   │   └── report_generator_skill.py
│   │
│   ├── utils/
│   │   └── parser.py
│   │
│   └── workflow/
│       └── workflow.py
│
├── examples/
│   └── llm_test.py
│
├── app.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
Getting Started
1. Clone the repository
git clone https://github.com/Rahul-3697/Athena.git
cd Athena
2. Create a virtual environment
Windows
python -m venv .venv
.venv\Scripts\activate
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Never commit .env or API keys to source control.

5. Run Athena
python app.py
Current Execution Flow

A basic research request currently follows:

User Goal
    │
    ▼
Agent
    │
    ▼
Workflow
    │
    ▼
PlannerSkill
    │
    ▼
Planner Prompt
    │
    ▼
OpenAI LLM
    │
    ▼
Parser
    │
    ▼
ExecutionPlan
    │
    ▼
Context
    │
    ▼
ReportGeneratorSkill
    │
    ▼
Report
Development Philosophy

Athena is being developed incrementally.

The guiding principles are:

Learn concepts before abstracting them.
One responsibility per module.
Prefer composition over tightly coupled classes.
Keep Skills independently testable.
Use typed contracts for important data.
Keep LLM providers behind an abstraction.
Keep prompts separate from execution logic.
Keep external capabilities behind Tools.
Prefer small, meaningful changes over large rewrites.
Every version should produce a working system.
Roadmap
v1.1 — Foundation
 Agent
 Workflow
 Context
 Skills
 LLM abstraction
 OpenAI integration
 Prompt layer
 Dataclass contracts
 Structured execution plan
 Parser
v1.2 — Tooling

Planned:

 Tool abstraction
 Web Search Tool
 Tool results contract
 Skill → Tool interaction
 Tool error handling
 Tool execution tracing
v1.3 — Agent Intelligence

Planned:

 Dynamic planning
 Dynamic routing
 Execution validation
 Retry mechanisms
 Structured tool calling
 Better execution state
v1.4 — Modern Agent Framework Integration

Planned:

 LangChain integration
 LangGraph integration
 Framework adapters
 Compare native Athena execution with LangGraph execution
Future
 Memory
 RAG
 Reflection
 Human-in-the-loop
 Multi-agent workflows
 MCP integration
 Observability
 UI
 Multiple LLM providers
 Domain-specific agents
Why Athena?

Athena is intentionally not designed to replace frameworks such as LangChain or LangGraph.

Instead, it is a place to understand why these frameworks work, what abstractions they provide, and where those abstractions are useful.

The long-term goal is to combine:

Athena Core
     │
     ├── Native Agent Architecture
     ├── Typed Contracts
     ├── Skills
     ├── Tools
     └── Execution Engine
             │
             ├── LangChain adapters
             ├── LangGraph adapters
             ├── MCP adapters
             └── Other AI frameworks

This allows Athena to remain understandable while still benefiting from the rapidly evolving AI ecosystem.

Status

🚧 Active Development

Athena is currently a learning-driven engineering project. APIs and architecture may change as new concepts are introduced and evaluated.
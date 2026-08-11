# Project Athena

> A modular AI agent framework for exploring, building, and understanding modern agentic AI systems.

## Vision

Project Athena is an evolving AI Agent Framework focused on modularity, explicit execution flow, typed contracts, reusable AI capabilities, and controlled tool execution.

The goal is not simply to wrap an existing agent framework. Athena is being developed as a learning-driven engineering platform where concepts such as Agents, Workflows, Skills, Context, LLMs, Tools, Tool Calling, Memory, Routing, LangChain, and LangGraph can be understood, implemented, and composed incrementally.

Athena currently provides a foundation for building tool-enabled agents and will progressively evolve toward a general-purpose agent runtime.

---

## Current Version

**v1.1 — Tool-Enabled Agent Runtime**

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
- Tool abstraction
- Tool Registry
- Tool Request / Input / Result contracts
- Tool validation
- Tool execution
- Tool descriptors
- Provider-specific tool formatting
- Tool calling abstraction
- Bounded agentic Tool Loop
- OpenAI Tool Calling adapter

---

## Architecture

```text
                         User Goal
                            │
                            ▼
                          Agent
                            │
                            ▼
                         Workflow
                            │
                            ▼
                           Skill
                            │
                            ▼
                        Tool Loop
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
            LLM       Tool Registry    Tool Executor
             │              │              │
             │              ▼              │
             │            Tools            │
             │                             │
             └──────────────┼──────────────┘
                            │
                            ▼
                       Tool Result
                            │
                            ▼
                           LLM
                            │
                            ▼
                       Final Answer
```

Athena deliberately separates reasoning, orchestration, tool discovery, validation, and execution.

---

## Core Concepts

### Agent

The Agent is the public entry point into Athena.

Responsibilities:

- Accept a user goal
- Create the initial Context
- Execute the configured Workflow
- Return the final result

Example:

```python
agent = Agent(
    name="Research Agent",
    workflow=workflow
)

result = agent.invoke(
    "Explain LangGraph and compare it with LangChain."
)
```

The Agent should remain lightweight and coordinate execution rather than contain business logic.

### Workflow

A Workflow defines the sequence of Skills that should execute.

```python
workflow = (
    Workflow("Research Workflow")
    .add(PlannerSkill(llm))
    .add(ReportGeneratorSkill())
)
```

The Workflow defines what should execute. It does not contain the implementation of individual Skills.

### Skill

A Skill represents a reusable unit of business or agent capability.

Current examples:

```text
PlannerSkill
ReportGeneratorSkill
```

A Skill follows this general pattern:

```text
Context
   │
   ▼
Skill
   │
   ├── Read required data
   ├── Perform its task
   └── Update Context
```

Skills should remain independently testable and should not directly depend on unrelated Skills.

---

## Context

Context represents the shared state of an Athena execution.

It allows Skills to communicate without directly depending on one another.

Conceptually:

```text
Context
│
├── goal
├── plan
├── report
└── metadata
```

The long-term objective is to keep important execution data strongly typed while retaining flexible metadata for extensions.

---

## Contracts

Athena uses Python dataclasses to define the structure of important objects flowing through the framework.

Current Tool contracts include:

```text
ToolRequest
ToolInput
ToolResult
ToolCall
ToolDescriptor
```

The contracts create explicit boundaries between different stages of execution.

### ToolRequest

Represents a request from an Agent or LLM to execute a Tool.

```python
ToolRequest(
    tool_name="mock_tool",
    arguments={
        "message": "Hello Athena"
    }
)
```

### ToolInput

Represents validated input passed to an actual Tool.

```python
ToolInput(
    name="mock_tool",
    arguments={
        "message": "Hello Athena"
    }
)
```

### ToolResult

Standardized result returned by a Tool.

```python
ToolResult(
    success=True,
    data="Hello Athena"
)
```

Failed execution:

```python
ToolResult(
    success=False,
    error="Tool execution failed"
)
```

### ToolCall

Provider-independent representation of an LLM Tool call.

```python
ToolCall(
    call_id="abc123",
    tool_name="mock_tool",
    arguments={
        "message": "Hello Athena"
    }
)
```

The `call_id` allows provider-specific systems such as OpenAI to correlate Tool execution results with the original model request.

### ToolDescriptor

An LLM-facing description of a Tool.

```python
ToolDescriptor(
    name="mock_tool",
    description="A development tool used to test Athena tool execution.",
    input_schema={...}
)
```

The descriptor exposes what the Tool can do without exposing the Tool implementation itself.

---

## Tool Architecture

Tools represent capabilities that interact with external systems or perform isolated operations.

The current architecture is:

```text
ToolRequest
     │
     ▼
ToolValidator
     │
     ▼
ToolInput
     │
     ▼
ToolExecutor
     │
     ▼
ToolRegistry
     │
     ▼
BaseTool
     │
     ▼
ToolResult
```

| Component | Responsibility |
|---|---|
| `ToolRequest` | Represents an execution request |
| `ToolValidator` | Validates whether a request is allowed |
| `ToolInput` | Represents validated Tool input |
| `ToolExecutor` | Executes a Tool |
| `ToolRegistry` | Stores and resolves available Tools |
| `BaseTool` | Defines the Tool interface |
| `ToolResult` | Standardizes execution results |

### BaseTool

Every Athena Tool implements the `BaseTool` abstraction.

A Tool provides:

```text
name
description
input_schema
execute()
```

Example:

```python
class MockTool(BaseTool):

    @property
    def name(self):
        return "mock_tool"

    @property
    def description(self):
        return "A development tool used to test Athena tool execution."

    @property
    def input_schema(self):
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string"
                }
            },
            "required": ["message"]
        }

    def execute(self, tool_input):
        ...
```

The Tool owns its own capability and input requirements.

### Tool Registry

The `ToolRegistry` maintains the set of Tools available to Athena.

```text
ToolRegistry
│
├── mock_tool
├── web_search
├── browser
└── legal_source_search
```

Tools are registered explicitly:

```python
registry = ToolRegistry()
registry.register(MockTool())
```

Tools can then be retrieved:

```python
tool = registry.get("mock_tool")
```

The registry also exposes Tool descriptors:

```python
descriptors = registry.descriptors()
```

This allows the LLM-facing layer to discover available capabilities without receiving direct access to Tool objects.

### Tool Validation

The `ToolValidator` creates a boundary between model-generated requests and actual Tool execution.

```text
LLM
 │
 ▼
ToolRequest
 │
 ▼
ToolValidator
 │
 ├── Tool exists?
 ├── Required arguments?
 ├── Unknown arguments?
 └── Basic argument types?
 │
 ▼
ToolExecutor
```

The LLM is therefore allowed to request a capability, but it does not directly execute the capability.

### Tool Executor

The `ToolExecutor` coordinates Tool execution.

```text
ToolRequest
     │
     ▼
ToolValidator
     │
     ▼
ToolInput
     │
     ▼
Tool
     │
     ▼
ToolResult
```

Execution failures are converted into `ToolResult` rather than automatically crashing the entire agent runtime.

---

## Tool Descriptors and Formatters

A Tool can expose a provider-independent descriptor:

```python
descriptor = tool.descriptor()
```

This creates:

```text
BaseTool
   │
   ▼
ToolDescriptor
   │
   ▼
LLM-facing metadata
```

Athena keeps provider-specific Tool representations outside the core Tool architecture.

```text
ToolDescriptor
      │
      ▼
ToolFormatter
      │
      ├── OpenAI Formatter
      ├── LangChain Formatter
      └── Future adapters
```

This prevents provider-specific schemas from leaking into `BaseTool`.

---

## Agentic Tool Loop

Athena v1.1 introduces the foundation of an actual agentic execution loop.

```text
                     User Goal
                         │
                         ▼
                        LLM
                         │
                         ▼
                  Tool decision
                         │
                         ▼
                     ToolCall
                         │
                         ▼
                   ToolRequest
                         │
                         ▼
                   ToolValidator
                         │
                         ▼
                   ToolExecutor
                         │
                         ▼
                       Tool
                         │
                         ▼
                    ToolResult
                         │
                         ▼
                        LLM
                         │
                         ▼
                    Final Answer
```

The loop can execute multiple Tool iterations and is bounded by a configurable maximum iteration count.

```python
tool_loop = ToolLoop(
    llm=llm,
    registry=registry,
    executor=executor,
    max_iterations=5,
)
```

---

## Runtime

Runtime components represent execution machinery used by Athena.

Current runtime component:

```text
runtime/
└── tool_loop.py
```

The Tool Loop is deliberately kept outside the Tool package.

```text
tools/
    Capabilities and Tool infrastructure

runtime/
    Execution machinery
```

---

## LLM Layer

LLM providers are abstracted behind interfaces.

```text
BaseLLM
   │
   ├── OpenAI
   ├── Gemini
   ├── Anthropic
   └── Other Providers
```

Tool calling has its own abstraction:

```text
BaseToolCallingLLM
   │
   ├── OpenAI Tool Calling Adapter
   ├── LangChain Adapter
   └── Future Providers
```

This allows the Agent runtime to remain independent of the specific LLM provider.

### OpenAI Tool Calling

Athena contains an OpenAI Tool Calling adapter responsible for translating between OpenAI's API representation and Athena's provider-independent contracts.

```text
OpenAI
   │
   ▼
OpenAIToolCallingLLM
   │
   ▼
ToolCall
   │
   ▼
Athena Runtime
```

Athena's core runtime does not directly depend on the OpenAI response format.

---

## Project Structure

```text
Project Athena V1.1/
│
├── athena/
│   ├── agent/
│   │   └── agent.py
│   │
│   ├── context/
│   │   └── context.py
│   │
│   ├── contracts/
│   │   ├── tool_call.py
│   │   ├── tool_descriptor.py
│   │   ├── tool_input.py
│   │   ├── tool_request.py
│   │   └── tool_result.py
│   │
│   ├── llms/
│   │   ├── base.py
│   │   ├── openai.py
│   │   ├── tool_calling.py
│   │   └── openai_tool_calling.py
│   │
│   ├── prompts/
│   │   └── planner.py
│   │
│   ├── runtime/
│   │   └── tool_loop.py
│   │
│   ├── skills/
│   │   ├── base_skill.py
│   │   ├── planner_skill.py
│   │   └── report_generator_skill.py
│   │
│   ├── tools/
│   │   ├── base_tool.py
│   │   ├── mock_tool.py
│   │   ├── tool_executor.py
│   │   ├── tool_formatter.py
│   │   ├── tool_registry.py
│   │   ├── tool_validator.py
│   │   └── formatters/
│   │       ├── base_formatter.py
│   │       └── openai_formatter.py
│   │
│   ├── utils/
│   │   └── parser.py
│   │
│   └── workflow/
│       └── workflow.py
│
├── examples/
│   ├── llm_test.py
│   ├── tool_test.py
│   ├── tool_formatter_test.py
│   ├── agentic_loop_test.py
│   ├── openai_connection_test.py
│   └── openai_tool_loop_test.py
│
├── app.py
├── requirements.txt
├── pyproject.toml
├── .env
├── .gitignore
└── README.md
```

---

## Running Athena

### 1. Clone the repository

```bash
git clone https://github.com/Rahul-3697/Athena.git
cd Athena
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scriptsctivate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit `.env` or API keys to source control.

### 5. Run the application

```bash
python app.py
```

---

## Testing

Tool system:

```bash
python -m examples.tool_test
```

Tool formatting:

```bash
python -m examples.tool_formatter_test
```

Mock agentic loop:

```bash
python -m examples.agentic_loop_test
```

OpenAI connection:

```bash
python -m examples.openai_connection_test
```

OpenAI Tool Loop:

```bash
python -m examples.openai_tool_loop_test
```

---

## Development Philosophy

Athena is being developed incrementally.

The guiding principles are:

1. Learn concepts before abstracting them.
2. One responsibility per module.
3. Prefer composition over tightly coupled classes.
4. Keep Skills independently testable.
5. Use typed contracts for important data.
6. Keep LLM providers behind abstractions.
7. Keep prompts separate from execution logic.
8. Keep external capabilities behind Tools.
9. Keep Tool execution controlled by Athena.
10. Do not allow LLMs to directly execute external capabilities.
11. Prefer small, meaningful changes over large rewrites.
12. Every version should produce a working system.
13. Avoid premature abstraction.
14. Keep the core framework independent from third-party AI frameworks where practical.
15. Use adapters when integrating external frameworks.

---

## Security Philosophy

Tool calling introduces a new execution boundary.

Athena follows:

```text
LLM
 │
 ▼
ToolRequest
 │
 ▼
Validation
 │
 ▼
Execution
 │
 ▼
External System
```

The LLM should never receive direct access to Tool objects or unrestricted external capabilities.

The Tool Registry defines what capabilities are available.

The Tool Validator defines whether a request is valid.

The Tool Executor controls actual execution.

This becomes especially important for future tools interacting with:

- Web services
- Databases
- Files
- Government portals
- Legal systems
- External APIs

---

## Legal AI Experiment

One planned real-world application for Athena is a legal-domain AI system.

The legal project will be used as a practical stress test for Athena's Tool architecture.

The first planned capability is:

```text
LegalSourceSearchTool
```

Conceptually:

```text
LegalResearchSkill
       │
       ▼
LegalSourceSearchTool
       │
       ├── Statutes
       ├── Rules
       ├── Regulations
       ├── Notifications
       ├── Judgments
       └── Government Sources
       │
       ▼
LegalSearchResult
```

The legal system will require strong grounding in authoritative sources. The Tool architecture therefore provides a natural foundation for building controlled, source-grounded legal research capabilities.

---

## LangChain and LangGraph

Athena is not intended to replace frameworks such as LangChain or LangGraph.

Instead, Athena is being developed to understand the underlying concepts and provide a controlled core architecture that can integrate with modern frameworks.

Future integrations may look like:

```text
Athena Core
     │
     ├── Native Runtime
     ├── LangChain Adapter
     ├── LangGraph Adapter
     ├── MCP Adapter
     └── Other Framework Adapters
```

This allows Athena to remain understandable while benefiting from the broader AI ecosystem.

---

## Roadmap

### v1.1 — Foundation & Tool Runtime

Completed:

- [x] Agent
- [x] Workflow
- [x] Context
- [x] Skills
- [x] LLM abstraction
- [x] OpenAI integration
- [x] Prompt layer
- [x] Dataclass contracts
- [x] Structured execution plan
- [x] Parser
- [x] Report generation
- [x] Base Tool
- [x] Tool Input
- [x] Tool Request
- [x] Tool Result
- [x] Tool Registry
- [x] Tool Validator
- [x] Tool Executor
- [x] Tool Descriptor
- [x] Tool Formatter
- [x] OpenAI Tool Formatter
- [x] Tool Calling abstraction
- [x] Tool Loop
- [x] Mock agentic loop
- [x] OpenAI Tool Calling adapter

Current limitation:

The OpenAI integration is implemented but live API execution depends on the local environment being able to reach the OpenAI API. The Athena runtime has been independently tested using the MockTool/MockLLM path.

### v1.2 — Real Tools

Planned:

- [ ] Tool schema improvements
- [ ] Web Search Tool
- [ ] Browser Tool
- [ ] File Tool
- [ ] API Tool
- [ ] Tool execution tracing
- [ ] Better Tool error handling
- [ ] Tool retry policies

### v1.3 — Agent Intelligence

Planned:

- [ ] Dynamic planning
- [ ] Dynamic routing
- [ ] Iterative reasoning
- [ ] Execution validation
- [ ] Retry mechanisms
- [ ] Reflection
- [ ] Better execution state
- [ ] Memory

### v1.4 — Legal Agent

Planned:

- [ ] Legal Issue Diagnosis
- [ ] Legal Source Search
- [ ] Legal Research Skill
- [ ] Source-grounded responses
- [ ] Legal citation contracts
- [ ] Authority identification
- [ ] Document generation
- [ ] Document review

### Future

- [ ] LangChain integration
- [ ] LangGraph integration
- [ ] MCP integration
- [ ] RAG
- [ ] Human-in-the-loop
- [ ] Multi-agent workflows
- [ ] Observability
- [ ] UI
- [ ] Multiple LLM providers
- [ ] Domain-specific agents

---

## Versioning Strategy

Athena uses incremental versions to represent meaningful architectural milestones.

```text
v1.0
Foundation

v1.1
Tool-Enabled Agent Runtime

v1.2
Real Tools

v1.3
Agent Intelligence

v1.4
Legal Agent

Future
Framework Integrations
```

Development branches should be used for new capabilities:

```text
feature/v1.2-tools
feature/v1.3-routing
feature/legal-agent
feature/langgraph-adapter
```

Stable milestones can then be merged into the main branch.

---

## Current Status

🚧 **Active Development**

Athena is currently a learning-driven engineering project.

The core Tool architecture and first agentic execution loop are being developed incrementally. APIs and architecture may evolve as new concepts are introduced and evaluated.

---

## License

License information will be added as the project matures.

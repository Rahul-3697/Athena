# Project Athena — Current Architecture & Roadmap

> A domain-agnostic Agent Runtime for building modular, tool-enabled and eventually multi-agent AI systems.

## 1. Vision

Athena is an evolving AI Agent Framework focused on understanding and implementing the core mechanics behind modern agentic AI systems.

The goal is not to become a legal-AI or RAG-specific framework. Instead, Athena provides a reusable foundation for domain-specific agents.

```text
                         ATHENA
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
            Legal        Research       DevOps
            Agent         Agent          Agent
```

Domains can provide their own Tools, Skills, Knowledge, Rules and Workflows while Athena provides the common execution and orchestration foundation.

---

## 2. Current Version

### v1.1 — Runtime Foundation + Capability Layer

Completed:

- Agent
- Workflow
- Context
- Skills
- Dataclass-based contracts
- LLM abstraction
- OpenAI Tool Calling
- Tool Registry
- Tool Validator
- Tool Executor
- Tool Runner
- Execution State
- Execution Status
- Execution Policy
- Retry Policy
- Timeout Policy
- Tool Loop
- Calculator Tool
- Document Loader
- Text Chunker
- Keyword Retriever
- File Search Tool
- Runtime tests
- Tool tests
- Integration tests

The first live agentic flow has been demonstrated with both computation and document-retrieval capabilities.

---

## 3. Architecture

```text
                    ATHENA
                       │
       ┌───────────────┼────────────────┐
       │               │                │
 Orchestration       Runtime        Capabilities
       │               │                │
 Agent              ToolLoop          Tools
 Workflow           ToolRunner        Skills
 Skills             State             Knowledge
 Context            Policies
                    Execution
                       │
                       ▼
                      LLM
```

Core principle:

> The LLM decides what should happen, while the Athena runtime controls how that decision is executed.

---

## 4. Main Responsibilities

### Agent
Coordinates higher-level execution.

### Workflow
Defines ordered execution of Skills.

### Skill
Represents reusable higher-level capabilities.

### Context
Represents application/workflow state.

```text
Context
├── goal
├── plan
├── report
└── application metadata
```

### ExecutionState
Represents runtime state for the current execution.

```text
ExecutionState
├── goal
├── iteration
├── status
├── tool_calls
├── tool_results
└── metadata
```

Important distinction:

```text
Context
    → What does the application know?

ExecutionState
    → What is the runtime doing?
```

---

## 5. Tool Architecture

```text
ToolDescriptor
      │
      ▼
ToolCall
      │
      ▼
ToolRequest
      │
      ▼
ToolRunner
      │
      ▼
ToolExecutor
      │
      ▼
Tool
      │
      ▼
ToolResult
```

### Tool Registry
Owns Tool discovery and lookup.

### Tool Validator
Validates Tool requests.

### Tool Executor
Creates ToolInput, resolves the Tool and executes it.

### Tool Runner
Controls Tool execution with retry and timeout policies.

### Tool Result

```text
ToolResult
├── success
├── data
└── error
```

---

## 6. LLM Layer

```text
BaseLLM
   │
   └── OpenAILLM

BaseToolCallingLLM
   │
   └── OpenAIToolCallingLLM
```

Provider-specific response formats stay inside adapters.

---

## 7. Tool Formatting

```text
ToolDescriptor
      │
      ▼
ToolFormatter
      │
      ▼
BaseToolFormatter
      │
      ├── OpenAI Formatter
      ├── Future Provider Formatter
      └── Future Framework Formatter
```

Formatting translates Athena Tool definitions into provider-specific representations. It does not execute Tools.

---

## 8. Current Agentic Loop

```text
User Goal
    ↓
LLM
    ↓
ToolCall
    ↓
ToolRequest
    ↓
ToolRunner
    ↓
ToolExecutor
    ↓
Tool
    ↓
ToolResult
    ↓
LLM
    ↓
Final Answer
```

The runtime supports multiple Tool iterations, execution limits, retries, timeouts and failure recovery.

---

## 9. Capability Layer

Athena has demonstrated two different capability types.

### CalculatorTool

```text
Expression
    ↓
CalculatorTool
    ↓
Result
```

### FileSearchTool

```text
Query
    ↓
FileSearchTool
    ↓
DocumentLoader
    ↓
TextChunker
    ↓
KeywordRetriever
    ↓
Retrieved passages
```

The same Athena runtime executes both without runtime changes.

---

## 10. Knowledge Layer

Knowledge is separate from Tool orchestration.

```text
Knowledge
├── Loaders
├── Chunking
└── Retrieval
```

Current flow:

```text
Document
    ↓
DocumentLoader
    ↓
TextChunker
    ↓
KeywordRetriever
    ↓
Retrieved Chunks
```

Future retrieval can evolve from:

```text
Keyword
   ↓
Vector
   ↓
Hybrid
   ↓
RAG
```

RAG is treated as a future knowledge capability, not the definition of Athena.

---

## 11. Testing

```text
tests/
├── runtime/
├── tools/
└── integration/
```

The intended distinction is:

```text
Runtime tests
    → state, policies, ToolLoop, ToolRunner

Tool tests
    → capabilities and Tool infrastructure

Integration tests
    → real provider/runtime/capability interactions
```

Examples are reserved for demonstrations.

---

## 12. Architectural Cleanup

The earlier `athena/core/` execution structure was removed because the active execution architecture is now maintained under:

```text
athena/runtime/
```

This avoids competing execution models.

The active architecture is centered on:

```text
Agent
Workflow
Skill
Runtime
Tools
Knowledge
LLM
Contracts
```

---

## 13. Domain Independence

Athena is intentionally domain agnostic.

```text
                    ATHENA
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      Legal         Research        DevOps
      Agent          Agent           Agent
        │              │              │
      Tools          Tools           Tools
      Skills         Skills          Skills
      Knowledge      Knowledge       Knowledge
```

Athena provides the reusable runtime. Domains provide their own capabilities.

---

## 14. Current Maturity

```text
Tool execution          ██████████
Runtime control         █████████░
Capability abstraction  █████████░
Basic knowledge         ███████░░░
Single-agent reasoning  ████░░░░░░
Planning                ██░░░░░░░░
Memory                  ░░░░░░░░░░
Governance              ░░░░░░░░░░
Observability           ░░░░░░░░░░
Evaluation              ░░░░░░░░░░
Multi-agent             ░░░░░░░░░░
```

The lower execution layers are intentionally being built before the more advanced agent capabilities.

---

## 15. Next Major Architecture — Agent Intelligence

Today Athena is fundamentally Tool-driven:

```text
Goal
 ↓
LLM
 ↓
ToolCall
 ↓
Tool
 ↓
Result
```

The next evolution is Agent-driven:

```text
Goal
 ↓
Understand
 ↓
Decide
 ↓
Plan
 ↓
Act
 ↓
Observe
 ↓
Re-evaluate
 ↓
Act again
 ↓
Complete
```

This is the next major architectural frontier.

---

## 16. Phase 3 — Agent Intelligence

First design concepts:

```text
AgentRequest
├── goal
├── context
└── constraints

AgentDecision
├── type
├── target
└── arguments

AgentResult
├── success
├── output
└── execution_state
```

Potential decision types:

```text
ANSWER
TOOL
SKILL
ASK_USER
DELEGATE
STOP
```

The goal is to separate:

```text
What should the Agent do?
```

from:

```text
How should Athena execute it?
```

This boundary will support later Planning, Memory, Human approval and Multi-agent orchestration.

---

## 17. Roadmap

```text
v1.1 — Runtime Foundation
    ✅ Complete

v1.2 — Capability Layer
    ✅ In progress
    - Calculator
    - Document retrieval
    - File Search

v1.3 — Agent Intelligence
    - AgentRequest
    - AgentDecision
    - AgentResult
    - Planning
    - Dynamic execution
    - Re-planning

v1.4 — Memory + Advanced Knowledge
    - Memory abstraction
    - Vector retrieval
    - Hybrid retrieval
    - RAG

v1.5 — Governance
    - Permissions
    - Human approval
    - Audit
    - Policy controls

v1.6 — Observability + Evaluation
    - Tracing
    - Metrics
    - Agent trajectories
    - Evaluation

v2.0 — Multi-Agent Runtime
    - Delegation
    - Supervisor agents
    - Agent-to-agent workflows
    - Agent graphs
```

---

## 18. Development Philosophy

1. Learn concepts before abstracting them.
2. Keep responsibilities explicit.
3. Prefer composition over tightly coupled classes.
4. Keep provider-specific code inside adapters.
5. Keep Tools independent from the runtime.
6. Keep Context separate from ExecutionState.
7. Add abstractions only when a real need appears.
8. Build deterministic tests before external integrations.
9. Preserve working milestones.
10. Do not add advanced infrastructure merely because it is fashionable.
11. Keep the core domain agnostic.
12. Let real capabilities reveal architectural requirements.

Key principle:

> **Do not build the entire future architecture today. Build the smallest abstraction that makes the next architectural step possible.**

---

## 19. One-Sentence Definition

> **Athena is a domain-agnostic Agent Runtime that separates reasoning, orchestration, capability execution, and runtime control so different domain-specific agents can be built on the same foundation.**

---

## 20. Current Status

**Active Development**

Completed:

- Runtime foundation
- Agentic Tool Loop
- Tool execution controls
- Calculator capability
- Document retrieval capability
- File Search capability
- Deterministic tests
- Integration tests
- Architecture cleanup

Current focus:

**Phase 3 — Agent Intelligence**

First design target:

**AgentRequest → AgentDecision → AgentResult**

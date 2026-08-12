# Project Athena — Workflow & Runtime Presentation Guide

## 1. Athena in One Picture

```text
User Goal
   ↓
Agent
   ↓
Workflow
   ↓
Skill
   ↓
Agent Runtime
   ↓
LLM
   ↓
ToolCall
   ↓
ToolLoop
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

## 2. Four Main Layers

### Orchestration
```text
Agent → Workflow → Skill
```
Decides what work should happen and in what order.

### Reasoning
```text
LLM → LLMResponse → ToolCall
```
Decides what should happen next.

### Runtime
```text
ToolLoop
ExecutionState
ExecutionStatus
ExecutionPolicy
ToolRunner
RetryPolicy
TimeoutPolicy
```
Controls and safely executes the agentic process.

### Capabilities
```text
ToolRegistry
ToolDescriptor
ToolRequest
ToolExecutor
Tool
ToolResult
```
Provides the actual capabilities.

---

## 3. End-to-End Workflow

```text
User
 ↓
Agent
 ↓
Workflow
 ↓
Skill
 ↓
ToolLoop
 ↓
LLM
 ├── Final Answer → DONE
 │
 └── ToolCall
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
     LOOP
```

The key principle is:

> The LLM decides what should happen; the Athena runtime controls how it happens.

---

## 4. ToolRunner

ToolRunner owns individual Tool execution behavior:

```text
ToolRunner
├── ToolExecutor
├── RetryPolicy
└── TimeoutPolicy
```

### Retry

```text
Tool
 ↓
Failure
 ↓
RetryPolicy
 ├── Retry available → Tool
 └── Exhausted → ToolResult(success=False)
```

### Timeout

```text
Tool
 ↓
Runs too long
 ↓
TimeoutPolicy
 ↓
ToolResult(success=False)
```

This keeps retry and timeout mechanics out of ToolLoop.

---

## 5. ToolLoop

ToolLoop coordinates the agentic cycle:

1. Ask the LLM what to do.
2. Detect ToolCalls.
3. Convert ToolCalls to ToolRequests.
4. Ask ToolRunner to execute them.
5. Send ToolResults back to the LLM.
6. Repeat until a final answer.
7. Stop when an execution policy is reached.

```text
             ToolLoop
                ↓
               LLM
                ↓
           ToolCall?
          /                 YES          NO
         ↓            ↓
    ToolRunner     COMPLETED
         ↓
    ToolResult
         ↓
        LLM
         ↓
        LOOP
```

---

## 6. Runtime State

### Context

Application/workflow state:

```text
Context
├── goal
├── plan
├── report
└── application metadata
```

### ExecutionState

Runtime state:

```text
ExecutionState
├── goal
├── iteration
├── status
├── tool_calls
├── tool_results
└── metadata
```

The distinction prevents Context from becoming a dumping ground for runtime internals.

---

## 7. Runtime Policies

### ExecutionPolicy

Controls the overall Agent execution boundary:

```text
max_iterations
max_tool_calls
```

### RetryPolicy

Controls Tool failure recovery:

```text
max_retries
```

### TimeoutPolicy

Controls individual Tool execution duration:

```text
timeout_seconds
```

The separation is:

```text
ExecutionPolicy
    → How much can the Agent execute?

RetryPolicy
    → What happens after Tool failure?

TimeoutPolicy
    → How long can a Tool run?
```

---

## 8. Error Philosophy

A Tool failure does not automatically mean Agent failure.

```text
Tool
 ↓
Failure
 ↓
ToolResult(success=False)
 ↓
LLM
 ↓
Agent may recover
```

Runtime failure is different:

```text
Runtime problem
 ↓
ExecutionStatus.FAILED
```

Policy exhaustion is different again:

```text
Execution limit
 ↓
ExecutionStatus.MAX_ITERATIONS
```

---

## 9. Current Runtime Architecture

```text
athena/runtime/
├── execution_state.py
├── execution_status.py
├── execution_policy.py
├── retry_policy.py
├── timeout_policy.py
├── tool_runner.py
└── tool_loop.py
```

Responsibilities:

```text
ExecutionState
    What is happening?

ExecutionStatus
    What state is execution in?

ExecutionPolicy
    How much execution is allowed?

RetryPolicy
    What happens after failure?

TimeoutPolicy
    How long can a Tool run?

ToolRunner
    Execute one Tool safely.

ToolLoop
    Coordinate the agentic cycle.
```

---

## 10. Testing Architecture

```text
examples/
├── runtime_test.py
│   └── state / status / execution policy
│
├── tool_runner_test.py
│   └── success / failure / retry / timeout
│
└── tool_loop_test.py
    └── LLM ↔ ToolRunner orchestration
```

This separation keeps tests focused and deterministic.

---

## 11. Live OpenAI Flow

```text
OpenAI
 ↓
OpenAIToolCallingLLM
 ↓
LLMResponse
 ↓
ToolCall
 ↓
ToolLoop
 ↓
ToolRequest
 ↓
ToolRunner
 ↓
ToolExecutor
 ↓
ToolResult
 ↓
OpenAI
 ↓
Final Answer
```

Provider-specific OpenAI response formats remain inside the OpenAI adapter and formatter.

---

## 12. Current Milestone

```text
ATHENA v1.1

Foundation                  [x]
Agent                       [x]
Workflow                    [x]
Skills                      [x]
Dataclass contracts         [x]
LLM abstraction             [x]
OpenAI integration          [x]
Tool Registry               [x]
Tool Executor               [x]
Tool Calling                [x]
First live agentic loop     [x]

Runtime Hardening
ExecutionState              [x]
ExecutionStatus             [x]
ExecutionPolicy             [x]
RetryPolicy                 [x]
TimeoutPolicy               [x]
ToolRunner                  [x]
Runtime tests               [x]
```

---

## 13. Next Phase

### v1.2 — Real Tools

Recommended order:

```text
CalculatorTool
      ↓
FileSearchTool
      ↓
WebSearchTool
```

Each tests a different capability:

```text
Calculator
    → deterministic execution

File Search
    → local data / retrieval

Web Search
    → external / network execution
```

---

## 14. Presentation Summary

When presenting Athena:

### Problem

> Build an Agent runtime where reasoning, orchestration, Tool discovery, and Tool execution remain separate.

### Architecture

```text
Agent
 ↓
Workflow
 ↓
Skill
 ↓
Runtime
 ↓
LLM + Tools
```

### Agentic Loop

```text
LLM
 ↓
ToolCall
 ↓
ToolRunner
 ↓
ToolResult
 ↓
LLM
 ↓
Final Answer
```

### Safety

```text
ExecutionPolicy
RetryPolicy
TimeoutPolicy
```

### Current Achievement

> Athena has successfully completed its first real OpenAI-driven agentic Tool loop and now has a hardened runtime with state tracking, execution limits, retries, timeouts, and deterministic tests.

### Next

> Move from framework validation to real capabilities by implementing production-style Tools.

---

## One-Line Architecture

> **Athena separates reasoning from execution: the LLM decides what should happen, while the runtime controls how that decision is safely executed.**

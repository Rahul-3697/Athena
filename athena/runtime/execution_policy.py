from dataclasses import dataclass


@dataclass
class ExecutionPolicy:

    max_iterations: int = 3

    max_tool_calls: int = 10
from dataclasses import dataclass


@dataclass
class TimeoutPolicy:
    timeout_seconds: float = 10.0
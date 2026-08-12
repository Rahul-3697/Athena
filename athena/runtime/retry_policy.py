from dataclasses import dataclass


@dataclass
class RetryPolicy:
    max_retries: int = 2
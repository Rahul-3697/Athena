"""
Centralized logging configuration for Project Athena.
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

from athena.config import settings

console = Console()

logging.basicConfig(
    level=settings.log_level,
    format="%(message)s",
    handlers=[
        RichHandler(
            console=console,
            rich_tracebacks=True,
            show_path=False,
        )
    ],
)

logger = logging.getLogger(settings.app_name)
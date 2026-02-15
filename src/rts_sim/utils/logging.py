"""Logging setup for the RTS simulator.

Inputs: optional log level, log file path.
Outputs: configured logging.
Invariants: no side effects beyond logging config.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
) -> None:
    """Configure root logger. Used by CLI and experiments.

    Inputs: level (e.g. logging.INFO), optional log_file path.
    Outputs: None.
    """
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(level=level, format=fmt, handlers=handlers)

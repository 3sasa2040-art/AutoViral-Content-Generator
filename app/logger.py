from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_dir: str | Path) -> logging.Logger:
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path / f"{name}.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def log_event(logger: logging.Logger, message: str, level: int = logging.INFO) -> None:
    logger.log(level, message)


if __name__ == "__main__":
    logger = setup_logger("system", "logs")
    log_event(logger, "Logger initialized")

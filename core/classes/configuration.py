from __future__ import annotations

from typing import Literal

# this is a serializable singleton global configuration file


class RuntimeConfig:

    worker_type: Literal["embedder", "crawler", "summarizer", "scheduler"]

    llm_configuration: str | None
    embedder_configuration: str | None

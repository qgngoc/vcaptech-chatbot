from abc import ABC, abstractmethod
from typing import List, Optional

from core.entities import TracingLog

class LogsRepository(ABC):

    @abstractmethod
    def insert_log(self, tracing_log: TracingLog) -> None:
        pass

    @abstractmethod
    def get_logs_by_trace_id(self, trace_id: str) -> list[dict]:
        pass
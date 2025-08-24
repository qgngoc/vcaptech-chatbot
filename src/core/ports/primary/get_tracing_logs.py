from abc import ABC, abstractmethod 
from typing import List

from core.entities import ReadFileConfig

class GetTracingLogsPort(ABC):
    """Use case for getting tracing logs."""

    @abstractmethod
    def get_tracing_logs(self, tracing_id: str) -> List[dict]:
        pass


from core.ports.primary.get_tracing_logs import GetTracingLogsPort
from core.ports.secondary.repositories import LogsRepository

class GetTracingLogsUseCaseImpl(GetTracingLogsPort):
    """Use case for getting tracing logs."""

    def __init__(self, logs_repository: LogsRepository):
        self.logs_repository = logs_repository

    def get_tracing_logs(self, tracing_id: str) -> list[dict]:
        return self.logs_repository.get_logs_by_trace_id(tracing_id)
import os
import logging
import retry
from core.entities import TracingLog
from pymongo import MongoClient
from core.ports.secondary.repositories import LogsRepository

class MongoDBLogsRepositoryImpl(LogsRepository):

    _COLLECTION_NAME = "tracing_logs"

    def __init__(self, mongodb_client: MongoClient):
        self.mongodb_client = mongodb_client
        self.db = self.mongodb_client[os.getenv("MONGODB_DB_NAME", "vcaptech_chatbot")]
        self.collection = self.db[self._COLLECTION_NAME]

    @retry.retry(tries=3, delay=5)
    def insert_log(self, tracing_log: TracingLog) -> None:
        try:
            tracing_log_dict = tracing_log.model_dump()
            tracing_log_dict['_id'] = tracing_log.id
            self.collection.insert_one(tracing_log_dict)
        except Exception as e:
            logging.exception(f"Error inserting log: {e}")
            raise e

    def get_logs_by_trace_id(self, trace_id: str) -> list[dict]:
        try:
            logs = list(self.collection.find({"trace_id": trace_id}))
            return logs
        except Exception as e:
            logging.exception(f"Error retrieving logs for trace_id {trace_id}: {e}")
            raise e

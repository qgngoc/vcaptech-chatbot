
from abc import ABC, abstractmethod
from typing import List

from core.entities import Tool, Client, RagConfig
from core.ports.secondary.services.embedding_service import EmbeddingService
from core.ports.secondary.services.retrieve_service import RetrieveService

class GetToolsService(ABC):
    """Use case for retrieving tools for a client."""
    
    @abstractmethod
    def get_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Retrieve tools for a client based on the provided RAG configuration."""
        pass

    @abstractmethod
    async def aget_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Asynchronously retrieve tools for a client based on the provided RAG configuration."""
        pass

    @abstractmethod
    def get_retrieve_tool_names(self) -> set[str]:
        """Get the names of the tools used for retrieval."""
        pass

from core.ports.secondary.services import GetToolsService, EmbeddingService, RetrieveService

from core.entities import Client, RagConfig, Tool, SearchQueryWithVector, Document


class GetToolsServiceImpl(GetToolsService):
    """Service implementation for retrieving tools for a client."""

    _RETRIEVE_TOOL_NAMES = {"search_local_knowledge_base"}

    def __init__(self):
        pass

    def get_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Retrieve tools for a client based on the provided RAG configuration."""
        def search_local_knowledge_base(query: str) -> list[Document]:
            """Search the local knowledge base to get the most relevant information to the query."""
            try:
                vector = embedding_service.create_embedding(query)
                response = retrieve_service.retrieve(
                    search_query=SearchQueryWithVector(
                        vector=vector,
                        text=query
                    ),
                    client=client,
                    limit=rag_config.top_k
                )
                return response
            except Exception as e:
                import logging
                logging.exception("Error retrieving documents from local knowledge base")
                return f"Error retrieving documents: {e}"
                
        search_local_knowledge_base_tool = Tool(
            name="search_local_knowledge_base",
            description="Search the local knowledge base to get the most relevant information to the query.",
            arguments={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the local knowledge base."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            },
            function=search_local_knowledge_base
        )


        def immediate_settlement(load: float, young_modulus: float) -> float:
            """
            Calculate the immediate settlement of a footing.

            Formula:
                settlement = load / E

            Args:
                load (float): The applied load on the footing (kN, N, or any consistent force unit).
                young_modulus (float): Young’s modulus of the soil (kPa, Pa, or consistent stress unit).

            Returns:
                float: The calculated immediate settlement (in displacement units consistent with load and modulus).
            """
            if young_modulus <= 0:
                raise ValueError("Young's modulus must be greater than 0")
            return load / young_modulus
        
        immediate_settlement_tool = Tool(
            name="immediate_settlement",
            description="Calculate the immediate settlement of a footing using the formula: settlement = load / E",
            arguments={
                "type": "object",
                "properties": {
                    "load": {
                        "type": "number",
                        "description": "The applied load on the footing (kN, N, or any consistent force unit)."
                    },
                    "young_modulus": {
                        "type": "number",
                        "description": "Young's modulus of the soil (kPa, Pa, or consistent stress unit)."
                    }
                },
                "required": ["load", "young_modulus"],
                "additionalProperties": False
            },
            function=immediate_settlement
        )


        def terzaghi_bearing_capacity(phi: int, gamma: float, Df: float, B: float) -> float:
            """
            Calculate ultimate bearing capacity using Terzaghi's formula for cohesionless soils.

            Args:
                phi (int): Soil friction angle in degrees (must be one of the following: 0, 5, 10, 15, 20, 25, 30, 35, 40).
                gamma (float): Unit weight of the soil (kN/m³ or consistent unit).
                Df (float): Depth of footing (m).
                B (float): Width or diameter of the footing (m).

            Returns:
                float: The ultimate bearing capacity of the soil (kPa or consistent stress unit).
            """
            phi_map = {
                0: {"Nc": 5.7, "Nq": 1.0, "Nr": 0.0},
                5: {"Nc": 7.3, "Nq": 1.6, "Nr": 0.5},
                10: {"Nc": 9.6, "Nq": 2.7, "Nr": 1.2},
                15: {"Nc": 12.9, "Nq": 4.4, "Nr": 2.5},
                20: {"Nc": 17.7, "Nq": 7.4, "Nr": 5.0},
                25: {"Nc": 25.1, "Nq": 12.7, "Nr": 9.7},
                30: {"Nc": 37.2, "Nq": 22.5, "Nr": 19.7},
                35: {"Nc": 57.8, "Nq": 41.4, "Nr": 42.4},
                40: {"Nc": 95.7, "Nq": 81.3, "Nr": 100.4},
            }
            if phi not in phi_map:
                raise ValueError(f"phi={phi} not found in table. Use one of: {list(phi_map.keys())}")

            Nq = phi_map[phi]["Nq"]
            Nr = phi_map[phi]["Nr"]

            q_ult = gamma * Df * Nq + 0.5 * gamma * B * Nr
            return q_ult

        terzaghi_bearing_capacity_tool = Tool(
            name="terzaghi_bearing_capacity",
            description="Calculate ultimate bearing capacity using Terzaghi's formula for cohesionless soils.",
            arguments={
                "type": "object",
                "properties": {
                    "phi": {
                        "type": "integer",
                        "description": "Soil friction angle in degrees (must be one of the following: 0, 5, 10, 15, 20, 25, 30, 35, 40)."
                    },
                    "gamma": {
                        "type": "number",
                        "description": "Unit weight of the soil (kN/m³ or consistent unit)."
                    },
                    "Df": {
                        "type": "number",
                        "description": "Depth of footing (m)."
                    },
                    "B": {
                        "type": "number",
                        "description": "Width or diameter of the footing (m)."
                    }
                },
                "required": ["phi", "gamma", "Df", "B"],
                "additionalProperties": False
            },
            function=terzaghi_bearing_capacity
        )


        return [search_local_knowledge_base_tool, immediate_settlement_tool, terzaghi_bearing_capacity_tool]

    async def aget_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Asynchronously retrieve tools for a client based on the provided RAG configuration."""
        # This is a placeholder implementation. Replace with actual asynchronous logic to retrieve tools.
        return self.get_tools(embedding_service, retrieve_service, client, rag_config)  # Simulating async behavior


    def get_retrieve_tool_names(self) -> set[str]:
        return self._RETRIEVE_TOOL_NAMES
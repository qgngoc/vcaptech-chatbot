import asyncio
import requests
import uuid
from typing import Union, List

from core.ports.primary.generate_response import GenerateResponsePort
from core.entities import Message, RagConfig, Client, RagResponse, ToolCall, Tool, ToolCallResponse, Document, DocumentWithVector, Citation, TracingLog, GenerationLogContent, CalculationLogContent, RetrievalLogContent, LLMConfig

from core.ports.secondary.services import LLMService, EmbeddingService, GetRetrieveToolsService, GetCitationsService, ToolCallHandlingService, RetrieveService, GetToolsService
from core.ports.secondary.repositories import LogsRepository

class GenerateResponseUseCaseImpl(GenerateResponsePort):
    """Implementation of the use case for generating responses using LLMs."""
    MAX_ITERATIONS = 5

    def __init__(self, llm_service: LLMService, embedding_service: EmbeddingService, retrieval_service: RetrieveService, get_tools_service: GetToolsService, get_citations_service: GetCitationsService, tool_call_handling_service: ToolCallHandlingService, logs_repository: LogsRepository, agent_system_prompt: str, input_rail_system_prompt: str):
        """ Initialize the GenerateResponseUseCaseImpl with necessary services."""
        self.llm_service = llm_service
        self.embedding_service = embedding_service
        self.retrieval_service = retrieval_service
        self.get_tools_service = get_tools_service
        self.get_citations_service = get_citations_service
        self.tool_call_handling_service = tool_call_handling_service
        self.logs_repository = logs_repository
        self.retrieve_tool_names = self.get_tools_service.get_retrieve_tool_names()
        self.agent_system_prompt = agent_system_prompt
        self.input_rail_system_prompt = input_rail_system_prompt
        self.max_iterations = self.MAX_ITERATIONS  # Maximum number of iterations for the RAG process


    def generate_response(self, messages: list[Message], client: Client, rag_config: RagConfig) -> RagResponse:
        """
        Generate a response based on the input messages.

        Args:
            messages (list[Message]): The list of messages to process.
            client (Client): The client object containing client-specific information.
            rag_config (RagConfig): The configuration for the RAG system, including LLM configurations.

        Returns:
            RagResponse: The response object containing the generated output and status.
        """
        trace_id = str(uuid.uuid4())
        blocked_by_input_rail = self._checking_input_rails(conversation_messages=messages, llm_config=rag_config.llm_config, trace_id=trace_id)

        if blocked_by_input_rail:
            return RagResponse(
                blocked_by_input_rail=True,
                trace_id=trace_id,
                answer=None,
                citations=[],
            )

        tools = self.get_tools_service.get_tools(self.embedding_service, self.retrieval_service, client, rag_config)
        if messages[0].role != "system":
            messages.insert(0, Message(role="system", content=self.agent_system_prompt))
        all_citations = []
        for i in range(self.max_iterations):
            llm_completion = self.llm_service.chat(llm_config=rag_config.llm_config, messages=messages, tools=tools)
            tool_calls = llm_completion.tool_calls
            text = llm_completion.text
            messages.append(Message(role='assistant', content=text, tool_calls=tool_calls))
            if not tool_calls:
                tracing_log = TracingLog(
                    id=str(uuid.uuid4()),
                    trace_id=trace_id,
                    type="generation",
                    content=GenerationLogContent(
                        messages=messages[:-1],
                        response=text,
                    )
                )
                self.logs_repository.insert_log(tracing_log)
                break  # Exit if no tool calls are made
            tool_call_responses = []
            for tool_call in tool_calls:
                tool_call_response, citations = self._handle_tool_call(tool_call, tools, trace_id)
                tool_call_responses.append(tool_call_response)
                all_citations.extend(citations)

            for tool_call_response in tool_call_responses:
                messages.append(Message(role='tool', content=tool_call_response))


        rag_response = RagResponse(
            answer=text,
            blocked_by_input_rail=blocked_by_input_rail,
            citations=all_citations,
            trace_id=trace_id,
        )
        return rag_response

    async def agenerate_response(self, messages: list[Message], client: Client, rag_config: RagConfig) -> RagResponse:
        """
        Asynchronously generate a response based on the input messages.

        Args:
            messages (list[Message]): The list of messages to process.
            client (Client): The client object containing client-specific information.
            rag_config (RagConfig): The configuration for the RAG system, including LLM configurations.

        Returns:
            RagResponse: The response object containing the generated output and status.
        """
        # Simulate an asynchronous call to an external service
        pass

    def _handle_calculation_tool_call(self, tool_call: ToolCall, tools: list[Tool]) -> list[ToolCallResponse]:
        tool_call_response = self.tool_call_handling_service.handle_tool_call(tool_call, tools)
        if not isinstance(tool_call_response.tool_response, str):
            tool_call_response.tool_response = str(tool_call_response.tool_response)
        return tool_call_response

    def _handle_retrieve_tool_call(self, tool_call: ToolCall, tools: list[Tool]) -> tuple[list[ToolCallResponse], list[Citation]]:
        tool_call_response = self.tool_call_handling_service.handle_tool_call(tool_call, tools)
        # print(tool_call_response)
        documents = []
        if isinstance(tool_call_response.tool_response, list):
            documents.extend(tool_call_response.tool_response)
        relevant_docs = '\n\n'.join([doc.content for doc in documents if isinstance(doc, Document) or isinstance(doc, DocumentWithVector)])
        tool_call_response.tool_response = relevant_docs
        citations = self.get_citations_service.get_citations(documents)
        return tool_call_response, citations

    def _handle_tool_call(self, tool_call: ToolCall, tools: list[Tool], trace_id: str) -> tuple[ToolCallResponse, list[Citation]]:
        all_citations = []
        if tool_call.name in self.retrieve_tool_names:
            tool_call_response, citations = self._handle_retrieve_tool_call(tool_call, tools)
            tracing_log = TracingLog(
                id=str(uuid.uuid4()),
                trace_id=trace_id,
                type="retrieval",
                content=RetrievalLogContent(
                    query=tool_call.arguments.get("query", ""),
                    citations=citations
                )
            )
            self.logs_repository.insert_log(tracing_log)
            all_citations.extend(citations)
        else:
            tool_call_response = self._handle_calculation_tool_call(tool_call, tools)
            tracing_log = TracingLog(
                id=str(uuid.uuid4()),
                trace_id=trace_id,
                type="calculation",
                content=CalculationLogContent(
                    tool_name=tool_call.name,
                    tool_args=tool_call.arguments,
                    tool_response=tool_call_response.tool_response if isinstance(tool_call_response.tool_response, str) else str(tool_call_response.tool_response)
                )
            )
            self.logs_repository.insert_log(tracing_log)
        return tool_call_response, all_citations
    

    def _checking_input_rails(self, conversation_messages: list[Message], llm_config: LLMConfig, trace_id: str) -> bool:
        last_message = conversation_messages[-1].content
        messages = [Message(role="system", content=self.input_rail_system_prompt), Message(role="user", content=f"The message: {last_message}\n.Does the message violate any policies?\nAnswer yes or no. Do not provide any explanation.")]

        llm_completion = self.llm_service.chat(messages=messages, llm_config=llm_config)
        if not llm_completion.text:
            raise Exception("No response from LLM")
        tracing_log = TracingLog(
            id=str(uuid.uuid4()),
            trace_id=trace_id,
            type="generation",
            content=GenerationLogContent(
                messages=messages,
                response=llm_completion.text
            )
        )
        self.logs_repository.insert_log(tracing_log)
        return "yes" in llm_completion.text.lower()
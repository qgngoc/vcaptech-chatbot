# TODO: Refactor this file to use a dependency injection framework like `dependency_injector` or `injector`.
# This will help manage dependencies more cleanly and make the code more maintainable.
# For now, we will keep it simple and manually instantiate the services and use cases.
# This is a temporary solution to get the application running.

import os

from core.entities import (
    LLMConfig,  
    ReadFileConfig,
    PdfReadFileConfig,
    TxtReadFileConfig,
    XlsxReadFileConfig,
    MdReadFileConfig,
    PptxReadFileConfig,
    DocxReadFileConfig,
    CsvReadFileConfig
)

from infrastructure.utils.prompts import (
    AGENTIC_RAG_SYSTEM_PROMPT,
    INPUT_RAIL_SYSTEM_PROMPT
)

from adapters.secondary.services.file_reading_services import (
    CSVFileReadingServiceImpl,
    DocxFileReadingServiceImpl,
    PdfFileReadingServiceImpl,
    TxtFileReadingServiceImpl,
    XlsxFileReadingServiceImpl,
    MdFileReadingServiceImpl,
    PptxFileReadingServiceImpl
    )

from adapters.secondary.services.chunking_services import (
    MarkdownChunkingServiceImpl
)

from adapters.secondary.services.llm_services.openai_llm_services import OpenAILLMServiceImpl

from adapters.secondary.services.embedding_services.openai_embedding_service import OpenAIEmbeddingServiceImpl
from adapters.secondary.services.retrieve_services.semantic_retrieve_services import SemanticRetrieveServiceImpl
from adapters.secondary.services.get_retrieve_tools_services.get_retrieve_tools_service import GetRetrieveToolsServiceImpl
from adapters.secondary.services.get_tools_services.get_tools_service import GetToolsServiceImpl
from adapters.secondary.services.get_citations_services.get_citations_service import GetCitationsServiceImpl
from adapters.secondary.services.tool_call_handling_services.tool_call_handling_service import ToolCallHandlingServiceImpl
from adapters.secondary.services.client_managing_services.client_managing_service import ClientManagingServiceImpl
from adapters.secondary.repositories.vectordb_repositories.qdrant_vectordb_repository import QdrantVectorDBRepositoryImpl
from adapters.secondary.repositories.logs_repositories.mongodb_logs_repository import MongoDBLogsRepositoryImpl

from core.usecases.generate_response import GenerateResponseUseCaseImpl
from core.usecases.get_llm_configs import GetLLMConfigsUseCaseImpl
from core.usecases.get_read_file_config import GetReadFileConfigUseCaseImpl
from core.usecases.index_document import IndexDocumentUseCaseImpl
from core.usecases.client_manage import ClientManageUseCaseImpl
from core.usecases.get_tracing_logs import GetTracingLogsUseCaseImpl

from qdrant_client import QdrantClient
from pymongo import MongoClient

qdrant_client = QdrantClient(
    url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
    # Uncomment if needed:
    # prefer_grpc=self.prefer_grpc,
    # api_key=self.qdrant_api_key,
)

mongodb_client = MongoClient(
    os.environ.get("MONGODB_URI", None)
)

openai_llm_service = OpenAILLMServiceImpl()

openai_llm_service.add_llm_config(
    key="GPT-4o-mini",
    llm_config=LLMConfig(
        model="gpt-4o-mini",
        temperature=0.01,
    )
)
openai_llm_service.add_llm_config(
    key="GPT-4o",
    llm_config=LLMConfig(
        model="gpt-4o",
        temperature=0.01,
    )
)

openai_llm_service.add_llm_config(  
    key="GPT-4.1-nano",
    llm_config=LLMConfig(
        model="gpt-4.1-nano",
        temperature=0.01,
    )
)

openai_llm_service.add_llm_config(
    key="GPT-4.1-mini",
    llm_config=LLMConfig(
        model="gpt-4.1-mini",
        temperature=0.01,   
    )
)   

openai_llm_service.add_llm_config(
    key="GPT-4.1",
    llm_config=LLMConfig(
        model="gpt-4.1",    
        temperature=0.01,
    )
)

embedding_service = OpenAIEmbeddingServiceImpl(model_name=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))


qdrant_vectordb_repository = QdrantVectorDBRepositoryImpl(
    collection_name=os.environ.get("QDRANT_COLLECTION_NAME", "agentic-rag"),
    embedding_service=embedding_service,
    qdrant_client=qdrant_client
)
mongodb_logs_repository = MongoDBLogsRepositoryImpl(
    mongodb_client=mongodb_client
)

semantic_retrieve_service = SemanticRetrieveServiceImpl(vectordb_repository=qdrant_vectordb_repository)

get_retrieve_tools_service = GetRetrieveToolsServiceImpl()
get_tools_service = GetToolsServiceImpl()

get_citations_service = GetCitationsServiceImpl()
tool_call_handling_service = ToolCallHandlingServiceImpl()

generate_response_port = GenerateResponseUseCaseImpl(
    llm_service=openai_llm_service,
    embedding_service=embedding_service,
    retrieval_service=semantic_retrieve_service,
    # get_retrieve_tools_service=get_retrieve_tools_service,
    get_tools_service=get_tools_service,
    get_citations_service=get_citations_service,
    tool_call_handling_service=tool_call_handling_service,
    logs_repository=mongodb_logs_repository,
    agent_system_prompt=AGENTIC_RAG_SYSTEM_PROMPT,
    input_rail_system_prompt=INPUT_RAIL_SYSTEM_PROMPT
)

get_llm_configs_port = GetLLMConfigsUseCaseImpl(
    llm_service=openai_llm_service
)

get_tracing_logs_port = GetTracingLogsUseCaseImpl(
    logs_repository=mongodb_logs_repository
)


get_read_file_config_port = GetReadFileConfigUseCaseImpl()

get_read_file_config_port.add_read_file_config(
    key="pdf",
    read_file_config=PdfReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="txt",
    read_file_config=TxtReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="xlsx",
    read_file_config=XlsxReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="md",
    read_file_config=MdReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="pptx",
    read_file_config=PptxReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="docx",
    read_file_config=DocxReadFileConfig(),
)

get_read_file_config_port.add_read_file_config(
    key="csv",
    read_file_config=CsvReadFileConfig(),
)


csv_file_reading_service = CSVFileReadingServiceImpl()
docx_file_reading_service = DocxFileReadingServiceImpl()
pdf_file_reading_service = PdfFileReadingServiceImpl()
txt_file_reading_service = TxtFileReadingServiceImpl()
xlsx_file_reading_service = XlsxFileReadingServiceImpl()
md_file_reading_service = MdFileReadingServiceImpl()
pptx_file_reading_service = PptxFileReadingServiceImpl()

markdown_chunking_service = MarkdownChunkingServiceImpl()

index_document_port = IndexDocumentUseCaseImpl(
    vectordb=qdrant_vectordb_repository,    
    embedding_service=embedding_service,
)

index_document_port.add_file_reading_service(
    key="csv",
    service=csv_file_reading_service
)
index_document_port.add_file_reading_service(
    key="docx",
    service=docx_file_reading_service
)
index_document_port.add_file_reading_service(
    key="pdf",
    service=pdf_file_reading_service
)
index_document_port.add_file_reading_service(
    key="txt",
    service=txt_file_reading_service
)
index_document_port.add_file_reading_service(
    key="xlsx",
    service=xlsx_file_reading_service
)
index_document_port.add_file_reading_service(
    key="md",
    service=md_file_reading_service
)
index_document_port.add_file_reading_service(   
    key="pptx",
    service=pptx_file_reading_service
)
index_document_port.add_chunking_service(
    key="csv",
    service=csv_file_reading_service
)

index_document_port.add_chunking_service(
    key='markdown',
    service=markdown_chunking_service
)

index_document_port.add_chunking_service(
    key='text',
    service=markdown_chunking_service
)

client_managing_service = ClientManagingServiceImpl(
    vector_db_repository=qdrant_vectordb_repository
)

client_manage_port = ClientManageUseCaseImpl(
    client_managing_service=client_managing_service
)
    
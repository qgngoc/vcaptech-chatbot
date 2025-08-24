
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse


from adapters.primary.rest.schemas import IndexDocumentsInputSchema, IndexDocumentsOutputSchema, IndexDocumentsBackgroundInputSchema, IndexDocumentsBackgroundOutputSchema
from core.ports.primary.index_document import IndexDocumentPort

from infrastructure.di.container import index_document_port

router = APIRouter(
    # prefix="/index_document",
    tags=["index_document"]
)

def get_index_document_port() -> IndexDocumentPort:
    """Dependency to provide the IndexDocumentPort."""
    return index_document_port

@router.post("/index_document")
async def index_document(input_data: IndexDocumentsInputSchema,
                         index_document_port: IndexDocumentPort = Depends(get_index_document_port)):
    """
    Index a document with its metadata.

    Args:
        input_data (IndexDocumentsInputSchema): The input schema containing client and input file information.

    Returns:
        IndexDocumentsOutputSchema: The output schema containing indexed documents with vectors.
    """
    try:
        # print(input_data.model_dump_json(indent=2))
        statuses = index_document_port.index_documents(
            client=input_data.client,
            input_files=input_data.input_files
        )
        return JSONResponse(content=IndexDocumentsOutputSchema(statuses=statuses).model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error indexing document: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
    
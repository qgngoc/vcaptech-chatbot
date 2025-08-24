
import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from core.ports.primary.get_tracing_logs import GetTracingLogsPort
from adapters.primary.rest.schemas import GetTracingLogsInputSchema, GetTracingLogsOutputSchema

from infrastructure.di.container import get_tracing_logs_port

router = APIRouter(
    # prefix="/get_read_file_config",
    tags=["get_tracing_logs"]
)


def get_get_tracing_logs_port() -> GetTracingLogsPort:
    """Dependency to provide the GetTracingLogsPort."""
    return get_tracing_logs_port


@router.get("/metrics/{tracing_id}")
async def get_tracing_logs(tracing_id: str,
                            get_tracing_logs_port: GetTracingLogsPort = Depends(get_get_tracing_logs_port)):
    """Endpoint to get tracing logs."""
    try:
        logs = get_tracing_logs_port.get_tracing_logs(tracing_id)
        output_data = GetTracingLogsOutputSchema(logs=logs)
        return JSONResponse(content=output_data.model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error getting tracing logs: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
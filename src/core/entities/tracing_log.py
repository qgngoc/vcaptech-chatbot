from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Callable, Literal

from .message import Message
from .citation import Citation

class GenerationLogContent(BaseModel):
    messages: list[Message]
    response: Union[str, Message, None]

class CalculationLogContent(BaseModel):
    tool_name: str
    tool_args: dict
    tool_response: Union[str, float, int, list, dict, None]

class RetrievalLogContent(BaseModel):
    query: str
    citations: list[Citation]

class TracingLog(BaseModel):
    id: Optional[str] = None
    trace_id: str
    user_id: Optional[str] = None
    type: Literal['calculation', 'retrieval', 'generation'] = 'generation'
    content: Union[GenerationLogContent, CalculationLogContent, RetrievalLogContent]
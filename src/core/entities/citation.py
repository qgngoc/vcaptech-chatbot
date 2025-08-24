from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Callable

class Citation(BaseModel):
    id: Optional[str] = None
    document_id: Optional[str] = None
    file_name: str
    file_path: str
    page_number: int
    page_content: str
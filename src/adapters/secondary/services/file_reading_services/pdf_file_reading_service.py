import logging
import pymupdf4llm
from typing import Union
from core.ports.secondary.services import PdfFileReadingService, LLMService
from core.entities import InputFile, FileContent, PageContent, PdfReadFileConfig, Message, LLMConfig, LLMCompletion

# from infrastructure.frameworks.marker_module import MarkerModule
# from core.ports.secondary.services.common.llm_service import LLMService
# from infrastructure.utils.utils import pdf_to_base64_images, extract_markdown_text

class PdfFileReadingServiceImpl(PdfFileReadingService):
    """Service implementation for reading PDF files."""
    def __init__(self):
        pass

    def _convert_to_markdown_pymupdf(self, path: str) -> Union[list[PageContent], None]:
        """Convert PDF to markdown using Pymupdf."""
        try:
            pages = pymupdf4llm.to_markdown(path, page_chunks=True)
            page_contents = []
            for i, page in enumerate(pages):
                md_text = page.get("text", "")
                if not md_text:
                    continue
                page_content = PageContent(
                    content=md_text,
                    page_number=i,
                )
                page_contents.append(page_content)
            return page_contents
        except Exception as e:
            logging.error(f"Error converting PDF to markdown by Pymupdf: {e}")
            return None

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        page_contents = self._convert_to_markdown_pymupdf(input_file.local_file_path)
        file_content = FileContent(
            file_name=input_file.file_name,
            file_path=input_file.local_file_path,
            page_contents=page_contents,
            content_format="markdown",
        )
        return file_content

    async def aread_file(self, input_file, read_file_config, **kwargs):
        # TODO: Implement asynchronous reading of PDF files
        pass


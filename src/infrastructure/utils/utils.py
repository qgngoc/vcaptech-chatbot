import base64
import io
import json
import os
import re
import subprocess
from typing import List

import fitz  # PyMuPDF


def extract_markdown_text(text: str):
    pattern = r"```markdown(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        markdown_text = match.group(1).strip()
        return markdown_text
    else:
        return text

def read_txt_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content
    
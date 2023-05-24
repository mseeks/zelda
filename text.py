import tempfile
from typing import Union 
from pdfminer.high_level import extract_text
from domain import PDF, AcademicPaper

def to_text(file: Union[AcademicPaper, PDF]) -> str:
    text = extract_text(file.name)
    
    return text
